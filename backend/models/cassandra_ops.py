from datetime import datetime, date, timezone, timedelta
from ..db_connections import cassandra_session

INSERT_EVENT = cassandra_session.prepare("""
INSERT INTO user_events (product_id, event_date, event_time, user_id, session_id, event_type, event_props)
VALUES (?, ?, ?, ?, ?, ?, ?)
""")

def log_event(product_id: str, user_id: str, session_id: str, event_type: str, event_props: dict = None):
    now = datetime.now(timezone.utc)
    props = {k: str(v) for k,v in (event_props or {}).items()}
    cassandra_session.execute_async(INSERT_EVENT, (product_id, date.today(), now, user_id, session_id, event_type, props))


# Prepared select per (product_id, event_date) partition
SELECT_BY_PRODUCT_DATE = cassandra_session.prepare("""
SELECT product_id, event_time, user_id, session_id, event_type, event_props
FROM user_events
WHERE product_id = ? AND event_date = ?
LIMIT ?
""")

def _daterange(start_date: date, end_date: date):
    """Yield dates inclusive from start_date to end_date (ascending)."""
    for n in range((end_date - start_date).days + 1):
        yield start_date + timedelta(n)


def get_product_timeline(product_id: str, start_date: date = None, end_date: date = None, limit: int = 100):
    """
    Retrieve up to `limit` events for product_id between start_date and end_date (inclusive).
    Returns list of events sorted descending by event_time (newest first).

    Note: Because our table partitions by (product_id, event_date) we query each date partition separately.
    This function fetches from most-recent date backwards until it accumulates `limit` events.
    """

    # Defaults: last 7 days
    today = date.today()
    if end_date is None:
        end_date = today
    if start_date is None:
        start_date = today - timedelta(days=6)

    # Normalize if start_date > end_date
    if start_date > end_date:
        start_date, end_date = end_date, start_date

    events = []

    # Query from end_date backwards to start_date so we get most recent data first
    dates = list(_daterange(start_date, end_date))
    dates.reverse()

    remaining = max(limit, 1)
    for d in dates:
        try:
            # Fetch up to `remaining` events from the partition for this date
            rows = cassandra_session.execute(SELECT_BY_PRODUCT_DATE, (product_id, d, remaining))
            for r in rows:
                # convert row to dict, make event_time ISO str
                events.append({
                    "product_id": r.product_id,
                    "event_time": r.event_time.isoformat() if hasattr(r.event_time, "isoformat") else str(r.event_time),
                    "user_id": r.user_id,
                    "session_id": r.session_id,
                    "event_type": r.event_type,
                    "event_props": dict(r.event_props) if r.event_props else {}
                })
            # update remaining
            remaining = limit - len(events)
            if remaining <= 0:
                break
        except Exception as e:
            # In production, log this properly. For now, include minimal info.
            print(f"Warning: failed to query events for {product_id} date {d}: {e}")
            continue

    # Sort all events by event_time descending (newest first) and trim to limit
    try:
        events.sort(key=lambda x: x["event_time"], reverse=True)
    except Exception:
        # If event_time strings are not directly comparable, leave as is (best-effort)
        pass

    return events[:limit]

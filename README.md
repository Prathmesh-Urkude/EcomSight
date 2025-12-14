# 🛒 E-Commerce Analytics System

## 📌 Project Introduction

The **E-Commerce Analytics System** is a backend application designed to handle the diverse data needs of modern e-commerce platforms using a **multi-database (polyglot persistence) architecture**. Traditional single-database systems struggle to efficiently manage transactional data, analytics, and real-time caching at scale.

To solve this problem, the system integrates **MongoDB**, **Cassandra**, and **Redis**, each selected for its specific strengths. The backend is built using **Python FastAPI**, providing a high-performance, scalable API layer, while **Docker** is used to containerize and manage the databases for easy deployment and portability.

This architecture enables efficient product and order management, fast analytics, low-latency access through caching, and high availability — making it suitable for real-world e-commerce analytics systems.

---

## 🚀 How to Run the Project

### Prerequisites

* Install **Python 3.11**
* Install **Docker Desktop**

---

### Step 1: Start Databases Using Docker

Run the Docker Compose file to start MongoDB, Cassandra, and Redis:

```bash
docker-compose up -d
```

Verify that all databases are running:

```bash
docker ps
```

(Optional) Access MongoDB shell:

```bash
docker exec -it ecom_mongo mongosh
```

---

### Step 2: Activate Virtual Environment

```bash
.venv\Scripts\Activate
```

---

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

---

### Step 4: Seed Product Data into MongoDB

```bash
python seed_products.py
```

---

### Step 5: Start FastAPI Backend

```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

---

### Step 6: Access the Application on your Local Machine

* API Base URL: **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

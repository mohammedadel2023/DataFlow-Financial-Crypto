## DataFlow-Financial-Crypto
> **Unifying Real-Time & Historical Financial Data to support a RAG system**

## 📖 Project Overview
Financial markets move in milliseconds, but understanding the *"Why"* behind a price change requires deep context from historical news. 

**DataFlow-Financial-Crypto** is a Hybrid Data Pipeline and RAG (Retrieval-Augmented Generation) Engine designed to bridge this gap. It automatically ingests crypto market data (via batch scraping and real-time streams), deduplicates it using a custom warehouse architecture, and allows users to ask natural language questions like:
> *"Why did Bitcoin crash 5% in the last hour?"*

## 🏗️ Architecture
This project implements a modified **Lambda Architecture** to handle both speed and depth:

1.  **Ingestion Layer:** Python-based scrapers (BeautifulSoup) orchestrated by **Apache Airflow** to collect news from sources like CoinDesk.
2.  **Data Lake (Raw):** Raw unstructured data (JSONL) is stored in **MinIO** (S3 compatible) with date-based partitioning.
3.  **Metadata & Deduplication:** **PostgreSQL** serves as the "Gatekeeper," using MD5 content hashing to prevent duplicate data from entering the pipeline.
4.  **Intelligence Layer:** A RAG system using **Qwen-2.5** and a Vector Database (ChromaDB) synthesizes answers from the collected data.



## 🛠️ Tech Stack

| Component | Tool | Purpose |
| :--- | :--- | :--- |
| **Language** | Python 3.10 | Core scripting and logic |
| **Orchestration** | Apache Airflow | Scheduling daily/hourly scrapers |
| **Storage (Object)** | MinIO | Storing raw JSONL files (Data Lake) |
| **Storage (Relational)** | PostgreSQL | Metadata, Deduplication, and Filtering |
| **Vector DB** | ChromaDB / Pinecone | Semantic search for RAG |
| **LLM** | Qwen-2.5 (via Ollama) | Reasoning and answer generation |
| **Containerization** | Docker Compose | Managing the entire infrastructure |

## Instructions
**You need to install docker before using it.**

**Download requirements by using:**
```pip install -r requirements.txt```

**Run the containers using:**
```docker-compose up -d```

**You can then start and stop containers using:**
```docker start container_name``` , ```docker stop container_name```

**List all containers using:**
```docker ps -a```
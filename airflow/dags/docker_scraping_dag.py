from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from datetime import datetime, timedelta

# =================================================================
# CONFIGURATION
# =================================================================
# 1. Run 'docker network ls' in your terminal to find this name.
# It usually looks like "d_en_project_default" or "d_en_project_mynet"
DOCKER_NETWORK_NAME = "d_en_project_mynet" 

# 2. Your Docker Image Name (Must match what you built)
IMAGE_NAME = "my_scraper_image:v1"
# =================================================================

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'containerized_scraper_dag',
    default_args=default_args,
    description='Runs the scraping logic in an isolated Docker container',
    schedule='@daily',
    start_date=datetime(2025, 2, 8),
    catchup=False,
    tags=['docker', 'production']
) as dag:

    run_scraper = DockerOperator(
        task_id='run_scraper_task',
        image=IMAGE_NAME,
        container_name='scraper_worker_job',
        api_version='auto',
        
        # --- CRITICAL FIX ---
        # 'force' ensures the container is deleted after it finishes
        auto_remove='force', 
        # --------------------
        
        # Network is required for the scraper to talk to Postgres/MinIO
        network_mode=DOCKER_NETWORK_NAME,
        
        # Command to run inside the container
        command="python src/main.py",
        
        # Environment variables for your config.py
        environment={
            "POSTGRES_USER": "M_admin",
            "POSTGRES_PASSWORD": "abcd2345",
            "POSTGRES_DB": "DataFlow-Financial-Crypto",
            "POSTGRES_HOST": "postgres-db",  # Matches service name in docker-compose
            "POSTGRES_PORT": "5432",
            "MINIO_ENDPOINT": "minio:9000",
            "MINIO_ACCESS_KEY": "abcd",
            "MINIO_SECRET_KEY": "abcd2345"
        },
        
        # Mount the docker socket to allow running containers
        docker_url="unix://var/run/docker.sock",
        
        # Prevents permission errors on some setups
        mount_tmp_dir=False
    )
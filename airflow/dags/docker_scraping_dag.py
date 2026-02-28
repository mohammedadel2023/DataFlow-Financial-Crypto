from airflow import DAG
from airflow.models import Variable
from airflow.providers.docker.operators.docker import DockerOperator
from datetime import datetime, timedelta

DOCKER_NETWORK_NAME = "d_en_project_mynet" 

IMAGE_NAME = "my_scraper_image:v9"

default_args = {
	'owner': 'airflow',
	'depends_on_past': False,
	'email_on_failure': False,
	'email_on_retry': False,
	'retries': 1,
	'retry_delay': timedelta(minutes=3),
}


with DAG(
	'containerized_scraper_dag',
	default_args=default_args,
	description='Runs the scraping logic in an isolated Docker container',
	schedule='0 9 * * *',
	start_date=datetime(2025, 2, 8),
	catchup=False,
	tags=['docker', 'production']
) as dag:

	scraper_config = Variable.get("db_config", deserialize_json=True)
	
	run_scraper = DockerOperator(
		task_id='run_scraper_task',
		image=IMAGE_NAME,
		container_name='scraper_worker_job',
		api_version='auto',
		
		auto_remove='force', 
		network_mode=DOCKER_NETWORK_NAME,
		command="python src/main.py",

		environment = scraper_config,
		
		docker_url="unix://var/run/docker.sock",
		
		mount_tmp_dir=False
	)
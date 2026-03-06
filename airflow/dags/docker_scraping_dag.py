from airflow import DAG
from airflow.models import Variable
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount
from datetime import datetime, timedelta

DOCKER_NETWORK_NAME = "d_en_project_mynet" 
IMAGE_NAME = "my_scraper_image:v2.02"
SHARED_DATA_PATH = "/shared/scraped_data.json"
HOST_DATA_DIR = "/host/pipeline/data"
HOST_LOGS_DIR = "/host/pipeline/logs"


data_mount = Mount(
	source = HOST_DATA_DIR,
	target = "/shared",
	type = "bind"
)

logs_mount = Mount(
	source = HOST_LOGS_DIR,
	target = "/logs",
	type = "bind"
)

default_args = {
	'owner': 'airflow',
	'depends_on_past': False,
	'email_on_failure': False,
	'email_on_retry': False,
	'retries': 1,
	'retry_delay': timedelta(minutes=3),
}


with DAG(
	dag_id = "containerized_scraper_dag",
	default_args = default_args,
	description = "Scrape → Deduplicate → Upload, each as an isolated Docker task",
	schedule = "0 9 * * *",
	start_date = datetime(2025, 2, 8),
	catchup = False,
	tags = ["docker", "production"]
) as dag:

	scraper_config = Variable.get("db_config", deserialize_json=True)

	run_scraper = DockerOperator(
		task_id = "run_scraper_task",
		image = IMAGE_NAME,
		container_name = "scraper_worker_job",
		api_version = "auto",
		auto_remove = "never",
		network_mode = DOCKER_NETWORK_NAME,
		command = f"python src/Data_Scraping/last_ar_of_fx.py --output {SHARED_DATA_PATH}",
		environment = {**scraper_config,"LOG_FILE":"/logs/pipeline.log"},
		mounts = [data_mount, logs_mount],
		docker_url = "unix://var/run/docker.sock",
		mount_tmp_dir = False
	)

	run_check_duplication = DockerOperator(
		task_id = "run_check_duplication",
		image = IMAGE_NAME,
		container_name = "processor_data_scraped_worker",
		api_version = "auto",
		auto_remove = "force",
		network_mode = DOCKER_NETWORK_NAME,
		command = f"python src/Batch_Handling/duplicate_checking.py --data {SHARED_DATA_PATH}",
		environment = {**scraper_config,"LOG_FILE":"/logs/pipeline.log"},
		mounts = [data_mount, logs_mount],
		docker_url = "unix://var/run/docker.sock",
		mount_tmp_dir = False
	)
	
	run_upload  = DockerOperator(
		task_id = "upload_on",
		image = IMAGE_NAME,
		container_name = "writer_data_scraped_worker",
		api_version = "auto",
		auto_remove = "force",
		network_mode = DOCKER_NETWORK_NAME,
		command = f"python src/Batch_Handling/write_on.py --data {SHARED_DATA_PATH}",
		environment = {**scraper_config,"LOG_FILE":"/logs/pipeline.log"},
		mounts = [data_mount, logs_mount],
		docker_url = "unix://var/run/docker.sock",
		mount_tmp_dir = False
	)

	run_scraper >> run_check_duplication >> run_upload

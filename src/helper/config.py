from pydantic_settings import BaseSettings , SettingsConfigDict


class setting (BaseSettings):

	minio_bucket_name : str
	minio_endpoint : str
	minio_access_key : str
	minio_secret_key : str
	postgres_user : str
	postgres_dbname : str
	postgres_passward : str
	postgres_host : str
	postgres_port : str
	AIRFLOW_UID : int



	model_config=SettingsConfigDict(env_file=".env")


def get_setting():
	return setting()
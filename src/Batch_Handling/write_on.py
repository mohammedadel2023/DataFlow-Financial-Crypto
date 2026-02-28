import boto3
from botocore.config import Config
import psycopg
from helper.config import get_setting
from datetime import datetime
import json
import io
import logging

logger = logging.getLogger(__name__)
    

def json_serial(obj):

	if isinstance(obj, datetime):
		return obj.isoformat()
	raise TypeError(f"Type {type(obj)} not serializable")

def write_on_minio(docs):
	setting = get_setting()

	logger.debug("establish a connection with minio")
	Client = boto3.client(
		"s3",
		endpoint_url = setting.minio_endpoint,
		aws_access_key_id = setting.minio_access_key,
		aws_secret_access_key = setting.minio_secret_key,
		config = Config(signature_version = "s3v4"),
		region_name = 'us-east-1'
	)

	logger.debug("the connection with minio is established successfuly")

	now = datetime.now()
	year = now.strftime("%Y")
	month = now.strftime("%m")
	day = now.strftime("%d")

	for doc in docs:

		jsonl_buffer = io.StringIO()
		for art in doc["list_of_art"]:
			json.dump(art, jsonl_buffer, default = json_serial)
			jsonl_buffer.write('\n')
		jsonl_buffer.seek(0)

		obj_name = f"{doc['topic_name']}/year={year}/month={month}/day={day}/articles_batch.jsonl"

		try :
			Client.put_object(
				Bucket = setting.minio_bucket_name,
				Key = obj_name,
				Body=jsonl_buffer.getvalue(),
				ContentType = "application/x-jsonlines",
			)
			logger.info(f"The article of tpoic :{doc['topic_name']} in date {year}/{month}/{day} is puted into bucket :{setting.minio_bucket_name} successfuly")
		except Exception as e:
			logger.error(f"Upload failed: {e}")

def write_on_postgreSQL(docs, connect_str:str,table:str ="batch_data"):

	logger.debug("establish a connection with postgreSQL")
	setting = get_setting()
	now = datetime.now()
	written_art = 0
	with psycopg.connect(connect_str) as conn:
		try :
			logger.debug("the connection with postgreSQL is established successfuly")
			with conn.cursor() as cur:

				for doc in docs:
					for art in doc["list_of_art"]:

						cur.execute(f"""
					 INSERT INTO {table} (content_hash, title, publish_date, scraped_at)
					  VALUES (%s, %s, %s, %s)
					 """,(art["hash"], art["art_title"], art["time"], now))
					written_art += 1
			conn.commit()
			logger.info(f"{written_art} articles are written on PostgreSQL successfully")
		except Exception as e:
			logger.error(f"error ocure before commit data into PostgreSQL :\n{e}")
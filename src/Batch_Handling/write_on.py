import boto3
from botocore.config import Config
import psycopg
from helper.config import get_setting
from datetime import datetime
import json
import io

def write_on_minio(docs):
	setting = get_setting()

	Client = boto3.client(
		"s3",
		endpoint_url = setting.minio_endpoint,
		aws_access_key_id = setting.minio_access_key,
		aws_secret_access_key = setting.minio_secret_key,
		config = Config(signature_version = "s3v4"),
		region_name = 'us-east-1'
	)

	now = datetime.now()
	year = now.strftime("%Y")
	month = now.strftime("%m")
	day = now.strftime("%d")

	for doc in docs:

		jsonl_buffer = io.StringIO()
		for art in doc["list_of_art"]:
			json.dump(art, jsonl_buffer)
			jsonl_buffer.write('\n')

		obj_name = f"{doc["topic_name"]}/year={year}/month={month}/day={day}/articles_batch.jsonl"

		try :
			Client.put_object(
				Bucket = setting.minio_bucket_name,
				Key = obj_name,
				Body=jsonl_buffer.getvalue(),
				ContentType = "application/x-jsonlines",
			)
			print(f"The article of tpoic :{doc["topic_name"]} in date {year}/{month}/{day} is puted into bucket :{setting.minio_bucket_name} successfuly")
		except Exception as e:
			print(f"Upload failed: {e}")

def write_on_postgreSQL(docs, connect_str:str,table:str ="batch_data"):

	setting = get_setting()
	now = datetime.now()
	with psycopg.connect(connect_str) as conn:
		try :
			with conn.cursor as cur:

				for doc in docs:
					for art in doc["list_of_art"]:

						cur.execute(f"""
					 INSERT INTO {table} (content_hash, title, publish_date, scraped_at)
					  VALUES (%s, %s, %s, %s)
					 """,(art["hash"], art["art_title"], art["time"], now))
			cur.commit()
		except Exception as e:
			print(f"error ocure before commit data into postgreSQL :\n{e}")
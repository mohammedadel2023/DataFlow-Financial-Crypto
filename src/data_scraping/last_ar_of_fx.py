import requests
from bs4 import BeautifulSoup
from art_data import data_arts
import boto3
from botocore.config import Config
from datetime import datetime
import json
import io
from helper.config import get_setting

def lasts_art_of(topic):
	url = f"https://www.coindesk.com/{topic}"

	response = requests.get(url)
	soup = BeautifulSoup(response.text, 'html.parser')

	doc_topic = {
		"topic_name":topic,
		"list_of_art":[]
	}

	article_containers = soup.find_all('div', class_='flex flex-col')


	for container in article_containers:
		link_tag = container.find('a')

		if link_tag:
			title_tag = link_tag.find('h2')
		
			if title_tag:
				title = title_tag.get_text(strip=True)
				link = link_tag['href']
				
				new_art = {
					"topic":topic,
					"art_add": f"https://www.coindesk.com{link}",
					"art_title": title,
					"discribtion":"",
					"writer":"",
					"time":"",
					"what_to_know":"",
					"text":"",
					"tags":[]
				}

				doc_topic['list_of_art'].append(new_art)

	return doc_topic

def scrap():

	setting = get_setting()

	Client = boto3.client(
		"s3",
		endpoint_url = setting.minio_endpoint,
		aws_access_key_id = setting.minio_access_key,
		aws_secret_access_key = setting.minio_secret_key,
		config = Config(signature_version = "s3v4"),
		region_name = 'us-east-1'
	)

	topics = ["markets", "tech", "business", "policy"]
	now = datetime.now()
	year = now.strftime("%Y")
	month = now.strftime("%m")
	day = now.strftime("%d")

	for topic in topics:
		doc_topic_data = lasts_art_of(topic)

		data_arts(doc_topic_data)

		jsonl_buffer = io.StringIO()
		for art in doc_topic_data["list_of_art"]:
			json.dump(art, jsonl_buffer)
			jsonl_buffer.write('\n')

		obj_name = f"{topic}/year={year}/month={month}/day={day}/articles_batch.jsonl"

		try :
			Client.put_object(
				Bucket = setting.minio_bucket_name,
				Key = obj_name,
				Body=jsonl_buffer.getvalue(),
				ContentType = "application/x-jsonlines",
			)
			print(f"The article of tpoic :{topic} in date {year}/{month}/{day} is puted into bucket :{setting.minio_bucket_name} successfuly")
		except Exception as e:
			print(f"Upload failed: {e}")

		
scrap()


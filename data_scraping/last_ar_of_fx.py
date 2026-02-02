import requests
from bs4 import BeautifulSoup
from art_data import data_arts
from minio import Minio
from minio.error import S3Error
from datetime import datetime
import json
import io

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

	Client = Minio(
		endpoint = "127.0.0.1:9000",
		access_key = "abcd",
		secret_key = "abcd2345",
		secure = False
	)

	topics = ["markets", "tech", "business", "policy"]
	bucket_name = "coindesk-raw"
	now = datetime.now()
	year = now.strftime("%Y")
	month = now.strftime("%m")
	day = now.strftime("%d")

	for topic in topics:
		doc_topic_data = lasts_art_of(topic)

		data_arts(doc_topic_data)

		obj_name = f"{topic}/year={year}/month={month}/day={day}/articles_batch.jsonl"
		tages = []
		for art in doc_topic_data["list_of_art"] :
			tages.extend(art["tags"])
		jsonl_content = "\n".join([json.dumps(art) for art in doc_topic_data["list_of_art"] ])
		data = io.BytesIO(jsonl_content.encode('utf-8'))

		Client.put_object(
			bucket_name = bucket_name,
			object_name = obj_name,
			length = len(jsonl_content),
			data = data,
			content_type = "application/x-jsonlines",
			tags = tages,
			metadata = topic
		)

		print(f"The article of tpoic :{topic} in date {year}/{month}/{day} is puted into bucket :{bucket_name} successfuly")
scrap()


import requests
from bs4 import BeautifulSoup
from .art_data import data_arts
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

	topics = ["markets", "tech", "business", "policy"]
	docs = []
	for topic in topics:
		doc_topic_data = lasts_art_of(topic)

		data_arts(doc_topic_data)
		docs.append(doc_topic_data)
	return docs


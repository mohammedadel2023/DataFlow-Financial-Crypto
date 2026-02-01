import requests
from bs4 import BeautifulSoup
from art_data import data_arts
import json

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

	for topic in topics:
		# 1. Get the data
		doc_topic_data = lasts_art_of(topic)
		
		# 2. Enrich the data
		data_arts(doc_topic_data)

		# 3. Save as JSONL
		try:
			# Change extension to .jsonl
			file_path = fr"C:\Users\User\OneDrive\D_EN_project\JSON_DATA\art_{topic}.jsonl"
			
			print(f"Saving {topic} to {file_path}...")
			
			with open(file_path, "w", encoding="utf-8") as f:
				# Loop through the list of articles
				for article in doc_topic_data['list_of_art']:
					# Dump ONE article per line
					json_line = json.dumps(article, ensure_ascii=False)
					f.write(json_line + "\n")
					
		except Exception as e:
			print(f"Error saving {topic}: {e}")

scrap()


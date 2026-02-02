import requests
from bs4 import BeautifulSoup
import time

def ex_art_data (art_obj):
	try:

		headers = {
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
		}
		response = requests.get(art_obj["art_add"], headers = headers)

		soup = BeautifulSoup(response.text,"html.parser")

		try:

			#  ---Head_handeling---
			header_div = soup.find("div",{"data-module-name":"article-header"})

			if header_div:
				article_header = header_div.div

				if (article_header.h2):
					art_obj["discribtion"] = article_header.h2.get_text(strip = True)

				wr_date = article_header.find_all("div")

				if (len(wr_date) >= 2):
					if ( wr_date[0].a):
						art_obj["writer"] = wr_date[0].a.get_text()
					
					if (wr_date[1].find('span')):
						art_obj["time"] = wr_date[1].find('span').get_text(strip=True)
		except Exception as e:
			print(f"Error parsing header for {art_obj['art_add']}: {e}")

		# extract "what to know part"
		what_to_know = soup.find('ul', class_='unordered-list')

		if (what_to_know):
			li = what_to_know.find_all('li')
			text = ""
			for i in li:
				text += i.get_text(strip = True) +" "
			art_obj["what_to_know"] = text.strip()

		# --- extract the text (body)----
		body_div = soup.find("div",{"data-module-name":"article-body"})

		if (body_div):
			article_body = body_div.div
			if (article_body):
				paragraph = article_body.find_all("p")
				The_text = ""

				for p in paragraph:
					The_text += p.get_text()
				art_obj["text"] = The_text

		#   ---extract the tages of article---

		article_tags = soup.find("div",{"data-module-name":"article-tags"}).div

		a_tags = article_tags.find_all("a")

		for a in a_tags:
			art_obj["tags"].append(a.get_text())

	except Exception as e:
		print(f"Failed to scrape {art_obj['art_add']}: {e}")

def data_arts (doc_arts):
	arts = doc_arts["list_of_art"]
	print(f"Scraping details for {len(arts)} articles in topic: {doc_arts['topic_name']}...")

	for i, art in enumerate(arts):
		ex_art_data(art)
		print(f" - Scraped: {art['art_title'][:30]}...")
		time.sleep(1)
#import requests
#from bs4 import BeautifulSoup
#
#BASE_URL = 'https://news.ycombinator.com/login?goto=news'
#USERNAME = "mohammed1_2-3"
#PASSWORD = "123456789"
#
#s = requests.Session()
#
#data = {"goto": "news", "acct": USERNAME, "pw": PASSWORD}
#r = s.post(f'{BASE_URL}\login', data=data)
#
#soup = BeautifulSoup(r.text, 'html.parser')
#
#if soup.find(id='logout') is not None:
#    print('Successfully logged in')
#else:
#    print('Authentication Error')
#    
#links = soup.findAll('tr', class_='athing')
#
#foramted_data = []
#
#for link in links :
#    data = {
#        "url":link.find_all('td')[2].span.a['href'],
#        "id":link['id'],
#        "title":link.find_all('td')[2].span.a.text,
#        "rank":int(link.find_all('td')[0].span.text.replace(".","")),
#	}
#    foramted_data.append(data)
#print(len(foramted_data))
#print(foramted_data[:6])


#links = soup.findAll('tr', class_='athing')
#
#for link in links:
#    data = {
#        'id': link['id'],
#        'title': link.find_all('td')[2].a.text,
#        "url": link.find_all('td')[2].a['href'],
#        "rank": int(link.find_all('td')[0].span.text.replace('.', ''))
#    }

#import requests
#
#url = "https://www.coindesk.com/api/v1/articles/section?size=10&section=markets"
#
## This 'headers' dictionary makes you look like a real Chrome browser
#headers = {
#    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
#    "Accept": "application/json",
#    "Referer": "https://www.coindesk.com/markets/",
#}
#
#response = requests.get(url, headers=headers)
#
#if response.status_code == 200:
#    data = response.json()
#    print("Success! Found", len(data), "articles.")
#else:
#    print(f"Failed with error: {response.status_code}")

import requests
from bs4 import BeautifulSoup

url = "https://www.coindesk.com/business/2026/01/30/tether-s-gold-holdings-top-usd17-billion-as-net-profits-surpassed-usd10-billion-for-2025/"

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')


#  ---Head_handeling---
#article_header = soup.find_all("div",{"data-module-name":"article-header"})[0].div
#
#discrebtion = article_header.h2.get_text(strip = True)
#
#wr_date = article_header.find_all("div")
#
#writer = wr_date[0].a.get_text()
#
#date = wr_date[1].find('span').get_text(strip=True)
#
#print(f"The discribtion is :\n{discrebtion}\n")
#print(f"the writer is :\n{writer}\n")
#print(f"the date is :\n{date}\n")
#print(wr_date[1])


# extract "what to know part"
#what_to_know = soup.find_all('ul', class_='unordered-list')
#
#li = what_to_know[0].find_all('li')
#for i in li:
#	print(i.string)

# --- extract the text (body)----
#article_body = soup.find("div",{"data-module-name":"article-body"}).div
#
#paragraph = article_body.find_all("p")
#
#The_text = ""
#
#for p in paragraph:
#	The_text += p.get_text()
#
#print(The_text)

#   ---extract the tages of article---

article_tags = soup.find("div",{"data-module-name":"article-tags"}).div

tags = []

a_tags = article_tags.find_all("a")

for a in a_tags:
	tags.append(a.get_text())
	print(a.get_text())

import hashlib
import psycopg
from helper.config import get_setting
from datetime import datetime
from dateutil import parser


def time_processing(art):

	clean_time = art['time'].replace("Updated", "").strip()
	clean_time = clean_time.replace("updated", "").strip()
	art['time'] = parser.parse(clean_time)
	return art['time']



def hashing(docs:list) -> None:

	for doc in docs:
		for art in doc["list_of_art"]:
			sha256 = hashlib.sha256()
			hash_text = str(time_processing(art)) + art["art_title"]
			#print(hash_text + "\n")
			sha256.update(hash_text.encode('utf-8'))
			art["hash"] = sha256.hexdigest()
			#print(f"the time of :{art['art_title']} is: {art['time']} and the hash is: {art['hash']}\n")

# Testing >> for hashing
#docs = [
#	{
#		"topic":"plicy",
#		"list_of_art":[
#			{
#				"time":"Jan 31, 2026, 6:22 p.m.",
#				"art_title":"ya rab"
#			},
#			{
#				"time":"Jan 29, 2026, 6:22 p.m.",
#				"art_title":"ya rabyyy"
#			}
#		]
#	},
#	{
#		"topic":"tech",
#		"list_of_art":[
#			{
#				"time":"Jan 31, 2026, 6:22 p.m.",
#				"art_title":"ya rab"
#			},
#			{
#				"time":"UpdatedJan 31, 2026, 10:46 p.m.",
#				"art_title":"ya rabyyy"
#			}
#		]
#	}
#]
#hashing(docs)

# duplication checking 

def check_duplication(connect_str: str, docs: list, hash_column: str="content_hash",
					  status_column: str="status", table: str="batch_data") -> None:

	with psycopg.connect(connect_str) as conn:
		with conn.cursor() as cur:
			for doc in docs:
				hash_list = [d["hash"] for d in doc["list_of_art"]]
				cur.execute(f"""
				SELECT {hash_column}, {status_column} 
				FROM {table}
				WHERE {hash_column} = ANY(%s)
				""",(hash_list,))

				existing_hashes = {row[0]: row[1] for row in cur.fetchall()}

				doc["list_of_art"] = [
					art for art in doc["list_of_art"] 
					if art["hash"] not in existing_hashes or existing_hashes[art["hash"]] == 'pending'
				]
				for art in doc["list_of_art"]:
					if art["hash"] in existing_hashes and existing_hashes[art["hash"]] == 'pending':
						art["on_postgress"] = False
					else:
						art["on_postgress"] = True
						


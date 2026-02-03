import hashlib
import psycopg
from helper.config import get_setting


def time_processing(art):
	time = []
	text = ""
	start_idx = 0
	if art["time"][0] == "U" or art["time"][0] == "u":
		start_idx = 7
	for i in range(start_idx, len(art["time"])):
		if (art["time"][i] != " "):
			if (art["time"][i] != ","):
				text += (art["time"][i])
		else:
			time.append(text)
			text = ""
	time.append(text)
	text_time = time[3] + time[4] + '/' + time[1]+ '/' + time[0] + '/' + time[2]
	art['time'] = text_time
	return art['time']



def hashing(docs):

	for doc in docs:
		for art in doc["list_of_art"]:
			sha256 = hashlib.sha256()
			hash_text = time_processing(art) + art["art_title"]
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

def check_duplication(connect_str,docs, hash_column:str = "content_hash", table:str ="batch_data"):

	with psycopg.connect(connect_str) as conn:
		with conn.cursor as cur:
			for doc in docs:
				hash_list = [d["hash"] for d in doc["list_of_art"]]
				cur.execute(f"""
				SELECT {hash_column} 
				FROM {table}
				WHERE {hash_column} = ANY(%s)
				""",(hash_list,))

				existing_hashes = {row[0] for row in cur.fetchall()}

				for art in doc["list_of_art"]:
					if art["hash"] in existing_hashes:
						doc["list_of_art"].remove(art)


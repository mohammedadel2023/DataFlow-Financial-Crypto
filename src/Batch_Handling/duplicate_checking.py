import hashlib
import psycopg
from dateutil import parser
import logging

logger = logging.getLogger(__name__)

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
			sha256.update(hash_text.encode('utf-8'))
			art["hash"] = sha256.hexdigest()


def check_duplication(connect_str: str, docs: list, hash_column: str="content_hash",
					  status_column: str="status", table: str="batch_data") -> None:

	logger.debug("Starting duplication checking && try to estabilish connection with PostgreSQL")
	with psycopg.connect(connect_str) as conn:
		with conn.cursor() as cur:
			logger.debug("Connection with PostgreSQL established successfully")
			for doc in docs:
				hash_list = [d["hash"] for d in doc["list_of_art"]]
				logger.debug(f"Checking for duplicates in {table} for {doc['topic_name']} topic")
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
						art["write_on_postgress"] = False
					else:
						art["write_on_postgress"] = True
						
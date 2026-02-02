from minio import Minio
from minio.error import S3Error
import json
def load_jsonl(file_path):
	"""
	Reads a JSONL file and returns a list of dictionaries.
	"""
	data = []
	with open(file_path, 'r', encoding='utf-8') as f:
		for line in f:
			line = line.strip()  # Remove leading/trailing whitespace
			if line:  # Skip empty lines
				try:
					json_object = json.loads(line)
					data.append(json_object)
				except json.JSONDecodeError as e:
					print(f"Error parsing line: {e}")
					continue
	return data

def main():
	
	client = Minio(
		endpoint="127.0.0.1:9000",
		access_key="abcd",
		secret_key="abcd2345",
		secure=False
	)

	file_source = r"C:\Users\User\OneDrive\D_EN_project\JSON_DATA\art_tech.jsonl"
	arts = load_jsonl(file_source)

	bucket_name = "coindesk-raw"
	destination_file = "tech/year=2026/month=1/day=31/articles_batch.jsonl"

	found = client.bucket_exists(bucket_name=bucket_name)

	if not (found):
		client.make_bucket(bucket_name)
		print("Created bucket", bucket_name)
	else:
		print("Bucket", bucket_name, "already exists")

	client.fput_object(
		bucket_name = bucket_name,
		object_name = destination_file,
		file_path = file_source,
		content_type = "application/x-jsonlines",
		user_metadata = {"topic":"markets"}
	)

	print(
		file_source, "successfully uploaded as object",
		destination_file, "to bucket", bucket_name,
	)

if __name__ == "__main__":
	try:
		main()
	except S3Error as exc:
		print("error occurred.", exc)

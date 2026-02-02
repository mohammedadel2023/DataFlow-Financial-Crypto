import boto3
from botocore.config import Config
import json
from helper.config import get_setting
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
	
	setting = get_setting()
	client = boto3.client(
		"s3",
		endpoint_url = setting.minio_endpoint,
		aws_access_key_id = setting.minio_access_key,
		aws_secret_access_key = setting.minio_secret_key,
		config = Config(signature_version='s3v4'),
		region_name='us-east-1'
	)

	file_source = r"C:\Users\User\OneDrive\D_EN_project\JSON_DATA\art_policy.jsonl"
	arts = load_jsonl(file_source)

	bucket_name = setting.minio_bucket_name
	destination_file = "policy/year=2026/month=1/day=31/articles_batch.jsonl"

	client.upload_file(
		file_source,
		bucket_name,
		destination_file
	)

	print(
		file_source, "successfully uploaded as object",
		destination_file, "to bucket", bucket_name,
	)

if __name__ == "__main__":
	try:
		main()
	except Exception as e:
		print(f"\nThe message error is:\n {e}\n")
		

import boto3
from botocore.config import Config


# Hardcode these JUST for this test to rule out config file errors
ENDPOINT = "http://127.0.0.1:9000"
ACCESS_KEY = "abcd"
SECRET_KEY = "abcd2345"
BUCKET = "coindesk-raw"

try:
    s3 = boto3.client(
        "s3",
        endpoint_url=ENDPOINT,
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        config=Config(signature_version="s3v4")
    )
    
    # Just try to list the buckets. If this works, your credentials are fine.
    response = s3.list_buckets()
    print("Success! Buckets found:", [b['Name'] for b in response['Buckets']])

except Exception as e:
    print(f"Failed: {e}")
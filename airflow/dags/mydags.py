from airflow.sdk import dag, task
from datetime import datetime

# 1. Define the DAG using the @dag decorator
@dag(
	schedule="@daily",
	start_date=datetime(2025, 1, 1),
	catchup=False,
	tags=["example", "sdk"]
)
def simple_sdk_dag():
	
	# 2. Define a task using the @task decorator
	@task
	def say_hello():
		print("Hello from the Airflow SDK!")
		return "Greeting sent"

	@task
	def process_data(message: str):
		print(f"Received message: {message}")

	# 3. Define the flow
	greeting = say_hello()
	process_data(greeting)

# 4. Instantiate the DAG
simple_sdk_dag()
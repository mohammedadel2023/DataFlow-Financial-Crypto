import psycopg

conn = psycopg.connect("dbname=DataFlow-Financial-Crypto user=M_admin password=abcd2345 host=localhost port=5432")

with conn.cursor() as cur:
    # Find which schema has batch_data
    cur.execute("""
        TRUNCATE TABLE batch_data;'
    """)
    results = cur.fetchall()
    for schema, table in results:
        print(f"Found in schema: '{schema}', table: '{table}'")
import json
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USERNAME"),
    password=os.getenv("DB_PASSWORD"),
)

cur = conn.cursor()

try:
    # reset tables
    cur.execute("TRUNCATE accepted, rejected RESTART IDENTITY;")

    # load accepted
    with open("data/processed/accepted.json") as f:
        accepted = json.load(f)

    for row in accepted:
        cur.execute(
            "INSERT INTO accepted (data) VALUES (%s)",
            [json.dumps(row)]
        )

    # load rejected
    with open("data/processed/rejected.json") as f:
        rejected = json.load(f)

    for row in rejected:
        cur.execute(
            "INSERT INTO rejected (data) VALUES (%s)",
            [json.dumps(row)]
        )

    conn.commit()

    print(f"Inserted {len(accepted)} accepted rows")
    print(f"Inserted {len(rejected)} rejected rows")

except Exception as e:
    conn.rollback()
    print("Error during load:", e)
    raise

finally:
    cur.close()
    conn.close()
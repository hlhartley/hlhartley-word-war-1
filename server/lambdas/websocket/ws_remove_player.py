import json
import psycopg2


host = ""
db_user = ""
db_password = ""
db_name = ""

conn = psycopg2.connect(
  dbname=db_name,
  user=db_user,
  password=db_password,
  host=host
)

def lambda_handler(event, context):
    connection_id = event.get("requestContext").get('connectionId')
    
    cur = conn.cursor()
    try:
        cur.execute(
            "DELETE FROM player WHERE connection_id = %s",
            (connection_id,)
        )
        conn.commit()
    except Exception:
        conn.rollback()
        
    return {'statusCode': 200}
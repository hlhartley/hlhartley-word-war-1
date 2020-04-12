import json
from utils import db_connection


conn = db_connection()

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
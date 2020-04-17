import json
import boto3
from utils import add_connection_to_game, db_connection

WS_URL = ""
conn = db_connection()

def lambda_handler(event, context):
    connection_id = event.get("requestContext").get('connectionId')
    body = json.loads(event.get("body"))
    id_game = body.get('gameId')
    
    try:
      add_connection_to_game(conn, id_game, connection_id)
      conn.commit()
    except Exception:
      conn.rollback()
    
    data = {
      "connection_id": connection_id,
      "id_game": id_game,
      "type": "ADD_CONNECTION"
    }

    gatewayapi = boto3.client("apigatewaymanagementapi", endpoint_url=WS_URL)
    
    try:
      gatewayapi.post_to_connection(
        ConnectionId=connection_id,
        Data=json.dumps(data).encode('utf-8'),
      )
      return {'statusCode': 200}
    except Exception:
      return {'statusCode': 400}
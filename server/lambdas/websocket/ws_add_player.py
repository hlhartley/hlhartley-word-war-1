import json
import boto3
from utils import add_connection_to_game, db_connection

WS_URL = ""
conn = db_connection()

def lambda_handler(event, context):
    connection_id = event.get("requestContext").get('connectionId')
    body = json.loads(event.get("body"))
    id_game = body.get('gameId')
    add_connection_to_game(conn, id_game, connection_id)
    conn.commit()

    gatewayapi = boto3.client("apigatewaymanagementapi", endpoint_url=WS_URL)
    gatewayapi.post_to_connection(
      ConnectionId=connection_id,
      Data=json.dumps({"connection_id": connection_id}).encode('utf-8'),
    )

    return {'statusCode': 200}
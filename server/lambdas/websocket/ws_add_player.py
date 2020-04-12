import json
from utils import add_player_to_game, check_existing_spymaster, db_connection


conn = db_connection()

def lambda_handler(event, context):
    connection_id = event.get("requestContext").get('connectionId')
    body = json.loads(event.get("body"))
    id_game = body.get('gameId')
    id_player = body.get('playerId')
    team = body.get('team')
    is_spymaster = body.get('isSpymaster', False)
      
    if is_spymaster and check_existing_spymaster(conn, id_game, team):
      return {'statusCode': 400}
    else:
      add_player_to_game(conn, id_game, id_player, is_spymaster, team, connection_id)
      conn.commit()
      return {'statusCode': 200}
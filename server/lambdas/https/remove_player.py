import json
from utils import db_connection, delete_player

conn = db_connection()

def lambda_handler(event, context):
    id_game = None
    id_player = None
    team = None
    pathParameters = event.get('pathParameters')
    
    if pathParameters:
      id_game = pathParameters.get('idGame')
      id_player = pathParameters.get('idPlayer')
      team = pathParameters.get('idTeam')
    
    row_count = delete_player(conn, id_game, team, id_player)
    
    if not row_count:
      return {
        'statusCode': 400,
        'headers': {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
        'body': json.dumps({
          'message': f'Unable to delete player: {id_player}. Player might not exist, is from wrong team, or is the spymaster'
        }),
      }
    else:
      conn.commit()
      return {
          'statusCode': 200,
          'body': json.dumps({'message': f'Successfully removed player {id_player}'}),
      }
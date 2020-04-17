import json
from utils import add_player_to_game, check_existing_spymaster, db_connection


conn = db_connection()

def lambda_handler(event, context):
    id_game = None
    id_player = None
    is_spymaster = False
    team = None
    pathParameters = event.get('pathParameters')
    queryStringParameters = event.get('queryStringParameters')
    
    if pathParameters:
      id_game = pathParameters.get('idGame')
      id_player = pathParameters.get('idPlayer')
      team = pathParameters.get('idTeam')
    
    if queryStringParameters:
      is_spymaster = queryStringParameters.get('is_spymaster', False)
      connection_id = queryStringParameters.get('connection_id', None)
      
    if is_spymaster and check_existing_spymaster(conn, id_game, team):
      return {
        'statusCode': 400,
        'headers': {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
        'body': json.dumps({'message': f'Spymaster already set for {team}'}),
      }
    else:
      add_player_to_game(conn, id_game, id_player, is_spymaster, team, connection_id)
      conn.commit()
      return {
          'statusCode': 200,
          'headers': {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
          'body': json.dumps({'message': f'Successfully added {id_player} to {team}'}),
      }
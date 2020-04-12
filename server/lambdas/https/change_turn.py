import json
from utils import db_connection, get_current_turn, change_turns

conn = db_connection()
  
def lambda_handler(event, context):
    id_game = None
    pathParameters = event.get('pathParameters')
    
    if pathParameters:
      id_game = pathParameters.get('idGame')
      
    team = get_current_turn(conn, id_game)
      
    if not team:
      return {
          'statusCode': 404,
          'headers': {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
          'body': json.dumps({'message': "Game not found"}),
      }
      
    try:
      change_turns(conn, id_game, team)
      conn.commit()
      return {
          'statusCode': 200,
          'headers': {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
          'body': json.dumps({'message': 'Successfully changed turns '}),
      }
    except Exception as err:
      return {
          'statusCode': 500,
          'headers': {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
          'body': json.dumps({'message': str(err)}),
      }
  
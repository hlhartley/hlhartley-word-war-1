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

def _add_player_to_game(id_game, id_player, is_spymaster, team):
  cur = conn.cursor()
  try:
    cur.execute("""
      INSERT INTO player (id_game, name, is_spymaster, team)
      VALUES (%s, %s, %s, %s)
    """, (id_game, id_player, is_spymaster, team))
  except Exception:
    conn.rollback()

def _check_existing_spymaster(id_game, team):
  cur = conn.cursor()
  try:
    cur.execute(""" 
      SELECT * FROM player
      WHERE id_game = %s AND team = %s AND is_spymaster = true;
    """, (id_game, team))
    return cur.fetchone()
  except Exception:
    conn.rollback()

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
      
    if is_spymaster and _check_existing_spymaster(id_game, team):
      return {
        'statusCode': 400,
        'headers': {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
        'body': json.dumps({'message': f'Spymaster already set for {team}'}),
      }
    else:
      _add_player_to_game(id_game, id_player, is_spymaster, team)
      conn.commit()
      return {
          'statusCode': 200,
          'headers': {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
          'body': json.dumps({'message': f'Successfully added {id_player} to {team}'}),
      }
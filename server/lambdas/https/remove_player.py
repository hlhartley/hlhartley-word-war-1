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

def _delete_player(id_game, team, id_player):
  cur = conn.cursor()
  try:
    cur.execute("""
      DELETE FROM player
      WHERE id_game = %s 
      AND team = %s
      AND name = %s
      AND is_spymaster = false
    """, (id_game, team, id_player,))
    return cur.rowcount
  except Exception:
    conn.rollback()

def lambda_handler(event, context):
    id_game = None
    id_player = None
    team = None
    pathParameters = event.get('pathParameters')
    
    if pathParameters:
      id_game = pathParameters.get('idGame')
      id_player = pathParameters.get('idPlayer')
      team = pathParameters.get('idTeam')
    
    row_count = _delete_player(id_game, team, id_player)
    
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
  
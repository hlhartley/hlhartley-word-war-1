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

def _add_player_to_game(id_game, id_player, is_spymaster, team, connection_id):
  cur = conn.cursor()
  try:
    cur.execute("""
      INSERT INTO player (id_game, name, is_spymaster, team, connection_id)
      VALUES (%s, %s, %s, %s, %s)
    """, (id_game, id_player, is_spymaster, team, connection_id))
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
    connection_id = event.get("requestContext").get('connectionId')
    body = json.loads(event.get("body"))
    id_game = body.get('gameId')
    id_player = body.get('playerId')
    team = body.get('team')
    is_spymaster = body.get('isSpymaster', False)
      
    if is_spymaster and _check_existing_spymaster(id_game, team):
      return {'statusCode': 400}
    else:
      _add_player_to_game(id_game, id_player, is_spymaster, team, connection_id)
      conn.commit()
      return {'statusCode': 200}
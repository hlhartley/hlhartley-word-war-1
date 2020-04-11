import json
import psycopg2

BOMB = 'bomb'
TEAM_1 = 'team_1'
TEAM_2 = 'team_2'
NEUTRAL = 'neutral'

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

def _perform_query(id_game, word):
  cur = conn.cursor()
  try:
    cur.execute("""
      SELECT game.turn, game_word.id_word, game_word.is_guessed, game_word.classifier 
      FROM game_word 
      JOIN word ON game_word.id_word = word.id
      JOIN game on game_word.id_game = game.id
      WHERE id_game = %s 
      AND word.content = %s;
    """, (id_game, word,))
    return cur.fetchone()
  except Exception:
    conn.rollback()
  
def _mark_word_as_guessed(id_game, id_word):
    cur = conn.cursor()
    try:
      cur.execute(""" 
        UPDATE game_word 
        SET is_guessed = true
        WHERE id_game = %s 
        AND id_word = %s;
      """, (id_game, id_word,))
    except Exception:
      conn.rollback()

def _change_turns(id_game, current_team, game_over=False):
    if game_over:
      turn = 'game_over'
    else:
      turn = TEAM_2 if current_team == TEAM_1 else TEAM_1
    
    cur = conn.cursor()
    try:
      cur.execute("UPDATE game SET turn = %s WHERE id = %s", (turn, id_game))
    except Exception:
      conn.rollback()
  
def lambda_handler(event, context):
    id_game = None
    word = None
    pathParameters = event.get('pathParameters')
    
    if pathParameters:
      id_game = pathParameters.get('idGame')
      team = pathParameters.get('idTeam')
      word = pathParameters.get('word')
      
    row = _perform_query(id_game, word)
    
    if not row:
      return {
        'statusCode': 404,
        'headers': {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
        'body': json.dumps({'message': f'{word} not found'}),
      }
  
    game_turn, id_word, is_guessed, classifier = row
    
    if game_turn != team:
      return {
        'statusCode': 400,
        'headers': {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
        'body': json.dumps({'message': "It is not your team's turn"}),
      }
    elif is_guessed:
      return {
        'statusCode': 400,
        'headers': {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
        'body': json.dumps({'message': f"{word} has already been guessed"}),
      }
    elif classifier == BOMB:
      _mark_word_as_guessed(id_game, id_word)
      _change_turns(id_game, team, game_over=True)
      conn.commit()
      return {
        'statusCode': 400,
        'headers': {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
        'body': json.dumps({'message': "OH NO!! BOOM"}),
      }
    else:
      _mark_word_as_guessed(id_game, id_word)
      _change_turns(id_game, team)
      conn.commit()
      return {
          'statusCode': 200,
          'headers': {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
          'body': json.dumps({'message': f'{word} successfully marked as guessed'}),
      }
  
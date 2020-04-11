import json
import psycopg2
import random


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

def _create_game():
  cur = conn.cursor()
  try:
    cur.execute("INSERT INTO game (turn) values (%s) RETURNING id", (TEAM_1,))
    return cur.fetchone()[0]
  except Exception:
    conn.rollback()
    
def _populate_words(idGame):
  cur = conn.cursor()
  classifiers = [BOMB] + [TEAM_1]*9 + [TEAM_2]*8 + [NEUTRAL]*7
  random.shuffle(classifiers)
  
  try:
    cur.execute("SELECT * FROM word ORDER BY RANDOM() LIMIT 25")
    words = cur.fetchall()
    game_words = []
  
    for i, word in enumerate(words):
      classifier = classifiers.pop()
      cur.execute(
        "INSERT INTO game_word (id_game, id_word, classifier, is_guessed) VALUES (%s, %s, %s, %s) RETURNING id",
        (idGame, word[0], classifier, False)
      )
      game_words.append({
        "id": cur.fetchone()[0],
        "text": word[1],
        "classifier": classifier,
        "is_guessed": False,
      })
    return game_words
    
  except Exception:
    conn.rollback()

def lambda_handler(event, context):
  id_game = _create_game()
  game_words = _populate_words(id_game)
  conn.commit()
  
  body = {
    'id_game': id_game,
    'current_turn': TEAM_1,
    'words': game_words,
    'team_1_remaining_words': 9,
    'team_2_remaining_words': 8,
    'team_1': [],
    'team_2': [],
  }
  
  return {
      'statusCode': 200,
      'headers': {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
      'body': json.dumps(body)
  }
  
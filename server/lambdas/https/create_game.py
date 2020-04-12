import json
from utils import db_connection, TEAM_1, create_game, populate_words

conn = db_connection()

def lambda_handler(event, context):
  id_game = create_game(conn)
  game_words = populate_words(conn, id_game)
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
  
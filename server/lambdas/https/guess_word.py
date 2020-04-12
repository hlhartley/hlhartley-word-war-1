import json
from utils import BOMB, TEAM_1, TEAM_2, NEUTRAL, db_connection, get_word_guess, mark_word_as_guessed


conn = db_connection()
  
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
      
    row = get_word_guess(conn, id_game, word)
    
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
      mark_word_as_guessed(conn, id_game, id_word)
      _change_turns(id_game, team, game_over=True)
      conn.commit()
      return {
        'statusCode': 400,
        'headers': {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
        'body': json.dumps({'message': "OH NO!! BOOM"}),
      }
    else:
      mark_word_as_guessed(conn, id_game, id_word)
      _change_turns(id_game, team)
      conn.commit()
      return {
          'statusCode': 200,
          'headers': {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
          'body': json.dumps({'message': f'{word} successfully marked as guessed'}),
      }
  
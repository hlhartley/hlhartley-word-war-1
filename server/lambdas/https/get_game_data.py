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

def _get_id_game(event):
    pathParameters = event.get('pathParameters')
    if pathParameters:
      return pathParameters.get('idGame')
    return None
    
def _is_spymaster(event):
    queryStringParameters = event.get('queryStringParameters')
    if queryStringParameters:
      return queryStringParameters.get('is_spymaster', False)
    return False

def _get_current_turn(id_game):
  cur = conn.cursor()
  try:
    cur.execute('SELECT turn FROM game where id = %s', (id_game,))
    return cur.fetchone()[0]
  except Exception:
    conn.rollback()
    
def _query_game_words(id_game):
  cur = conn.cursor()
  try:
    cur.execute("""
      SELECT game_word.id, word.content, game_word.classifier, game_word.is_guessed FROM game_word 
      JOIN word ON game_word.id_word = word.id
      WHERE id_game = %s
      ORDER BY game_word.id;
    """, (id_game,))
    return cur.fetchall()
  except Exception:
    conn.rollback()
    
def _map_game_words(query_results, is_spymaster):
  return [
    {
      "id": row[0],
      "text": row[1],
      "classifier": row[2] if is_spymaster or row[3] else None,
      "is_guessed": row[3],
    }
    for row in query_results
  ]  
  
def _get_remaining_words(game_words):
    team_1 = 9
    team_2 = 8
    
    for game_word in game_words:
        classifier = game_word.get('classifier')
        is_guessed = game_word.get('is_guessed')
        
        if classifier == TEAM_1 and is_guessed:
          team_1 = team_1 - 1
        elif classifier == TEAM_2 and is_guessed:
          team_2 = team_2 - 1
    
    return team_1, team_2
    
def _query_game_players(id_game):
  cur = conn.cursor()
  
  try:
    cur.execute("""
      SELECT id, name, is_spymaster, team
      FROM player where id_game = %s
    """,(id_game,))
    return cur.fetchall()
  except Exception:
    conn.rollback()

def _map_players(query_results):
  return [
    {
      "id": row[0],
      "name": row[1],
      "is_spymaster": row[2], 
      "team": row[3],
    } 
    for row in query_results
  ]
  
def _get_each_teams_players(all_players):
  team1 = []
  team2 = []
  
  for player in all_players:
    player_team = player.get('team')
    if player_team == TEAM_1:
      team1.append(player)
    elif player_team == TEAM_2:
      team2.append(player)
  
  return team1, team2
  
def _check_winner(team_1_count, team_2_count):
  if not team_1_count:
    return TEAM_1
  elif not team_2_count:
    return TEAM_2
  else:
    return None
  
def lambda_handler(event, context):
    id_game = _get_id_game(event)
    is_spymaster = _is_spymaster(event)
    query_results = _query_game_words(id_game)
    
    if not query_results:
      return {
        'statusCode': 404,
        'headers': {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
        'body': json.dumps({'message': 'Game not found'}),
      }

    game_words = _map_game_words(query_results, is_spymaster)
    team_1_count, team_2_count = _get_remaining_words(game_words)
    all_players = _map_players(_query_game_players(id_game))
    team_1, team_2 = _get_each_teams_players(all_players)
    current_turn = _get_current_turn(id_game)
    body = {
      'id_game': id_game,
      "current_turn": current_turn,
      "winner": _check_winner(team_1_count, team_2_count),
      'words': game_words,
      'team_1_remaining_words': team_1_count,
      'team_2_remaining_words': team_2_count,
      'team_1': team_1,
      'team_2': team_2,
    }

    return {
        'statusCode': 200,
        'headers': {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
        'body': json.dumps(body),
    }
  
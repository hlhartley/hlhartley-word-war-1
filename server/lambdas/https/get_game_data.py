import json
from utils import BOMB, TEAM_1, TEAM_2, NEUTRAL, db_connection, \
  get_current_turn, get_game_players, get_game_words, \
  map_players, map_game_words, get_remaining_words, get_each_teams_players, check_winner


conn = db_connection()

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
    
def lambda_handler(event, context):
    id_game = _get_id_game(event)
    is_spymaster = _is_spymaster(event)
    query_results = get_game_words(conn, id_game)
    
    if not query_results:
      return {
        'statusCode': 404,
        'headers': {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
        'body': json.dumps({'message': 'Game not found'}),
      }

    game_words = map_game_words(query_results, is_spymaster)
    team_1_count, team_2_count = get_remaining_words(game_words)
    all_players = map_players(get_game_players(conn, id_game))
    team_1, team_2 = get_each_teams_players(all_players)
    current_turn = get_current_turn(conn, id_game)
    body = {
      'id_game': id_game,
      "current_turn": current_turn,
      "winner": check_winner(team_1_count, team_2_count),
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
  
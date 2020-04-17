import json
import boto3
from utils import db_connection, BOMB, TEAM_1, TEAM_2, NEUTRAL, \
  get_current_turn, get_game_words, map_game_words, get_game_players, map_players, \
  check_winner, get_each_teams_players, get_remaining_words


WS_URL = ""
conn = db_connection()
    
def _generate_body(query_results, id_game, all_players, is_spymaster=False):
  game_words = map_game_words(query_results, is_spymaster)
  team_1_count, team_2_count = get_remaining_words(game_words)
  team_1, team_2 = get_each_teams_players(all_players)
  current_turn = get_current_turn(conn, id_game)

  return {
    'type': "GET_GAME_DATA",
    'id_game': id_game,
    "current_turn": current_turn,
    "winner": check_winner(team_1_count, team_2_count),
    'words': game_words,
    'team_1_remaining_words': team_1_count,
    'team_2_remaining_words': team_2_count,
    'team_1': team_1,
    'team_2': team_2,
  }
    
def _send_data_to(all_players, id_game, query_results):
  gatewayapi = boto3.client("apigatewaymanagementapi", endpoint_url=WS_URL)
  spymaster_body = _generate_body(query_results, id_game, all_players, is_spymaster=True)
  player_body = _generate_body(query_results, id_game, all_players)
  
  for player in all_players:
    connection_id = player.get('connection_id')
    body = spymaster_body if player.get('is_spymaster') else player_body
    
    try:
        gatewayapi.post_to_connection(
          ConnectionId=connection_id,
          Data=json.dumps(body).encode('utf-8'),
        )
    except Exception:
      continue
  
def lambda_handler(event, context):
    body = json.loads(event.get("body", {}))
    id_game = body.get('gameId')
    query_results = get_game_words(conn, id_game)
    
    if not query_results:
      return {'statusCode': 404}
    else:
      all_players = map_players(get_game_players(conn, id_game))
      _send_data_to(all_players, id_game, query_results)
      return {'statusCode': 200}
  
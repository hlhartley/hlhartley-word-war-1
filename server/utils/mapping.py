def map_game_words(query_results, is_spymaster):
  return [
    {
      "id": row[0],
      "text": row[1],
      "classifier": row[2] if is_spymaster or row[3] else None,
      "is_guessed": row[3],
    }
    for row in query_results
  ]

def map_players(query_results):
  return [
    {
      "id": row[0],
      "name": row[1],
      "is_spymaster": row[2], 
      "team": row[3],
      "connection_id": row[4],
    } 
    for row in query_results
  ]
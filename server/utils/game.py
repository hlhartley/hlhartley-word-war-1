from .constants import TEAM_1, TEAM_2


def get_remaining_words(game_words):
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

def get_each_teams_players(all_players):
  team1 = []
  team2 = []
  
  for player in all_players:
    player_team = player.get('team')
    if player_team == TEAM_1:
      team1.append(player)
    elif player_team == TEAM_2:
      team2.append(player)
  
  return team1, team2

def check_winner(team_1_count, team_2_count):
  if not team_1_count:
    return TEAM_1
  elif not team_2_count:
    return TEAM_2
  else:
    return None
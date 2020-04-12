import random
from .constants import BOMB, TEAM_1, TEAM_2, NEUTRAL

def create_game(conn):
  cur = conn.cursor()
  try:
    cur.execute("INSERT INTO game (turn) values (%s) RETURNING id", (TEAM_1,))
    return cur.fetchone()[0]
  except Exception:
    conn.rollback()

def populate_words(conn, id_game):
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
        (id_game, word[0], classifier, False)
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

def get_current_turn(conn, id_game):
  cur = conn.cursor()
  try:
    cur.execute('SELECT turn FROM game where id = %s', (id_game,))
    return cur.fetchone()[0]
  except Exception:
    conn.rollback()

def change_turns(conn, id_game, current_team, game_over=False):
    if game_over:
      turn = 'game_over'
    else:
      turn = TEAM_2 if current_team == TEAM_1 else TEAM_1
    
    cur = conn.cursor()
    try:
      cur.execute("UPDATE game SET turn = %s WHERE id = %s", (turn, id_game))
    except Exception:
      conn.rollback()

def get_game_words(conn, id_game):
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

def get_game_players(conn, id_game):
  cur = conn.cursor()
  
  try:
    cur.execute("""
      SELECT id, name, is_spymaster, team, connection_id
      FROM player where id_game = %s
    """,(id_game,))
    return cur.fetchall()
  except Exception:
    conn.rollback()

def add_player_to_game(conn, id_game, id_player, is_spymaster, team, connection_id=None):
  cur = conn.cursor()
  try:
    cur.execute("""
      INSERT INTO player (id_game, name, is_spymaster, team, connection_id)
      VALUES (%s, %s, %s, %s, %s)
    """, (id_game, id_player, is_spymaster, team, connection_id))
  except Exception:
    conn.rollback()

def delete_player(conn, id_game, team, id_player):
  cur = conn.cursor()
  try:
    cur.execute("""
      DELETE FROM player
      WHERE id_game = %s 
      AND team = %s
      AND name = %s
      AND is_spymaster = false
    """, (id_game, team, id_player,))
    return cur.rowcount
  except Exception:
    conn.rollback()

def check_existing_spymaster(conn, id_game, team):
  cur = conn.cursor()
  try:
    cur.execute(""" 
      SELECT * FROM player
      WHERE id_game = %s AND team = %s AND is_spymaster = true;
    """, (id_game, team))
    return cur.fetchone()
  except Exception:
    conn.rollback()

def get_word_guess(conn, id_game, word):
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

def mark_word_as_guessed(conn, id_game, id_word):
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
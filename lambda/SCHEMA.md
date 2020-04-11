* GAME table
  * id
  * turn

* WORD table
  * id
  * content

* GAME_WORD table
  * id 
  * id_game 
  * id_word 
  * classifier 
  * is_guessed 

* PLAYER table
  * id 
  * id_game 
  * name 
  * is_spymaster 
  * team 
  * connection_id 

import React, { useState, useEffect } from 'react';
import './main.scss';
import Board from './Board/Board';
import CardsRemaining from './CardsRemaining/CardsRemaining';
import TeamTurn from './TeamTurn/TeamTurn';
import Timer from './Timer/Timer';
import { fetchData } from './Helpers/requests';
import { createPlayer } from './Helpers/requests';

function App() {
  const [gameId, setGameId] = useState(0);
  const [words, setWords] = useState([])
  const [redCardCount, setRedCardCount] = useState(0);
  const [blueCardCount, setBlueCardCount] = useState(0);
  const [teamTurn, setTeamTurn] = useState('Red');
  const [isModal, setModal] = useState(true);
  const [displayForm, toggleForm] = useState(false);
  const [playerName, setPlayerName] = useState('');
  const [team, setTeam] = useState('team_1');
  const [role, setRole] = useState('player');

  async function createNewGame() {
    const result = await fetchData({ method: 'POST' });
    setWords(result.words)
    setRedCardCount(result.team_1_remaining_words);
    setBlueCardCount(result.team_2_remaining_words);
    determineTeamTurn(result.current_turn);
    setGameId(result.id_game);
  }
  
  async function getGameData(gameId) {
    const result = await fetchData({ method: 'GET', gameId });
    setWords(result.words)
    setRedCardCount(result.team_1_remaining_words);
    setBlueCardCount(result.team_2_remaining_words);
    determineTeamTurn(result.current_turn);
    console.log(result)
  }
  
  async function createNewPlayer() {
    const result = await createPlayer({ gameId, team, playerName });
  }

  function determineTeamTurn(team) {
    if (team === "team_1") {
      setTeamTurn('Red')
    } else {
      setTeamTurn('Blue')
    }
  }

  function handleSubmit(event) {
    event.preventDefault()
    createNewPlayer();
    getGameData(gameId);
    setModal(false);
  }

  function inputPlayerName(name) {
    setPlayerName(name);
  }

  function selectTeam(team) {
    setTeam(team);
  }

  function selectRole(role) {
    setRole(role);
  }

  function inputGameId(gameId) {
    setGameId(gameId);
  }

  function showForm() {
    return (
      <form onSubmit={handleSubmit}>
        <div>
          Red Team: 
        </div>
        <div>
          Blue Team: 
        </div>
        <label>Name:</label>
        <input type="text" value={playerName} name="name" onChange={(event) => inputPlayerName(event.target.value)}></input>
        <div>
          Select team: <button type="button" value="team_1" onClick={(event) => selectTeam(event.target.value)}>Red team</button><button type="button" value="team_2" onClick={(event) => selectTeam(event.target.value)}>Blue team</button>
        </div>
        <div>
          Select role: <button type="button" value="player" onClick={(event) => selectRole(event.target.value)}>Player</button><button type="button" value="spymaster" onClick={(event) => selectRole(event.target.value)}>Spymaster</button>
        </div>
        <label>Game Code:</label>
        <input type="text" name="gameId" value={gameId} onChange={(event) => inputGameId(event.target.value)}></input>
        <input type="submit" value="Submit" />
      </form>
    )
  }

  function render() {
    if (!isModal) {
      return (
        <div>
          <header>
            <h1>Word War I</h1>
            <div className="buttons__container">
              <button type="button" className="btn btn-primary" onClick={() => setModal(true)}>New Game</button>
              <button type="button" className="btn btn-primary" onClick={() => getGameData(gameId)}>Reset Game</button>
            </div>
          </header>
          <div className="dashboard__container">
            <CardsRemaining 
              redCardCount={redCardCount}
              blueCardCount={blueCardCount}
            />
            <TeamTurn 
              teamTurn={teamTurn}
            />
            <Timer />
          </div>
          <Board 
            setRedCardCount={setRedCardCount}
            setBlueCardCount={setBlueCardCount}
            words={words}
            gameId={gameId}
          />
        </div>
      )
    } else {
      return(
        <div>
          <header>
            <h1>Word War I</h1>
          </header>
            <button type="button" className="btn btn-primary" onClick={() => createNewGame()}>Create New Game</button>
            <button type="button" className="btn btn-primary" onClick={() => toggleForm(!displayForm)}>Join Game</button>
            {gameId > 0 && <div>
              Share this game code with your friends: {gameId}
            </div>}
            {displayForm && showForm()}
        </div>
      )
    }
  }

  return (
    <div className="App">
      {render()}
    </div>
  );
}

export default App;

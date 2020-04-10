import React, { useState, useEffect } from 'react';
import './main.scss';
import Board from './Board/Board';
import CardsRemaining from './CardsRemaining/CardsRemaining';
import TeamTurn from './TeamTurn/TeamTurn';
import Timer from './Timer/Timer';
import { fetchData } from './Helpers/requests';
import { createPlayer } from './Helpers/requests';

function App() {
  const [gameId, setGameId] = useState();
  const [words, setWords] = useState([])
  const [redCardCount, setRedCardCount] = useState(0);
  const [blueCardCount, setBlueCardCount] = useState(0);
  const [teamTurn, setTeamTurn] = useState('Red');
  const [isModal, setModal] = useState(true);
  const [displayForm, toggleForm] = useState(false);
  const [playerName, setPlayerName] = useState('');
  const [team, setTeam] = useState('team_2');
  const [isSpymaster, setSpymaster] = useState(false);
  const [errorMessage, setErrorMessage] = useState();
  const [redTeam, setRedTeam] = useState([]);
  const [blueTeam, setBlueTeam] = useState([]);

  async function createNewGame() {
    const result = await fetchData({ method: 'POST' });
    setWords(result.words)
    setRedCardCount(result.team_1_remaining_words);
    setBlueCardCount(result.team_2_remaining_words);
    determineTeamTurn(result.current_turn);
    setRedTeam(result.team_1);
    setBlueTeam(result.team_2);
    setGameId(result.id_game);
  }
  
  async function getGameData(gameId) {
    const result = await fetchData({ method: 'GET', gameId });
    setWords(result.words)
    setRedCardCount(result.team_1_remaining_words);
    setBlueCardCount(result.team_2_remaining_words);
    determineTeamTurn(result.current_turn);
    setRedTeam(result.team_1);
    setBlueTeam(result.team_2);
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

  function showForm() {
    return (
      <form onSubmit={handleSubmit}>
        <div className="separator">Info</div>
        <div className="input-group">
          <div className="input-group-prepend">
            <span className="input-group-text" id="basic-addon1">Game Code</span>
          </div>
          <input type="text" name="gameId" value={gameId} className="form-control" aria-label="Game Code" aria-describedby="basic-addon1" onChange={(event) => setGameId(event.target.value)} onBlur={() => getGameData(gameId)}></input>
        </div>
        <div className="input-group">
          <div className="input-group-prepend">
            <span className="input-group-text" id="basic-addon1">Name</span>
          </div>
          <input type="text" value={playerName} name="name" className="form-control" aria-label="Name" aria-describedby="basic-addon1" onChange={(event) => setPlayerName(event.target.value)}></input>
        </div>
        <div className="buttons__container">
          <button type="button" value="false" name="options" id="option1" className="btn btn-outline-dark" autoComplete="off" onClick={(event) => setSpymaster(event.target.value)}><i className="fas fa-user"></i> Player</button>
          <span>OR</span>
          <button type="button" value="true" name="options" id="option2" className="btn btn-dark" autoComplete="off" onClick={(event) => setSpymaster(event.target.value)}><i className="fas fa-user-secret"></i> Spymaster</button>
        </div>
        <div className="team-members__container">
          <div className="red">
            <span>{redTeam.length > 0 ? `${redTeam.length} members` : `0 members`}</span>
            <button type="button" value="team_1" className="btn btn-danger" onClick={(event) => setTeam(event.target.value)}><i className="far fa-flag"></i> Join team</button>
          </div>
          <div className="blue">
            <span>{blueTeam.length > 0 ? `${blueTeam.length} members` : `0 members`}</span>
            <button type="button" value="team_2" className="btn btn-primary" onClick={(event) => setTeam(event.target.value)}><i className="far fa-flag"></i> Join team</button>
          </div>
        </div>
        <div className="buttons__container">
          <input type="submit" value="Enter Game" className="btn btn-info" />
        </div>
      </form>
    )
  }

  function render() {
    console.log(redTeam, blueTeam)
    if (!isModal) {
      return (
        <div>
          <header>
            <h1>Word War I</h1>
            <div className="buttons__container">
              <button type="button" className="btn btn-info" onClick={() => setModal(true)}>New Game</button>
              <button type="button" className="btn btn-outline-info" onClick={() => getGameData(gameId)}>Reset Game</button>
            </div>
          </header>
          <div className="dashboard__container">
            { isSpymaster ? <div className={redTeam ? "red player-role" : "blue player-role"}><i className="fas fa-user-secret"></i> <span>Spymaster</span></div> : <div className={redTeam ? "red player-role" : "blue player-role"}><i className="fas fa-user"></i> <span>Player</span></div> }
            <CardsRemaining 
              redCardCount={redCardCount}
              blueCardCount={blueCardCount}
            />
            <TeamTurn 
              teamTurn={teamTurn}
            />
            <Timer />
          </div>
          {errorMessage}
          <Board 
            setRedCardCount={setRedCardCount}
            setBlueCardCount={setBlueCardCount}
            words={words}
            gameId={gameId}
            team={team}
            getGameData={getGameData}
            setErrorMessage={setErrorMessage}
          />
        </div>
      )
    } else {
      return(
        <div className="modal-screen">
          <header>
            <h1>Word War I</h1>
          </header>
          <div className="buttons__container">
            <button type="button" className="btn btn-outline-info" onClick={() => createNewGame()}>Create New Game</button>
            <button type="button" className="btn btn-info" onClick={() => toggleForm(!displayForm)}>Join Game</button>
          </div>
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

import React, { useState, useEffect } from 'react';
import './main.scss';
import Board from './Board/Board';
import CardsRemaining from './CardsRemaining/CardsRemaining';
import TeamTurn from './TeamTurn/TeamTurn';
import Timer from './Timer/Timer';
import { fetchData, createPlayer } from './Helpers/requests';
import { socket, addPlayer, removePlayer, getGameData } from './Helpers/socket';

function App() {
  const [gameId, setGameId] = useState();
  const [words, setWords] = useState([])
  const [team1CardCount, setTeam1CardCount] = useState(0);
  const [team2CardCount, setTeam2CardCount] = useState(0);
  const [teamTurn, setTeamTurn] = useState();
  const [isModal, setModal] = useState(true);
  const [displayForm, toggleForm] = useState(false);
  const [playerName, setPlayerName] = useState('');
  const [team, setTeam] = useState('team_1');
  const [isSpymaster, setSpymaster] = useState(false);
  const [errorMessage, setErrorMessage] = useState();
  const [team_1, setTeam1] = useState([]); //red
  const [team_2, setTeam2] = useState([]); //blue

  useEffect(() => {
    socket.addEventListener('message', function (event) {
      let data = null; 
      
      try {
        data = JSON.parse(event.data);
      } catch (error) {
        console.error(error);
      }

      debugger

      if (data) {
        setWords(data.words);
        setTeam1CardCount(data.team_1_remaining_words);
        setTeam2CardCount(data.team_2_remaining_words);
        determineTeamTurn(data.current_turn);
        setTeam1(data.team_1);
        setTeam2(data.team_2);
      }

    })
  }, []);

  async function createNewGame() {
    const result = await fetchData({ method: 'POST' });
    setWords(result.words)
    setTeam1CardCount(result.team_1_remaining_words);
    setTeam2CardCount(result.team_2_remaining_words);
    determineTeamTurn(result.current_turn);
    setTeam1(result.team_1);
    setTeam2(result.team_2);
    setGameId(result.id_game);
  }
  
  // async function getGameData(gameId) {
  //   const result = await fetchData({ method: 'GET', gameId });
  //   setWords(result.words);
  //   setTeam1CardCount(result.team_1_remaining_words);
  //   setTeam2CardCount(result.team_2_remaining_words);
  //   determineTeamTurn(result.current_turn);
  //   setTeam1(result.team_1);
  //   setTeam2(result.team_2);
  //   console.log(result)
  // }
  
  // async function createNewPlayer(selectedTeam) {
  //   await createPlayer({ gameId, team: selectedTeam, playerName, isSpymaster });
  // }

  function determineTeamTurn(team) {
    setTeamTurn(team);
  }

  function handleSubmit(event) {
    event.preventDefault()
    getGameData(gameId);
    setModal(false);
  }

  // async function joinTeam(selectedTeam) {
  //   setTeam(selectedTeam);
  //   await createNewPlayer(selectedTeam);
  //   getGameData(gameId);
  // }
  
  async function joinTeam(selectedTeam) {
    setTeam(selectedTeam);
    await addPlayer(gameId, playerName, selectedTeam, isSpymaster);
    getGameData(gameId);
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
          <button type="button" name="options" id="option1" className="btn btn-outline-dark" autoComplete="off" onClick={() => setSpymaster(false)}><i className="fas fa-user"></i> Player</button>
          <span>OR</span>
          <button type="button" name="options" id="option2" className="btn btn-outline-dark" autoComplete="off" onClick={() => setSpymaster(true)}><i className="fas fa-user-secret"></i> Spymaster</button>
        </div>
        <div className="team-members__container">
          <div className="team_1">
            <div>
              {team_1.length === 0 ? <div>0 members</div> : team_1.map((member) => member.is_spymaster ? <div><i className="fas fa-user-secret"></i>{member.name}</div> : <div><i className="fas fa-user"></i>{member.name}</div>)}
            </div>
            <button type="button" value="team_1" className="btn btn-danger" onClick={(event) => joinTeam(event.target.value)}><i className="far fa-flag"></i> Join team {`(${team_1.length})`}</button>
          </div>
          <div className="team_2">
            <div>
              {team_2.length === 0 ? <div>0 members</div> : team_2.map((member) => member.is_spymaster ? <div><i className="fas fa-user-secret"></i>{member.name}</div> : <div><i className="fas fa-user"></i>{member.name}</div>)}
            </div>
            <button type="button" value="team_2" className="btn btn-primary" onClick={(event) => joinTeam(event.target.value)}><i className="far fa-flag"></i> Join team {`(${team_2.length})`}</button>
          </div>
        </div>
        <div className="buttons__container">
          <input type="submit" value="Enter Game" className="btn btn-info" />
        </div>
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
              <button type="button" className="btn btn-info" onClick={() => setModal(true)}>New Game</button>
              <button type="button" className="btn btn-outline-info" onClick={() => getGameData(gameId)}>Reset Game</button>
            </div>
          </header>
          <div className="dashboard__container">
            { isSpymaster ? <div className={team_1 ? "team_1 player-role" : "team_2 player-role"}><i className="fas fa-user-secret"></i> <span>Spymaster</span></div> : <div className={team_1 ? "team_1 player-role" : "team_2 player-role"}><i className="fas fa-user"></i> <span>Player</span></div> }
            <CardsRemaining 
              team1CardCount={team1CardCount}
              team2CardCount={team2CardCount}
            />
            <TeamTurn 
              teamTurn={teamTurn}
            />
            <Timer />
          </div>
          {errorMessage}
          <Board 
            setTeam1CardCount={setTeam1CardCount}
            setTeam2CardCount={setTeam2CardCount}
            words={words}
            gameId={gameId}
            team={teamTurn} // This should just be {team}
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

import React, { useState, useEffect } from 'react';
import './main.scss';
import Board from './Board/Board';
import CardsRemaining from './CardsRemaining/CardsRemaining';
import TeamTurn from './TeamTurn/TeamTurn';
import Timer from './Timer/Timer';
import { fetchData } from './Helpers/requests';

function App() {
  const [gameId, setGameId] = useState(null);
  const [words, setWords] = useState([])
  const [redCardCount, setRedCardCount] = useState(0);
  const [blueCardCount, setBlueCardCount] = useState(0);
  const [teamTurn, setTeamTurn] = useState('Red');

  async function createNewGame() {
    const result = await fetchData({ method: 'POST' });
    setWords(result.words)
    setRedCardCount(result.team_1_remaining_words);
    setBlueCardCount(result.team_2_remaining_words);
    setGameId(result.id_game);
    console.log(result)
  }
  
  async function getGameData(gameId) {
    const result = await fetchData({ method: 'GET', gameId });
    setWords(result.words)
    setRedCardCount(result.team_1_remaining_words);
    setBlueCardCount(result.team_2_remaining_words);
  }

  return (
    <div className="App">
      <header>
        <h1>Word War I</h1>
        <div className="buttons__container">
          <button type="button" className="btn btn-primary" onClick={() => createNewGame()}>New Game</button>
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
  );
}

export default App;

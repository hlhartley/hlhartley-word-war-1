import React, { useState, useEffect } from 'react';
import './main.scss';
import Board from './Board/Board';
import CardsRemaining from './CardsRemaining/CardsRemaining';
import TeamTurn from './TeamTurn/TeamTurn';
import Timer from './Timer/Timer';
import { fetchData } from './Helpers/requests';

function App() {
  const [redCardCount, setRedCardCount] = useState(8);
  const [blueCardCount, setBlueCardCount] = useState(9);
  const [teamTurn, setTeamTurn] = useState('Red');
  const [words, setWords] = useState([])

  useEffect(async () => {
    const result = await fetchData('22', 'GET');
    console.log(result)
    setWords(result.words)
  }, []);

  return (
    <div className="App">
      <header>
        <h1>Word War I</h1>
        <div className="buttons__container">
          <button type="button" className="btn btn-primary">New Game</button>
          <button type="button" className="btn btn-primary">Reset Game</button>
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
      />
    </div>
  );
}

export default App;

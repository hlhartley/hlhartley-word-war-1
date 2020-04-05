import React from 'react';
import './main.scss';
import Board from './Board/Board';
import CardsRemaining from './CardsRemaining/CardsRemaining';
import PlayerTurn from './PlayerTurn/PlayerTurn';
import Timer from './Timer/Timer';

function App() {
  return (
    <div className="App">
      <header>
        <h1>Word War I</h1>
        <div className="buttons__container">
          <button>New Game</button>
          <button>Reset Game</button>
        </div>
      </header>
      <div className="dashboard__container">
        <CardsRemaining />
        <PlayerTurn />
        <Timer />
      </div>
      <Board />
    </div>
  );
}

export default App;

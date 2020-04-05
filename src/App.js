import React from 'react';
import './main.scss';
import Board from './Board/Board';
import CardsRemaining from './CardsRemaining/CardsRemaining';
import PlayerTurn from './PlayerTurn/PlayerTurn';
import Timer from './Timer/Timer';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Word War I</h1>
      </header>
      <button>End Game</button>
      <CardsRemaining />
      <PlayerTurn />
      <Timer />
      <Board />
    </div>
  );
}

export default App;

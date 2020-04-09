import React, { useState } from 'react';
import '../main.scss';

function Timer() {
  const [countDown, setCountDown] = useState(30);
  const [timerOn, toggleTimer] = useState(true);

  return (
    <div className="Timer">
      <span>{countDown} seconds</span>
      <button type="button" className={timerOn ? "btn btn-outline-success" : "btn btn-outline-danger"}>{timerOn ? "start" : "stop"}</button>
    </div>
  );
}

export default Timer;
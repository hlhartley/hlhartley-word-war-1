import React, { useState } from 'react';
import '../main.scss';

function Timer() {
  const [countDown, setCountDown] = useState(30);
  const [timerOn, toggleTimer] = useState(true);

  return (
    <div className="Timer">
      <i class="far fa-clock"></i>
      <span>{countDown} s</span>
      <button type="button" className={timerOn ? "btn btn-success" : "btn btn-danger"}>{timerOn ? "start" : "stop"}</button>
    </div>
  );
}

export default Timer;
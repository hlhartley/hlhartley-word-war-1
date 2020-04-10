import React from 'react';
import '../main.scss';

function CardsRemaining(props) {
  return (
    <div className="CardsRemaining">
      <span className="blue card-count"> <i class="fas fa-square"></i>{props.blueCardCount} </span>
      <span className="red card-count"> <i class="fas fa-square"></i>{props.redCardCount} </span>
      <span className="bomb card-count"> <i class="fas fa-bomb"></i>1 </span>
    </div>
  );
}

export default CardsRemaining;
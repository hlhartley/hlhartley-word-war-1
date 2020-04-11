import React from 'react';
import '../main.scss';

function CardsRemaining(props) {
  return (
    <div className="CardsRemaining">
      <span className="team_2 card-count"> <i className="fas fa-square"></i>{props.team2CardCount} </span>
      <span className="team_1 card-count"> <i className="fas fa-square"></i>{props.team1CardCount} </span>
      <span className="bomb card-count"> <i className="fas fa-bomb"></i>1 </span>
    </div>
  );
}

export default CardsRemaining;
import React from 'react';
import '../main.scss';

function CardsRemaining(props) {
  return (
    <div className="CardsRemaining">
      Cards Remaining: <span className="blue-card-count">{props.blueCardCount}</span> - <span className="red-card-count">{props.redCardCount}</span>
    </div>
  );
}

export default CardsRemaining;
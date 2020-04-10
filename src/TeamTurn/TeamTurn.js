import React from 'react';
import '../main.scss';

function TeamTurn(props) {
  return (
    <div className="TeamTurn">
      <span className={props.teamTurn === "Red" ? "red team-turn__text" : "blue team-turn__text"}><i class="fas fa-user-friends"></i>'s Turn</span>
    </div>
  );
}

export default TeamTurn;
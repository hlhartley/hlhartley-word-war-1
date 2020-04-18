import React from 'react';
import '../main.scss';

function TeamTurn(props) {
  return (
    <div className="TeamTurn">
      <span className={props.teamTurn === "team_1" ? "team_1 team-turn__text" : "team_2 team-turn__text"}><i className="fas fa-user-friends"></i>'s Turn</span>
    </div>
  );
}

export default TeamTurn;
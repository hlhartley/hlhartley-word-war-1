import React from 'react';
import '../main.scss';

function Board(props) {
  console.log(props.words)
  return (
    <div className="Board">
      <div className="words__row">
        {props.words.map((word) => {
          return <section className={word.classifier}>{word.text}</section>
        })}
      </div>
    </div>
  );
}

export default Board;
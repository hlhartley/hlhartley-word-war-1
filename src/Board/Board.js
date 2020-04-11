import React from 'react';
import '../main.scss';
import { makeGuess } from '../Helpers/requests';

function Board(props) {
  const { gameId, team, getGameData } = props;
  async function guessWord(word) {
    await makeGuess({ gameId, team, word });
    getGameData(gameId)
  }

  return (
    <div className="Board">
      <div className="words__row">
        {props.words.map((word) => {
          return <section key={word.text} className={word.is_guessed ? word.classifier : ''} onClick={() => guessWord(word.text)}>{word.text}</section>
        })}
      </div>
    </div>
  );
}

export default Board;
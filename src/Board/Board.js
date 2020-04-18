import React from 'react';
import '../main.scss';
import { makeGuess } from '../Helpers/requests';
import { getGameData } from '../Helpers/socket';

function Board(props) {
  const { gameId, team, isSpymaster } = props;
 
  async function guessWord(word) {
    if (word.is_guessed || isSpymaster) {
      return;
    }
    await makeGuess({ gameId, team, word: word.text });
    getGameData(gameId);
  }

  function sectionClass(word) {
    const classes = [];
    
    if (word.is_guessed && isSpymaster) {
      classes.push('spymaster__guessed');
    }
    if (word.is_guessed || isSpymaster) {
      classes.push(word.classifier);
    }

    return classes.join(' ');
  }

  return (
    <div className="Board">
      <div className="words__row">
        {props.words.map((word) => {
          return (
            <section key={word.text} className={sectionClass(word)} onClick={() => guessWord(word)}>
              {word.text}
            </section>
          )
        })}
      </div>
    </div>
  );
}

export default Board;
const BASE_URL = `https://ndlqoav0w5.execute-api.us-west-2.amazonaws.com/dev`

export const fetchData = async ({ method, gameId, data = null }) => {
  let endpoint;
  let params;
  switch (method) {
    case 'DELETE':
      params = { 
        method
      };
      endpoint = `${BASE_URL}/game/${gameId}`
      break
    case 'POST':
        params = {
          method,
          headers: {
            'Content-type': 'application/json'
          },
        };
        endpoint = `${BASE_URL}/game/`
        break
    case 'GET':
      params = {
        method,
        headers: {
          'Content-type': 'application/json'
        },
      };
      endpoint = `${BASE_URL}/game/${gameId}`
      break
    default:
      params = {
        method: method,
        body: JSON.stringify(data),
        headers: {
          'Content-type': 'application/json'
        }
      }
  }

  const response = await fetch(endpoint, params);

  if (response.status >= 300) {
    throw new Error('Failed network request')
  } else {
    return await response.json()
  }
}

export const makeGuess = async ({ gameId, team, word }) => {
  let endpoint = `${BASE_URL}/game/${gameId}/team/${team}/guess/${word}`
  const response = await fetch(endpoint, 
    {
      method: 'POST',
      headers: {
        'Content-type': 'application/json'
      },
    })

  if (response.status >= 300) {
    return "It's not your turn"
  } else {
    return await response.json()
  }
}


export const createPlayer = async ({ gameId, team, playerName, connectionId ,isSpymaster }) => {
  let endpoint = `${BASE_URL}/game/${gameId}/team/${team}/player/${playerName}?connection_id=${connectionId}`
  if (isSpymaster) endpoint += '&is_spymaster=true';

  const response = await fetch(endpoint, 
    {
      method: 'POST',
      headers: {
        'Content-type': 'application/json'
      },
    })

  if (response.status >= 300) {
    throw new Error('Failed network request')
  } else {
    return await response.json()
  }
}
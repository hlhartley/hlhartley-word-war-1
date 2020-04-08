export const fetchData = async (gameId, method, data = null) => {
  const endpoint = `https://ndlqoav0w5.execute-api.us-west-2.amazonaws.com/dev/game/${gameId}`
  let params;
  switch (method) {
    case 'DELETE':
      params = { 
        method,
        mode: 'no-cors' 
      };
      break
    case 'GET':
      params = {
        method,
        headers: {
          'Content-type': 'application/json'
        },
      }
      break
    default:
      params = {
        method: method,
        body: JSON.stringify(data),
        headers: {
          'Content-type': 'application/json'
        },
        mode: 'no-cors'
      }
  }

  const response = await fetch(endpoint, params);

  if (response.status >= 300) {
    throw new Error('Failed network request')
  } else {
    return await response.json()
  }
}
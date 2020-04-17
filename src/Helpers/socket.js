const SOCKET_URL = 'wss://emkh1mv1x1.execute-api.us-west-2.amazonaws.com/dev/';

export const socket = new WebSocket(SOCKET_URL);

export const addPlayer = (gameId, playerId, team, isSpymaster) => {
  socket.send(JSON.stringify({
    action: "addPlayer", 
    gameId,
    playerId,
    team,
    isSpymaster,
  }))  
};

export const removePlayer = () => {
  socket.send(JSON.stringify({ action: "removePlayer" }))  
};

export const getGameData = (gameId) => {
  socket.send(JSON.stringify({ 
    action: "getGameData", 
    gameId, 
  }))    
};

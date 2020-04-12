## Infrastructure

We are using a "serverless" setup utilizing AWS services. There are 2 Api Gateways:

1) HTTPS API Gateway --> Lambda --> RDS(Postgres)
2) Websocket API Gateway --> Lambda --> RDS(Postgres)

## HTTP endpoints

  Will document

## WebSocket events

  0. From the client app, you can do something like this:

  1. To add player (action = addPlayer)
      
      ```
        socket.send(JSON.stringify({
          "action": "addPlayer", 
          "gameId": 84,
          "playerId": "Boolean",
          "team": "team_1",
          "isSpymaster": true,
        }))  
      ```
  
  2. To remove player (action = removePlayer)
  
      ```
        socket.send(JSON.stringify({ "action": "removePlayer" }))  
      ```
      
  3. To get game data (action = getGameData)
  
      ```
        socket.send(JSON.stringify({ "action": "getGameData", "gameId": 84 }))  
      ```

## Infrastructure

We are using a "serverless" setup utilizing AWS services. There are 2 Api Gateways:

1) REST API Gateway --> Lambda --> RDS(Postgres)
2) WebSocket API Gateway --> Lambda --> RDS(Postgres)

## HTTPS endpoints

  1. To create game
      
      `POST /game`
      
  2. To get game data
  
      `GET /game/<idGame>`
      
  3. To submit a word guess
  
      `POST /game/<idGame>/team/<idTeam>/guess/<word>`
  
  4. To force game to change turns (ex: timer runs out)

      `POST /game/<idGame>/change-turn`
      
  5. To add player to team (**deprecated**, use the WebSocket action instead)
  
      `POST /game/<idGame>/team/<idTeam>/player/<idPlayer>`
      
      `POST /game/<idGame>/team/<idTeam>/player/<idPlayer>?is_spymaster=true` - for spymaster
  
  6. To remove player (**deprecated**, use the WebSocket action instead)
  
      `DELETE /game/<idGame>/team/<idTeam>/player/<idPlayer>`
      

## WebSocket events

  0. From the client app, you can do something like this to instantiate a socket connection:
  
      ```
        const socket = new WebSocket('wss://<some_websocket_url>');
        
        // To listen to messages from the server add an event listener:
        
        socket.onmessage = function(event) {
          console.log(JSON.parse(event.data))
        }
      ```

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

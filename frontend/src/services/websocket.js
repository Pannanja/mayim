const endpoint = "ws://localhost:8000/ws";

export function connectToWebSocket(onMessageCallback) {
  const ws = new WebSocket(endpoint);

  ws.onmessage = function (event) {
      const data = JSON.parse(event.data);
      onMessageCallback(data);
  };

  return ws;
}

export function sendMessage(ws, message) {
  ws.send(message);
}
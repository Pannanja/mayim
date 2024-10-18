const endpoint = "ws://localhost:8000/ws";

export function connectToWebSocket(onMessageCallback) {
  const ws = new WebSocket(endpoint);

  ws.onopen = function () {
    console.log('WebSocket connection established');
  };

  ws.onmessage = function (event) {
    const data = JSON.parse(event.data);
    onMessageCallback(data);
  };

  ws.onclose = function () {
    console.log('WebSocket connection closed');
  };

  ws.onerror = function (error) {
    console.error('WebSocket error:', error);
  };

  return ws;
}

export function sendMessage(ws, message) {
  if (ws && ws.readyState === WebSocket.OPEN) {
    ws.send(message);
  } else {
    console.error('WebSocket is not open. Ready state:', ws.readyState);
  }
}

export const fetchQuestions = (socket) => {
  if (socket && socket.readyState === WebSocket.OPEN) {
    socket.send(JSON.stringify({ type: 'fetch_questions' }));
  } else {
    console.error('WebSocket is not open. Ready state:', socket.readyState);
  }
};
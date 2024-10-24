import React, { useState, useEffect } from 'react';
import { connectToWebSocket, sendMessage } from '../services/websocket';

const ChatBox = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [socket, setSocket] = useState(null);

  useEffect(() => {
    const ws = connectToWebSocket((newMessage) => {
      if (newMessage.sender === "bot") {
        setMessages((prevMessages) => [...prevMessages, { sender: 'Chatbot', text: newMessage.message }]);
      }
    });
    setSocket(ws);
    
    return () => {
      ws.close();
    };
  }, []);

  const handleSend = () => {
    if (input.trim() && socket) {
      // Add the user's message to the chat
      setMessages((prevMessages) => [...prevMessages, { sender: 'You', text: input }]);
      // Send message as JSON to the server
      sendMessage(socket, JSON.stringify({ message: input }));
      setInput('');
    }
  };

  return (
    <div style={{ padding: '10px' }}>
      <div style={{ height: '150px', overflowY: 'auto', border: '1px solid #ccc', marginBottom: '10px' }}>
        {messages.map((msg, index) => (
          <div key={index}>
            <strong>{msg.sender}: </strong>{msg.text}
          </div>
        ))}
      </div>
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={(e) => e.key === 'Enter' && handleSend()}
        placeholder="Type your message..."
      />
      <button onClick={handleSend}>Send</button>
    </div>
  );
};

export default ChatBox;
import React, { useState, useEffect } from 'react';
import { connectToWebSocket, sendMessage } from '../../services/websocket';
import { useReferences } from '../../context/ReferenceContext';
import './ChatBox.css'; // Import the CSS file

const ChatBox = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [socket, setSocket] = useState(null);
  const { references } = useReferences();

  useEffect(() => {
    const ws = connectToWebSocket((newMessage) => {
      // if the message is from the bot, append the token to the last message
      if (newMessage.sender === "bot") {
        console.log(newMessage);
        if (newMessage.type === "start")
          setMessages((prevMessages) => [...prevMessages, { sender: 'Chatbot', text: newMessage.message }]);
        else if (newMessage.type === "stream")
          setMessages((prevMessages) => [...prevMessages.slice(0, prevMessages.length - 1), { sender: 'Chatbot', text: prevMessages[prevMessages.length - 1].text + newMessage.message }]);
        else if (newMessage.type === "end")
          setMessages((prevMessages) => [...prevMessages, { sender: 'Chatbot', text: prevMessages[prevMessages.length - 1].text + newMessage.message }]);
        else
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
      // Send message as JSON to the server, including the reference list
      const messagePayload = {
        message: input,
        references: references,
      };
      sendMessage(socket, JSON.stringify(messagePayload));
      setInput('');
    }
  };

  return (
    <div className="chatbox-container">
      <div className="chatbox-messages">
        {messages.map((msg, index) => (
          <div key={index} className={msg.sender === 'You' ? 'user-message' : 'bot-message'}>
            <strong>{msg.sender}: </strong>{msg.text}
          </div>
        ))}
      </div>
      <div className="input-row">
        <input
          type="text"
          className="chatbox-input"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSend()}
          placeholder="Message the stars..."
        />
        <button className="chatbox-button" onClick={handleSend}>Send</button>
      </div>
    </div>
  );
};

export default ChatBox;
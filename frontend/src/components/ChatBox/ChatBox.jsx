import React, { useState, useEffect, useRef, ChangeEvent, KeyboardEvent } from 'react';
import { useWebSocket } from '../../services/useWebSocket'; // Custom hook to manage WebSocket connection
import { useReferences } from '../../context/ReferenceContext';
import './ChatBox.css'; // Import the CSS file

const url = 'ws://localhost:8000/ws'; // WebSocket server URL
const ChatBox = () => {
  const [messages, setMessages] = useState([{ user: 'Bot', msg: 'Welcome! How can I be of service today?' }]);
  const [input, setInput] = useState('');
  const { references } = useReferences();

  // WebSocket connection logic (message handling & status tracking)
  const { response, isOpen, sendMessage } = useWebSocket(url);
  const messagesEndRef = useRef(null); // Ref for scrolling to the latest message
  const containerRef = useRef(null); // Ref for the chat container
  const [autoScroll, setAutoScroll] = useState(true);

  useEffect(() => {
    // Handle WebSocket responses and update messages
    if (response) {
      setMessages((prevMessages) => {
        const lastMessage = prevMessages[prevMessages.length - 1];
        // Update last bot message or add a new one
        if (lastMessage && lastMessage.user === 'Bot') {
          lastMessage.msg = response;
          return [...prevMessages];
        } else {
          return [...prevMessages, { user: 'Bot', msg: response }];
        }
      });
    }
  }, [response]);

  // Updates input field on change
  const handleChange = (event) => {
    setInput(event.target.value);
  };

  // Handles sending of messages from the user
  const handleSubmit = () => {
    if (input.trim()) {
      const userMessage = { user: 'User', msg: input };
      setMessages((prevMessages) => [...prevMessages, userMessage]); // Add user message to list
      setInput('');

      if (isOpen) {
        sendMessage(input); // Send message via WebSocket if open
      }
    }
  };

  const scrollToBottom = () => {
    if(containerRef.current && autoScroll) {
      if (messagesEndRef.current) {
        messagesEndRef.current.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      }
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  };

  // Scrolls to the bottom of the chat container whenever a new message is added
  useEffect(() => {
    scrollToBottom();
  }, [messages]);


  // Handles "Enter" key submission without needing to click the send button
  const handleKeyDown = (event) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault(); // Prevent default newline
      handleSubmit();
    }
  };

  return (
    <div className="chatbox-container">
      <div className="chat-header">
        {/* Connection status indicator and title */}
        <div className={`connection-status ${isOpen ? 'online' : 'offline'}`}></div>
        <b>Look to the Heavens</b>
      </div>
      <div className="chat-container" ref={containerRef}>
        {/* Display chat messages */}
        <div className="chatbox-messages">
          {messages.map((msg, index) => (
            <div key={index} className={msg.user === 'User' ? 'user-message' : 'bot-message'}>
              <strong>{msg.user}: </strong>
              <br />
              {msg.msg}
            </div>
          ))}
          <div ref={messagesEndRef} /> {/* Reference to scroll to the latest message */}
        </div>
        {/* Input form for typing and sending messages */}
        <form className="chat-form" onSubmit={(e) => e.preventDefault()}>
          <div className="input-row">
            <textarea
              value={input}
              onChange={handleChange}
              onKeyDown={handleKeyDown}
              placeholder="Converse with your models..."
              rows={2}
              className="chatbox-input"
            />
            <div className='send-options'>
              <button type="button" onClick={handleSubmit} className="chatbox-button">Send</button>
              <label className="autoscroll-checkbox">
                <input
                  type="checkbox"
                  checked={autoScroll}
                  onChange={() => setAutoScroll(!autoScroll)}
                  />
                Auto Scroll
            </label>
                </div>
          </div>
        </form>
      </div>
    </div>
  );
};

export default ChatBox;
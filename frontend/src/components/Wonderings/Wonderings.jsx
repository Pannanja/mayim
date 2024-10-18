import React, { useState, useEffect } from 'react';
import { connectToWebSocket, fetchQuestions } from '../../services/websocket';
import './Wonderings.css'; // Make sure to create and style this CSS file

const defaultQuestions = [
  "What is the meaning of life?",
  "How can I find inner peace?",
  "What is the purpose of suffering?",
  "How do I connect with my spiritual self?",
  "What is the nature of the universe?"
];

const Wonderings = ({ onAddToChat }) => {
  const [hoveredIndex, setHoveredIndex] = useState(null);
  const [questions, setQuestions] = useState(defaultQuestions);
  const [socket, setSocket] = useState(null);

  useEffect(() => {
    const ws = connectToWebSocket((newMessage) => {
      if (newMessage.type === 'questions') {
        setQuestions(newMessage.questions);
      }
    });
    setSocket(ws);

    return () => {
      ws.close();
    };
  }, []);

  useEffect(() => {
    if (socket) {
      fetchQuestions(socket);
    }
  }, [socket]);

  return (
    <div className="wonderings-container">
      {questions.map((question, index) => (
        <div
          key={index}
          className={`wondering-dot ${hoveredIndex === index ? 'expanded' : ''}`}
          onMouseEnter={() => setHoveredIndex(index)}
          onMouseLeave={() => setHoveredIndex(null)}
          onClick={() => onAddToChat(question)}
        >
          <div className="wondering-question">{question}</div>
        </div>
      ))}
    </div>
  );
};

export default Wonderings;
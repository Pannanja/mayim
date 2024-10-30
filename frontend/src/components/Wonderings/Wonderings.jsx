import React, { useState, useEffect } from 'react';
import './Wonderings.css'; // Make sure to create and style this CSS file

const defaultTopics = [
  "Afterlife",
  "Free Will",
  "Consciousness",
  "Morality",
  "Marriage",
];

const Wondering = ({ topic, onAddToChat }) => {
  const [question, setQuestion] = useState(topic);
  const [hovered, setHovered] = useState(false);

  const fetchQuestion = async () => {
    const response = await fetch(`/wondering?topic=${topic}`);
    const reader = response.body.getReader();
    const decoder = new TextDecoder("utf-8");
    let done = false;
    let buffer = "";

    while (!done) {
      const { value, done: doneReading } = await reader.read();
      done = doneReading;
      buffer += decoder.decode(value, { stream: true });

      // Split the response into individual JSON objects
      const parsedResponses = buffer.split("\n").filter(Boolean);

      // Process each complete JSON object
      parsedResponses.forEach((responseStr, index) => {
        try {
          const parsedResponse = JSON.parse(responseStr);
          const content = parsedResponse.message?.content || "";
          setQuestion((prevQuestion) => (prevQuestion === topic ? content : prevQuestion + content));
        } catch (error) {
          if (index === parsedResponses.length - 1) {
            // If it's the last item and parsing failed, it might be incomplete
            buffer = responseStr;
          } else {
            console.error('Error parsing response:', error);
          }
        }
      });

      // Remove processed JSON objects from the buffer
      buffer = parsedResponses.length ? parsedResponses[parsedResponses.length - 1] : "";
    }
  };

  return (
    <div
      className={`wondering-dot ${hovered ? 'expanded' : ''}`}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
      onClick={fetchQuestion}
    >
      <div className="wondering-question" onClick={() => onAddToChat(question)}>
        {question}
      </div>
    </div>
  );
};

const Wonderings = ({ onAddToChat }) => {
  return (
    <div className="wonderings-container">
      {defaultTopics.map((topic, index) => (
        <Wondering key={index} topic={topic} onAddToChat={onAddToChat} />
      ))}
    </div>
  );
};

export default Wonderings;
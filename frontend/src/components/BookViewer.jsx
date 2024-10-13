import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';

const BookViewer = () => {
  const { bookId, chapter } = useParams();
  const [verses, setVerses] = useState([]);

  useEffect(() => {
    fetch(`/verses/${bookId}/${chapter}`)
      .then((response) => response.json())
      .then((data) => setVerses(data))
      .catch((error) => console.error('Error fetching verses:', error));
  }, [bookId, chapter]);

  const handleImportToChat = (text) => {
    // Logic for importing selected text into the chat
    // Could be implemented using a global state or WebSocket message
    console.log('Text imported to chat:', text);
  };

  return (
    <div style={{ padding: '10px' }}>
      <h2>Book: {bookId}, Chapter: {chapter}</h2>
      <div>
        {verses.map((verse, index) => (
          <p key={index} onClick={() => handleImportToChat(verse.text)}>
            {verse.text}
          </p>
        ))}
      </div>
      <div>
        <Link to={`/verses/${bookId}/${parseInt(chapter) - 1}`}>Previous Chapter</Link>
        <Link to={`/verses/${bookId}/${parseInt(chapter) + 1}`}>Next Chapter</Link>
      </div>
    </div>
  );
};

export default BookViewer;
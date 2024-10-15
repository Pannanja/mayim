import React, { useState } from 'react';

const Reference = ({ addReference }) => {
  const [book, setBook] = useState('');
  const [chapter, setChapter] = useState('');
  const [verse, setVerse] = useState('');

  const handleAddReference = () => {
    if (book && chapter && verse) {
      addReference({ book, chapter, verse });
      setBook('');
      setChapter('');
      setVerse('');
    }
  };

  return (
    <div>
      <h2>Add Reference</h2>
      <div>
        <label>
          Book:
          <input
            type="text"
            value={book}
            onChange={(e) => setBook(e.target.value)}
          />
        </label>
      </div>
      <div>
        <label>
          Chapter:
          <input
            type="text"
            value={chapter}
            onChange={(e) => setChapter(e.target.value)}
          />
        </label>
      </div>
      <div>
        <label>
          Verse:
          <input
            type="text"
            value={verse}
            onChange={(e) => setVerse(e.target.value)}
          />
        </label>
      </div>
      <button onClick={handleAddReference}>Add to References</button>
    </div>
  );
};

export default Reference;
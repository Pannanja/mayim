import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';

const Verses = () => {
  const [verses, setVerses] = useState([]);
  const { bookId, chapter } = useParams();

  useEffect(() => {
    fetch(`/books/${bookId}/${chapter}`)
      .then((response) => response.json())
      .then((data) => setVerses(data))
      .catch((error) => console.error('Error fetching verses:', error));
  }, [bookId, chapter]);

  return (
    <div>
    <h2>Chapter</h2>
    <table style={{ width: '100%', borderCollapse: 'collapse' }}>
      <thead>
      </thead>
      <tbody>
        {verses.map((item, index) => (
          <tr key={index}>
            <td style={{ padding: '8px', textAlign: 'right' }}>{item.text}</td>
            <td style={{ padding: '8px', textAlign: 'right' }}>{item.verse}</td>
          </tr>
        ))}
      </tbody>
    </table>
  </div>
  );
};

export default Verses;

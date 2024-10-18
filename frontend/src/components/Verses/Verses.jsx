import './Verses.css';
import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { useCurrentChapter } from '../../context/CurrentChapterContext';

const Verses = () => {
  const [verses, setVerses] = useState([]);
  const { bookId, chapter } = useParams();
  const { setCurrentChapter } = useCurrentChapter();

  useEffect(() => {
    const fetchVerses = async () => {
      try {
        const response = await fetch(`/verses/${bookId}/${chapter}`);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        console.log('Fetched data:', data);
        if (Array.isArray(data)) {
          setVerses(data);
          setCurrentChapter({ bookId, chapter });
        } else {
          console.error('Expected an array but got:', data);
          setVerses([]);
        }
      } catch (error) {
        console.error('Error fetching verses:', error);
        setVerses([]);
      }
    };

    fetchVerses();
  }, [bookId, chapter, setCurrentChapter]);

  return (
    <div className="StoneTable">
      <h2>Chapter</h2>
      <table style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
        </thead>
        <tbody>
          {Array.isArray(verses) ? (
            verses.map((item, index) => (
              <tr key={index}>
                <td style={{ padding: '8px', textAlign: 'right' }}>{item.text}</td>
                <td style={{ padding: '8px', textAlign: 'right' }}>{item.verse}</td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan="2">No verses available</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
};

export default Verses;
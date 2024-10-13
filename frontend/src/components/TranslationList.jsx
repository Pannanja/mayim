import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';

const TranslationList = () => {
  const [translations, setTranslations] = useState([]);

  useEffect(() => {
    fetch('/translations')
      .then((response) => response.json())
      .then((data) => setTranslations(data))
      .catch((error) => console.error('Error fetching translations:', error));
  }, []);

  return (
    <div style={{ padding: '10px' }}>
      <h2>Translations</h2>
      <ul>
        {translations.map((translation) => (
          <li key={translation.id}>
            <Link to={`/books/${translation.id}`}>{translation.name}</Link>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default TranslationList;
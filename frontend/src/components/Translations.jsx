import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

const Translations = () => {
  const [translations, setTranslations] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchTranslations = async () => {
      try {
        const response = await fetch('/translations');
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        console.log('Fetched data:', data);
        if (Array.isArray(data)) {
          setTranslations(data);
        } else {
          console.error('Expected an array but got:', data);
          setTranslations([]);
        }
      } catch (error) {
        console.error('Error fetching translations:', error);
        setTranslations([]);
      }
    };

    fetchTranslations();
  }, []);

  const handleClick = (id) => {
    navigate(`/books/${id}`);
  };

  return (
    <div>
      <h1>Translations</h1>
      <ul>
        {translations.length > 0 ? (
          translations.map((translation) => (
            <li key={translation.id} onClick={() => handleClick(translation.id)}>
              {translation.name} ({translation.language})
            </li>
          ))
        ) : (
          <li>No translations available</li>
        )}
      </ul>
    </div>
  );
};

export default Translations;
import './Books.css';
import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import Scroll from './Scroll'; // Import the Scroll component

const Books = () => {
  const [books, setBooks] = useState([]);
  const { translationId = 1 } = useParams();
  const navigate = useNavigate();

  useEffect(() => {
    const fetchBooks = async () => {
      try {
        const response = await fetch(`/books/${translationId}`);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        console.log('Fetched data:', data);
        if (Array.isArray(data)) {
          setBooks(data);
        } else {
          console.error('Expected an array but got:', data);
          setBooks([]);
        }
      } catch (error) {
        console.error('Error fetching books:', error);
        setBooks([]);
      }
    };

    fetchBooks();
  }, [translationId]);

  const handleClick = (bookId) => {
    navigate(`/verses/${bookId}/1`); // Default to chapter 1 for now
  };

  return (
    <Scroll>
      <div className="ScriptureScroll">
        <ul>
          {Array.isArray(books) ? (
            books.map((book) => (
              <li key={book.id} onClick={() => handleClick(book.id)}>
                {book.name_in_english}
              </li>
            ))
          ) : (
            <li>No books available</li>
          )}
        </ul>
      </div>
    </Scroll>
  );
};

export default Books;
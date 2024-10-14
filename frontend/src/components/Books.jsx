import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';

const Books = () => {
  const [books, setBooks] = useState([]);
  const { translationId } = useParams();
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
    <div>
      <h1>Books</h1>
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
  );
};

export default Books;
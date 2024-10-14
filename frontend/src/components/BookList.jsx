import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';

const BookList = () => {
  const { translationId } = useParams();
  const [books, setBooks] = useState([]);

  useEffect(() => {
    fetch(`/books/${translationId}`)
      .then((response) => response.json())
      .then((data) => setBooks(data))
      .catch((error) => console.error('Error fetching books:', error));
  }, [translationId]);

  return (
    <div style={{ padding: '10px' }}>
      <h2>Books</h2>
      <ul>
        {books.map((book) => (
          <li key={book.id}>
            <Link to={`/books/1`}>{book.name}</Link>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default BookList;
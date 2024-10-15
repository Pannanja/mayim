import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import Translations from './Translations';
import Books from './Books';
import Verses from './Verses';

const BibleBrowser = () => {
  return (
    <Router>
      <div>
        {/* Navigation Menu */}
        <nav style={{ marginBottom: '20px' }}>
          <Link to="/translations">Translations</Link> |{' '}
          <Link to="/books/1">Books for Translation 1</Link> |{' '}
          <Link to="/verses/1/1">Verses for Book 1, Chapter 1</Link>
        </nav>

        {/* Route Definitions */}
        <Routes>
          <Route path="/" element={<Books />} />
          <Route path="/translations" element={<Translations />} />
          <Route path="/books/:translationId" element={<Books />} />
          <Route path="/verses/:bookId/:chapter" element={<Verses />} />
        </Routes>
      </div>
    </Router>
  );
};

export default BibleBrowser;

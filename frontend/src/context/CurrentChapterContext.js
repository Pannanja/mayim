// src/context/CurrentChapterContext.js
import React, { createContext, useContext, useState } from 'react';

const CurrentChapterContext = createContext();

export const useCurrentChapter = () => useContext(CurrentChapterContext);

export const CurrentChapterProvider = ({ children }) => {
  const [currentChapter, setCurrentChapter] = useState({ bookId: '', chapter: '' });

  return (
    <CurrentChapterContext.Provider value={{ currentChapter, setCurrentChapter }}>
      {children}
    </CurrentChapterContext.Provider>
  );
};
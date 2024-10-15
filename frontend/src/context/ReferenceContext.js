// src/context/ReferenceContext.js
import React, { createContext, useContext, useState, useEffect } from 'react';

const ReferenceContext = createContext();

export const useReferences = () => useContext(ReferenceContext);

export const ReferenceProvider = ({ children }) => {
  const [references, setReferences] = useState(() => {
    const savedReferences = localStorage.getItem('references');
    return savedReferences ? JSON.parse(savedReferences) : [];
  });

  useEffect(() => {
    localStorage.setItem('references', JSON.stringify(references));
  }, [references]);

  const addReference = (newReference) => {
    setReferences([...references, newReference]);
  };

  const removeReference = (index) => {
    setReferences(references.filter((_, i) => i !== index));
  };

  return (
    <ReferenceContext.Provider value={{ references, addReference, removeReference }}>
      {children}
    </ReferenceContext.Provider>
  );
};
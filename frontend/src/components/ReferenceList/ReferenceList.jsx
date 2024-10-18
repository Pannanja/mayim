import React from 'react';
import { useReferences } from '../../context/ReferenceContext';
import { useCurrentChapter } from '../../context/CurrentChapterContext';
import './ReferenceList.css'; // Import the CSS file

const ReferenceList = () => {
  const { references, addReference, removeReference } = useReferences();
  const { currentChapter } = useCurrentChapter();

  const importCurrentChapter = () => {
    const { bookId, chapter } = currentChapter;
    if (bookId && chapter) {
      const newReference = {
        book: bookId,
        chapter: chapter,
      };
      addReference(newReference);
    } else {
      console.error('Current chapter is not set');
    }
  };

  return (
    <div className="reference-list">
      <h2>Reference List</h2>
      <button className="import-button" onClick={importCurrentChapter}>Import Current Chapter</button>
      <ul>
        {references.map((ref, index) => (
          <li key={index} className="reference-cloud">
            {ref.book} Chapter {ref.chapter}
            <button className="remove-button" onClick={() => removeReference(index)}>X</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ReferenceList;
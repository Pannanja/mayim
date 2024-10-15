import React from 'react';
import { useReferences } from '../context/ReferenceContext';
import { useCurrentChapter } from '../context/CurrentChapterContext';

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
    <div>
      <h2>Reference List</h2>
      <button onClick={importCurrentChapter}>Import Current Chapter</button>
      <ul>
        {references.map((ref, index) => (
          <li key={index}>
            {ref.book} Chapter {ref.chapter}
            <button onClick={() => removeReference(index)}>Remove</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ReferenceList;
import React from 'react';

const Verse = ({ data }) => {
    return (
        <div>
          <h2>Chapter</h2>
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
            </thead>
            <tbody>
              {data.map((item, index) => (
                <tr key={index}>
                  <td style={{ padding: '8px', textAlign: 'right' }}>{item.text}</td>
                  <td style={{ padding: '8px', textAlign: 'right' }}>{item.verse}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      
    );
};

export default Verse;
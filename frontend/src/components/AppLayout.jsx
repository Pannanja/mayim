// frontend/components/AppLayout.jsx
import React from 'react';
import ChatBox from './ChatBox';
import BookViewer from './BookViewer';

const AppLayout = ({ children }) => {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100vh' }}>
      {/* Fixed Chat Box */}
      <div style={{ flex: '0 1 auto', borderBottom: '1px solid #ccc' }}>
        <ChatBox />
      </div>
      
      {/* Dynamic Content Area */}
      <div style={{ flex: '1 1 auto', overflowY: 'auto' }}>
        <BookViewer />
        {children}
      </div>
    </div>
  );
};

export default AppLayout;

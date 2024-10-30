// FileTransmit.js

import React, { useRef } from 'react';

function FileTransmit({ onUploadComplete }) {
  const fileInputRef = useRef();

  const handleUploadClick = () => {
    fileInputRef.current.click();
  };

  const handleFileChange = async (event) => {
    const files = event.target.files;
    if (files.length > 0) {
      const formData = new FormData();
      for (const file of files) {
        formData.append('files', file);
      }

      try {
        const response = await fetch('http://127.0.0.1:8000/file_transmit/upload', {
          method: 'POST',
          body: formData,
        });

        if (response.ok) {
          alert('Files successfully uploaded');
          if (onUploadComplete) {
            onUploadComplete();
          }
        } else {
          const errorData = await response.json();
          alert('Upload failed: ' + errorData.error);
        }
      } catch (error) {
        alert('Upload failed: ' + error.message);
      } finally {
        // Clear the input value to allow the same files to be selected again if needed
        event.target.value = null;
      }
    }
  };

  const handleDownloadClick = async () => {
    try {
      const response = await fetch(`http://127.0.0.1:8000/file_transmit/download`);
      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'workspace.zip';
        document.body.appendChild(a);
        a.click();
        a.remove();
      } else {
        const errorData = await response.json();
        alert('Download failed: ' + errorData.error);
      }
    } catch (error) {
      alert('Download failed: ' + error.message);
    }
  };

  return (
    <div style={{ display: 'flex', gap: '10px' }}>
      <input
        type="file"
        ref={fileInputRef}
        style={{ display: 'none' }}
        onChange={handleFileChange}
        multiple // Allow multiple file selection
      />
      <button onClick={handleUploadClick}>Upload</button>
      <button onClick={handleDownloadClick}>Download</button>
    </div>
  );
}

export default FileTransmit;

// ConfigWindow.js

import React, { useState } from 'react';
import ConfigManager from './ConfigManager';

function ConfigWindow({ onClose }) {
  const settings = ConfigManager.getSettings();

  const [llmModel, setLlmModel] = useState(settings.llmModel);
  const [backendScript, setBackendScript] = useState(settings.backendScript);
  const [workingFolder, setWorkingFolder] = useState(settings.workingFolder);

  const handleSave = () => {
    ConfigManager.setSettings(llmModel, backendScript, workingFolder);
    onClose();
  };

  return (
    <div style={styles.overlay}>
      <div style={styles.window}>
        <h2>Settings</h2>
        <div>
          <label>
            LLM model:
            <input 
              type="text" 
              value={llmModel} 
              onChange={(e) => setLlmModel(e.target.value)} 
            />
          </label>
        </div>
        <div>
          <label>
            Backend script:
            <input 
              type="text" 
              value={backendScript} 
              onChange={(e) => setBackendScript(e.target.value)} 
            />
          </label>
        </div>
        <div>
          <label>
            Working folder:
            <input 
              type="text" 
              value={workingFolder} 
              onChange={(e) => setWorkingFolder(e.target.value)} 
            />
          </label>
        </div>
        <button onClick={handleSave}>Save</button>
        <button onClick={onClose}>Cancel</button>
      </div>
    </div>
  );
}

const styles = {
  overlay: {
    position: 'fixed',
    top: 0,
    left: 0,
    width: '100%',
    height: '100%',
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    zIndex: 1000,
  },
  window: {
    backgroundColor: 'white',
    padding: '20px',
    borderRadius: '5px',
    boxShadow: '0 0 10px rgba(0, 0, 0, 0.3)',
  },
};

export default ConfigWindow;

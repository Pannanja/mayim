// App.js

import React from 'react';
import { ReactFlowProvider } from 'reactflow';
import Canvas from './Canvas';

function GraphApp() {
  return (
    <ReactFlowProvider>
      <Canvas />
    </ReactFlowProvider>
  );
}

export default GraphApp;

// Node.js

import { memo, useCallback, useState, useEffect } from 'react';
import NodeLayout from './NodeLayout';
import { useGraphManager } from './GraphManagerContext';

// Helper functions to remove references
export const removePrevs = (nodes, nodeId) => {
  const nodeToRemovePrevs = nodes.find(node => node.id === nodeId);
  if (!nodeToRemovePrevs) return nodes;

  nodeToRemovePrevs.prevs.forEach(prevId => {
    const prevNode = nodes.find(node => node.id === prevId);
    if (prevNode) {
      prevNode.data.nexts = prevNode.data.nexts.filter(id => id !== nodeId);
      if (prevNode.data.true_next === nodeId) prevNode.data.true_next = null;
      if (prevNode.data.false_next === nodeId) prevNode.data.false_next = null;
    }
  });

  nodeToRemovePrevs.prevs = [];
  return nodes;
};

export const removeTrueFalse = (nodes, nodeId) => {
  const nodeToRemoveTrueFalse = nodes.find(node => node.id === nodeId);
  if (!nodeToRemoveTrueFalse) return nodes;

  const trueNextId = nodeToRemoveTrueFalse.data.true_next;
  if (trueNextId) {
    const trueNextNode = nodes.find(node => node.id === trueNextId);
    if (trueNextNode) {
      trueNextNode.prevs = trueNextNode.prevs.filter(id => id !== nodeId);
    }
  }

  const falseNextId = nodeToRemoveTrueFalse.data.false_next;
  if (falseNextId) {
    const falseNextNode = nodes.find(node => node.id === falseNextId);
    if (falseNextNode) {
      falseNextNode.prevs = falseNextNode.prevs.filter(id => id !== nodeId);
    }
  }

  nodeToRemoveTrueFalse.data.true_next = null;
  nodeToRemoveTrueFalse.data.false_next = null;
  return nodes;
};

export const removeNexts = (nodes, nodeId) => {
  const nodeToRemoveNexts = nodes.find(node => node.id === nodeId);
  if (!nodeToRemoveNexts) return nodes;

  nodeToRemoveNexts.data.nexts.forEach(nextId => {
    const nextNode = nodes.find(node => node.id === nextId);
    if (nextNode) {
      nextNode.prevs = nextNode.prevs.filter(id => id !== nodeId);
    }
  });

  nodeToRemoveNexts.data.nexts = [];
  return nodes;
};

function Node({ data, isConnectable, id, prevs }) {
  const {
    nodes,
    setNodes,
  } = useGraphManager();
  const [nodeData, setNodeData] = useState(data);

  useEffect(() => {
    setNodeData(data);
  }, [data]);

  const updateNodeData = (updateFn) => {
    setNodes((nds) => {
      return nds.map((node) => {
        if (node.id === id) {
          return {
            ...node,
            data: updateFn(node.data),
          };
        }
        return node;
      });
    });
  };

  const onChangeName = useCallback((evt) => {
    updateNodeData((prevData) => ({ ...prevData, name: evt.target.value }));
  }, [id, setNodes]);

  const onChangeDescription = useCallback((evt) => {
    updateNodeData((prevData) => ({ ...prevData, description: evt.target.value }));
  }, [id, setNodes]);

  const onChangeType = useCallback((evt) => {
    updateNodeData((prevData) => ({ ...prevData, type: evt.target.value }));
  }, [id, setNodes]);

  const onChangeTool = useCallback((tool) => {
    updateNodeData((prevData) => ({ ...prevData, tool }));
  }, [id, setNodes]);

  const onResize = useCallback((width, height) => {
    updateNodeData((prevData) => ({ ...prevData, width, height }));
  }, [id, setNodes]);

  return (
    <NodeLayout
      data={nodeData}
      isConnectable={isConnectable}
      onChangeName={onChangeName}
      onChangeDescription={onChangeDescription}
      onChangeType={onChangeType}
      onChangeTool={onChangeTool}
      onResize={onResize}
      prevs={prevs}
    />
  );
}

export const addNode = (nodes, setNodes, nodeIdCounter, setNodeIdCounter, newPosition) => {
  const newNode = {
    id: nodeIdCounter.toString(),
    type: 'textUpdater',
    data: { name: `Node ${nodeIdCounter}`, description: '', type: 'STEP', nexts: [], true_next: null, false_next: null, width: 200, height: 200 },
    position: newPosition,
    prevs: []
  };
  setNodes((nds) => nds.concat(newNode));
  setNodeIdCounter(nodeIdCounter + 1);
};

export const deleteNode = (nodes, setNodes, edges, setEdges, nodeId) => {
  let updatedNodes = [...nodes];
  const nodeToDelete = updatedNodes.find((node) => node.id === nodeId);
  if (!nodeToDelete) return;

  // Use helper functions to clean up references
  updatedNodes = removePrevs(updatedNodes, nodeId);
  updatedNodes = removeTrueFalse(updatedNodes, nodeId);
  updatedNodes = removeNexts(updatedNodes, nodeId);

  // Remove the node itself
  updatedNodes = updatedNodes.filter((node) => node.id !== nodeId);
  setNodes(updatedNodes);

  // Remove edges connected to this node
  setEdges((eds) => eds.filter((edge) => edge.source !== nodeId && edge.target !== nodeId));
};

export default memo(Node);

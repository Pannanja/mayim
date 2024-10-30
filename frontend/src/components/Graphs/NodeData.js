// NodeData.js

class NodeData {
  constructor({
    uniq_id = '',
    pos_x = 0,
    pos_y = 0,
    width = 200,
    height = 200,
    nexts = [],
    type = 'START',
    name = '',
    description = '',
    tool = '',
    true_next = null,
    false_next = null,
  }) {
    this.uniq_id = uniq_id;
    this.pos_x = pos_x;
    this.pos_y = pos_y;
    this.width = width;
    this.height = height;
    this.nexts = nexts;
    this.type = type;
    this.name = name;
    this.description = description;
    this.tool = tool;
    this.true_next = true_next;
    this.false_next = false_next;
  }

  static fromReactFlowNode(node) {
    return new NodeData({
      uniq_id: node.id,
      pos_x: node.position.x,
      pos_y: node.position.y,
      width: node.width || node.data.width || 200,
      height: node.height || node.data.height || 200,
      nexts: node.data.nexts || [],
      type: node.data.type || 'STEP',
      name: node.data.name,
      description: node.data.description || '',
      tool: node.data.tool || '',
      true_next: node.data.true_next || null,
      false_next: node.data.false_next || null,
    });
  }

  static fromDict(data) {
    return new NodeData(data);
  }

  toReactFlowNode() {
    return {
      id: this.uniq_id,
      type: 'textUpdater',
      data: {
        name: this.name,
        description: this.description,
        nexts: this.nexts,
        type: this.type,
        tool: this.tool,
        true_next: this.true_next,
        false_next: this.false_next,
        width: this.width,
        height: this.height,
      },
      position: { x: this.pos_x, y: this.pos_y },
      width: this.width,
      height: this.height,
    };
  }

  toDict() {
    const {
      uniq_id, pos_x, pos_y, width, height,
      nexts, type, name, description,
      tool, true_next, false_next,
    } = this;

    return {
      uniq_id,
      pos_x,
      pos_y,
      width,
      height,
      nexts,
      type,
      name,
      description,
      tool,
      true_next,
      false_next,
    };
  }
}

export default NodeData;

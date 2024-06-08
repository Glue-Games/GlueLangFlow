import type {Node, Edge, EdgeTypes } from "reactflow";
import { MarkerType } from "reactflow";
import { HumanFeedbackEdge } from "./HumanFeedbackEdge";

export function getInitialEdges(nodes: Node[]): Edge[] {
  const edges: Edge[] = []
  const outputNode = nodes[nodes.length - 1]

  for (let i =0; i < nodes.length - 1; ++i) {
    edges.push({
      animated: true,
      id: `${nodes[i].id}->${nodes[i+1].id}`,
      source: nodes[i].id,
      sourceHandle: 'r',
      target: nodes[i+1].id,
      style: {stroke: "black"},
      markerEnd: {
        type: MarkerType.ArrowClosed,
        width: 30,
        height: 30,
        color: 'black',
      },
      targetHandle: 'l'
    })
    if (nodes[i].data.hasTextArea)
    edges.push({
      animated: true,
      source: outputNode.id,
      target: nodes[i].id,
      id: `human-feedback-${i}`,
      sourceHandle: 'b',
      style: {stroke: "black"},
      // label: "Human Feedback",
      markerEnd: {
        type: MarkerType.ArrowClosed,
        width: 40,
        height: 40,
        color: 'black',
      },
      type: 'HumanFeedback',
      targetHandle: 'b'
    })
  }
  return edges;
}

export const edgeTypes = {
  'HumanFeedback': HumanFeedbackEdge,
  // Add your custom edge types here!
} satisfies EdgeTypes;

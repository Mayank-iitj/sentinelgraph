import React, { useEffect } from 'react';
import { ReactFlow, Controls, Background, BackgroundVariant, useNodesState, useEdgesState, useReactFlow, ReactFlowProvider } from '@xyflow/react';
import dagre from 'dagre';
import AttackNode from './AttackNode';

const nodeTypes = { attackNode: AttackNode };

const getLayoutedElements = (nodes: any[], edges: any[], direction = 'LR') => {
  const dagreGraph = new dagre.graphlib.Graph();
  dagreGraph.setDefaultEdgeLabel(() => ({}));
  
  const nodeWidth = 240;
  const nodeHeight = 120;
  
  dagreGraph.setGraph({ rankdir: direction, nodesep: 50, ranksep: 120 });
  
  nodes.forEach((node) => {
    dagreGraph.setNode(node.id, { width: nodeWidth, height: nodeHeight });
  });
  
  edges.forEach((edge) => {
    dagreGraph.setEdge(edge.source, edge.target);
  });
  
  dagre.layout(dagreGraph);
  
  const newNodes = nodes.map((node) => {
    const nodeWithPosition = dagreGraph.node(node.id);
    return {
      ...node,
      position: {
        x: nodeWithPosition.x - nodeWidth / 2,
        y: nodeWithPosition.y - nodeHeight / 2,
      },
    };
  });
  
  return { nodes: newNodes, edges };
};

function LayoutComponent({ initialNodes, initialEdges, running }: any) {
  const { fitView } = useReactFlow();
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);

  useEffect(() => {
    const { nodes: layoutedNodes, edges: layoutedEdges } = getLayoutedElements(initialNodes, initialEdges);
    setNodes(layoutedNodes);
    
    // Apply styling to edges
    const styledEdges = layoutedEdges.map(e => ({
      ...e,
      type: 'smoothstep',
      animated: running || e.animated,
      style: { 
        stroke: (running || e.animated) ? '#ef4444' : '#334155', 
        strokeWidth: 2,
        filter: (running || e.animated) ? 'drop-shadow(0 0 5px rgba(239,68,68,0.5))' : 'none'
      },
      labelBgStyle: { fill: '#0B0F19', stroke: '#1E293B', strokeWidth: 1 },
      labelBgPadding: [8, 4],
      labelBgBorderRadius: 16,
      labelStyle: { fill: '#e2e8f0', fontSize: 10, fontFamily: 'monospace', fontWeight: 600 }
    }));
    
    setEdges(styledEdges);
  }, [initialNodes, initialEdges, running]);

  useEffect(() => {
    if (nodes.length > 0) {
      setTimeout(() => {
        fitView({ padding: 0.2, includeHiddenNodes: false, duration: 800 });
      }, 50);
    }
  }, [nodes, fitView]);

  return (
    <ReactFlow
      nodes={nodes}
      edges={edges}
      onNodesChange={onNodesChange}
      onEdgesChange={onEdgesChange}
      nodeTypes={nodeTypes}
      fitView
      className="bg-[#0B0F19]"
      proOptions={{ hideAttribution: true }}
    >
      <Background color="#1E293B" variant={BackgroundVariant.Dots} gap={16} size={1} />
      <Controls className="bg-slate-900 border border-slate-800 fill-slate-300 shadow-xl rounded-md overflow-hidden" />
    </ReactFlow>
  );
}

export default function AttackPathGraph({ initialNodes, initialEdges, running = false }: { initialNodes: any[], initialEdges: any[], running?: boolean }) {
  return (
    <div className="w-full h-full overflow-hidden relative">
      <ReactFlowProvider>
        <LayoutComponent initialNodes={initialNodes} initialEdges={initialEdges} running={running} />
      </ReactFlowProvider>
    </div>
  );
}

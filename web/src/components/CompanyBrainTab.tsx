import { useState } from 'react';
import { Search, GitCommit, FileText, User, Sparkles, MessageSquare, Loader2 } from 'lucide-react';
import { ReactFlow, Controls, Background, MarkerType } from '@xyflow/react';

export default function CompanyBrainTab() {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState([
    {
      role: 'user',
      content: 'Why is planted_entry_svc_0 exposed to the internet?'
    },
    {
      role: 'assistant',
      content: 'To reduce latency for the new partner integration.',
      sources: ['adr_demo_001']
    }
  ]);

  const handleAsk = async () => {
    if (!query.trim()) return;
    const userMsg = query;
    setQuery('');
    setMessages(prev => [...prev, { role: 'user', content: userMsg }]);
    setLoading(true);
    
    try {
      const res = await fetch('http://localhost:8000/brain/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: userMsg })
      });
      
      const data = await res.json();
      
      if (!res.ok) {
        throw new Error(data.detail || 'Error connecting to brain API');
      }
      
      setMessages(prev => [...prev, { role: 'assistant', content: data.answer, sources: data.sources }]);
    } catch (e: any) {
      setMessages(prev => [...prev, { role: 'assistant', content: e.message || 'Error connecting to brain API.' }]);
    } finally {
      setLoading(false);
    }
  };

  const nodes = [
    { id: 'p', type: 'input', position: { x: 50, y: 100 }, data: { label: 'User 0' }, className: 'bg-[#8b5cf6]/20 border-[#8b5cf6] text-[#8b5cf6] p-3 rounded-full border-2 text-xs font-bold text-center w-20 h-20 flex items-center justify-center shadow-[0_0_15px_rgba(139,92,246,0.3)]' },
    { id: 't', type: 'default', position: { x: 250, y: 100 }, data: { label: 'Team 0' }, className: 'bg-[#10b981]/20 border-[#10b981] text-[#10b981] p-3 rounded-lg border-2 text-xs font-bold text-center shadow-[0_0_10px_rgba(16,185,129,0.2)] w-32' },
    { id: 's', type: 'output', position: { x: 450, y: 100 }, data: { label: 'exposed-entry-0' }, className: 'bg-primary/20 border-primary text-primary p-3 rounded-lg border-2 text-xs font-mono shadow-[0_0_15px_rgba(99,102,241,0.3)] w-40 text-center' },
    { id: 'd', type: 'output', position: { x: 50, y: 250 }, data: { label: 'ADR 001' }, className: 'bg-warning/20 border-warning text-warning p-3 rounded-md border-2 text-xs font-bold text-center shadow-[0_0_10px_rgba(245,158,11,0.2)] w-32' }
  ];

  const edges = [
    { id: 'e1', source: 'p', target: 't', label: 'MEMBER_OF', type: 'smoothstep', labelBgStyle: { fill: '#060609', stroke: '#1f2232', strokeWidth: 1 }, labelBgPadding: [6, 4] as [number, number], labelBgBorderRadius: 8, labelStyle: { fill: '#94a3b8', fontSize: 10 }, style: { stroke: '#4b5563', strokeWidth: 2 }, markerEnd: { type: MarkerType.ArrowClosed, color: '#4b5563' } },
    { id: 'e2', source: 't', target: 's', label: 'OWNS', type: 'smoothstep', labelBgStyle: { fill: '#060609', stroke: '#1f2232', strokeWidth: 1 }, labelBgPadding: [6, 4] as [number, number], labelBgBorderRadius: 8, labelStyle: { fill: '#94a3b8', fontSize: 10 }, style: { stroke: '#4b5563', strokeWidth: 2 }, markerEnd: { type: MarkerType.ArrowClosed, color: '#4b5563' } },
    { id: 'e3', source: 'p', target: 'd', label: 'AUTHORED', type: 'smoothstep', labelBgStyle: { fill: '#060609', stroke: '#1f2232', strokeWidth: 1 }, labelBgPadding: [6, 4] as [number, number], labelBgBorderRadius: 8, labelStyle: { fill: '#94a3b8', fontSize: 10 }, style: { stroke: '#4b5563', strokeWidth: 2 }, markerEnd: { type: MarkerType.ArrowClosed, color: '#4b5563' } }
  ];

  return (
    <div className="grid grid-cols-12 gap-6 h-[calc(100vh-120px)]">
      {/* Left Column */}
      <div className="col-span-5 flex flex-col gap-6 h-full">
        <div className="panel flex-1 flex flex-col overflow-hidden">
          <h2 className="text-xl font-bold mb-4 flex items-center gap-2 text-foreground">
            <Search className="w-5 h-5 text-primary drop-shadow-[0_0_8px_rgba(99,102,241,0.5)]" /> Ask the Brain
          </h2>
          <div className="flex-1 bg-[#060609]/80 border border-border/80 rounded-xl flex flex-col shadow-inner">
            <div className="flex-1 p-5 space-y-6 overflow-y-auto">
              
              {messages.map((msg, i) => (
                <div key={i} className="flex gap-4">
                  {msg.role === 'user' ? (
                    <>
                      <div className="w-10 h-10 rounded-full bg-surface-elevated border border-border flex flex-shrink-0 items-center justify-center text-muted">
                        <User className="w-5 h-5" />
                      </div>
                      <div className="bg-surface-elevated/80 border border-border/50 p-4 rounded-2xl rounded-tl-sm text-sm text-foreground shadow-sm">
                        {msg.content}
                      </div>
                    </>
                  ) : (
                    <>
                      <div className="w-10 h-10 rounded-full bg-primary/20 border border-primary/30 text-primary flex flex-shrink-0 items-center justify-center shadow-[0_0_10px_rgba(99,102,241,0.3)]">
                        <Sparkles className="w-5 h-5" />
                      </div>
                      <div className="bg-primary/10 border border-primary/20 p-5 rounded-2xl rounded-tr-sm text-sm flex-1 shadow-[0_4px_20px_rgba(99,102,241,0.05)]">
                        <p className="text-foreground leading-relaxed whitespace-pre-wrap">{msg.content}</p>
                        {msg.sources && msg.sources.length > 0 && (
                          <div className="mt-4 pt-3 border-t border-primary/20 text-xs flex items-center gap-3">
                            <span className="font-bold text-primary flex items-center gap-1"><FileText className="w-3.5 h-3.5" /> SOURCES:</span>
                            {msg.sources.map((s: string, idx: number) => (
                              <span key={idx} className="bg-primary/20 text-primary px-2.5 py-1 rounded-md cursor-pointer hover:bg-primary/30 transition-colors border border-primary/30">{s}</span>
                            ))}
                          </div>
                        )}
                      </div>
                    </>
                  )}
                </div>
              ))}

              {loading && (
                <div className="flex gap-4">
                  <div className="w-10 h-10 rounded-full bg-primary/20 border border-primary/30 text-primary flex flex-shrink-0 items-center justify-center shadow-[0_0_10px_rgba(99,102,241,0.3)]">
                    <Loader2 className="w-5 h-5 animate-spin" />
                  </div>
                  <div className="bg-primary/10 border border-primary/20 p-5 rounded-2xl rounded-tr-sm text-sm flex-1 flex items-center">
                    <span className="text-primary animate-pulse font-mono text-xs">Querying FalkorDB and OpenRouter...</span>
                  </div>
                </div>
              )}

            </div>
            <div className="p-4 border-t border-border/80 bg-surface/50 rounded-b-xl">
              <div className="flex gap-3">
                <div className="relative flex-1">
                  <MessageSquare className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-muted" />
                  <input 
                    type="text" 
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    onKeyDown={(e) => e.key === 'Enter' && handleAsk()}
                    placeholder="Ask about architecture, decisions, owners..." 
                    className="w-full bg-[#060609] border border-border rounded-lg pl-10 pr-4 py-2.5 text-sm focus:outline-none focus:border-primary/50 focus:ring-1 focus:ring-primary/50 transition-all text-foreground" 
                  />
                </div>
                <button onClick={handleAsk} disabled={loading} className="btn btn-primary text-sm px-6 disabled:opacity-50">Ask</button>
              </div>
            </div>
          </div>
        </div>
        
        <div className="panel h-64 flex flex-col">
          <h2 className="text-lg font-bold mb-4 flex items-center gap-2 text-foreground">
            <GitCommit className="w-5 h-5 text-warning drop-shadow-[0_0_8px_rgba(245,158,11,0.5)]" /> Decision Lineage
          </h2>
          <div className="bg-[#060609]/80 border border-border/80 rounded-xl p-5 flex-1 overflow-y-auto shadow-inner relative">
            <div className="absolute left-8 top-5 bottom-5 w-px bg-border"></div>
            
            <div className="relative pl-10">
              <div className="absolute left-0 top-1.5 w-4 h-4 rounded-full bg-warning border-4 border-[#060609] shadow-[0_0_10px_rgba(245,158,11,0.4)]" />
              <div className="font-bold text-foreground">ADR 001: Bypass WAF</div>
              <div className="text-muted text-xs mb-3 flex items-center gap-2">
                <span>2026-09-01</span> • <span>Author: User 0</span>
              </div>
              <div className="bg-surface-elevated/80 p-3 rounded-lg border border-border/50 text-sm text-foreground/90 italic shadow-sm">
                "We decided to expose planted_entry_svc_0 directly to the internet and bypass the WAF to reduce latency..."
              </div>
            </div>
          </div>
        </div>
      </div>
      
      {/* Right Column */}
      <div className="col-span-7 panel flex flex-col overflow-hidden h-full">
        <h2 className="text-xl font-bold mb-4 flex items-center gap-2 text-foreground">
          <FileText className="w-5 h-5 text-success drop-shadow-[0_0_8px_rgba(16,185,129,0.5)]" /> Ownership & Knowledge Graph
        </h2>
        <div className="flex-1 w-full bg-[#060609]/80 border border-border/80 rounded-xl overflow-hidden shadow-inner relative">
           <ReactFlow 
              nodes={nodes} 
              edges={edges} 
              fitView 
              className="dark"
              proOptions={{ hideAttribution: true }}
            >
              <Background color="#1f2232" gap={20} size={1} />
              <Controls className="bg-surface border-border fill-muted" />
            </ReactFlow>
        </div>
      </div>
    </div>
  );
}

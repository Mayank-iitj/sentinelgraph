import { History, FastForward, Users, CheckCircle, CheckCircle2 } from 'lucide-react';
import { motion } from 'framer-motion';
import { ReactFlow, Controls, Background, MarkerType } from '@xyflow/react';

export default function AgentsMemoryTab() {
  const nodes = [
    { id: 'db', position: { x: 300, y: 150 }, data: { label: 'FalkorDB\n(Shared Memory)' }, className: 'bg-[#060609] border-primary text-primary p-4 rounded-xl border-2 text-sm font-bold text-center shadow-[0_0_20px_rgba(99,102,241,0.5)] w-32' },
    { id: 'a1', position: { x: 50, y: 50 }, data: { label: 'Triage Agent' }, className: 'bg-danger/20 border-danger text-danger p-3 rounded-lg border-2 text-xs font-bold text-center shadow-[0_0_10px_rgba(244,63,94,0.3)]' },
    { id: 'a2', position: { x: 50, y: 250 }, data: { label: 'Investigator Agent' }, className: 'bg-warning/20 border-warning text-warning p-3 rounded-lg border-2 text-xs font-bold text-center shadow-[0_0_10px_rgba(245,158,11,0.3)]' },
    { id: 'a3', position: { x: 550, y: 50 }, data: { label: 'Remediation Agent' }, className: 'bg-success/20 border-success text-success p-3 rounded-lg border-2 text-xs font-bold text-center shadow-[0_0_10px_rgba(16,185,129,0.3)]' },
    { id: 'a4', position: { x: 550, y: 250 }, data: { label: 'Memory Agent' }, className: 'bg-[#8b5cf6]/20 border-[#8b5cf6] text-[#8b5cf6] p-3 rounded-lg border-2 text-xs font-bold text-center shadow-[0_0_10px_rgba(139,92,246,0.3)]' }
  ];

  const edges = [
    { id: 'e1', source: 'a1', target: 'db', label: 'WRITES VERDICT', animated: true, style: { stroke: '#f43f5e', strokeWidth: 2 }, markerEnd: { type: MarkerType.ArrowClosed, color: '#f43f5e' } },
    { id: 'e2', source: 'db', target: 'a2', label: 'TRIGGERS', animated: true, style: { stroke: '#f59e0b', strokeWidth: 2 }, markerEnd: { type: MarkerType.ArrowClosed, color: '#f59e0b' } },
    { id: 'e3', source: 'a2', target: 'db', label: 'ADDS OWNER', animated: true, style: { stroke: '#f59e0b', strokeWidth: 2 }, markerEnd: { type: MarkerType.ArrowClosed, color: '#f59e0b' } },
    { id: 'e4', source: 'db', target: 'a3', label: 'TRIGGERS', animated: true, style: { stroke: '#10b981', strokeWidth: 2 }, markerEnd: { type: MarkerType.ArrowClosed, color: '#10b981' } },
    { id: 'e5', source: 'a4', target: 'db', label: 'CONSOLIDATES', animated: true, style: { stroke: '#8b5cf6', strokeWidth: 2 }, markerEnd: { type: MarkerType.ArrowClosed, color: '#8b5cf6' } }
  ];

  return (
    <div className="grid grid-cols-12 gap-6 h-[calc(100vh-120px)]">
      <div className="col-span-5 flex flex-col gap-6 h-full">
        <div className="panel flex-1 flex flex-col">
          <h2 className="text-xl font-bold mb-6 flex items-center gap-2 text-foreground">
            <Users className="w-5 h-5 text-primary drop-shadow-[0_0_8px_rgba(99,102,241,0.5)]" /> Handoff Timeline
          </h2>
          <div className="relative border-l-2 border-border/50 ml-6 pl-8 pb-4 space-y-8 mt-2 flex-1 overflow-y-auto pr-4">
            <motion.div initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.1 }} className="relative">
              <div className="absolute -left-[43px] bg-[#060609] p-1.5 rounded-full border-2 border-primary shadow-[0_0_10px_rgba(99,102,241,0.4)]">
                <div className="w-2.5 h-2.5 bg-primary rounded-full"></div>
              </div>
              <div className="text-xs text-primary font-bold tracking-wider mb-1">10:01 AM</div>
              <div className="font-bold text-lg text-foreground flex items-center gap-2">TriageAgent <span className="bg-primary/20 text-primary px-2 py-0.5 rounded text-[10px] uppercase border border-primary/30">Active</span></div>
              <div className="text-sm mt-3 bg-surface-elevated/80 p-4 rounded-xl border border-border shadow-md">
                Claimed <code className="text-danger bg-danger/10 px-1 rounded">finding_true_0</code>. Verdict: <strong className="text-danger">ACT</strong>.
              </div>
            </motion.div>
            
            <motion.div initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.3 }} className="relative">
              <div className="absolute -left-[43px] bg-[#060609] p-1.5 rounded-full border-2 border-warning shadow-[0_0_10px_rgba(245,158,11,0.4)]">
                <div className="w-2.5 h-2.5 bg-warning rounded-full"></div>
              </div>
              <div className="text-xs text-warning font-bold tracking-wider mb-1">10:02 AM</div>
              <div className="font-bold text-lg text-foreground flex items-center gap-2">InvestigatorAgent <span className="bg-warning/20 text-warning px-2 py-0.5 rounded text-[10px] uppercase border border-warning/30">Active</span></div>
              <div className="text-sm mt-3 bg-surface-elevated/80 p-4 rounded-xl border border-border shadow-md">
                Expanded context. Owner found: <strong className="text-warning">User 0</strong>.
              </div>
            </motion.div>
            
            <motion.div initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.5 }} className="relative">
              <div className="absolute -left-[43px] bg-[#060609] p-1.5 rounded-full border-2 border-success shadow-[0_0_10px_rgba(16,185,129,0.4)]">
                <div className="w-2.5 h-2.5 bg-success rounded-full"></div>
              </div>
              <div className="text-xs text-success font-bold tracking-wider mb-1">10:03 AM</div>
              <div className="font-bold text-lg text-foreground flex items-center gap-2">RemediationAgent <span className="bg-success/20 text-success px-2 py-0.5 rounded text-[10px] uppercase border border-success/30">Complete</span></div>
              <div className="text-sm mt-3 bg-surface-elevated/80 p-4 rounded-xl border border-border shadow-md flex items-start gap-2">
                <CheckCircle2 className="w-4 h-4 text-success mt-0.5" />
                <span>Drafted containment playbook. Assigned ticket to User 0.</span>
              </div>
            </motion.div>
          </div>
        </div>
      </div>
      
      <div className="col-span-7 flex flex-col gap-6 h-full">
        {/* NEW: Interactive ReactFlow for Multi-Agent Architecture */}
        <div className="panel h-[50%] flex flex-col overflow-hidden relative">
          <h2 className="text-xl font-bold mb-4 flex items-center gap-2 text-foreground z-10">
            <CheckCircle className="w-5 h-5 text-[#8b5cf6] drop-shadow-[0_0_8px_rgba(139,92,246,0.5)]" /> Autonomous Swarm Architecture
          </h2>
          <div className="absolute inset-0 top-14 bg-[#060609]/50 border-t border-border/50">
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

        <div className="flex flex-col gap-4 flex-1 h-[50%]">
          <div className="panel flex-1 flex flex-col">
            <h2 className="text-sm font-bold flex items-center gap-2 text-muted">
              <History className="w-4 h-4 text-warning" /> Bi-temporal Memory Inspector
            </h2>
            <div className="space-y-4 mt-4 flex-1 overflow-y-auto">
              <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }} className="p-4 bg-surface-elevated/80 border border-success/30 rounded-xl text-sm shadow-[0_4px_20px_rgba(16,185,129,0.05)] relative overflow-hidden">
                <div className="flex justify-between items-center text-xs mb-2">
                  <span className="text-muted font-mono bg-[#060609] px-2 py-1 rounded border border-border">ID: 83f9a2c</span>
                  <span className="text-success font-bold tracking-widest uppercase flex items-center gap-1"><CheckCircle className="w-3.5 h-3.5" /> ACTIVE</span>
                </div>
                <div className="font-medium text-foreground text-sm leading-relaxed">Payment gateway uses Kafka.</div>
              </motion.div>
              
              <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.4 }} className="p-4 bg-[#060609]/50 border border-danger/20 rounded-xl text-sm relative overflow-hidden group">
                <div className="flex justify-between items-center text-xs mb-2 opacity-60">
                  <span className="text-muted font-mono bg-[#060609] px-2 py-1 rounded border border-border">ID: 12a4b8e</span>
                  <span className="text-danger font-bold tracking-widest uppercase">SUPERSEDED</span>
                </div>
                <div className="font-medium text-foreground/50 text-sm leading-relaxed line-through decoration-danger/30 decoration-2">Payment gateway uses RabbitMQ.</div>
              </motion.div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

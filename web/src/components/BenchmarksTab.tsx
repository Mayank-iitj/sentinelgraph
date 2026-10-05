import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { motion } from 'framer-motion';
import { Brain, Zap, Target } from 'lucide-react';

export default function BenchmarksTab() {
  const data = [
    { name: 'Precision@10', CVSS: 0.20, SentinelGraph: 1.00 },
    { name: 'Recall (Criticals)', CVSS: 0.12, SentinelGraph: 1.00 },
  ];

  return (
    <div className="flex flex-col gap-6 h-full max-w-5xl mx-auto pb-10">
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="panel border-primary/30 shadow-[0_8px_30px_rgba(99,102,241,0.1)] relative overflow-hidden">
        <div className="absolute top-0 right-0 w-96 h-96 bg-primary/10 rounded-full blur-3xl pointer-events-none -z-10" />
        <h2 className="text-2xl font-black mb-8 flex items-center gap-3 text-foreground tracking-tight">
          <Target className="w-7 h-7 text-primary drop-shadow-[0_0_10px_rgba(99,102,241,0.5)]" /> 
          Triage Benchmark (vs CVSS-only Baseline)
        </h2>
        
        <div className="h-80 w-full mb-8">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={data} margin={{ top: 20, right: 30, left: 0, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#1f2232" vertical={false} />
              <XAxis dataKey="name" stroke="#94a3b8" tick={{ fill: '#94a3b8', fontSize: 14, fontWeight: 500 }} axisLine={{ stroke: '#1f2232' }} tickLine={false} dy={10} />
              <YAxis stroke="#94a3b8" tick={{ fill: '#94a3b8' }} axisLine={{ stroke: '#1f2232' }} tickLine={false} dx={-10} />
              <Tooltip 
                cursor={{ fill: '#161821' }}
                contentStyle={{ backgroundColor: '#0f1016', border: '1px solid #1f2232', borderRadius: '12px', color: '#fff', boxShadow: '0 10px 25px rgba(0,0,0,0.5)' }} 
                itemStyle={{ fontWeight: 'bold' }}
              />
              <Legend wrapperStyle={{ paddingTop: '20px' }} />
              <Bar dataKey="CVSS" fill="#f43f5e" radius={[6, 6, 0, 0]} maxBarSize={80} />
              <Bar dataKey="SentinelGraph" fill="#10b981" radius={[6, 6, 0, 0]} maxBarSize={80} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="grid grid-cols-2 gap-6">
          <div className="bg-[#060609]/80 border border-border rounded-2xl p-6 text-center shadow-inner relative overflow-hidden">
            <div className="absolute top-0 left-0 w-full h-1 bg-danger" />
            <div className="text-sm font-semibold text-muted uppercase tracking-wider mb-2">Decoys Escalated (Top 10)</div>
            <div className="text-5xl font-black text-danger my-3 drop-shadow-[0_0_10px_rgba(244,63,94,0.3)]">8</div>
            <div className="text-sm font-medium text-muted/80 bg-surface px-3 py-1 rounded-full inline-block">CVSS-Only Baseline</div>
          </div>
          <div className="bg-[#060609]/80 border border-border rounded-2xl p-6 text-center shadow-inner relative overflow-hidden">
            <div className="absolute top-0 left-0 w-full h-1 bg-success" />
            <div className="text-sm font-semibold text-muted uppercase tracking-wider mb-2">Decoys Escalated (Top 10)</div>
            <div className="text-5xl font-black text-success my-3 drop-shadow-[0_0_10px_rgba(16,185,129,0.3)]">0</div>
            <div className="text-sm font-medium text-primary/80 bg-primary/10 border border-primary/20 px-3 py-1 rounded-full inline-block">SentinelGraph</div>
          </div>
        </div>
      </motion.div>
      
      <div className="grid grid-cols-2 gap-6">
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }} className="panel">
          <h2 className="text-lg font-bold mb-6 flex items-center gap-2 text-foreground border-b border-border/50 pb-4">
            <Zap className="w-5 h-5 text-warning" /> Memory & Concurrency
          </h2>
          <ul className="space-y-4">
            <li className="flex justify-between items-center p-3 bg-surface-elevated/50 rounded-lg hover:bg-surface-elevated transition-colors border border-transparent hover:border-border cursor-default">
              <span className="text-muted font-medium">Recall Accuracy</span>
              <span className="font-bold text-white bg-[#060609] px-3 py-1 rounded shadow-inner">95%</span>
            </li>
            <li className="flex justify-between items-center p-3 bg-surface-elevated/50 rounded-lg hover:bg-surface-elevated transition-colors border border-transparent hover:border-border cursor-default">
              <span className="text-muted font-medium">Contradiction Handling</span>
              <span className="font-bold text-white bg-[#060609] px-3 py-1 rounded shadow-inner">100%</span>
            </li>
            <li className="flex justify-between items-center p-3 bg-success/10 rounded-lg border border-success/20 shadow-[0_0_15px_rgba(16,185,129,0.05)] cursor-default">
              <span className="text-success font-semibold">Playbook Reuse Savings</span>
              <span className="font-black text-success">80% fewer steps</span>
            </li>
            <li className="flex justify-between items-center p-3 bg-surface-elevated/50 rounded-lg hover:bg-surface-elevated transition-colors border border-transparent hover:border-border cursor-default">
              <span className="text-muted font-medium">Concurrency Stats</span>
              <span className="font-bold text-white bg-[#060609] px-3 py-1 rounded shadow-inner text-xs">50 req/s, 0 lost</span>
            </li>
          </ul>
        </motion.div>
        
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.4 }} className="panel">
          <h2 className="text-lg font-bold mb-6 flex items-center gap-2 text-foreground border-b border-border/50 pb-4">
            <Brain className="w-5 h-5 text-primary" /> Company Brain Extractor
          </h2>
          <ul className="space-y-4">
            <li className="flex justify-between items-center p-3 bg-surface-elevated/50 rounded-lg hover:bg-surface-elevated transition-colors border border-transparent hover:border-border cursor-default">
              <span className="text-muted font-medium">Answer Accuracy</span>
              <span className="font-bold text-white bg-[#060609] px-3 py-1 rounded shadow-inner">92%</span>
            </li>
            <li className="flex justify-between items-center p-3 bg-primary/10 rounded-lg border border-primary/20 shadow-[0_0_15px_rgba(99,102,241,0.05)] cursor-default">
              <span className="text-primary font-semibold">Citation Precision</span>
              <span className="font-black text-primary">95%</span>
            </li>
            <li className="flex justify-between items-center p-3 bg-surface-elevated/50 rounded-lg hover:bg-surface-elevated transition-colors border border-transparent hover:border-border cursor-default">
              <span className="text-muted font-medium">Stale Knowledge Detection</span>
              <span className="font-bold text-white bg-[#060609] px-3 py-1 rounded shadow-inner">100%</span>
            </li>
          </ul>
        </motion.div>
      </div>
    </div>
  );
}

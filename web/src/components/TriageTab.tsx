import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { AlertTriangle, Play, ShieldAlert, Cpu, CheckCircle2, ChevronRight, Activity, Terminal } from 'lucide-react';
import AttackPathGraph from './AttackPathGraph';

export default function TriageTab() {
  const [running, setRunning] = useState(false);
  const [flatMode, setFlatMode] = useState(false);
  const [activeStep, setActiveStep] = useState(-1);
  
  const findings = [
    { id: 'finding_true_0', asset: 'exposed-entry-0', cve: 'CVE-2026-PLANT0', score: 9.5, cvss: 4.5, rank: 1, verdict: 'act', reason: '4 hops to crown jewel' },
    { id: 'finding_decoy_0', asset: 'isolated-dev-0', cve: 'CVE-2026-DECOY0', score: 1.0, cvss: 9.9, rank: 2, verdict: 'ignore', reason: 'Isolated asset, no paths' },
  ];

  const nodes = [
    { id: '1', type: 'attackNode', data: { label: 'exposed-entry-0', subtext: 'CVE-2026-PLANT0', status: 'CRITICAL', tier: 'entry' } },
    { id: '2', type: 'attackNode', data: { label: 'internal-hop-0', subtext: 'Pivot Host', status: 'WARN', tier: 'hop' } },
    { id: '3', type: 'attackNode', data: { label: 'crown-jewel', subtext: 'Production DB', status: 'TARGET', tier: 'target' } }
  ];

  const edges = [
    { id: 'e1-2', source: '1', target: '2', label: 'CONNECTS_TO' },
    { id: 'e2-3', source: '2', target: '3', label: 'HAS_ACCESS' }
  ];

  const handleRun = () => {
    setRunning(true);
    setActiveStep(0);
    
    // Simulate steps
    setTimeout(() => setActiveStep(1), 800);
    setTimeout(() => setActiveStep(2), 1600);
    setTimeout(() => setActiveStep(3), 2400);
    setTimeout(() => setRunning(false), 3200);
  };

  const steps = [
    { text: "TriageAgent checking finding_true_0...", icon: <Activity className="w-4 h-4 text-muted" /> },
    { text: "> CALL tool blast_radius(asset_id='exposed-entry-0')", icon: <Terminal className="w-4 h-4 text-primary" />, color: "text-primary" },
    { text: "Evidence: 4 hops to crown-jewel.", icon: <ShieldAlert className="w-4 h-4 text-warning" />, color: "text-warning" },
    { text: "Verdict: ACT.", icon: <CheckCircle2 className="w-4 h-4 text-danger" />, color: "text-danger font-bold" }
  ];

  return (
    <div className="grid grid-cols-12 gap-6 h-[calc(100vh-120px)]">
      {/* Left Column: Queue */}
      <div className="col-span-4 flex flex-col gap-4 h-full">
        <div className="panel flex flex-col h-full overflow-hidden">
          <div className="flex justify-between items-center mb-6 pb-4 border-b border-border/50">
            <h2 className="text-xl font-bold flex items-center gap-2 text-foreground">
              <AlertTriangle className="w-5 h-5 text-warning drop-shadow-[0_0_8px_rgba(245,158,11,0.5)]" /> 
              Findings Queue
            </h2>
            <button onClick={handleRun} disabled={running} className="btn btn-primary text-sm shadow-[0_0_15px_rgba(99,102,241,0.4)]">
              {running ? <Activity className="w-4 h-4 animate-spin" /> : <Play className="w-4 h-4" />}
              {running ? 'Triaging...' : 'Run Triage'}
            </button>
          </div>
          
          <label onClick={() => setFlatMode(!flatMode)} className="text-xs text-muted flex items-center gap-2 cursor-pointer mb-4 hover:text-foreground transition-colors w-max">
            <div className={`w-10 h-5 rounded-full p-1 transition-colors ${flatMode ? 'bg-primary' : 'bg-surface-elevated'}`}>
              <div className={`w-3 h-3 rounded-full bg-white transition-transform ${flatMode ? 'translate-x-5' : ''}`} />
            </div>
            Counterfactual Mode (CVSS Only)
          </label>

          <div className="flex flex-col gap-3 overflow-y-auto pr-2 pb-4">
            {findings.map((f, i) => (
              <motion.div 
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.1 }}
                key={f.id} 
                className={`bg-surface-elevated/50 border backdrop-blur-sm p-4 rounded-xl cursor-pointer transition-all duration-300 hover:-translate-y-1 ${f.verdict === 'act' ? 'border-danger/30 hover:border-danger hover:shadow-[0_4px_20px_rgba(244,63,94,0.15)]' : 'border-border hover:border-primary/50'}`}
              >
                <div className="flex justify-between items-start mb-3">
                  <div className="font-bold text-base text-foreground tracking-tight">{f.cve}</div>
                  <span className={`text-xs px-2.5 py-1 rounded-md font-bold tracking-wider ${f.verdict === 'act' ? 'bg-danger/10 text-danger border border-danger/20 shadow-[0_0_10px_rgba(244,63,94,0.2)]' : 'bg-surface border border-border text-muted'}`}>
                    {f.verdict.toUpperCase()}
                  </span>
                </div>
                <div className="text-sm text-muted mb-4 flex items-center gap-2">
                  <span className="bg-surface px-2 py-1 rounded text-xs border border-border font-mono">{f.asset}</span>
                </div>
                
                <div className="space-y-1.5">
                  <div className="flex justify-between text-xs">
                    <span className="text-muted font-medium">Risk Score</span>
                    <span className="text-primary font-bold">{f.score.toFixed(1)}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <div className="flex-1 bg-surface h-2 rounded-full overflow-hidden border border-border/50">
                      <motion.div 
                        initial={{ width: 0 }}
                        animate={{ width: `${(f.score / 10) * 100}%` }}
                        transition={{ duration: 1, delay: 0.5 }}
                        className={`h-full ${f.score > 8 ? 'bg-danger' : f.score > 5 ? 'bg-warning' : 'bg-primary'} shadow-[0_0_10px_currentColor]`}
                      />
                    </div>
                  </div>
                </div>
                <div className="text-xs text-muted/80 mt-4 pt-3 border-t border-border/50 flex items-start gap-1.5">
                  <ChevronRight className="w-3.5 h-3.5 mt-0.5 text-primary" />
                  <span className="leading-relaxed">{f.reason}</span>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </div>
      
      {/* Right Column: Graph and Terminal */}
      <div className="col-span-8 flex flex-col gap-4 h-full overflow-hidden">
        <div className="panel flex-1 flex flex-col p-0 overflow-hidden relative border-border/50 h-full">
          <div className="absolute top-0 left-0 right-0 z-10 p-5 bg-gradient-to-b from-surface/90 to-transparent pointer-events-none">
            <h2 className="text-xl font-bold flex items-center gap-2 drop-shadow-md">
              <ShieldAlert className="w-5 h-5 text-primary drop-shadow-[0_0_8px_rgba(99,102,241,0.5)]" /> 
              Attack Path Topology
            </h2>
          </div>
          <div className="flex-1 w-full h-full relative overflow-hidden rounded-b-xl">
            <AttackPathGraph initialNodes={nodes} initialEdges={edges} running={running} />
          </div>
        </div>
        
        <div className="panel h-56 flex flex-col bg-[#0f1016]/95 border-border/50">
          <h2 className="text-sm font-bold tracking-wider uppercase mb-3 flex items-center gap-2 text-muted">
            <Cpu className="w-4 h-4 text-primary" /> Sentinel Runtime Trace
          </h2>
          <div className="flex-1 bg-[#060609] border border-border/80 rounded-lg p-4 font-mono text-sm overflow-y-auto shadow-inner relative">
            <div className="absolute top-0 left-0 w-1 h-full bg-primary/20" />
            <AnimatePresence>
              {activeStep >= 0 ? (
                <div className="space-y-3">
                  {steps.map((step, idx) => (
                    idx <= activeStep && (
                      <motion.div 
                        initial={{ opacity: 0, x: -10 }}
                        animate={{ opacity: 1, x: 0 }}
                        key={idx}
                        className={`flex items-start gap-3 ${step.color || 'text-muted'}`}
                      >
                        <span className="text-muted/50 mt-0.5">[{`00:00:0${idx + 1}`}]</span>
                        <div className="mt-0.5">{step.icon}</div>
                        <span>{step.text}</span>
                      </motion.div>
                    )
                  ))}
                  {running && (
                    <motion.div 
                      initial={{ opacity: 0 }} animate={{ opacity: 1 }}
                      className="flex items-center gap-2 text-muted/50 mt-2 ml-14"
                    >
                      <div className="w-1.5 h-1.5 bg-primary rounded-full animate-ping" />
                      processing...
                    </motion.div>
                  )}
                </div>
              ) : (
                <div className="text-muted/40 h-full flex items-center justify-center italic">
                  System idle. Click 'Run Triage' to initiate Graph Agent analysis.
                </div>
              )}
            </AnimatePresence>
          </div>
        </div>
      </div>
    </div>
  );
}

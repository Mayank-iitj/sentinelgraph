import React from 'react';
import { Shield, Brain, Activity, Database, Server, AlertTriangle, Users } from 'lucide-react';
import { motion } from 'framer-motion';

export default function DashboardTab() {
  const stats = [
    { label: 'Active Agents', value: '4', icon: <Brain className="w-5 h-5 text-primary" />, color: 'border-primary/50 bg-primary/5 text-primary' },
    { label: 'Graph Nodes', value: '12,408', icon: <Database className="w-5 h-5 text-success" />, color: 'border-success/50 bg-success/5 text-success' },
    { label: 'Pending Alerts', value: '2', icon: <AlertTriangle className="w-5 h-5 text-danger" />, color: 'border-danger/50 bg-danger/5 text-danger' },
    { label: 'Resolved (24h)', value: '156', icon: <Shield className="w-5 h-5 text-warning" />, color: 'border-warning/50 bg-warning/5 text-warning' },
  ];

  return (
    <div className="h-full flex flex-col gap-6 max-w-7xl mx-auto w-full">
      <div className="grid grid-cols-4 gap-6">
        {stats.map((stat, i) => (
          <motion.div 
            initial={{ opacity: 0, y: 20 }} 
            animate={{ opacity: 1, y: 0 }} 
            transition={{ delay: i * 0.1 }}
            key={stat.label} 
            className={`panel border ${stat.color} flex items-center justify-between p-6`}
          >
            <div>
              <div className="text-sm font-semibold text-muted mb-1">{stat.label}</div>
              <div className="text-4xl font-black text-foreground drop-shadow-md">{stat.value}</div>
            </div>
            <div className="w-14 h-14 rounded-full bg-[#060609] shadow-inner border border-border flex items-center justify-center">
              {stat.icon}
            </div>
          </motion.div>
        ))}
      </div>

      <div className="grid grid-cols-2 gap-6 flex-1">
        <motion.div initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.4 }} className="panel flex flex-col relative overflow-hidden">
          <div className="absolute top-0 right-0 w-64 h-64 bg-primary/10 rounded-full blur-3xl pointer-events-none" />
          <h2 className="text-xl font-bold mb-6 flex items-center gap-2 text-foreground">
            <Server className="w-5 h-5 text-primary" /> System Overview
          </h2>
          <div className="flex-1 flex flex-col justify-center gap-6 z-10">
            <div>
              <div className="flex justify-between text-sm mb-2 font-medium">
                <span className="text-muted">FalkorDB Graph Engine</span>
                <span className="text-success">Connected</span>
              </div>
              <div className="h-2 w-full bg-[#060609] rounded-full overflow-hidden border border-border">
                <div className="h-full bg-success w-full shadow-[0_0_10px_currentColor]" />
              </div>
            </div>
            <div>
              <div className="flex justify-between text-sm mb-2 font-medium">
                <span className="text-muted">Anthropic Claude 3.5 API</span>
                <span className="text-success">98ms latency</span>
              </div>
              <div className="h-2 w-full bg-[#060609] rounded-full overflow-hidden border border-border">
                <div className="h-full bg-primary w-full shadow-[0_0_10px_currentColor]" />
              </div>
            </div>
            <div>
              <div className="flex justify-between text-sm mb-2 font-medium">
                <span className="text-muted">MCP Tools Server</span>
                <span className="text-success">Active (Port 8001)</span>
              </div>
              <div className="h-2 w-full bg-[#060609] rounded-full overflow-hidden border border-border">
                <div className="h-full bg-warning w-full shadow-[0_0_10px_currentColor]" />
              </div>
            </div>
          </div>
        </motion.div>

        <motion.div initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.5 }} className="panel flex flex-col relative overflow-hidden">
          <div className="absolute top-0 right-0 w-64 h-64 bg-danger/10 rounded-full blur-3xl pointer-events-none" />
          <h2 className="text-xl font-bold mb-6 flex items-center gap-2 text-foreground">
            <Activity className="w-5 h-5 text-danger" /> Latest Threat Intelligence
          </h2>
          <div className="flex-1 flex flex-col gap-4 z-10">
            <div className="bg-[#060609]/80 border border-border rounded-xl p-4 shadow-inner flex items-start gap-4">
              <div className="w-10 h-10 rounded-full bg-danger/20 border border-danger/50 text-danger flex items-center justify-center shrink-0 shadow-[0_0_10px_rgba(244,63,94,0.3)]">
                <AlertTriangle className="w-5 h-5" />
              </div>
              <div>
                <div className="font-bold text-foreground mb-1 text-lg">CVE-2026-PLANT0 detected</div>
                <div className="text-sm text-muted">A critical vulnerability was found on exposed-entry-0 with a direct path to the crown jewel. Triage Agent has escalated this finding.</div>
                <div className="text-xs text-danger font-mono mt-2 bg-danger/10 px-2 py-1 rounded inline-block border border-danger/20">CVSS 4.5 • Risk Score 9.5</div>
              </div>
            </div>
            <div className="bg-[#060609]/80 border border-border rounded-xl p-4 shadow-inner flex items-start gap-4 opacity-70">
              <div className="w-10 h-10 rounded-full bg-success/20 border border-success/50 text-success flex items-center justify-center shrink-0">
                <Shield className="w-5 h-5" />
              </div>
              <div>
                <div className="font-bold text-foreground mb-1 text-lg">Decoy neutralized</div>
                <div className="text-sm text-muted">CVE-2026-DECOY0 was evaluated and ignored due to being fully isolated from production assets.</div>
              </div>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  );
}

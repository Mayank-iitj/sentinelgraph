import { Handle, Position } from '@xyflow/react';
import { Activity } from 'lucide-react';

export default function AttackNode({ data }: { data: any }) {
  const { label, subtext, status, tier } = data;

  const styles = {
    entry: 'border-danger/60 bg-danger/10 shadow-[0_0_15px_rgba(244,63,94,0.3)]',
    hop: 'border-warning/60 bg-warning/10 shadow-[0_0_10px_rgba(245,158,11,0.2)]',
    target: 'border-primary/60 bg-primary/10 shadow-[0_0_20px_rgba(99,102,241,0.4)]'
  };

  const badgeStyles = {
    CRITICAL: 'bg-danger text-white',
    WARN: 'bg-warning text-white',
    TARGET: 'bg-primary text-white',
    COMPROMISED: 'bg-danger text-white'
  };

  const style = styles[tier as keyof typeof styles] || styles.hop;
  const badgeStyle = badgeStyles[status as keyof typeof badgeStyles] || 'bg-surface-elevated text-muted';

  return (
    <div className={`p-4 rounded-xl border-2 backdrop-blur-md min-w-[220px] ${style}`}>
      <Handle type="target" position={Position.Left} className="w-1.5 h-6 rounded-sm bg-slate-400 border-none -ml-1 opacity-70" />
      
      <div className="flex justify-between items-start mb-3">
        <span className={`text-[10px] px-2 py-0.5 rounded shadow-sm font-bold tracking-wider ${badgeStyle}`}>
          {status}
        </span>
        <Activity className="w-4 h-4 text-foreground/50" />
      </div>
      
      <div className="font-mono text-sm text-foreground font-bold truncate">
        {label}
      </div>
      <div className="text-xs text-muted mt-1 truncate">
        {subtext}
      </div>

      <Handle type="source" position={Position.Right} className="w-1.5 h-6 rounded-sm bg-slate-400 border-none -mr-1 opacity-70" />
    </div>
  );
}

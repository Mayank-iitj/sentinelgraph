import { useState, useEffect } from 'react';
import LandingPage from './components/LandingPage';
import DashboardTab from './components/DashboardTab';
import TriageTab from './components/TriageTab';
import AgentsMemoryTab from './components/AgentsMemoryTab';
import CompanyBrainTab from './components/CompanyBrainTab';
import BenchmarksTab from './components/BenchmarksTab';
import { Shield, Brain, Activity, BarChart2, LayoutDashboard } from 'lucide-react';
import PillNav from './components/PillNav';

function App() {
  const [activeTab, setActiveTab] = useState('landing');
  
  useEffect(() => {
    const handleHash = () => {
      const hash = window.location.hash.replace('#', '');
      if (['dashboard', 'triage', 'memory', 'brain', 'bench'].includes(hash)) {
        setActiveTab(hash);
      }
    };
    
    // Set initial tab from hash if present
    handleHash();
    
    window.addEventListener('hashchange', handleHash);
    return () => window.removeEventListener('hashchange', handleHash);
  }, []);

  if (activeTab === 'landing') {
    return <LandingPage onEnter={() => {
      setActiveTab('dashboard');
      window.location.hash = 'dashboard';
    }} />;
  }

  const shieldLogo = `data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="%236366f1" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>`;

  return (
    <div className="min-h-screen flex flex-col bg-background text-foreground overflow-hidden selection:bg-primary/30">
      <header className="glass sticky top-0 z-50 flex items-center justify-between px-8 py-4 border-b border-border/50">
        <div className="flex items-center gap-3 group cursor-pointer" onClick={() => window.location.hash = 'dashboard'}>
          <div className="relative">
            <div className="absolute inset-0 bg-primary blur-md opacity-40 group-hover:opacity-70 transition-opacity duration-500 rounded-full" />
            <Shield className="text-primary w-8 h-8 relative z-10" />
          </div>
          <h1 className="text-xl font-black tracking-tighter text-transparent bg-clip-text bg-gradient-to-r from-white to-white/70">
            Sentinel<span className="text-primary">Graph</span>
          </h1>
        </div>
        
        <PillNav
          logo={shieldLogo}
          logoAlt="Logo"
          items={[
            { label: 'Dashboard', href: '#dashboard', icon: <LayoutDashboard className="w-4 h-4" /> },
            { label: 'Triage', href: '#triage', icon: <Activity className="w-4 h-4" /> },
            { label: 'Memory', href: '#memory', icon: <Brain className="w-4 h-4" /> },
            { label: 'Brain', href: '#brain', icon: <Shield className="w-4 h-4" /> },
            { label: 'Benchmarks', href: '#bench', icon: <BarChart2 className="w-4 h-4" /> }
          ]}
          activeHref={`#${activeTab}`}
          ease="power2.easeOut"
          baseColor="#6366f1"
          pillColor="#060609"
          hoveredPillTextColor="#ffffff"
          pillTextColor="#94a3b8"
        />

        <div className="flex items-center gap-4 text-sm font-medium">
          <div className="flex items-center gap-2 text-muted bg-[#060609] border border-border/80 px-4 py-1.5 rounded-full shadow-inner">
            <span className="w-2 h-2 rounded-full bg-success shadow-[0_0_8px_rgba(16,185,129,0.8)] animate-pulse" />
            Tenant: <span className="text-foreground tracking-wide font-mono text-xs">DEMO_1</span>
          </div>
        </div>
      </header>
      
      <main className="flex-1 p-8 max-w-[1600px] w-full mx-auto relative">
        {activeTab === 'dashboard' && <DashboardTab />}
        {activeTab === 'triage' && <TriageTab />}
        {activeTab === 'memory' && <AgentsMemoryTab />}
        {activeTab === 'brain' && <CompanyBrainTab />}
        {activeTab === 'bench' && <BenchmarksTab />}
      </main>
    </div>
  );
}

export default App;

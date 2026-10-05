import React, { useState, useEffect } from 'react';
import { ChevronDown, ArrowRight, Shield, Menu, X, Database, Cpu, Lock, BookOpen } from 'lucide-react';

interface LandingPageProps {
  onEnter: () => void;
}

export default function LandingPage({ onEnter }: LandingPageProps) {
  const [scrolled, setScrolled] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [currentView, setCurrentView] = useState<'home' | 'features' | 'architecture' | 'docs'>('home');

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 20);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  useEffect(() => {
    if (mobileMenuOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = 'auto';
    }
  }, [mobileMenuOpen]);

  const navTo = (view: 'home' | 'features' | 'architecture' | 'docs') => {
    setCurrentView(view);
    setMobileMenuOpen(false);
    window.scrollTo(0, 0);
  };

  return (
    <div className="font-helvetica-neue bg-brand-cream min-h-screen text-brand-dark overflow-x-hidden">
      {/* Navbar */}
      <nav
        className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
          scrolled || currentView !== 'home' ? 'bg-brand-cream/90 backdrop-blur-md shadow-sm' : 'bg-transparent'
        }`}
      >
        <div className="max-w-7xl mx-auto px-6 lg:px-8">
          <div className="relative flex items-center h-16 md:h-20">
            {/* Desktop left links */}
            <div className="hidden md:flex items-center gap-8 animate-fade-down stagger-1">
              <button onClick={() => navTo('features')} className="text-sm text-brand-dark tracking-wide uppercase hover:opacity-70 transition-opacity">
                Features
              </button>
              <button onClick={() => navTo('architecture')} className="text-sm text-brand-dark tracking-wide uppercase hover:opacity-70 transition-opacity">
                Architecture
              </button>
              <button onClick={() => navTo('docs')} className="text-sm text-brand-dark tracking-wide uppercase hover:opacity-70 transition-opacity">
                Docs
              </button>
            </div>

            {/* Center logo */}
            <div className="absolute left-1/2 -translate-x-1/2 flex items-center gap-2 animate-fade-down stagger-2 cursor-pointer" onClick={() => navTo('home')}>
              <Shield className="w-5 h-5 text-brand-dark" />
              <span className="text-xl text-brand-dark tracking-tight font-helvetica-neue font-bold">Sentinel<span className="font-light">Graph</span></span>
            </div>

            {/* Desktop CTA */}
            <button 
              onClick={onEnter}
              className="hidden md:inline-flex items-center ml-auto px-5 py-2.5 bg-brand-dark text-white text-sm tracking-wide uppercase rounded-full hover:bg-brand-green transition-colors animate-fade-down stagger-3"
            >
              Enter Dashboard
            </button>

            {/* Mobile hamburger */}
            <button
              className="md:hidden ml-auto z-50 w-10 h-10 flex flex-col items-center justify-center relative"
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              aria-label="Toggle menu"
            >
              <div className="w-full h-full relative flex items-center justify-center">
                <div
                  className={`absolute w-6 h-[2px] bg-brand-dark rounded transition-all duration-300 ease-[cubic-bezier(0.68,-0.6,0.32,1.6)] ${
                    mobileMenuOpen ? 'rotate-45' : 'top-[-3.5px]'
                  }`}
                />
                <div
                  className={`absolute w-6 h-[2px] bg-brand-dark rounded transition-all duration-300 ease-[cubic-bezier(0.68,-0.6,0.32,1.6)] ${
                    mobileMenuOpen ? '-rotate-45' : 'top-[3.5px]'
                  }`}
                />
              </div>
            </button>
          </div>
        </div>
      </nav>

      {/* Mobile overlay */}
      <div
        className={`md:hidden fixed inset-0 bg-brand-cream z-40 transition-opacity duration-500 ease-[cubic-bezier(0.22,1,0.36,1)] ${
          mobileMenuOpen ? 'opacity-100 pointer-events-auto' : 'opacity-0 pointer-events-none'
        }`}
      >
        <div
          className={`flex flex-col items-center justify-center h-full gap-8 transition-transform duration-500 delay-100 ease-[cubic-bezier(0.22,1,0.36,1)] ${
            mobileMenuOpen ? 'translate-y-0 opacity-100' : '-translate-y-8 opacity-0'
          }`}
        >
          <button className="text-3xl text-brand-dark tracking-tight" onClick={() => navTo('features')}>Features</button>
          <button className="text-3xl text-brand-dark tracking-tight" onClick={() => navTo('architecture')}>Architecture</button>
          <button className="text-3xl text-brand-dark tracking-tight" onClick={() => navTo('docs')}>Docs</button>
          <button 
            onClick={onEnter}
            className="mt-4 inline-flex items-center px-8 py-3.5 bg-brand-dark text-white text-lg tracking-wide rounded-full"
          >
            Enter Dashboard
          </button>
        </div>
      </div>

      {/* View Router */}
      {currentView === 'home' && (
        <section className="relative w-full h-screen min-h-[700px] overflow-hidden bg-brand-cream animate-fade-up">
          <div className="absolute inset-0">
            <video
              src="https://d8j0ntlcm91z4.cloudfront.net/user_38xzZboKViGWJOttwIXH07lWA1P/hf_20260820_010308_b1636845-4c15-4ab6-b0c9-9a29bfb0c6e3.mp4"
              autoPlay muted loop playsInline
              className="w-full h-full object-cover object-bottom"
            />
          </div>
          <div className="relative z-10 flex flex-col items-start max-w-7xl mx-auto pt-28 md:pt-36 px-6 lg:px-8">
            <button onClick={onEnter} className="inline-flex items-center gap-2 px-4 py-2 rounded-full border border-brand-dark/15 bg-white/60 backdrop-blur-sm hover:bg-white/80 transition-colors mb-5 md:mb-6 animate-fade-up stagger-3">
              <span className="text-sm text-brand-dark">Live for Graph Hacks today! Powered by FalkorDB.</span>
              <ArrowRight className="w-3.5 h-3.5 text-brand-dark" />
            </button>
            <h1 className="text-left text-3xl sm:text-4xl md:text-5xl lg:text-6xl text-brand-dark leading-[1.05] tracking-tight max-w-4xl font-helvetica-neue animate-fade-up stagger-4">
              One unified system to triage,<br className="hidden sm:block" /> investigate, and remediate alerts
            </h1>
            <div className="w-full mt-8 md:mt-10 animate-fade-up stagger-5">
              <p className="text-left text-xs tracking-[0.25em] uppercase text-brand-dark/50 mb-6 md:mb-8 font-helvetica-neue">Powered by</p>
              <div className="flex flex-wrap items-center justify-start gap-6 md:gap-12 lg:gap-16 animate-fade-up stagger-6">
                <span className="font-playfair font-bold text-lg md:text-xl lg:text-2xl text-brand-dark/80 whitespace-nowrap">FalkorDB</span>
                <span className="font-oswald uppercase font-medium text-lg md:text-xl lg:text-2xl text-brand-dark/80 whitespace-nowrap">ANTHROPIC</span>
                <span className="font-montserrat font-bold text-lg md:text-xl lg:text-2xl text-brand-dark/80 whitespace-nowrap">FastAPI</span>
                <span className="font-roboto-slab font-semibold text-lg md:text-xl lg:text-2xl text-brand-dark/80 whitespace-nowrap">ReactFlow</span>
                <span className="font-raleway font-bold text-lg md:text-xl lg:text-2xl text-brand-dark/80 whitespace-nowrap">OpenRouter</span>
              </div>
            </div>
          </div>
        </section>
      )}

      {currentView === 'features' && (
        <section className="pt-32 pb-20 px-6 lg:px-8 max-w-7xl mx-auto min-h-screen animate-fade-up">
          <h1 className="text-4xl md:text-5xl font-helvetica-neue tracking-tight mb-4">Core Features</h1>
          <p className="text-xl text-brand-dark/70 mb-16 max-w-2xl leading-relaxed">Experience a paradigm shift in security operations through graph-native intelligence.</p>
          <div className="grid md:grid-cols-3 gap-12">
            <div className="space-y-4">
              <div className="w-12 h-12 bg-brand-dark text-white rounded-2xl flex items-center justify-center mb-6"><Database className="w-6 h-6" /></div>
              <h3 className="text-xl font-bold font-helvetica-neue">Graph-Native Triage</h3>
              <p className="text-brand-dark/70 leading-relaxed">Calculate exact blast radius via topological multi-hop reasoning. See how findings traverse your environment, avoiding CVSS decoys.</p>
            </div>
            <div className="space-y-4">
              <div className="w-12 h-12 bg-brand-green text-white rounded-2xl flex items-center justify-center mb-6"><Cpu className="w-6 h-6" /></div>
              <h3 className="text-xl font-bold font-helvetica-neue">Autonomous MCP Agents</h3>
              <p className="text-brand-dark/70 leading-relaxed">Swarm intelligence leveraging Model Context Protocol to execute algorithms like PageRank directly against the FalkorDB substrate.</p>
            </div>
            <div className="space-y-4">
              <div className="w-12 h-12 bg-brand-dark/10 text-brand-dark border border-brand-dark/20 rounded-2xl flex items-center justify-center mb-6"><Lock className="w-6 h-6" /></div>
              <h3 className="text-xl font-bold font-helvetica-neue">Company Brain</h3>
              <p className="text-brand-dark/70 leading-relaxed">Bi-temporal memory graph maps architecture decisions (ADRs) to physical infrastructure, instantly finding the exact engineer who introduced a flaw.</p>
            </div>
          </div>
        </section>
      )}

      {currentView === 'architecture' && (
        <section className="pt-32 pb-20 px-6 lg:px-8 max-w-4xl mx-auto min-h-screen animate-fade-up">
          <h1 className="text-4xl md:text-5xl font-helvetica-neue tracking-tight mb-4">System Architecture</h1>
          <p className="text-xl text-brand-dark/70 mb-12 leading-relaxed">Designed for infinite scaling and seamless context routing.</p>
          <div className="bg-white border border-brand-dark/10 p-8 md:p-12 rounded-3xl shadow-sm mb-12">
            <h3 className="text-lg font-bold mb-6 font-helvetica-neue uppercase tracking-widest text-brand-dark/50">Data Flow</h3>
            <div className="space-y-8">
              <div className="flex flex-col md:flex-row gap-6 items-start">
                <span className="bg-brand-dark text-brand-cream text-xs px-3 py-1 rounded-full uppercase tracking-widest font-bold mt-1">1. Ingestion</span>
                <p className="leading-relaxed text-lg">Alerts and findings are continuously streamed into the <strong className="font-playfair">FalkorDB</strong> context layer via bulk UNWIND queries, mapping vulnerable assets and access tokens.</p>
              </div>
              <div className="flex flex-col md:flex-row gap-6 items-start">
                <span className="bg-brand-green text-brand-cream text-xs px-3 py-1 rounded-full uppercase tracking-widest font-bold mt-1">2. Triage</span>
                <p className="leading-relaxed text-lg">The Triage Agent utilizes <strong className="font-oswald">MCP Tools</strong> to calculate multi-hop blast radius, ranking threats based on direct graph paths to critical data rather than isolated severity scores.</p>
              </div>
              <div className="flex flex-col md:flex-row gap-6 items-start">
                <span className="bg-brand-dark text-brand-cream text-xs px-3 py-1 rounded-full uppercase tracking-widest font-bold mt-1">3. Brain</span>
                <p className="leading-relaxed text-lg">The Company Brain uses <strong className="font-montserrat">Graph RAG</strong> to map mitigated vulnerabilities to original Architectural Decision Records (ADRs) and assigns remediation tasks to the correct team.</p>
              </div>
            </div>
          </div>
        </section>
      )}

      {currentView === 'docs' && (
        <section className="pt-32 pb-20 px-6 lg:px-8 max-w-5xl mx-auto min-h-screen animate-fade-up">
          <h1 className="text-4xl md:text-5xl font-helvetica-neue tracking-tight mb-4">Documentation</h1>
          <p className="text-xl text-brand-dark/70 mb-12 leading-relaxed">Quick start guides and API references.</p>
          
          <div className="bg-[#111] text-brand-cream p-8 rounded-3xl shadow-xl overflow-x-auto font-mono text-sm leading-loose">
            <div className="flex items-center gap-2 mb-6 border-b border-white/10 pb-4">
              <BookOpen className="w-5 h-5 text-brand-cream/50" />
              <span className="text-brand-cream/50 uppercase tracking-widest text-xs font-bold font-helvetica-neue">Getting Started</span>
            </div>
            <p className="text-brand-green"># Clone the repository</p>
            <p>git clone https://github.com/your-org/sentinelgraph</p>
            <br />
            <p className="text-brand-green"># Configure environment</p>
            <p>cp .env.example .env</p>
            <p>echo "OPENROUTER_API_KEY=sk-or-v1-..." {">>"} .env</p>
            <br />
            <p className="text-brand-green"># Start FalkorDB and API</p>
            <p>docker-compose up -d --build</p>
            <br />
            <p className="text-brand-green"># Run frontend</p>
            <p>cd web && npm run dev</p>
          </div>
        </section>
      )}
    </div>
  );
}

// Schema for SentinelGraph
// We create indices for fast lookups.

// Security Indices
CREATE INDEX ON :Asset(id);
CREATE INDEX ON :Asset(internet_exposed);
CREATE INDEX ON :Asset(crown_jewel);
CREATE INDEX ON :Service(id);
CREATE INDEX ON :Identity(id);
CREATE INDEX ON :Vulnerability(id);
CREATE INDEX ON :Vulnerability(cve);
CREATE INDEX ON :Alert(id);
CREATE INDEX ON :Finding(id);
CREATE INDEX ON :Incident(id);

// Memory & Coordination Indices
CREATE INDEX ON :Session(id);
CREATE INDEX ON :Fact(id);
CREATE INDEX ON :Playbook(id);
CREATE INDEX ON :AgentTask(id);

// Brain Indices
CREATE INDEX ON :Person(id);
CREATE INDEX ON :Team(id);
CREATE INDEX ON :Project(id);
CREATE INDEX ON :Document(id);
CREATE INDEX ON :Ticket(id);
CREATE INDEX ON :ChatThread(id);
CREATE INDEX ON :Decision(id);

// Generic provenance index
CREATE INDEX ON :Document(source_id);
CREATE INDEX ON :Ticket(source_id);
CREATE INDEX ON :ChatThread(source_id);
CREATE INDEX ON :Decision(source_id);

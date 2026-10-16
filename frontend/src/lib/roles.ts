// Curated Authentic Technology, Engineering, Data, Cloud & AI Roles Catalog
const RAW_ALL_ROLES: string[] = [
  // 1. AI & Intelligent Systems (ai_agents & ml_engineering)
  "AI Agent Engineer",
  "AI Architect",
  "AI Engineer",
  "AI Product Manager",
  "AI Safety Engineer",
  "AI/ML Engineer",
  "Computer Vision Engineer",
  "Data Scientist",
  "Deep Learning Engineer",
  "MLOps Engineer",
  "Machine Learning Engineer",
  "NLP Engineer",
  "Prompt Engineer",
  "RAG Systems Engineer",
  "Search & Recommendation Engineer",
  "Vector Database Engineer",

  // 2. Data Engineering & Analytics (data_engineering & data_analytics)
  "Analytics Engineer",
  "Big Data Engineer",
  "Business Intelligence Engineer",
  "Data Analyst",
  "Data Architect",
  "Data Engineer",
  "Data Governance & Privacy Officer",
  "Database Administrator (DBA)",
  "Database Reliability Engineer",
  "Product Analyst",
  "Quantitative Analyst",

  // 3. Backend, Distributed Systems & Systems (backend_systems)
  ".NET Backend Engineer",
  "API & Microservices Engineer",
  "Backend Engineer",
  "DevTools Engineer",
  "Distributed Systems Engineer",
  "Go Backend Engineer",
  "Java Backend Engineer",
  "Node.js Backend Engineer",
  "Python Backend Engineer",
  "QA Automation Engineer",
  "Rust Systems Engineer",
  "Systems Engineer",
  "Test Automation Architect",

  // 4. Frontend & Design Systems (frontend_ui)
  "Accessibility Engineer",
  "Frontend Architect",
  "Frontend Engineer",
  "Product Designer (UI/UX)",
  "React Developer",
  "UI/UX Design Systems Engineer",
  "Web Performance Engineer",

  // 5. Fullstack Engineering (fullstack_general)
  "Fullstack Engineer",
  "Integration Engineer",
  "Senior Software Engineer",
  "Software Engineer",
  "Staff Software Engineer",

  // 6. Cloud, DevOps & Platform Engineering (devops_platform)
  "Chaos Engineer",
  "Cloud Architect",
  "Cloud Infrastructure Engineer",
  "DevOps Engineer",
  "Kubernetes Administrator",
  "Linux Systems Administrator",
  "Platform Engineer",
  "Release & Automation Engineer",
  "Site Reliability Engineer (SRE)",

  // 7. Cybersecurity & Ethical Hacking (security_cyber)
  "Application Security Engineer",
  "Cloud Security Architect",
  "Cybersecurity Analyst",
  "DevSecOps Engineer",
  "Ethical Hacker",
  "Incident Response Engineer",
  "Network Security Engineer",
  "Penetration Tester",
  "Security Engineer",

  // 8. Mobile Application Engineering (mobile_dev)
  "Android Kotlin Developer",
  "Flutter Mobile Developer",
  "Mobile Engineer",
  "React Native Developer",
  "iOS Swift Developer",

  // 9. Embedded Systems, Firmware & IoT (embedded_systems)
  "Embedded Systems Engineer",
  "Firmware Engineer",
  "IoT Systems Engineer",
  "Real-Time Kernel Engineer",
  "Robotics Software Engineer",

  // 10. Blockchain & Web3 Protocols (blockchain_web3)
  "Blockchain Developer",
  "DeFi Quantitative Architect",
  "Smart Contract Engineer",
  "Solidity Developer",
  "Web3 Protocol Engineer",

  // 11. Marketplace, Fintech & Platforms (marketplace_systems)
  "Dynamic Pricing & Matching Engineer",
  "Fintech Systems Engineer",
  "Marketplace Systems Engineer",
  "Payments & Ledger Engineer",

  // 12. Technology Leadership & Architecture Strategy (tech_leadership_advisory)
  "Chief Technology Officer (CTO)",
  "Enterprise Solutions Architect",
  "Head of Engineering",
  "Technical Director",
  "Technical Lead (Tech Lead)",
  "Technical Program Manager (TPM)",
  "VP of Engineering"
];

// Clean deduplicated list of technology roles
export const ALL_ROLES: string[] = Array.from(new Set(RAW_ALL_ROLES)).sort();
export const ALL_TECH_ROLES: string[] = ALL_ROLES;

export function isTechnicalRole(roleName: string): boolean {
  if (!roleName) return false;
  const r = roleName.trim().toLowerCase();
  if (ALL_ROLES.some((role) => role.toLowerCase() === r)) return true;
  const techKeywords = [
    "engineer", "developer", "architect", "analyst", "scientist", "devops",
    "sre", "cloud", "security", "machine learning", "ai", "fullstack",
    "backend", "frontend", "systems", "cto", "tech lead", "technical lead",
    "programmer", "database", "infrastructure", "platform", "embedded", "firmware",
    "hacker", "blockchain", "solidity", "firmware"
  ];
  return techKeywords.some((kw) => r.includes(kw));
}

// Core roles featured in quick-select pills
export const POPULAR_ROLES: string[] = [
  "Ethical Hacker",
  "AI Engineer",
  "Backend Engineer",
  "Frontend Engineer",
  "Fullstack Engineer",
  "Data Analyst",
  "Data Engineer",
  "DevOps Engineer",
  "Cloud Architect",
  "Machine Learning Engineer",
  "Security Engineer",
  "Site Reliability Engineer (SRE)",
  "Mobile Engineer",
  "Embedded Systems Engineer",
  "Blockchain Developer",
  "Chief Technology Officer (CTO)"
];

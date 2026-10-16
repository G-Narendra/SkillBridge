import json
import os

PROFILES_JSON = r"e:\Moving\Desktop\SkillBridge\project\backend\role_profiles_465.json"
ROLES_TS = r"e:\Moving\Desktop\SkillBridge\project\frontend\src\lib\roles.ts"

with open(PROFILES_JSON, "r", encoding="utf-8") as f:
    profiles = json.load(f)

# Non-technical or physical/business disciplines that do NOT produce software/code repositories
disqualified_keywords = [
    'accountant', 'accounting', 'account executive', 'affiliate marketing', 'agile coach', 'angel investor',
    'animator', 'banking', 'board member', 'brand manager', 'brand strategist', 'business development',
    'business model', 'business strategist', 'ceo', 'cfo', 'channel sales', 'chief security officer',
    'chief strategy officer', 'clinical operations', 'cmo', 'co founder', 'community manager',
    'company secretary', 'competitive analyst', 'compliance officer', 'content creator', 'content strategist',
    'content writer', 'contract manager', 'conversion rate', 'coo', 'copy editor', 'copywriter',
    'corporate lawyer', 'cpo', 'crm specialist', 'crowdfunding', 'csr manager', 'cultural consultant',
    'curriculum designer', 'customer discovery', 'customer experience', 'customer interview',
    'customer marketing', 'customer onboarding', 'customer success', 'customer support', 'demand generation',
    'director of marketing', 'director of sales', 'dispute resolution', 'diversity equity', 'domain strategist',
    'dtc brand', 'dtc e-commerce', 'dtc e commerce', 'dtc retention', 'dtc supply chain', 'e commerce manager',
    'ecommerce manager', 'early stage legal', 'email deliverability', 'email marketing', 'enterprise sdr',
    'esg analyst', 'event coordinator', 'event marketing', 'executive assistant', 'executive coach',
    'exit strategy', 'export manager', 'facilities manager', 'field marketing', 'field operations',
    'finance manager', 'financial analyst', 'foreign market', 'founder ceo', 'founder entrepreneur',
    'fractional cfo', 'fractional cmo', 'fractional coo', 'fractional vp', 'fulfillment engineer',
    'fundraising', 'game designer', 'general counsel', 'general manager', 'global hr', 'global marketing',
    'go to market', 'grant writer', 'graphic designer', 'ground reality', 'growth hacker', 'growth marketing',
    'head of customer success', 'head of growth', 'head of marketing', 'head of operations',
    'head of partnerships', 'head of people', 'head of sales', 'healthcare compliance', 'hr generalist',
    'hr manager', 'idea critic', 'ideation facilitator', 'implementation specialist', 'inbound marketing',
    'industrial designer', 'industry expert', 'influencer', 'innovation consultant', 'innovation manager',
    'inside sales', 'instructional designer', 'international business', 'international tax', 'inventory manager',
    'investment analyst', 'investor relations', 'ip lawyer', 'ipo specialist', 'key account manager',
    'landing page specialist', 'landing page optimizer', 'lead generation', 'legal counsel', 'legal operations',
    'level designer', 'localization specialist', 'logistics coordinator', 'logo designer', 'macro economist',
    'management consultant', 'manufacturing engineer', 'market research', 'marketing manager',
    'marketing operations', 'marketing ops', 'marketplace ops', 'materials engineer', 'mechanical engineer',
    'media buyer', 'mentor advisor', 'merchandiser', 'monetization designer', 'motion designer',
    'motion graphics', 'narrative designer', 'office manager', 'onboarding specialist', 'operations analyst',
    'operations manager', 'packaging engineer', 'partner manager', 'partner marketing', 'partnership development',
    'partnership manager', 'payments compliance', 'payroll specialist', 'performance marketer',
    'performance marketing', 'portfolio manager', 'pr specialist', 'pricing analyst', 'pricing strategist',
    'problem researcher', 'procurement', 'product evangelist', 'product marketing manager', 'public relations',
    'recruiter', 'recruiting coordinator', 'referral program', 'regulatory affairs', 'retail buyer',
    'retail manager', 'retention marketer', 'revenue accountant', 'revenue operations', 'revops',
    'sales development', 'sales engineer', 'sales manager', 'sales operations', 'sales ops manager',
    'sales representative', 'scrum master', 'seo specialist', 'search engine optimization', 'social media',
    'solution debater', 'solution entrepreneur', 'sourcing manager', 'sourcing specialist', 'startup namer',
    'store manager', 'strategic planner', 'strategy consultant', 'succession planner', 'supply chain',
    'support specialist', 'sustainability officer', 'talent acquisition', 'tax advisor', 'tax manager',
    'technical recruiter', 'telecommunications specialist', 'tokenomics expert', 'trade compliance',
    'training manager', 'training specialist', 'transportation manager', 'treasurer', 'ui researcher',
    'unit economics analyst', 'user acquisition', 'user experience researcher', 'ux researcher', 'ux writer',
    'valuation model', 'vc investor', 'venture capitalist', 'video editor', 'video producer', 'videographer',
    'visual designer', 'warehouse manager', 'writer', 'yield manager'
]

curated_roles = {}
for rname, rdata in profiles.items():
    r_low = rname.lower().strip()
    if not any(k in r_low for k in disqualified_keywords):
        curated_roles[rname] = rdata

# For leadership roles, assign authentic technology strategy and architecture skills
leadership_skills = {
    'languages': ['System Architecture', 'Cloud Strategy'],
    'frameworks': ['Agile Governance', 'RFC Processes'],
    'databases': ['Data Governance', 'FinOps'],
    'tools': ['AWS', 'Security Auditing', 'Disaster Recovery']
}

for rname in curated_roles:
    r_low = rname.lower()
    if any(k in r_low for k in ['cto', 'vp engineering', 'director of engineering', 'head of engineering', 'fractional cto']):
        curated_roles[rname]['categories'] = leadership_skills
        curated_roles[rname]['raw_skills'] = ['System Architecture', 'Cloud Strategy', 'FinOps', 'Security Auditing']

print(f"Original profiles: {len(profiles)}, Curated technology profiles: {len(curated_roles)}")

with open(PROFILES_JSON, "w", encoding="utf-8") as f:
    json.dump(curated_roles, f, indent=2)

sorted_roles = sorted(list(curated_roles.keys()))
roles_ts_content = '''// Curated Authentic Technology, Engineering, Data, Cloud & AI Roles Catalog
const RAW_ALL_ROLES: string[] = [
''' + '\n'.join([f'  "{r}",' for r in sorted_roles]) + '''
];

// Clean deduplicated list of technology roles
export const ALL_ROLES: string[] = Array.from(new Set(RAW_ALL_ROLES)).sort();

// Core roles featured in quick-select pills
export const POPULAR_ROLES: string[] = [
  "Data Analyst",
  "Backend Engineer",
  "Frontend Engineer",
  "Fullstack Engineer",
  "AI Engineer",
  "Data Engineer",
  "DevOps Engineer",
  "Cloud Architect",
  "Machine Learning Engineer",
  "Security Engineer",
  "Site Reliability Engineer",
  "Mobile Developer",
  "CTO"
];
'''

with open(ROLES_TS, "w", encoding="utf-8") as f:
    f.write(roles_ts_content)

print(f"Saved {len(curated_roles)} technology roles to {PROFILES_JSON} and {ROLES_TS}")

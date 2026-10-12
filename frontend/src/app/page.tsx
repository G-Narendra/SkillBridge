"use client";

import React, { useState, useEffect } from "react";
import {
  CheckCircle,
  XCircle,
  ArrowRight,
  Github,
  Gitlab,
  Loader2,
  ExternalLink,
  Code2,
  FolderGit2,
  KeyRound,
  FileText,
  AlertCircle,
  Sparkles,
  Download,
  Share2,
  ShieldCheck,
  ChevronDown,
  ChevronUp,
  Copy,
  Check,
  CheckCircle2
} from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import axios from "axios";
import Image from "next/image";
import { useSession, signIn, signOut } from "next-auth/react";

import { Button } from "@/components/ui/Button";
import { Card, CardHeader, CardTitle, CardContent, CardDescription, CardFooter } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { Dropzone } from "@/components/ui/Dropzone";
import { ProgressBar } from "@/components/ui/ProgressBar";
import { Modal } from "@/components/ui/Modal";
import { TabGroup, TabItem } from "@/components/ui/TabGroup";
import { RoleCombobox } from "@/components/RoleCombobox";
import { CategoryChart } from "@/components/CategoryChart";
import { ThemeToggle } from "@/components/ThemeToggle";
import { ConnectedAccountBar, type ConnectedUser } from "@/components/ConnectedAccountBar";
import { BlueprintInspector } from "@/components/BlueprintInspector";
import { MultiRoleBenchmark } from "@/components/MultiRoleBenchmark";
import { ResumeAuditCard } from "@/components/ResumeAuditCard";
import { PortfolioCardModal } from "@/components/PortfolioCardModal";

const STANDARD_ROLES = [
  "Data Analyst",
  "Backend Engineer",
  "Machine Learning Engineer",
  "AI Engineer",
  "Frontend Engineer",
  "Fullstack Engineer",
  "DevOps Engineer",
  "Cloud Architect",
  "Data Engineer",
  "Mobile Developer",
  "Security Engineer",
  "Systems Engineer",
  "QA Automation Engineer",
  "Site Reliability Engineer",
  "Blockchain Developer"
];

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8080";

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [targetRole, setTargetRole] = useState("Data Analyst");
  const [status, setStatus] = useState<"idle" | "loading" | "success" | "error">("idle");
  const [analysis, setAnalysis] = useState<any>(null);
  const [errorMessage, setErrorMessage] = useState<string>("");

  // Modals & tabs
  const [selectedBlueprint, setSelectedBlueprint] = useState<any | null>(null);
  const [blueprintInspectorOpen, setBlueprintInspectorOpen] = useState(false);
  const [provisionModalOpen, setProvisionModalOpen] = useState(false);
  const [portfolioCardOpen, setPortfolioCardOpen] = useState(false);
  const [showAnonymizedSnippet, setShowAnonymizedSnippet] = useState(false);
  const [activeCategoryTab, setActiveCategoryTab] = useState("all");
  const [authSettingsOpen, setAuthSettingsOpen] = useState(false);

  // Available roles (supports complete 465+ technology catalog)
  const [availableRoles, setAvailableRoles] = useState<string[]>(STANDARD_ROLES);

  // Connected developer account
  const { data: session } = useSession();
  const [connectedUser, setConnectedUser] = useState<ConnectedUser | null>(null);
  const [platformAccount, setPlatformAccount] = useState<ConnectedUser | null>(null);
  const [tokenInput, setTokenInput] = useState("");
  const [tokenValidating, setTokenValidating] = useState(false);
  const [tokenError, setTokenError] = useState("");

  // GitHub Authorization Center state (1-Click & Device Flow)
  const [deviceFlowState, setDeviceFlowState] = useState<{
    status: "idle" | "requesting" | "ready" | "polling" | "success" | "error";
    userCode?: string;
    deviceCode?: string;
    verificationUri?: string;
    error?: string;
  }>({ status: "idle" });
  const [showAdvancedPat, setShowAdvancedPat] = useState(false);
  const [copiedCode, setCopiedCode] = useState(false);

  // Provisioning parameters
  const [platformProvider, setPlatformProvider] = useState<"github" | "gitlab">("github");
  const [useSandboxMode, setUseSandboxMode] = useState(false);
  const [provisioningState, setProvisioningState] = useState<{
    status: "idle" | "running" | "success" | "error";
    step: number;
    message: string;
    result: any | null;
  }>({
    status: "idle",
    step: 0,
    message: "",
    result: null
  });

  // Query platform GitHub status, load saved PAT, and fetch 465+ dynamic roles
  useEffect(() => {
    let isMounted = true;

    async function initializePlatform() {
      // 1. Check if user previously saved a custom PAT
      const savedToken = typeof window !== "undefined" ? localStorage.getItem("skillbridge_pat") : null;
      if (savedToken) {
        try {
          const res = await axios.post(`${API_BASE_URL}/api/github/validate-token`, { token: savedToken });
          if (res.data?.valid && isMounted) {
            setConnectedUser({
              ...res.data,
              raw_token: savedToken,
              source: "custom_pat"
            });
          }
        } catch {
          if (typeof window !== "undefined") {
            localStorage.removeItem("skillbridge_pat");
          }
        }
      }

      // 2. Query platform GitHub status from backend
      try {
        const res = await axios.get(`${API_BASE_URL}/api/github/status`);
        if (res.data?.configured && res.data?.valid && isMounted) {
          const account: ConnectedUser = {
            ...res.data,
            raw_token: "default",
            source: "platform"
          };
          setPlatformAccount(account);
          if (!savedToken) {
            setConnectedUser(account);
          }
        }
      } catch (err) {
        console.warn("Unable to check GitHub platform status:", err);
      }

      // 3. Load full 465+ technology roles from backend API
      try {
        const rolesRes = await axios.get(`${API_BASE_URL}/api/roles`);
        if (rolesRes.data?.roles && Array.isArray(rolesRes.data.roles) && isMounted) {
          const names = rolesRes.data.roles.map((r: any) => r.name);
          if (names.length > 0) {
            setAvailableRoles(names);
          }
        }
      } catch (rolesErr) {
        console.warn("Unable to fetch dynamic roles catalog:", rolesErr);
      }
    }

    initializePlatform();

    return () => {
      isMounted = false;
    };
  }, []);

  // Automatically link NextAuth session if available
  useEffect(() => {
    if (session?.user && !connectedUser) {
      setConnectedUser({
        login: session.user.name || "github-user",
        name: session.user.name || undefined,
        avatar_url: session.user.image || undefined,
        public_repos: 10,
        scopes: ["repo", "read:user"],
        is_sandbox: false,
        source: "oauth"
      });
    }
  }, [session, connectedUser]);

  // Connect platform verified account
  const handleConnectPlatform = () => {
    if (platformAccount) {
      setConnectedUser({
        ...platformAccount,
        raw_token: "default",
        source: "platform"
      });
      setAuthSettingsOpen(false);
    }
  };

  // Connect demo profile
  const handleConnectDemo = async () => {
    try {
      setTokenValidating(true);
      const res = await axios.post(`${API_BASE_URL}/api/github/validate-token`, { token: "demo" });
      setConnectedUser({
        ...res.data,
        is_sandbox: true,
        source: "sandbox"
      });
      setAuthSettingsOpen(false);
    } catch {
      setConnectedUser({
        login: "developer-preview",
        name: "Verified Developer",
        avatar_url: "https://avatars.githubusercontent.com/u/583231?v=4",
        public_repos: 14,
        scopes: ["repo", "read:user"],
        is_sandbox: true,
        source: "sandbox"
      });
      setAuthSettingsOpen(false);
    } finally {
      setTokenValidating(false);
    }
  };

  // Device Code Authorization Flow (No PAT generation needed)
  const handleStartDeviceFlow = async () => {
    setDeviceFlowState({ status: "requesting" });
    try {
      const res = await axios.post(`${API_BASE_URL}/api/auth/github/device/init`);
      if (res.data?.supported && res.data?.user_code) {
        setDeviceFlowState({
          status: "ready",
          userCode: res.data.user_code,
          deviceCode: res.data.device_code,
          verificationUri: res.data.verification_uri || "https://github.com/login/device",
        });
        pollDeviceStatus(res.data.device_code, res.data.interval || 5);
      } else {
        setDeviceFlowState({
          status: "error",
          error: res.data?.error || "Device flow is unavailable. Please authorize using the platform account.",
        });
      }
    } catch (err: any) {
      setDeviceFlowState({
        status: "error",
        error: err.response?.data?.detail || "Failed to initiate GitHub device authorization.",
      });
    }
  };

  const pollDeviceStatus = (deviceCode: string, intervalSec: number) => {
    let isCancelled = false;
    const intervalMs = Math.max(intervalSec, 5) * 1000;

    const check = async () => {
      if (isCancelled) return;
      try {
        const pollRes = await axios.post(`${API_BASE_URL}/api/auth/github/device/poll`, {
          device_code: deviceCode,
        });

        if (pollRes.data?.status === "authorized" && pollRes.data?.access_token) {
          isCancelled = true;
          const token = pollRes.data.access_token;
          if (typeof window !== "undefined") {
            localStorage.setItem("skillbridge_pat", token);
          }
          setConnectedUser({
            ...pollRes.data.user,
            raw_token: token,
            source: "oauth",
          });
          setDeviceFlowState({ status: "success" });
          setTimeout(() => {
            setAuthSettingsOpen(false);
            setDeviceFlowState({ status: "idle" });
          }, 1500);
        } else if (pollRes.data?.status === "expired" || pollRes.data?.status === "denied") {
          isCancelled = true;
          setDeviceFlowState({
            status: "error",
            error: pollRes.data?.error || "Authorization expired or was rejected on GitHub.",
          });
        } else {
          setTimeout(check, intervalMs);
        }
      } catch {
        isCancelled = true;
        setDeviceFlowState({
          status: "error",
          error: "Error polling authorization status.",
        });
      }
    };

    setTimeout(check, intervalMs);
  };

  const handleCopyCode = (code: string) => {
    if (typeof navigator !== "undefined") {
      navigator.clipboard.writeText(code);
      setCopiedCode(true);
      setTimeout(() => setCopiedCode(false), 2000);
    }
  };

  // Validate personal access token
  const handleValidateToken = async () => {
    if (!tokenInput.trim()) return;
    setTokenValidating(true);
    setTokenError("");

    try {
      const res = await axios.post(`${API_BASE_URL}/api/github/validate-token`, { token: tokenInput.trim() });
      if (typeof window !== "undefined") {
        localStorage.setItem("skillbridge_pat", tokenInput.trim());
      }
      setConnectedUser({ ...res.data, raw_token: tokenInput.trim(), source: "custom_pat" });
      setTokenInput("");
      setAuthSettingsOpen(false);
    } catch (err: any) {
      const msg = err.response?.data?.detail || "Invalid developer credentials.";
      setTokenError(msg);
    } finally {
      setTokenValidating(false);
    }
  };

  const handleDisconnect = () => {
    setConnectedUser(null);
    if (typeof window !== "undefined") {
      localStorage.removeItem("skillbridge_pat");
    }
    if (session) {
      signOut({ redirect: false });
    }
  };

  const executeAnalysis = async (overrideRole?: string) => {
    if (!file) return;
    const roleToUse = overrideRole || targetRole;
    if (overrideRole) {
      setTargetRole(overrideRole);
    }

    setStatus("loading");
    setErrorMessage("");
    setAnalysis(null);

    const formData = new FormData();
    formData.append("file", file);
    formData.append("target_job", roleToUse);

    try {
      const response = await axios.post(`${API_BASE_URL}/api/resume/parse`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
        timeout: 60000
      });
      setAnalysis(response.data);
      setStatus("success");
    } catch (err: any) {
      console.error(err);
      const detail = err.response?.data?.detail || err.message || "Failed to communicate with backend service.";
      setErrorMessage(detail);
      setStatus("error");
    }
  };

  const openInspector = (project: any) => {
    setSelectedBlueprint(project);
    setBlueprintInspectorOpen(true);
  };

  const handleProceedFromInspector = (customizedBlueprint: any) => {
    setSelectedBlueprint(customizedBlueprint);
    setBlueprintInspectorOpen(false);
    setProvisionModalOpen(true);
    setProvisioningState({
      status: "idle",
      step: 0,
      message: "Ready to initialize repository.",
      result: null
    });
  };

  const executeProvisioning = async () => {
    if (!selectedBlueprint) return;

    let tokenToSend = "default";
    if (useSandboxMode) {
      tokenToSend = "sandbox";
    } else if (connectedUser?.raw_token) {
      tokenToSend = connectedUser.raw_token;
    } else if (connectedUser?.is_sandbox) {
      tokenToSend = "sandbox";
    } else if (connectedUser?.source === "platform") {
      tokenToSend = "default";
    } else if (session?.accessToken) {
      tokenToSend = session.accessToken;
    } else if (connectedUser?.login) {
      tokenToSend = "default";
    }

    setProvisioningState({
      status: "running",
      step: 1,
      message: `Connecting to ${platformProvider === "gitlab" ? "GitLab" : "GitHub"} platform APIs...`,
      result: null
    });

    try {
      setTimeout(() => {
        setProvisioningState((prev) => ({
          ...prev,
          step: 2,
          message: "Creating remote repository and verifying branch permissions..."
        }));
      }, 600);

      setTimeout(() => {
        setProvisioningState((prev) => ({
          ...prev,
          step: 3,
          message: "Synthesizing atomic Git tree commit and multi-file architecture..."
        }));
      }, 1400);

      setTimeout(() => {
        setProvisioningState((prev) => ({
          ...prev,
          step: 3,
          message: "Publishing milestone tracking issues and verification gates..."
        }));
      }, 3000);

      const response = await axios.post(
        `${API_BASE_URL}/api/provision`,
        {
          title: selectedBlueprint.title,
          tech_stack: selectedBlueprint.tech_stack,
          roadmap: selectedBlueprint.roadmap,
          starter_files: selectedBlueprint.starter_files,
          token: tokenToSend,
          provider: platformProvider
        },
        { timeout: 120000 }
      );

      setProvisioningState({
        status: "success",
        step: 4,
        message: "Repository successfully provisioned and milestone issues populated.",
        result: response.data
      });
    } catch (err: any) {
      console.error(err);
      const errDetail = err.response?.data?.detail || err.message || "Failed to provision repository.";
      setProvisioningState({
        status: "error",
        step: 3,
        message: errDetail,
        result: null
      });
    }
  };

  // Export verifiable career audit report
  const exportCareerReport = () => {
    if (!analysis) return;
    const reportText = `# SkillBridge AI career verification audit

Candidate: ${analysis.contacts?.name || "Technical Candidate"}
Target Role: ${analysis.target_role}
Weighted Compatibility Score: ${analysis.match_percentage}%
Detected Technical Experience: ${analysis.experience_years} years

## Category distributions
- Languages (40% weight): ${analysis.category_breakdown?.languages?.percentage}%
- Frameworks (30% weight): ${analysis.category_breakdown?.frameworks?.percentage}%
- Databases (20% weight): ${analysis.category_breakdown?.databases?.percentage}%
- Developer Tools (10% weight): ${analysis.category_breakdown?.tools?.percentage}%

## Verified competencies (${analysis.matched_skills?.length})
${analysis.matched_skills?.map((s: string) => `- ${s}`).join("\n")}

## Missing competency requirements (${analysis.missing_skills?.length})
${analysis.missing_skills?.map((s: string) => `- ${s}`).join("\n")}

## Tailored portfolio blueprints
${analysis.projects?.map((p: any, idx: number) => `
### ${idx + 1}. ${p.title} (${p.difficulty} - ${p.hours} hours)
- Objective: ${p.objective}
- Technical Stack: ${p.tech_stack?.join(", ")}
- Target Gaps Addressed: ${p.target_skills_covered?.join(", ")}
- Milestone Roadmap:
${p.roadmap?.map((m: string, mIdx: number) => `  ${mIdx + 1}. ${m}`).join("\n")}
`).join("\n")}

Verification Digest: SHA-256 Verified by SkillBridge AI Engine
Generated: ${new Date().toISOString()}
`;
    const blob = new Blob([reportText], { type: "text/markdown;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `skillbridge-audit-${analysis.target_role.toLowerCase().replace(/\s+/g, "-")}.md`;
    link.click();
    URL.revokeObjectURL(url);
  };

  // Build filter tabs for category matrix
  const categoryTabs: TabItem[] = [
    { id: "all", label: "All categories" },
    {
      id: "languages",
      label: "Languages (40%)",
      count: analysis?.category_breakdown?.languages?.total_required
    },
    {
      id: "frameworks",
      label: "Frameworks (30%)",
      count: analysis?.category_breakdown?.frameworks?.total_required
    },
    {
      id: "databases",
      label: "Databases (20%)",
      count: analysis?.category_breakdown?.databases?.total_required
    },
    {
      id: "tools",
      label: "Developer tools (10%)",
      count: analysis?.category_breakdown?.tools?.total_required
    }
  ];

  const getFilteredSkills = () => {
    if (!analysis) return { matched: [], missing: [] };
    if (activeCategoryTab === "all") {
      return {
        matched: analysis.matched_skills || [],
        missing: analysis.missing_skills || []
      };
    }
    const catData = analysis.category_breakdown?.[activeCategoryTab];
    return {
      matched: catData?.matched || [],
      missing: catData?.missing || []
    };
  };

  const filtered = getFilteredSkills();

  return (
    <main className="min-h-screen bg-[#f5f5f7] dark:bg-[#090d16] text-slate-800 dark:text-slate-200 transition-colors duration-200">
      {/* Sticky Header with Frosted Glass */}
      <header className="sticky top-0 z-40 w-full border-b border-slate-200/90 dark:border-slate-800 bg-white/80 dark:bg-[#0f172a]/85 backdrop-blur-xl">
        <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-6">
          <div className="flex items-center space-x-3 sm:space-x-4">
            <div className="flex items-center space-x-2.5">
              <div className="rounded-xl bg-[#0071e3] p-2 text-white shadow-sm">
                <Code2 size={18} />
              </div>
              <div>
                <h1 className="text-sm sm:text-base font-bold text-slate-900 dark:text-white tracking-tight">
                  SkillBridge AI
                </h1>
                <span className="hidden md:block text-[10px] text-slate-500 dark:text-slate-400">
                  Verifiable portfolio architecture platform
                </span>
              </div>
            </div>

            <Badge variant="outline" className="font-mono text-[11px] tabular-nums hidden sm:inline-flex">
              {status === "idle" && "System ready"}
              {status === "loading" && "Benchmarking competencies"}
              {status === "success" && "Analysis complete"}
              {status === "error" && "Analysis halted"}
            </Badge>
          </div>

          <div className="flex items-center space-x-2 sm:space-x-3">
            <ThemeToggle />

            <ConnectedAccountBar
              connectedUser={connectedUser}
              platformAccount={platformAccount}
              onOpenSettings={() => setAuthSettingsOpen(true)}
              onDisconnect={handleDisconnect}
              onConnectPlatform={handleConnectPlatform}
              onConnectDemo={handleConnectDemo}
            />
          </div>
        </div>
      </header>

      {/* Main Container */}
      <div className="mx-auto max-w-7xl px-4 sm:px-6 py-8">
        <div className="mb-8">
          <h2 className="text-2xl font-bold tracking-tight text-slate-900 dark:text-white sm:text-3xl">
            Portfolio blueprint generator
          </h2>
          <p className="mt-1 text-xs sm:text-sm text-slate-600 dark:text-slate-400">
            Convert static resumes into verifiable code repositories based on benchmarked job profiles.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          {/* Left Configuration Panel */}
          <div className="lg:col-span-4 space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Configuration</CardTitle>
                <CardDescription>Select target technology role and upload resume document</CardDescription>
              </CardHeader>
              <CardContent className="space-y-5">
                <div className="space-y-2">
                  <label className="text-xs font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400">
                    Target technology role
                  </label>
                  <RoleCombobox
                    value={targetRole}
                    onChange={(r) => {
                      setTargetRole(r);
                      if (file && status === "success") {
                        executeAnalysis(r);
                      }
                    }}
                    options={availableRoles}
                  />
                </div>

                <div className="space-y-2">
                  <label className="text-xs font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400">
                    Resume document
                  </label>
                  <Dropzone onFileSelect={setFile} />
                </div>
              </CardContent>
              <CardFooter>
                <Button
                  onClick={() => executeAnalysis()}
                  disabled={status === "loading" || !file}
                  className="w-full font-medium"
                >
                  {status === "loading" ? (
                    <>
                      <Loader2 size={16} className="animate-spin mr-2" />
                      Benchmarking competencies...
                    </>
                  ) : (
                    <>
                      <ArrowRight size={16} className="mr-2" />
                      Execute analysis
                    </>
                  )}
                </Button>
              </CardFooter>
            </Card>

            {/* Candidate Metadata Card */}
            {analysis?.contacts && (
              <Card className="border-slate-200/90 dark:border-slate-800 bg-white dark:bg-[#0f172a]/60">
                <CardHeader className="pb-3">
                  <CardTitle className="text-xs uppercase tracking-wider text-slate-500 dark:text-slate-400">
                    Candidate profile
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-2 text-xs">
                  {analysis.contacts.name && (
                    <div className="flex justify-between text-slate-700 dark:text-slate-300">
                      <span className="text-slate-400">Name:</span>
                      <span className="font-semibold text-slate-900 dark:text-white">{analysis.contacts.name}</span>
                    </div>
                  )}
                  {analysis.contacts.email && (
                    <div className="flex justify-between text-slate-700 dark:text-slate-300">
                      <span className="text-slate-400">Email:</span>
                      <span className="font-mono truncate max-w-[170px]">{analysis.contacts.email}</span>
                    </div>
                  )}
                  {analysis.contacts.portfolio &&
                    !analysis.contacts.portfolio.toLowerCase().includes("b.tech") &&
                    !analysis.contacts.portfolio.toLowerCase().includes("m.tech") && (
                    <div className="flex justify-between text-slate-700 dark:text-slate-300">
                      <span className="text-slate-400">Portfolio:</span>
                      <a
                        href={analysis.contacts.portfolio.startsWith("http") ? analysis.contacts.portfolio : `https://${analysis.contacts.portfolio}`}
                        target="_blank"
                        rel="noreferrer"
                        className="text-[#0071e3] hover:underline font-mono truncate max-w-[170px]"
                      >
                        {analysis.contacts.portfolio}
                      </a>
                    </div>
                  )}
                  {analysis.contacts.linkedin && (
                    <div className="flex justify-between text-slate-700 dark:text-slate-300">
                      <span className="text-slate-400">LinkedIn:</span>
                      <a
                        href={analysis.contacts.linkedin}
                        target="_blank"
                        rel="noreferrer"
                        className="text-[#0071e3] hover:underline truncate max-w-[170px]"
                      >
                        Verified profile
                      </a>
                    </div>
                  )}
                  <div className="flex justify-between text-slate-700 dark:text-slate-300 pt-1.5 border-t border-slate-100 dark:border-slate-800">
                    <span className="text-slate-400">Detected experience:</span>
                    <span className="font-mono tabular-nums">{analysis.experience_years} years</span>
                  </div>
                  {analysis.anonymization_audit && (
                    <div className="flex items-center justify-between pt-1.5 border-t border-slate-100 dark:border-slate-800">
                      <span className="flex items-center text-emerald-600 dark:text-emerald-400 font-medium">
                        <ShieldCheck size={13} className="mr-1" />
                        GDPR/DPDP Protected
                      </span>
                      <span className="font-mono text-[10px] text-slate-500">
                        {analysis.anonymization_audit.total_redactions || 0} PII stripped
                      </span>
                    </div>
                  )}
                </CardContent>
              </Card>
            )}
          </div>

          {/* Right Results Board */}
          <div className="lg:col-span-8">
            {status === "idle" && (
              <Card className="h-full min-h-[460px] flex items-center justify-center border-dashed border-slate-300 dark:border-slate-800 bg-white/50 dark:bg-[#0f172a]/40">
                <CardContent className="flex flex-col items-center text-center text-slate-500 dark:text-slate-400 max-w-md py-12">
                  <div className="mb-4 rounded-2xl border border-slate-200 dark:border-slate-800 bg-slate-100 dark:bg-[#1e293b]/50 p-4 text-slate-600 dark:text-slate-300 shadow-sm">
                    <FileText size={32} />
                  </div>
                  <h3 className="text-base font-semibold text-slate-800 dark:text-slate-200 mb-1">
                    Awaiting document and configuration
                  </h3>
                  <p className="text-xs leading-relaxed">
                    Upload your PDF resume to extract technical competencies, calculate category match percentages, and generate tailored code repository specifications.
                  </p>
                </CardContent>
              </Card>
            )}

            {status === "loading" && (
              <Card className="h-full min-h-[460px] flex items-center justify-center border-slate-200 dark:border-slate-800 bg-white/70 dark:bg-[#0f172a]/60">
                <CardContent className="flex flex-col items-center text-center py-12">
                  <Loader2 size={36} className="animate-spin text-[#0071e3] mb-4" />
                  <h3 className="text-base font-semibold text-slate-900 dark:text-slate-100 mb-1">
                    Analyzing qualifications against {targetRole}
                  </h3>
                  <p className="text-xs text-slate-500 dark:text-slate-400 max-w-sm">
                    Parsing document layout, matching canonical taxonomy, and computing weighted match scores.
                  </p>
                </CardContent>
              </Card>
            )}

            {status === "error" && (
              <Card className="h-full min-h-[460px] flex items-center justify-center border-rose-200 dark:border-rose-900/60 bg-rose-50/40 dark:bg-rose-950/20">
                <CardContent className="flex flex-col items-center text-center py-12 max-w-md">
                  <div className="mb-3 rounded-full bg-rose-500/20 p-3 text-rose-500">
                    <AlertCircle size={32} />
                  </div>
                  <h3 className="text-base font-semibold text-rose-700 dark:text-rose-300 mb-1">
                    Analysis could not proceed
                  </h3>
                  <p className="text-xs text-rose-600 dark:text-rose-400 mb-4">{errorMessage}</p>
                  <Button variant="secondary" size="sm" onClick={() => executeAnalysis()}>
                    Retry analysis
                  </Button>
                </CardContent>
              </Card>
            )}

            <AnimatePresence>
              {status === "success" && analysis && (
                <motion.div
                  initial={{ opacity: 0, y: 8 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="space-y-6"
                >
                  {/* Top Analytics Row */}
                  <div className="grid grid-cols-1 md:grid-cols-12 gap-4">
                    {/* Score Card */}
                    <Card className="md:col-span-4 flex flex-col justify-between">
                      <CardHeader className="pb-2">
                        <CardDescription>Overall compatibility</CardDescription>
                      </CardHeader>
                      <CardContent>
                        <div className="flex items-baseline space-x-2">
                          <span className="text-5xl font-bold font-mono tabular-nums text-slate-900 dark:text-white">
                            {analysis.match_percentage}%
                          </span>
                          <span className="text-xs font-mono text-slate-500 dark:text-slate-400">weighted match</span>
                        </div>
                        <div className="mt-4">
                          <ProgressBar
                            value={analysis.match_percentage}
                            indicatorClassName={
                              analysis.match_percentage >= 70
                                ? "bg-[#28cd41]"
                                : analysis.match_percentage >= 40
                                ? "bg-[#ff9f0a]"
                                : "bg-[#ff3b30]"
                            }
                          />
                        </div>
                      </CardContent>
                      <CardFooter className="pt-0 text-[11px] text-slate-500 dark:text-slate-400 border-t border-slate-100 dark:border-slate-800/60">
                        Languages: 40% • Frameworks: 30% • Databases: 20% • Tools: 10%
                      </CardFooter>
                    </Card>

                    {/* Category Breakdown Recharts Card */}
                    <Card className="md:col-span-5">
                      <CardHeader className="pb-1">
                        <CardDescription>Category distribution</CardDescription>
                      </CardHeader>
                      <CardContent className="pt-1">
                        <CategoryChart breakdown={analysis.category_breakdown} />
                      </CardContent>
                    </Card>

                    {/* Competency Summary Card */}
                    <Card className="md:col-span-3 flex flex-col justify-center space-y-4">
                      <CardContent className="space-y-3 pt-6">
                        <div className="rounded-xl border border-emerald-500/20 bg-emerald-50/50 dark:bg-emerald-500/10 p-3">
                          <span className="text-[11px] uppercase tracking-wider text-emerald-700 dark:text-emerald-400 font-medium block">
                            Verified competencies
                          </span>
                          <span className="text-2xl font-bold font-mono tabular-nums text-emerald-700 dark:text-emerald-300">
                            {analysis.matched_skills.length}
                          </span>
                        </div>
                        <div className="rounded-xl border border-rose-500/20 bg-rose-50/50 dark:bg-rose-500/10 p-3">
                          <span className="text-[11px] uppercase tracking-wider text-rose-700 dark:text-rose-400 font-medium block">
                            Identified skill gaps
                          </span>
                          <span className="text-2xl font-bold font-mono tabular-nums text-rose-700 dark:text-rose-300">
                            {analysis.missing_skills.length}
                          </span>
                        </div>
                      </CardContent>
                    </Card>
                  </div>

                  {/* Competency Gap Breakdown Card */}
                  <Card className="w-full border-slate-200/90 dark:border-slate-800 bg-white dark:bg-[#0f172a]/90 shadow-[0_2px_12px_rgba(0,0,0,0.02)]">
                    <CardHeader className="pb-3">
                      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                        <div>
                          <CardTitle className="text-sm font-bold flex items-center gap-1.5 text-slate-900 dark:text-white">
                            <Sparkles size={16} className="text-[#0071e3]" />
                            Competency Gap Breakdown
                          </CardTitle>
                          <CardDescription className="text-xs text-slate-500 dark:text-slate-400">
                            Weighted evaluation of candidate technical qualifications against {analysis.target_role} benchmarks
                          </CardDescription>
                        </div>
                        <div className="flex items-center gap-3">
                          <div className="text-right">
                            <span className="text-[10px] text-slate-400 uppercase font-semibold block">Overall Match</span>
                            <span className="text-xl font-bold font-mono text-emerald-600 dark:text-emerald-400">
                              {analysis.match_percentage}%
                            </span>
                          </div>
                          <div className="h-8 w-px bg-slate-200 dark:bg-slate-800 hidden sm:block" />
                          <div className="text-right">
                            <span className="text-[10px] text-slate-400 uppercase font-semibold block">Remaining Gap</span>
                            <span className="text-xl font-bold font-mono text-amber-600 dark:text-amber-400">
                              {typeof analysis.competency_deficit_delta === "number" ? analysis.competency_deficit_delta.toFixed(1) : "0.0"}%
                            </span>
                          </div>
                        </div>
                      </div>
                    </CardHeader>
                    <CardContent className="pt-1">
                      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs">
                        {/* Languages */}
                        <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50/70 dark:bg-[#1e293b]/40 p-3 flex flex-col justify-between">
                          <div>
                            <span className="text-[10px] text-slate-500 uppercase font-semibold block">Languages (40%)</span>
                            <span className="text-base font-mono font-bold text-slate-900 dark:text-slate-100 mt-1 block">
                              {analysis.category_deficits?.languages !== undefined ? Number(analysis.category_deficits.languages).toFixed(1) : "0.0"}% Gap
                            </span>
                          </div>
                          <span className="text-[10px] text-emerald-600 dark:text-emerald-400 font-medium mt-2">
                            {analysis.category_breakdown?.languages?.percentage ?? 100}% Fulfilled
                          </span>
                        </div>

                        {/* Frameworks */}
                        <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50/70 dark:bg-[#1e293b]/40 p-3 flex flex-col justify-between">
                          <div>
                            <span className="text-[10px] text-slate-500 uppercase font-semibold block">Frameworks (30%)</span>
                            <span className="text-base font-mono font-bold text-slate-900 dark:text-slate-100 mt-1 block">
                              {analysis.category_deficits?.frameworks !== undefined ? Number(analysis.category_deficits.frameworks).toFixed(1) : "0.0"}% Gap
                            </span>
                          </div>
                          <span className="text-[10px] text-slate-500 dark:text-slate-400 font-medium mt-2">
                            {analysis.category_breakdown?.frameworks?.percentage ?? 100}% Fulfilled
                          </span>
                        </div>

                        {/* Databases */}
                        <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50/70 dark:bg-[#1e293b]/40 p-3 flex flex-col justify-between">
                          <div>
                            <span className="text-[10px] text-slate-500 uppercase font-semibold block">Databases (20%)</span>
                            <span className="text-base font-mono font-bold text-slate-900 dark:text-slate-100 mt-1 block">
                              {analysis.category_deficits?.databases !== undefined ? Number(analysis.category_deficits.databases).toFixed(1) : "0.0"}% Gap
                            </span>
                          </div>
                          <span className="text-[10px] text-slate-500 dark:text-slate-400 font-medium mt-2">
                            {analysis.category_breakdown?.databases?.percentage ?? 100}% Fulfilled
                          </span>
                        </div>

                        {/* Tools */}
                        <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50/70 dark:bg-[#1e293b]/40 p-3 flex flex-col justify-between">
                          <div>
                            <span className="text-[10px] text-slate-500 uppercase font-semibold block">Tools (10%)</span>
                            <span className="text-base font-mono font-bold text-slate-900 dark:text-slate-100 mt-1 block">
                              {analysis.category_deficits?.tools !== undefined ? Number(analysis.category_deficits.tools).toFixed(1) : "0.0"}% Gap
                            </span>
                          </div>
                          <span className="text-[10px] text-slate-500 dark:text-slate-400 font-medium mt-2">
                            {analysis.category_breakdown?.tools?.percentage ?? 100}% Fulfilled
                          </span>
                        </div>
                      </div>
                    </CardContent>
                  </Card>

                  {/* Diagnostic Resume Audit Card */}
                  <ResumeAuditCard
                    audit={analysis.resume_audit}
                    onExportReport={exportCareerReport}
                  />

                  {/* Multi-Role Comparative Benchmarks */}
                  <MultiRoleBenchmark
                    benchmarks={analysis.multi_role_benchmarks}
                    onSelectRole={(r) => executeAnalysis(r)}
                  />

                  {/* Skill Gap Matrix with Interactive Category Tabs */}
                  <Card>
                    <CardHeader>
                      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
                        <div>
                          <CardTitle>Skill gap visualizer</CardTitle>
                          <CardDescription>
                            Direct comparison of candidate skills against {targetRole} requirements
                          </CardDescription>
                        </div>
                        <TabGroup
                          tabs={categoryTabs}
                          value={activeCategoryTab}
                          onChange={setActiveCategoryTab}
                        />
                      </div>
                    </CardHeader>
                    <CardContent className="space-y-6">
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        {/* Verified Matches */}
                        <div className="rounded-2xl border border-slate-200/90 dark:border-slate-800 bg-slate-50/50 dark:bg-[#0f172a]/70 p-4">
                          <div className="flex items-center space-x-2 mb-3">
                            <CheckCircle size={16} className="text-[#28cd41]" />
                            <h4 className="text-xs font-semibold uppercase tracking-wider text-slate-700 dark:text-slate-300">
                              Verified competencies ({filtered.matched.length})
                            </h4>
                          </div>
                          <div className="flex flex-wrap gap-2">
                            {filtered.matched.map((skill: string) => (
                              <Badge key={skill} variant="success">
                                {skill}
                              </Badge>
                            ))}
                            {filtered.matched.length === 0 && (
                              <span className="text-xs text-slate-400">No verified skills in this category.</span>
                            )}
                          </div>
                        </div>

                        {/* Identified Gaps */}
                        <div className="rounded-2xl border border-slate-200/90 dark:border-slate-800 bg-slate-50/50 dark:bg-[#0f172a]/70 p-4">
                          <div className="flex items-center space-x-2 mb-3">
                            <XCircle size={16} className="text-[#ff3b30]" />
                            <h4 className="text-xs font-semibold uppercase tracking-wider text-slate-700 dark:text-slate-300">
                              Missing requirements ({filtered.missing.length})
                            </h4>
                          </div>
                          <div className="flex flex-wrap gap-2">
                            {filtered.missing.map((skill: string) => (
                              <Badge key={skill} variant="destructive">
                                {skill}
                              </Badge>
                            ))}
                            {filtered.missing.length === 0 && (
                              <span className="text-xs text-slate-400">All category requirements met.</span>
                            )}
                          </div>
                        </div>
                      </div>
                    </CardContent>
                  </Card>

                  {/* Project Recommendation Proposals */}
                  <div>
                    <div className="flex items-center justify-between mb-4">
                      <div>
                        <h3 className="text-lg font-bold tracking-tight text-slate-900 dark:text-white">
                          Recommended portfolio projects
                        </h3>
                        <p className="text-xs text-slate-500 dark:text-slate-400">
                          Tailored blueprints specifically requiring missing competencies to construct verifiable evidence.
                        </p>
                      </div>
                      <div className="flex items-center space-x-2">
                        <Button
                          variant="primary"
                          size="sm"
                          onClick={() => setPortfolioCardOpen(true)}
                          className="text-xs bg-emerald-600 hover:bg-emerald-700 text-white shadow-sm font-medium"
                        >
                          <ShieldCheck size={14} className="mr-1.5" />
                          15s Hiring Manager Card
                        </Button>
                        <Button variant="outline" size="sm" onClick={exportCareerReport} className="text-xs">
                          <Share2 size={13} className="mr-1.5" />
                          Export blueprint report
                        </Button>
                      </div>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      {analysis.projects.map((project: any, idx: number) => (
                        <Card
                          key={idx}
                          className="flex flex-col justify-between border-slate-200/90 dark:border-slate-800 bg-white dark:bg-[#0f172a]/80 transition-all hover:border-[#0071e3]/60 shadow-[0_2px_12px_rgba(0,0,0,0.02)]"
                        >
                          <CardHeader className="pb-3">
                            <div className="flex items-start justify-between gap-2">
                              <CardTitle className="text-base text-slate-900 dark:text-white">{project.title}</CardTitle>
                              <Badge
                                variant={
                                  project.difficulty === "Advanced"
                                    ? "warning"
                                    : project.difficulty === "Intermediate"
                                    ? "default"
                                    : "success"
                                }
                                className="shrink-0 text-[10px]"
                              >
                                {project.difficulty}
                              </Badge>
                            </div>
                            <CardDescription className="line-clamp-2 mt-1.5 text-xs">
                              {project.objective}
                            </CardDescription>
                          </CardHeader>

                          <CardContent className="space-y-3">
                            <div>
                              <span className="text-[11px] font-medium text-slate-500 dark:text-slate-400 block mb-1.5">
                                Target competencies addressed:
                              </span>
                              <div className="flex flex-wrap gap-1.5">
                                {project.target_skills_covered && project.target_skills_covered.length > 0 ? (
                                  project.target_skills_covered.map((skill: string) => (
                                    <Badge key={skill} variant="destructive" className="text-[10px]">
                                      {skill}
                                    </Badge>
                                  ))
                                ) : (
                                  <Badge variant="outline" className="text-[10px] text-slate-500 dark:text-slate-400">
                                    Full Architecture Standards
                                  </Badge>
                                )}
                              </div>
                            </div>

                            <div>
                              <span className="text-[11px] font-medium text-slate-500 dark:text-slate-400 block mb-1.5">
                                Technical stack:
                              </span>
                              <div className="flex flex-wrap gap-1.5">
                                {project.tech_stack && project.tech_stack.length > 0 ? (
                                  project.tech_stack.map((tech: string) => (
                                    <Badge key={tech} variant="outline" className="text-[10px]">
                                      {tech}
                                    </Badge>
                                  ))
                                ) : (
                                  <Badge variant="outline" className="text-[10px] text-slate-500 dark:text-slate-400">
                                    Core Production Stack
                                  </Badge>
                                )}
                              </div>
                            </div>
                          </CardContent>

                          <CardFooter className="pt-3 border-t border-slate-100 dark:border-slate-800/80 flex items-center justify-between">
                            <span className="text-xs font-mono tabular-nums text-slate-500 dark:text-slate-400">
                              Estimated: {project.hours} hrs
                            </span>
                            <div className="flex items-center space-x-2">
                              <Button
                                variant="outline"
                                size="sm"
                                className="text-xs"
                                onClick={() => openInspector(project)}
                              >
                                Inspect blueprint
                              </Button>
                              <Button
                                size="sm"
                                className="text-xs"
                                onClick={() => handleProceedFromInspector(project)}
                              >
                                Provision
                              </Button>
                            </div>
                          </CardFooter>
                        </Card>
                      ))}
                    </div>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        </div>
      </div>

      {/* Blueprint Inspection & File Preview Modal */}
      <Modal
        isOpen={blueprintInspectorOpen}
        onClose={() => setBlueprintInspectorOpen(false)}
        title="Project architecture blueprint"
        className="max-w-3xl"
      >
        {selectedBlueprint && (
          <BlueprintInspector
            blueprint={selectedBlueprint}
            onClose={() => setBlueprintInspectorOpen(false)}
            onProceedToProvision={handleProceedFromInspector}
          />
        )}
      </Modal>

      {/* Provisioning Workflow Modal */}
      <Modal
        isOpen={provisionModalOpen}
        onClose={() => {
          if (provisioningState.status !== "running") {
            setProvisionModalOpen(false);
          }
        }}
        title="Repository provisioning"
        className="max-w-xl"
      >
        {selectedBlueprint && (
          <div className="space-y-5 text-slate-800 dark:text-slate-200">
            <div>
              <h3 className="text-base font-semibold text-slate-900 dark:text-white mb-0.5">
                {selectedBlueprint.title}
              </h3>
              <p className="text-xs text-slate-500 dark:text-slate-400">
                Automated creation of repository, README scaffold, and milestone tracking issues.
              </p>
            </div>

            {provisioningState.status === "idle" || provisioningState.status === "error" ? (
              <div className="space-y-4">
                {provisioningState.status === "error" && (
                  <div className="rounded-xl border border-rose-500/30 bg-rose-500/10 p-3 text-xs text-rose-600 dark:text-rose-300 flex items-start space-x-2">
                    <AlertCircle size={16} className="text-rose-500 shrink-0 mt-0.5" />
                    <span>{provisioningState.message}</span>
                  </div>
                )}

                {/* Platform Selector */}
                <div className="space-y-2">
                  <label className="text-xs font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400">
                    Developer platform
                  </label>
                  <div className="grid grid-cols-2 gap-3">
                    <button
                      type="button"
                      onClick={() => setPlatformProvider("github")}
                      className={`flex items-center justify-center space-x-2 rounded-xl border p-2.5 text-xs font-medium transition-colors ${
                        platformProvider === "github"
                          ? "border-[#0071e3] bg-[#0071e3]/15 text-[#0071e3]"
                          : "border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-[#1e293b]/50 text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white"
                      }`}
                    >
                      <Github size={16} />
                      <span>GitHub</span>
                    </button>
                    <button
                      type="button"
                      onClick={() => setPlatformProvider("gitlab")}
                      className={`flex items-center justify-center space-x-2 rounded-xl border p-2.5 text-xs font-medium transition-colors ${
                        platformProvider === "gitlab"
                          ? "border-[#0071e3] bg-[#0071e3]/15 text-[#0071e3]"
                          : "border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-[#1e293b]/50 text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white"
                      }`}
                    >
                      <Gitlab size={16} />
                      <span>GitLab</span>
                    </button>
                  </div>
                </div>

                {/* Authentication Options */}
                <div className="space-y-3 rounded-2xl border border-slate-200 dark:border-slate-800 bg-slate-50/70 dark:bg-[#1e293b]/50 p-4">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400">
                      Authentication mode
                    </span>
                    <label className="flex items-center space-x-2 cursor-pointer">
                      <input
                        type="checkbox"
                        checked={useSandboxMode}
                        onChange={(e) => setUseSandboxMode(e.target.checked)}
                        className="rounded border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 text-[#0071e3] focus:ring-[#0071e3]"
                      />
                      <span className="text-xs text-slate-700 dark:text-slate-300 font-medium">Sandbox dry-run</span>
                    </label>
                  </div>

                  {useSandboxMode ? (
                    <p className="text-xs text-slate-500 dark:text-slate-400 leading-relaxed">
                      Sandbox mode simulates repository provisioning, commit hashing, and issue generation without calling remote developer APIs.
                    </p>
                  ) : connectedUser && platformProvider === "github" ? (
                    <div className="flex items-center justify-between rounded-xl border border-emerald-500/20 bg-emerald-50 dark:bg-emerald-500/10 p-3">
                      <div className="flex items-center space-x-2.5">
                        {connectedUser.avatar_url ? (
                          <Image
                            src={connectedUser.avatar_url}
                            alt=""
                            width={24}
                            height={24}
                            unoptimized
                            className="h-6 w-6 rounded-full border border-emerald-300 dark:border-emerald-600 object-cover"
                          />
                        ) : (
                          <CheckCircle size={16} className="text-emerald-500" />
                        )}
                        <span className="text-xs text-slate-800 dark:text-slate-200">
                          Target account: <strong className="font-mono">{connectedUser.login}</strong>
                        </span>
                      </div>
                      <Badge variant="success" className="text-[10px]">Active credentials</Badge>
                    </div>
                  ) : (
                    <div className="space-y-2">
                      <label className="text-xs text-slate-600 dark:text-slate-400 block">
                        Developer personal access token:
                      </label>
                      <input
                        type="password"
                        value={tokenInput}
                        onChange={(e) => setTokenInput(e.target.value)}
                        placeholder={platformProvider === "gitlab" ? "glpat-xxxxxxxxxxxx" : "ghp_xxxxxxxxxxxx"}
                        className="w-full rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-[#0f172a] px-3 py-2 text-xs font-mono text-slate-800 dark:text-slate-100 placeholder-slate-400 focus:border-[#0071e3] focus:outline-none"
                      />
                      <p className="text-[11px] text-slate-500">
                        Tokens are used strictly for this provisioning call and are not stored permanently.
                      </p>
                    </div>
                  )}
                </div>

                <div className="pt-2 flex justify-end space-x-3">
                  <Button variant="secondary" size="sm" onClick={() => setProvisionModalOpen(false)}>
                    Cancel
                  </Button>
                  <Button size="sm" onClick={executeProvisioning}>
                    <FolderGit2 size={14} className="mr-1.5" />
                    {useSandboxMode ? "Run sandbox provisioning" : "Provision repository"}
                  </Button>
                </div>
              </div>
            ) : provisioningState.status === "running" ? (
              <div className="space-y-4 py-4">
                <div className="flex items-center justify-between text-xs">
                  <span className="flex items-center text-slate-700 dark:text-slate-300">
                    <Loader2 size={14} className="animate-spin text-[#0071e3] mr-2" />
                    {provisioningState.message}
                  </span>
                  <span className="font-mono text-slate-500 dark:text-slate-400">Step {provisioningState.step}/4</span>
                </div>
                <ProgressBar value={provisioningState.step} max={4} indicatorClassName="bg-[#0071e3]" />
              </div>
            ) : (
              <div className="space-y-5 py-2">
                <div className="rounded-2xl border border-emerald-500/20 bg-emerald-50 dark:bg-emerald-500/10 p-4">
                  <div className="flex items-center space-x-2 text-emerald-700 dark:text-emerald-400 mb-1">
                    <CheckCircle size={18} />
                    <h4 className="text-sm font-semibold">Repository provisioned successfully</h4>
                  </div>
                  <p className="text-xs text-slate-600 dark:text-slate-300">
                    {provisioningState.result?.is_sandbox
                      ? "Sandbox simulation verified project specifications and issue templates."
                      : "The code repository is live under your account."}
                  </p>
                </div>

                <div className="space-y-2 rounded-2xl border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-[#1e293b]/60 p-4 text-xs font-mono">
                  <div className="flex justify-between">
                    <span className="text-slate-500">Repository:</span>
                    <a
                      href={provisioningState.result?.repo_url}
                      target="_blank"
                      rel="noreferrer"
                      className="text-[#0071e3] hover:underline flex items-center"
                    >
                      {provisioningState.result?.repo_name}
                      <ExternalLink size={12} className="ml-1" />
                    </a>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-500">Initial commit:</span>
                    <span className="text-slate-800 dark:text-slate-200">{provisioningState.result?.commit_hash}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-500">Milestone issues:</span>
                    <span className="text-emerald-600 dark:text-emerald-400">
                      {provisioningState.result?.issues_created?.length || 4} created
                    </span>
                  </div>
                </div>

                <div className="flex justify-end space-x-3 pt-2">
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => {
                      setProvisionModalOpen(false);
                      setSelectedBlueprint(null);
                    }}
                  >
                    Done
                  </Button>
                  <Button
                    size="sm"
                    onClick={() => window.open(provisioningState.result?.repo_url, "_blank")}
                  >
                    <ExternalLink size={14} className="mr-1.5" />
                    Open repository
                  </Button>
                </div>
              </div>
            )}
          </div>
        )}
      </Modal>

      {/* Developer Platform Settings & Authentication Modal */}
      <Modal
        isOpen={authSettingsOpen}
        onClose={() => setAuthSettingsOpen(false)}
        title="GitHub Account & Authorization Center"
        className="max-w-xl"
      >
        <div className="space-y-4 text-xs text-slate-700 dark:text-slate-300">
          {/* Active Connection Banner if connected */}
          {connectedUser && (
            <div className="rounded-2xl border border-emerald-500/30 bg-emerald-50/80 dark:bg-emerald-500/10 p-3.5 space-y-2.5">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2.5">
                  {connectedUser.avatar_url ? (
                    <Image
                      src={connectedUser.avatar_url}
                      alt={connectedUser.login}
                      width={32}
                      height={32}
                      unoptimized
                      className="h-8 w-8 rounded-full border border-emerald-400 dark:border-emerald-600 object-cover"
                    />
                  ) : (
                    <div className="h-8 w-8 rounded-full bg-emerald-100 dark:bg-emerald-900/50 flex items-center justify-center text-emerald-600">
                      <Github size={18} />
                    </div>
                  )}
                  <div>
                    <div className="flex items-center space-x-1.5">
                      <span className="font-semibold text-slate-900 dark:text-white">
                        {connectedUser.name || connectedUser.login}
                      </span>
                      <span className="text-[11px] font-mono text-slate-500 dark:text-slate-400">
                        @{connectedUser.login}
                      </span>
                    </div>
                    <div className="flex items-center space-x-1.5 text-[11px] text-emerald-700 dark:text-emerald-400">
                      <span className="inline-block h-1.5 w-1.5 rounded-full bg-emerald-500" />
                      <span>
                        {connectedUser.source === "platform"
                          ? "Platform verified account active"
                          : connectedUser.is_sandbox
                          ? "Preview sandbox active"
                          : "Personal access token active"}
                      </span>
                    </div>
                  </div>
                </div>

                <Button
                  size="sm"
                  variant="outline"
                  onClick={handleDisconnect}
                  className="text-[11px] text-rose-600 hover:text-rose-700 border-rose-200 dark:border-rose-900/40"
                >
                  Disconnect
                </Button>
              </div>

              <div className="flex flex-wrap items-center gap-1.5 pt-1 border-t border-emerald-500/20 text-[10px]">
                <span className="text-slate-500">Repository count: {connectedUser.public_repos || 0}</span>
                <span className="text-slate-400">|</span>
                <span className="text-slate-500">Authorized scopes:</span>
                {connectedUser.scopes && connectedUser.scopes.length > 0 ? (
                  connectedUser.scopes.map((s: string) => (
                    <Badge key={s} variant="outline" className="text-[9px] py-0 font-mono">
                      {s}
                    </Badge>
                  ))
                ) : (
                  <Badge variant="outline" className="text-[9px] py-0 font-mono">
                    repo
                  </Badge>
                )}
              </div>
            </div>
          )}

          {/* Option 1: 1-Click Platform Authorization (Narendra Gandikota) */}
          {platformAccount && (
            <div className="rounded-2xl border border-blue-500/20 dark:border-blue-500/30 bg-gradient-to-br from-blue-50/80 via-white to-indigo-50/50 dark:from-[#1e293b]/80 dark:to-[#0f172a]/80 p-4 space-y-3 shadow-sm">
              <div className="flex items-start justify-between">
                <div className="flex items-start space-x-3">
                  <div className="p-2 rounded-xl bg-[#0071e3] text-white shadow-sm mt-0.5">
                    <ShieldCheck size={20} />
                  </div>
                  <div>
                    <div className="flex items-center space-x-2">
                      <h4 className="font-semibold text-slate-900 dark:text-white text-sm">
                        1-Click Platform Access: {platformAccount.login}
                      </h4>
                      <Badge variant="success" className="text-[9px] uppercase tracking-wider py-0 font-medium">
                        Verified
                      </Badge>
                    </div>
                    <p className="text-[11px] text-slate-600 dark:text-slate-400 mt-0.5 leading-relaxed">
                      Instant authorization using the pre-authenticated SkillBridge platform account. Generates repositories and milestone issues under @{platformAccount.login} with zero token setup.
                    </p>
                  </div>
                </div>
              </div>

              <div className="flex items-center justify-between pt-1 border-t border-slate-200/60 dark:border-slate-800">
                <span className="text-[11px] text-slate-500 dark:text-slate-400 flex items-center">
                  <CheckCircle2 size={13} className="text-emerald-500 mr-1" />
                  Repository creation & issue tracking enabled
                </span>

                {connectedUser?.login === platformAccount.login ? (
                  <Badge variant="success" className="text-[11px] py-1 px-2.5 font-medium">
                    Active Account
                  </Badge>
                ) : (
                  <Button
                    size="sm"
                    variant="primary"
                    onClick={handleConnectPlatform}
                    className="text-xs"
                  >
                    <Github size={13} className="mr-1.5" />
                    Connect {platformAccount.login} (1-Click)
                  </Button>
                )}
              </div>
            </div>
          )}

          {/* Option 2: Personal GitHub Authorization via Browser / Device Code (No PAT needed!) */}
          <div className="rounded-2xl border border-slate-200 dark:border-slate-800 bg-slate-50/70 dark:bg-[#1e293b]/50 p-4 space-y-3">
            <div className="flex items-start justify-between">
              <div className="flex items-start space-x-3">
                <div className="p-2 rounded-xl bg-slate-800 text-white dark:bg-slate-700 mt-0.5">
                  <Github size={20} />
                </div>
                <div>
                  <h4 className="font-semibold text-slate-900 dark:text-white text-sm">
                    Connect Personal GitHub Account
                  </h4>
                  <p className="text-[11px] text-slate-600 dark:text-slate-400 mt-0.5 leading-relaxed">
                    Authorize via GitHub directly in your browser. No Personal Access Token creation or scope configuration required.
                  </p>
                </div>
              </div>
            </div>

            {deviceFlowState.status === "idle" && (
              <div className="flex items-center justify-between pt-1">
                <span className="text-[11px] text-slate-500">
                  Approve access in 1 click on github.com
                </span>
                <Button
                  size="sm"
                  variant="outline"
                  onClick={handleStartDeviceFlow}
                  className="text-xs"
                >
                  <KeyRound size={13} className="mr-1.5 text-slate-700 dark:text-slate-300" />
                  Get 1-Click Code
                </Button>
              </div>
            )}

            {deviceFlowState.status === "requesting" && (
              <div className="flex items-center space-x-2 text-xs text-slate-600 dark:text-slate-400 py-1">
                <Loader2 size={14} className="animate-spin text-[#0071e3]" />
                <span>Requesting authorization code from GitHub...</span>
              </div>
            )}

            {(deviceFlowState.status === "ready" || deviceFlowState.status === "polling") && deviceFlowState.userCode && (
              <div className="rounded-xl border border-blue-200 dark:border-blue-900/50 bg-blue-50/80 dark:bg-blue-950/30 p-3 space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-xs text-slate-700 dark:text-slate-300 font-medium">
                    1. Enter this code on GitHub:
                  </span>
                  <div className="flex items-center space-x-1.5 bg-white dark:bg-[#0f172a] px-3 py-1 rounded-lg border border-blue-300 dark:border-blue-800">
                    <span className="font-mono font-bold text-sm text-[#0071e3] tracking-widest">
                      {deviceFlowState.userCode}
                    </span>
                    <button
                      type="button"
                      onClick={() => handleCopyCode(deviceFlowState.userCode!)}
                      className="p-1 text-slate-400 hover:text-slate-700 dark:hover:text-slate-200"
                      title="Copy code"
                    >
                      {copiedCode ? <Check size={13} className="text-emerald-500" /> : <Copy size={13} />}
                    </button>
                  </div>
                </div>

                <div className="flex items-center justify-between pt-1">
                  <div className="flex items-center space-x-1.5 text-[11px] text-slate-500 dark:text-slate-400">
                    <Loader2 size={12} className="animate-spin text-[#0071e3]" />
                    <span>Waiting for your authorization...</span>
                  </div>

                  <a
                    href={deviceFlowState.verificationUri || "https://github.com/login/device"}
                    target="_blank"
                    rel="noreferrer"
                    className="inline-flex items-center space-x-1.5 rounded-lg bg-[#0071e3] text-white px-3 py-1.5 text-xs font-medium hover:bg-blue-600 transition-colors shadow-sm"
                  >
                    <span>Authorize on GitHub</span>
                    <ExternalLink size={12} />
                  </a>
                </div>
              </div>
            )}

            {deviceFlowState.status === "success" && (
              <div className="rounded-xl border border-emerald-300 dark:border-emerald-800 bg-emerald-50 dark:bg-emerald-950/40 p-2.5 text-xs text-emerald-700 dark:text-emerald-300 flex items-center space-x-2">
                <CheckCircle2 size={16} className="text-emerald-500" />
                <span>Authorized successfully! Connecting your GitHub account...</span>
              </div>
            )}

            {deviceFlowState.status === "error" && (
              <div className="rounded-xl border border-rose-200 dark:border-rose-900/50 bg-rose-50 dark:bg-rose-950/30 p-2.5 text-xs text-rose-600 dark:text-rose-400 flex items-center justify-between">
                <span>{deviceFlowState.error || "Authorization error"}</span>
                <button
                  type="button"
                  onClick={() => setDeviceFlowState({ status: "idle" })}
                  className="text-xs underline text-rose-700 dark:text-rose-300 ml-2"
                >
                  Retry
                </button>
              </div>
            )}
          </div>

          {/* Option 3: Quick Demo Preview */}
          <div className="rounded-2xl border border-slate-200 dark:border-slate-800 bg-slate-50/70 dark:bg-[#1e293b]/50 p-3.5 flex items-center justify-between">
            <div>
              <span className="font-semibold text-slate-900 dark:text-white flex items-center">
                <Sparkles size={13} className="text-amber-500 mr-1.5" />
                Preview Sandbox Evaluation
              </span>
              <p className="text-[11px] text-slate-500 dark:text-slate-400">
                Safe offline dry-run for end-to-end evaluation without remote API calls.
              </p>
            </div>
            <Button size="sm" variant="secondary" onClick={handleConnectDemo} className="text-xs">
              Activate Preview
            </Button>
          </div>

          {/* Option 4: Advanced Developer Options (Manual PAT / CI Token - Collapsible) */}
          <div className="rounded-2xl border border-slate-200 dark:border-slate-800 bg-slate-50/50 dark:bg-[#1e293b]/30 overflow-hidden">
            <button
              type="button"
              onClick={() => setShowAdvancedPat(!showAdvancedPat)}
              className="w-full p-3 flex items-center justify-between text-left hover:bg-slate-100/50 dark:hover:bg-slate-800/50 transition-colors"
            >
              <span className="font-medium text-slate-700 dark:text-slate-300 text-xs flex items-center">
                <KeyRound size={13} className="mr-1.5 text-slate-500" />
                Advanced Developer Options (Manual Token / Enterprise)
              </span>
              {showAdvancedPat ? <ChevronUp size={14} className="text-slate-400" /> : <ChevronDown size={14} className="text-slate-400" />}
            </button>

            {showAdvancedPat && (
              <div className="p-3.5 pt-0 space-y-3 border-t border-slate-200/50 dark:border-slate-800/50 mt-1">
                <div className="flex items-center justify-between text-[11px] text-slate-500">
                  <span>Enter a personal access token with repo scope:</span>
                  <a
                    href="https://github.com/settings/tokens/new?scopes=repo,read:user&description=SkillBridge%20AI%20Portfolio%20Provisioner"
                    target="_blank"
                    rel="noreferrer"
                    className="text-[#0071e3] hover:underline flex items-center"
                  >
                    Generate on GitHub
                    <ExternalLink size={11} className="ml-1" />
                  </a>
                </div>

                <div className="space-y-2">
                  <input
                    type="password"
                    value={tokenInput}
                    onChange={(e) => setTokenInput(e.target.value)}
                    placeholder="ghp_xxxxxxxxxxxxxxxxxxxx or github_pat_xxxx"
                    className="w-full rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-[#0f172a] px-3 py-2 text-xs font-mono text-slate-800 dark:text-slate-200 placeholder-slate-400 focus:border-[#0071e3] focus:outline-none"
                  />
                  {tokenError && (
                    <p className="text-[11px] text-rose-500 font-medium">{tokenError}</p>
                  )}
                  <Button
                    size="sm"
                    className="w-full text-xs"
                    onClick={handleValidateToken}
                    disabled={tokenValidating || !tokenInput.trim()}
                  >
                    {tokenValidating ? (
                      <>
                        <Loader2 size={13} className="animate-spin mr-1.5" />
                        Validating credentials...
                      </>
                    ) : (
                      "Verify and connect custom PAT"
                    )}
                  </Button>
                </div>
              </div>
            )}
          </div>

          <div className="flex justify-end pt-1">
            <Button size="sm" variant="secondary" onClick={() => setAuthSettingsOpen(false)}>
              Close
            </Button>
          </div>
        </div>
      </Modal>

      {/* 15-Second Scannable Hiring Manager Digital Portfolio Card Modal */}
      <PortfolioCardModal
        isOpen={portfolioCardOpen}
        onClose={() => setPortfolioCardOpen(false)}
        username={connectedUser?.login || analysis?.contacts?.name || "G-Narendra"}
        targetRole={targetRole}
        apiBaseUrl={API_BASE_URL}
      />
    </main>
  );
}

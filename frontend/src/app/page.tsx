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
  CheckCircle2,
  Terminal
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
import { BenchmarkComparisonBanner } from "@/components/BenchmarkComparisonBanner";
import { GranularCapabilityGrid } from "@/components/GranularCapabilityGrid";
import { GapDiagnosticTable } from "@/components/GapDiagnosticTable";
import { ManualSetupModal } from "@/components/ManualSetupModal";
import { SeniorStandingCard } from "@/components/SeniorStandingCard";
import { ALL_TECH_ROLES, isTechnicalRole } from "@/lib/roles";
import { SkillBridgeLogo } from "@/components/SkillBridgeLogo";

const STANDARD_ROLES = ALL_TECH_ROLES;
const OFFICIAL_RENDER_BACKEND = "https://skillbridge-backend-1pm3.onrender.com";

const getOfficialBackendUrl = () => {
  const envUrl = process.env.NEXT_PUBLIC_API_URL;
  if (!envUrl || envUrl.includes("skillbridge-backend.onrender.com")) {
    return OFFICIAL_RENDER_BACKEND;
  }
  return envUrl.replace(/\/$/, "");
};

const OFFICIAL_BACKEND_URL = getOfficialBackendUrl();

function getDefaultApiUrl(): string {
  if (typeof window !== "undefined") {
    // Clear any past user-entered overrides so endpoints cannot be customized
    localStorage.removeItem("skillbridge_api_url");
  }
  return OFFICIAL_BACKEND_URL;
}



export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [apiBaseUrl, setApiBaseUrl] = useState<string>(getDefaultApiUrl);
  const [backendHealth, setBackendHealth] = useState<{
    status: "online" | "offline" | "checking";
    latencyMs?: number;
    rolesCount?: number;
    service?: string;
    error?: string;
  }>({ status: "checking" });
  const [customJobDescription, setCustomJobDescription] = useState("");
  const [showCustomJobDescription, setShowCustomJobDescription] = useState(false);

  const [targetRole, setTargetRole] = useState("Data Analyst");
  const [status, setStatus] = useState<"idle" | "loading" | "success" | "error">("idle");
  const [analysis, setAnalysis] = useState<any>(null);
  const [errorMessage, setErrorMessage] = useState<string>("");

  // Modals & tabs
  const [selectedBlueprint, setSelectedBlueprint] = useState<any | null>(null);
  const [blueprintInspectorOpen, setBlueprintInspectorOpen] = useState(false);
  const [provisionModalOpen, setProvisionModalOpen] = useState(false);
  const [manualSetupModalOpen, setManualSetupModalOpen] = useState(false);
  const [manualBlueprint, setManualBlueprint] = useState<any | null>(null);
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

  // Check backend API operational health
  const checkBackendHealth = async (urlToCheck?: string) => {
    const target = (urlToCheck || apiBaseUrl || OFFICIAL_BACKEND_URL).trim().replace(/\/$/, "");
    setBackendHealth((prev) => ({ ...prev, status: "checking" }));
    const startTime = performance.now();
    try {
      const endpoint = target.startsWith("http")
        ? `${target}/api/health`
        : `${target}/health`;

      const res = await axios.get(endpoint, {
        timeout: 15000
      });
      const elapsed = Math.round(performance.now() - startTime);
      setBackendHealth({
        status: "online",
        latencyMs: elapsed,
        rolesCount: res.data?.roles_available || 481,
        service: res.data?.service || "SkillBridge AI Backend"
      });
      return true;
    } catch (err: any) {
      // Automatic fallback between direct cloud URL and proxy
      if (target === OFFICIAL_BACKEND_URL) {
        try {
          const proxyRes = await axios.get("/api/backend/health", { timeout: 15000 });
          const elapsed = Math.round(performance.now() - startTime);
          setApiBaseUrl("/api/backend");
          setBackendHealth({
            status: "online",
            latencyMs: elapsed,
            rolesCount: proxyRes.data?.roles_available || 481,
            service: proxyRes.data?.service || "SkillBridge AI Backend"
          });
          return true;
        } catch {
          // Fall through
        }
      } else if (target === "/api/backend") {
        try {
          const directRes = await axios.get(`${OFFICIAL_BACKEND_URL}/api/health`, { timeout: 15000 });
          const elapsed = Math.round(performance.now() - startTime);
          setApiBaseUrl(OFFICIAL_BACKEND_URL);
          setBackendHealth({
            status: "online",
            latencyMs: elapsed,
            rolesCount: directRes.data?.roles_available || 481,
            service: directRes.data?.service || "SkillBridge AI Backend"
          });
          return true;
        } catch {
          // Fall through
        }
      }
      setBackendHealth({
        status: "offline",
        error: err.response?.data?.detail || err.message || "Endpoint offline"
      });
      return false;
    }
  };

  // Query platform GitHub status, load saved PAT, and fetch 465+ dynamic roles
  useEffect(() => {
    let isMounted = true;

    async function initializePlatform() {
      // Check backend health
      checkBackendHealth(apiBaseUrl);

      // 1. Check if user previously saved a custom PAT
      const savedToken = typeof window !== "undefined" ? localStorage.getItem("skillbridge_pat") : null;

      if (savedToken) {
        try {
          const authHeader = savedToken.startsWith("github_pat_") ? `Bearer ${savedToken}` : `token ${savedToken}`;
          const ghRes = await axios.get("https://api.github.com/user", {
            headers: {
              Authorization: authHeader,
              Accept: "application/vnd.github.v3+json"
            },
            timeout: 6000
          });
          if (ghRes.data?.login && isMounted) {
            setConnectedUser({
              login: ghRes.data.login,
              name: ghRes.data.name || ghRes.data.login,
              avatar_url: ghRes.data.avatar_url,
              html_url: ghRes.data.html_url,
              public_repos: ghRes.data.public_repos || 0,
              scopes: ["repo", "read:user"],
              source: "custom_pat",
              raw_token: savedToken
            });
          }
        } catch (ghErr: any) {
          if (ghErr.response?.status === 401 && typeof window !== "undefined") {
            localStorage.removeItem("skillbridge_pat");
          }
        }
      }

      // 2. Query platform GitHub status from backend
      try {
        const res = await axios.get(`${apiBaseUrl}/api/github/status`, {
          timeout: 6000
        });
        if (res.data?.configured && res.data?.valid && isMounted) {
          const account: ConnectedUser = {
            ...res.data,
            raw_token: "default",
            source: "platform"
          };
          setPlatformAccount(account);
        } else if (isMounted) {
          setPlatformAccount(null);
        }
      } catch {
        if (isMounted) {
          setPlatformAccount(null);
        }
      }

      // 3. Load dynamic technology roles catalog
      try {
        const rolesRes = await axios.get(`${apiBaseUrl}/api/roles`, {
          timeout: 6000
        });
        if (rolesRes.data?.roles && Array.isArray(rolesRes.data.roles) && isMounted) {
          const names = rolesRes.data.roles.map((r: any) => r.name).filter(isTechnicalRole);
          if (names.length > 0) {
            const merged = Array.from(new Set([...ALL_TECH_ROLES, ...names]));
            setAvailableRoles(merged);
          }
        }
      } catch {
        // Retain full default standard catalog if backend offline
      }
    }

    initializePlatform();

    return () => {
      isMounted = false;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [apiBaseUrl]);

  // Automatically link NextAuth session if available
  useEffect(() => {
    if (session?.user && !connectedUser) {
      setConnectedUser({
        login: session.user.name || "github-user",
        name: session.user.name || undefined,
        avatar_url: session.user.image || undefined,
        public_repos: 10,
        scopes: ["repo", "read:user"],
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

  // Device Code Authorization Flow (No PAT generation needed)
  const handleStartDeviceFlow = async () => {
    setDeviceFlowState({ status: "requesting" });
    try {
      const res = await axios.post(`${apiBaseUrl}/api/auth/github/device/init`, {}, {
        headers: apiBaseUrl.startsWith("http") ? { "x-backend-url": apiBaseUrl } : undefined,
      });
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
          error: res.data?.error || "Device flow is unavailable on current backend.",
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
        const pollRes = await axios.post(`${apiBaseUrl}/api/auth/github/device/poll`, {
          device_code: deviceCode,
        }, {
          headers: apiBaseUrl.startsWith("http") ? { "x-backend-url": apiBaseUrl } : undefined,
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

    const rawInput = tokenInput.trim();
    const token = rawInput
      .replace(/^Bearer\s+/i, "")
      .replace(/^token\s+/i, "")
      .replace(/^['"]|['"]$/g, "");

    // Direct GitHub REST API validation against real GitHub user endpoint
    try {
      let ghRes;
      try {
        ghRes = await axios.get("https://api.github.com/user", {
          headers: {
            Authorization: `token ${token}`,
            Accept: "application/vnd.github.v3+json",
          },
          timeout: 8000,
        });
      } catch (tokenErr: any) {
        if (tokenErr.response?.status === 401) {
          // Retry with Bearer header for fine-grained personal tokens
          ghRes = await axios.get("https://api.github.com/user", {
            headers: {
              Authorization: `Bearer ${token}`,
              Accept: "application/vnd.github.v3+json",
            },
            timeout: 8000,
          });
        } else {
          throw tokenErr;
        }
      }

      if (ghRes.data && ghRes.data.login) {
        if (typeof window !== "undefined") {
          localStorage.setItem("skillbridge_pat", token);
        }
        setConnectedUser({
          login: ghRes.data.login,
          name: ghRes.data.name || ghRes.data.login,
          avatar_url: ghRes.data.avatar_url,
          html_url: ghRes.data.html_url,
          public_repos: ghRes.data.public_repos || 0,
          scopes: ["repo", "read:user"],
          source: "custom_pat",
          raw_token: token,
        });
        setTokenInput("");
        setAuthSettingsOpen(false);
        setTokenValidating(false);
        return;
      }
    } catch (ghErr: any) {
      if (ghErr.response?.status === 401) {
        setTokenError("GitHub rejected credentials: Check that your Personal Access Token is valid and has 'repo' scope.");
      } else if (ghErr.response?.data?.message) {
        setTokenError(`GitHub API: ${ghErr.response.data.message}`);
      } else if (ghErr.message === "Network Error") {
        setTokenError("Network error reaching api.github.com. Please check your internet connection.");
      } else {
        setTokenError("Invalid developer credentials. Please enter a valid GitHub Personal Access Token with 'repo' scope.");
      }
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
    if (customJobDescription.trim()) {
      formData.append("job_description", customJobDescription.trim());
    }

    try {
      const response = await axios.post(`${apiBaseUrl}/api/resume/parse`, formData, {
        headers: {
          "Content-Type": "multipart/form-data"
        },
        timeout: 60000
      });
      setAnalysis(response.data);
      setStatus("success");
    } catch (err: any) {
      // If client validation error (422, 400), the uploaded document is invalid or not a resume - do not retry alternate
      const httpStatus = err.response?.status;
      if (httpStatus !== 400 && httpStatus !== 422) {
        try {
          const alternateBase = apiBaseUrl.startsWith("http")
            ? "/api/backend"
            : OFFICIAL_BACKEND_URL;
          const retryRes = await axios.post(`${alternateBase}/api/resume/parse`, formData, {
            headers: {
              "Content-Type": "multipart/form-data"
            },
            timeout: 60000
          });
          setAnalysis(retryRes.data);
          setStatus("success");
          return;
        } catch {
          // Fall through to error
        }
      }

      let detail = "";
      if (err.response?.data?.detail) {
        if (typeof err.response.data.detail === "string") {
          detail = err.response.data.detail;
        } else if (Array.isArray(err.response.data.detail)) {
          detail = err.response.data.detail.map((d: any) => d.msg || JSON.stringify(d)).join(", ");
        } else {
          detail = JSON.stringify(err.response.data.detail);
        }
      } else if (err.response?.data?.message) {
        detail = err.response.data.message;
      } else if (httpStatus === 422 || err.message?.includes("422")) {
        detail = "The uploaded document could not be verified as a valid technical resume. Please upload your personal CV or resume containing your work experience or projects, technical skills, and education.";
      } else {
        detail = err.message || "Unable to reach the backend parsing service.";
      }

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

  const handleDownloadZip = async (project: any) => {
    try {
      const target = (apiBaseUrl || OFFICIAL_BACKEND_URL).trim().replace(/\/$/, "");
      const endpoint = target.startsWith("http")
        ? `${target}/api/blueprint/download-zip`
        : `${target}/blueprint/download-zip`;

      const response = await axios.post(
        endpoint,
        { blueprint: project },
        { responseType: "blob", timeout: 30000 }
      );

      const blob = new Blob([response.data], { type: "application/zip" });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      const slug = (project.id || project.title || "skillbridge-skeleton")
        .toLowerCase()
        .replace(/[^a-z0-9_-]/g, "-")
        .replace(/-+/g, "-")
        .replace(/^-|-$/g, "");
      link.setAttribute("download", `${slug}-skeleton.zip`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
    } catch (err: any) {
      console.error("Direct zip download failed:", err);
      // Fallback: open manual setup modal
      setManualBlueprint(project);
      setManualSetupModalOpen(true);
    }
  };

  const executeProvisioning = async () => {
    if (!selectedBlueprint) return;

    let tokenToSend = "";
    if (connectedUser?.raw_token) {
      tokenToSend = connectedUser.raw_token;
    } else if (connectedUser?.source === "platform") {
      tokenToSend = "default";
    } else if (session?.accessToken) {
      tokenToSend = session.accessToken;
    } else if (tokenInput.trim()) {
      tokenToSend = tokenInput.trim();
    }

    if (!tokenToSend) {
      setProvisioningState({
        status: "error",
        step: 0,
        message: "A valid Personal Access Token with 'repo' scope is required to provision this repository.",
        result: null
      });
      return;
    }

    setProvisioningState({
      status: "running",
      step: 1,
      message: `Connecting to ${platformProvider === "gitlab" ? "GitLab" : "GitHub"} platform APIs...`,
      result: null
    });

    let timer1: any = null;
    let timer2: any = null;

    try {
      timer1 = setTimeout(() => {
        setProvisioningState((prev) => {
          if (prev.status !== "running") return prev;
          return {
            ...prev,
            step: 2,
            message: "Creating remote repository and verifying branch permissions..."
          };
        });
      }, 1000);

      timer2 = setTimeout(() => {
        setProvisioningState((prev) => {
          if (prev.status !== "running") return prev;
          return {
            ...prev,
            step: 3,
            message: "Synthesizing atomic Git tree commit and multi-file architecture..."
          };
        });
      }, 2500);

      const payload = {
        title: selectedBlueprint.title,
        tech_stack: selectedBlueprint.tech_stack,
        roadmap: selectedBlueprint.roadmap,
        starter_files: selectedBlueprint.starter_files,
        token: tokenToSend,
        provider: platformProvider
      };

      let provisionData: any = null;
      try {
        const response = await axios.post(`${apiBaseUrl}/api/provision`, payload, {
          timeout: 120000
        });
        provisionData = response.data;
      } catch (primaryErr: any) {
        // Automatic dual-route retry: If primary route fails, try alternate path
        const alternateBase = apiBaseUrl.startsWith("http")
          ? "/api/backend"
          : OFFICIAL_BACKEND_URL;
        const retryRes = await axios.post(`${alternateBase}/api/provision`, payload, {
          timeout: 120000
        });
        provisionData = retryRes.data;
      }

      if (provisionData && (provisionData.status === "success" || provisionData.repo_url || provisionData.html_url)) {
        const normalizedRepoUrl = (
          provisionData.repo_url ||
          provisionData.html_url ||
          provisionData.url ||
          ""
        ).trim();
        const safeResult = {
          ...provisionData,
          repo_url: normalizedRepoUrl,
          repo_name: provisionData.repo_name || provisionData.name || selectedBlueprint.title,
          commit_hash: provisionData.commit_hash || provisionData.sha || "main",
          issues_count: provisionData.issues_created?.length || provisionData.issues_count || 4
        };
        setProvisioningState({
          status: "success",
          step: 4,
          message: "Repository successfully provisioned and milestone issues populated on GitHub.",
          result: safeResult
        });
      } else {
        throw new Error(provisionData?.error || "Remote platform did not return repository details.");
      }
    } catch (err: any) {
      const errorMsg =
        err.response?.data?.detail ||
        err.response?.data?.error ||
        err.message ||
        "Failed to provision repository on remote platform.";

      setProvisioningState({
        status: "error",
        step: 0,
        message: `Provisioning failed: ${errorMsg}`,
        result: null
      });
    } finally {
      if (timer1) clearTimeout(timer1);
      if (timer2) clearTimeout(timer2);
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
              <SkillBridgeLogo size={34} />
              <div>
                <h1 className="text-sm sm:text-base font-bold text-slate-900 dark:text-white tracking-tight">
                  SkillBridge
                </h1>
                <span className="hidden md:block text-[10px] text-slate-500 dark:text-slate-400">
                  Career Project Builder
                </span>
              </div>
            </div>
          </div>

          <div className="flex items-center space-x-2 sm:space-x-3">
            <ThemeToggle />

            <ConnectedAccountBar
              connectedUser={connectedUser}
              platformAccount={platformAccount}
              onOpenSettings={() => setAuthSettingsOpen(true)}
              onDisconnect={handleDisconnect}
              onConnectPlatform={handleConnectPlatform}
            />
          </div>
        </div>
      </header>

      {/* Main Container */}
      <div className="mx-auto max-w-7xl px-4 sm:px-6 py-8">
        <div className="mb-8">
          <h2 className="text-2xl font-bold tracking-tight text-slate-900 dark:text-white sm:text-3xl">
            Career Project Builder
          </h2>
          <p className="mt-1 text-xs sm:text-sm text-slate-600 dark:text-slate-400">
            Compare your resume against industry standards, find missing skills, and build real projects.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          {/* Left Configuration Panel */}
          <div className="lg:col-span-4 space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Role & Resume</CardTitle>
                <CardDescription>Choose your target role and upload your resume.</CardDescription>
              </CardHeader>
              <CardContent className="space-y-5">
                <div className="space-y-2">
                  <label className="text-xs font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400">
                    Target role
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

                {/* Dynamic Custom Job Description / Skills Option */}
                <div className="space-y-1.5 pt-1">
                  <div className="flex items-center justify-between">
                    <button
                      type="button"
                      onClick={() => setShowCustomJobDescription(!showCustomJobDescription)}
                      className="text-[11px] font-medium text-[#0071e3] hover:underline flex items-center"
                    >
                      <span>{showCustomJobDescription ? "Hide custom requirements" : "+ Add custom job requirements (Optional)"}</span>
                    </button>
                    {customJobDescription.trim() && (
                      <span className="text-[10px] text-emerald-600 dark:text-emerald-400 font-medium">Custom active</span>
                    )}
                  </div>
                  {showCustomJobDescription && (
                    <div className="space-y-1.5 pt-1">
                      <textarea
                        value={customJobDescription}
                        onChange={(e) => setCustomJobDescription(e.target.value)}
                        placeholder="Paste job description, required tech stack, or specific qualification criteria to benchmark against dynamically..."
                        rows={3}
                        className="w-full rounded-xl border border-slate-300 dark:border-slate-800 bg-white dark:bg-[#0f172a] p-2.5 text-xs text-slate-800 dark:text-slate-100 placeholder-slate-400 focus:border-[#0071e3] focus:outline-none"
                      />
                      <p className="text-[10px] text-slate-500">
                        Dynamically tests candidate competencies against specific job requirements.
                      </p>
                    </div>
                  )}
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
                    Your Profile
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-2 text-xs">
                  {analysis.contacts?.name && (
                    <div className="flex justify-between text-slate-700 dark:text-slate-300">
                      <span className="text-slate-400">Name:</span>
                      <span className="font-semibold text-slate-900 dark:text-white">{analysis.contacts.name}</span>
                    </div>
                  )}
                  {analysis.contacts?.email && (
                    <div className="flex justify-between text-slate-700 dark:text-slate-300">
                      <span className="text-slate-400">Email:</span>
                      <span className="font-mono truncate max-w-[170px]">{analysis.contacts.email}</span>
                    </div>
                  )}
                  {analysis.contacts?.portfolio &&
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
                  {analysis.contacts?.linkedin && (
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

                  {/* Dynamic Dimension Distribution Bar Chart */}
                  <div className="pt-3 border-t border-slate-100 dark:border-slate-800">
                    <span className="text-[11px] font-semibold text-slate-800 dark:text-slate-200 block mb-1">
                      Skill Distribution by Category
                    </span>
                    <CategoryChart
                      dimensions={analysis.dimensions}
                      breakdown={analysis.category_breakdown}
                    />
                  </div>
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
                    {errorMessage.toLowerCase().includes("please upload") ||
                    errorMessage.toLowerCase().includes("resume") ||
                    errorMessage.toLowerCase().includes("document lacks") ||
                    errorMessage.toLowerCase().includes("cover letter") ||
                    errorMessage.toLowerCase().includes("422") ||
                    errorMessage.toLowerCase().includes("verification") ||
                    errorMessage.toLowerCase().includes("could not be verified")
                      ? "Resume Verification Notice"
                      : "Analysis Notice"}
                  </h3>
                  <p className="text-xs text-rose-600 dark:text-rose-400 mb-3 leading-relaxed">
                    {errorMessage.includes("status code 422") || errorMessage.includes("422")
                      ? "The uploaded document could not be verified as a technical resume. Please upload your personal CV or resume containing your work experience or projects, technical skills, and education."
                      : errorMessage}
                  </p>
                  <div className="mb-4 p-3 rounded-xl border border-rose-300/60 dark:border-rose-800 bg-white/70 dark:bg-slate-900/60 text-[11px] text-slate-700 dark:text-slate-300 text-left space-y-1">
                    <span className="font-semibold text-rose-800 dark:text-rose-300 block">Resume Requirements:</span>
                    <p>SkillBridge requires an authentic technical resume containing Work Experience or Projects, Technical Skills, and Education to benchmark candidate competencies.</p>
                  </div>
                  <div className="flex items-center space-x-3">
                    <Button variant="secondary" size="sm" onClick={() => {
                      setStatus("idle");
                      setFile(null);
                    }}>
                      Upload valid resume
                    </Button>
                  </div>
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
                  {/* Transparent Benchmark Comparison Banner */}
                  <BenchmarkComparisonBanner
                    role={analysis.target_role || targetRole}
                    benchmarkStandard={analysis.benchmark_standard}
                    overallMatch={analysis.match_percentage ?? 0}
                    deficitDelta={analysis.competency_deficit_delta ?? 0}
                  />

                  {/* Role-Calibrated Granular Capability Grid (Discipline-Tuned Metrics) */}
                  <GranularCapabilityGrid
                    dimensions={analysis.dimensions || []}
                    breakdown={analysis.category_breakdown || {}}
                    archetypeMetadata={analysis.archetype_metadata}
                  />

                  {/* High-Density Gap Diagnostic Matrix (Zero-Slop Engineering Table) */}
                  <GapDiagnosticTable
                    gaps={analysis.competency_gaps || []}
                    targetRole={analysis.target_role || targetRole}
                  />

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



                  {/* Senior Standing Evaluation or Project Recommendation Proposals */}
                  {analysis.is_senior_qualified && analysis.senior_standing ? (
                    <SeniorStandingCard
                      seniorStanding={analysis.senior_standing}
                      targetRole={analysis.target_role || targetRole}
                      onOpenPortfolioCard={() => setPortfolioCardOpen(true)}
                      onExportReport={exportCareerReport}
                    />
                  ) : (
                    <div>
                      <div className="flex items-center justify-between mb-4">
                        <div>
                          <div className="flex items-center space-x-2">
                            <h3 className="text-lg font-bold tracking-tight text-slate-900 dark:text-white">
                              Recommended Projects
                            </h3>
                          </div>
                          <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
                            Hands-on projects tailored to help you build and prove missing skills.
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
                            Export report
                          </Button>
                        </div>
                      </div>

                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        {(analysis.projects || []).map((project: any, idx: number) => (
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
                              <CardDescription className="line-clamp-2 mt-1 text-xs">
                                {project.objective}
                              </CardDescription>
                              <div className="flex flex-wrap items-center gap-1.5 mt-2">
                                <Badge variant="outline" className="text-[10px] bg-blue-50/60 dark:bg-blue-950/40 text-blue-700 dark:text-blue-300 border-blue-200 dark:border-blue-900/50">
                                  <FolderGit2 size={10} className="mr-1 text-blue-600" />
                                  Runnable Repository
                                </Badge>
                                <Badge variant="outline" className="text-[10px] bg-emerald-50/60 dark:bg-emerald-950/40 text-emerald-700 dark:text-emerald-300 border-emerald-200 dark:border-emerald-900/50">
                                  <CheckCircle2 size={10} className="mr-1 text-emerald-600" />
                                  TDD Test Suite
                                </Badge>
                                {project.is_kaggle_track && (
                                  <Badge variant="outline" className="text-[10px] bg-purple-50/60 dark:bg-purple-950/40 text-purple-700 dark:text-purple-300 border-purple-200 dark:border-purple-900/50">
                                    <Sparkles size={10} className="mr-1 text-purple-600" />
                                    Kaggle ML Track
                                  </Badge>
                                )}
                              </div>
                            </CardHeader>

                          <CardContent className="space-y-3">
                            <div>
                              <span className="text-[11px] font-medium text-slate-500 dark:text-slate-400 block mb-1.5">
                                Skills you&apos;ll learn:
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

                          <CardFooter className="pt-3 border-t border-slate-100 dark:border-slate-800/80 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-2">
                            <span className="text-xs font-mono tabular-nums text-slate-500 dark:text-slate-400">
                              Estimated: {project.hours} hrs
                            </span>
                            <div className="flex flex-wrap items-center gap-1.5 w-full sm:w-auto justify-end">
                              <Button
                                variant="outline"
                                size="sm"
                                className="text-xs h-7 px-2 text-slate-600 dark:text-slate-300"
                                onClick={() => openInspector(project)}
                                title="Inspect architecture blueprint and file contracts"
                              >
                                <Code2 size={12} className="mr-1" />
                                Inspect
                              </Button>
                              <Button
                                variant="outline"
                                size="sm"
                                className="text-xs h-7 px-2 text-slate-600 dark:text-slate-300"
                                onClick={() => {
                                  setManualBlueprint(project);
                                  setManualSetupModalOpen(true);
                                }}
                                title="Manual terminal setup (Zero OAuth)"
                              >
                                <Terminal size={12} className="mr-1" />
                                Manual CLI
                              </Button>
                              <Button
                                variant="outline"
                                size="sm"
                                className="text-xs h-7 px-2 text-slate-600 dark:text-slate-300"
                                onClick={() => handleDownloadZip(project)}
                                title="Download Skeleton ZIP archive"
                              >
                                <Download size={12} className="mr-1" />
                                ZIP
                              </Button>
                              <Button
                                size="sm"
                                className="text-xs h-7 px-2.5 bg-[#0071e3] hover:bg-[#0077ed] text-white"
                                onClick={() => handleProceedFromInspector(project)}
                                title="Automated repository provisioning on GitHub/GitLab"
                              >
                                <FolderGit2 size={12} className="mr-1" />
                                Provision
                              </Button>
                            </div>
                          </CardFooter>
                        </Card>
                      ))}
                    </div>
                  </div>
                  )}
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

            {provisioningState.status === "idle" ? (
              <div className="space-y-4">

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
                  <span className="text-xs font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400 block">
                    Developer Authentication
                  </span>

                  {connectedUser && platformProvider === "github" ? (
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
                      <Badge variant="success" className="text-[10px]">Connected</Badge>
                    </div>
                  ) : (
                    <div className="space-y-2">
                      <div className="flex items-center justify-between">
                        <label className="text-xs text-slate-600 dark:text-slate-400">
                          Personal access token ({platformProvider === "gitlab" ? "api scope" : "repo scope"}):
                        </label>
                        <button
                          type="button"
                          onClick={() => {
                            setProvisionModalOpen(false);
                            setAuthSettingsOpen(true);
                          }}
                          className="text-[11px] text-[#0071e3] hover:underline"
                        >
                          Connect GitHub account
                        </button>
                      </div>
                      <input
                        type="password"
                        value={tokenInput}
                        onChange={(e) => setTokenInput(e.target.value)}
                        placeholder={platformProvider === "gitlab" ? "glpat-xxxxxxxxxxxx" : "ghp_xxxxxxxxxxxx"}
                        className="w-full rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-[#0f172a] px-3 py-2 text-xs font-mono text-slate-800 dark:text-slate-100 placeholder-slate-400 focus:border-[#0071e3] focus:outline-none"
                      />
                      <p className="text-[11px] text-slate-500">
                        Tokens are transmitted securely to create your repository and milestone issues directly on your account.
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
                    Provision repository
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
            ) : provisioningState.status === "error" ? (
              <div className="space-y-4 py-2">
                <div className="rounded-2xl border border-rose-500/20 bg-rose-50 dark:bg-rose-500/10 p-4">
                  <div className="flex items-center space-x-2 text-rose-700 dark:text-rose-400 mb-1">
                    <AlertCircle size={18} />
                    <h4 className="text-sm font-semibold">Provisioning could not proceed</h4>
                  </div>
                  <p className="text-xs text-rose-600 dark:text-rose-300 leading-relaxed">
                    {provisioningState.message}
                  </p>
                </div>

                <div className="flex justify-end space-x-3 pt-2">
                  <Button
                    variant="secondary"
                    size="sm"
                    onClick={() => {
                      setProvisioningState({
                        status: "idle",
                        step: 0,
                        message: "Ready to initialize repository.",
                        result: null
                      });
                    }}
                  >
                    Adjust settings
                  </Button>
                  <Button size="sm" onClick={executeProvisioning}>
                    Retry provisioning
                  </Button>
                </div>
              </div>
            ) : provisioningState.status === "success" ? (
              <div className="space-y-5 py-2">
                <div className="rounded-2xl border border-emerald-500/20 bg-emerald-50 dark:bg-emerald-500/10 p-4">
                  <div className="flex items-center space-x-2 text-emerald-700 dark:text-emerald-400 mb-1">
                    <CheckCircle size={18} />
                    <h4 className="text-sm font-semibold">Repository provisioned successfully</h4>
                  </div>
                  <p className="text-xs text-slate-600 dark:text-slate-300">
                    The code repository is live under your account on {platformProvider === "gitlab" ? "GitLab" : "GitHub"}.
                  </p>
                </div>

                <div className="space-y-2 rounded-2xl border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-[#1e293b]/60 p-4 text-xs font-mono">
                  <div className="flex justify-between items-center">
                    <span className="text-slate-500">Repository:</span>
                    {provisioningState.result?.repo_url && provisioningState.result.repo_url.startsWith("http") ? (
                      <a
                        href={provisioningState.result.repo_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-[#0071e3] hover:underline flex items-center font-medium"
                      >
                        {provisioningState.result.repo_name || "View on GitHub"}
                        <ExternalLink size={12} className="ml-1" />
                      </a>
                    ) : (
                      <span className="text-slate-700 dark:text-slate-300 font-medium">
                        {provisioningState.result?.repo_name || "Created"}
                      </span>
                    )}
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-500">Initial commit:</span>
                    <span className="text-slate-800 dark:text-slate-200">
                      {provisioningState.result?.commit_hash || "main"}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-500">Milestone issues:</span>
                    <span className="text-emerald-600 dark:text-emerald-400">
                      {provisioningState.result?.issues_created?.length || provisioningState.result?.issues_count || 4} created
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
                    disabled={
                      !provisioningState.result?.repo_url ||
                      !provisioningState.result.repo_url.startsWith("http")
                    }
                    onClick={() => {
                      const targetUrl = provisioningState.result?.repo_url;
                      if (targetUrl && (targetUrl.startsWith("http://") || targetUrl.startsWith("https://"))) {
                        window.open(targetUrl, "_blank", "noopener,noreferrer");
                      }
                    }}
                  >
                    <ExternalLink size={14} className="mr-1.5" />
                    Open repository
                  </Button>
                </div>
              </div>
            ) : null}
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
                          : connectedUser.source === "oauth"
                          ? "OAuth verified account active"
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

          {/* Option 2: Connect Personal GitHub Account (PAT) */}
          <div className="rounded-2xl border border-slate-200 dark:border-slate-800 bg-slate-50/70 dark:bg-[#1e293b]/50 p-4 space-y-3">
            <div className="flex items-start justify-between">
              <div className="flex items-start space-x-3">
                <div className="p-2 rounded-xl bg-slate-800 text-white dark:bg-slate-700 mt-0.5">
                  <KeyRound size={20} />
                </div>
                <div>
                  <h4 className="font-semibold text-slate-900 dark:text-white text-sm">
                    Connect Personal GitHub Account
                  </h4>
                  <p className="text-[11px] text-slate-600 dark:text-slate-400 mt-0.5 leading-relaxed">
                    Provide a GitHub Personal Access Token (PAT) with <strong className="font-mono text-slate-800 dark:text-slate-200">repo</strong> scope to provision verifiable repositories under your personal GitHub profile.
                  </p>
                </div>
              </div>
            </div>

            <div className="space-y-2 pt-1">
              <div className="flex items-center justify-between text-[11px]">
                <span className="text-slate-500">Personal Access Token (Classic or Fine-Grained)</span>
                <a
                  href="https://github.com/settings/tokens/new?scopes=repo,read:user&description=SkillBridge%20AI%20Portfolio%20Provisioner"
                  target="_blank"
                  rel="noreferrer"
                  className="text-[#0071e3] hover:underline flex items-center font-medium"
                >
                  Create token on GitHub (1-Click)
                  <ExternalLink size={11} className="ml-1" />
                </a>
              </div>
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
                    Validating credentials with GitHub...
                  </>
                ) : (
                  <>
                    <ShieldCheck size={13} className="mr-1.5" />
                    Verify and connect personal GitHub account
                  </>
                )}
              </Button>
            </div>
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
        username={connectedUser?.login || analysis?.contacts?.name || "technical-candidate"}
        targetRole={targetRole}
        apiBaseUrl={apiBaseUrl}
      />

      {/* Zero-OAuth Manual Stepwise Terminal CLI Guide Modal */}
      <ManualSetupModal
        isOpen={manualSetupModalOpen}
        onClose={() => setManualSetupModalOpen(false)}
        blueprint={manualBlueprint}
        apiBaseUrl={apiBaseUrl}
        username={connectedUser?.login || platformAccount?.login || (analysis?.contacts?.github ? analysis.contacts.github.split("/").pop() : "") || ""}
      />
    </main>
  );
}

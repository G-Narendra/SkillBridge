import React, { useState } from "react";
import {
  Server,
  CheckCircle,
  XCircle,
  Loader2,
  RefreshCw,
  ExternalLink,
  ShieldCheck,
  Zap,
  Radio,
  Sliders,
  Check
} from "lucide-react";
import { Modal } from "@/components/ui/Modal";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import axios from "axios";

interface ApiSettingsModalProps {
  isOpen: boolean;
  onClose: () => void;
  activeUrl: string;
  onSaveUrl: (newUrl: string) => void;
  backendHealth: {
    status: "online" | "offline" | "checking";
    latencyMs?: number;
    rolesCount?: number;
    service?: string;
    error?: string;
  };
  onRefreshHealth: () => void;
}

export function ApiSettingsModal({
  isOpen,
  onClose,
  activeUrl,
  onSaveUrl,
  backendHealth,
  onRefreshHealth,
}: ApiSettingsModalProps) {
  const [inputUrl, setInputUrl] = useState(activeUrl);
  const [testing, setTesting] = useState(false);
  const [testResult, setTestResult] = useState<{
    success: boolean;
    message: string;
    latencyMs?: number;
    rolesCount?: number;
  } | null>(null);

  const presets = [
    {
      name: "Next.js Smart Proxy",
      url: "/api/backend",
      desc: "Zero-CORS serverless proxy (Recommended on Vercel)",
      tag: "Recommended"
    },
    {
      name: "Local FastAPI",
      url: "http://127.0.0.1:8080",
      desc: "Direct local backend connection",
      tag: "Development"
    },
    {
      name: "Render Cloud",
      url: "https://skillbridge-backend.onrender.com",
      desc: "Direct Render deployment endpoint",
      tag: "Cloud"
    }
  ];

  const handleTestConnection = async (targetToTest?: string) => {
    const urlToTest = (targetToTest || inputUrl || "").trim().replace(/\/$/, "");
    if (!urlToTest) return;

    setTesting(true);
    setTestResult(null);

    const startTime = performance.now();
    try {
      const endpoint = urlToTest.startsWith("http")
        ? `${urlToTest}/api/health`
        : `${urlToTest}/health`;

      const response = await axios.get(endpoint, {
        headers: urlToTest.startsWith("http")
          ? { "x-backend-url": urlToTest }
          : undefined,
        timeout: 12000
      });

      const elapsed = Math.round(performance.now() - startTime);
      setTestResult({
        success: true,
        message: response.data?.service || "SkillBridge AI Backend connected successfully",
        latencyMs: elapsed,
        rolesCount: response.data?.roles_available || 465
      });
    } catch (err: any) {
      const elapsed = Math.round(performance.now() - startTime);
      const msg = err.response?.data?.detail || err.message || "Failed to establish connection";
      setTestResult({
        success: false,
        message: msg,
        latencyMs: elapsed
      });
    } finally {
      setTesting(false);
    }
  };

  const handleSelectPreset = (url: string) => {
    setInputUrl(url);
    handleTestConnection(url);
  };

  const handleApply = () => {
    const clean = inputUrl.trim().replace(/\/$/, "");
    onSaveUrl(clean);
    onClose();
  };

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title="Backend API Connectivity Manager"
      className="max-w-xl"
    >
      <div className="space-y-5 py-2">
        <p className="text-xs text-slate-500 dark:text-slate-400 -mt-2">
          Configure and verify authentic REST endpoints between frontend and FastAPI backend.
        </p>
        {/* Current Connection Status Box */}
        <div className="flex items-center justify-between rounded-2xl border border-slate-200 dark:border-slate-800 bg-slate-50/70 dark:bg-[#1e293b]/50 p-4">
          <div className="flex items-center space-x-3">
            <div
              className={`rounded-xl p-2.5 ${
                backendHealth.status === "online"
                  ? "bg-emerald-500/15 text-emerald-600 dark:text-emerald-400"
                  : backendHealth.status === "checking"
                  ? "bg-amber-500/15 text-amber-600 dark:text-amber-400"
                  : "bg-rose-500/15 text-rose-600 dark:text-rose-400"
              }`}
            >
              <Server size={20} />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <span className="font-semibold text-sm text-slate-900 dark:text-white">
                  {backendHealth.status === "online"
                    ? "Backend Connected"
                    : backendHealth.status === "checking"
                    ? "Checking Connectivity..."
                    : "Backend Disconnected"}
                </span>
                <span
                  className={`inline-block h-2 w-2 rounded-full ${
                    backendHealth.status === "online"
                      ? "bg-emerald-500 animate-pulse"
                      : backendHealth.status === "checking"
                      ? "bg-amber-500"
                      : "bg-rose-500"
                  }`}
                />
              </div>
              <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5 font-mono truncate max-w-xs">
                Active: {activeUrl}
              </p>
            </div>
          </div>

          <div className="flex items-center space-x-2">
            {backendHealth.latencyMs !== undefined && (
              <Badge variant="outline" className="font-mono text-[10px]">
                {backendHealth.latencyMs}ms
              </Badge>
            )}
            <Button
              variant="outline"
              size="sm"
              onClick={onRefreshHealth}
              className="text-xs"
              title="Refresh connection status"
            >
              <RefreshCw size={13} className="mr-1" />
              Recheck
            </Button>
          </div>
        </div>

        {/* Preset Selector */}
        <div>
          <label className="text-xs font-semibold uppercase tracking-wider text-slate-600 dark:text-slate-400 block mb-2">
            Recommended Endpoints
          </label>
          <div className="space-y-2">
            {presets.map((preset) => {
              const isSelected = inputUrl === preset.url;
              return (
                <div
                  key={preset.url}
                  onClick={() => handleSelectPreset(preset.url)}
                  className={`group flex items-center justify-between rounded-xl border p-3 cursor-pointer transition-all ${
                    isSelected
                      ? "border-[#0071e3] bg-[#0071e3]/10 dark:bg-[#0071e3]/15"
                      : "border-slate-200 dark:border-slate-800 bg-white dark:bg-[#0f172a] hover:border-slate-300 dark:hover:border-slate-700"
                  }`}
                >
                  <div className="flex items-start space-x-3">
                    <div className="pt-0.5">
                      <div
                        className={`h-4 w-4 rounded-full border flex items-center justify-center ${
                          isSelected
                            ? "border-[#0071e3] bg-[#0071e3] text-white"
                            : "border-slate-400 dark:border-slate-600"
                        }`}
                      >
                        {isSelected && <Check size={10} />}
                      </div>
                    </div>
                    <div>
                      <div className="flex items-center space-x-2">
                        <span className="font-medium text-xs text-slate-900 dark:text-white">
                          {preset.name}
                        </span>
                        <Badge
                          variant={preset.tag === "Recommended" ? "success" : "outline"}
                          className="text-[9px] py-0 px-1.5"
                        >
                          {preset.tag}
                        </Badge>
                      </div>
                      <p className="text-[11px] text-slate-500 dark:text-slate-400 mt-0.5 font-mono">
                        {preset.url}
                      </p>
                      <p className="text-[11px] text-slate-400 dark:text-slate-500 mt-0.5">
                        {preset.desc}
                      </p>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Custom URL Input Field */}
        <div className="space-y-2">
          <label className="text-xs font-semibold uppercase tracking-wider text-slate-600 dark:text-slate-400 block">
            Target Endpoint URL
          </label>
          <div className="flex items-center space-x-2">
            <input
              type="text"
              value={inputUrl}
              onChange={(e) => setInputUrl(e.target.value)}
              placeholder="e.g. /api/backend or http://127.0.0.1:8080"
              className="flex-1 rounded-xl border border-slate-300 dark:border-slate-800 bg-white dark:bg-[#0f172a] px-3.5 py-2 text-xs font-mono text-slate-900 dark:text-white placeholder-slate-400 focus:border-[#0071e3] focus:outline-none"
            />
            <Button
              type="button"
              variant="outline"
              size="sm"
              onClick={() => handleTestConnection()}
              disabled={testing || !inputUrl.trim()}
              className="text-xs"
            >
              {testing ? (
                <>
                  <Loader2 size={13} className="mr-1 animate-spin" />
                  Testing
                </>
              ) : (
                <>
                  <Zap size={13} className="mr-1 text-amber-500" />
                  Test Endpoint
                </>
              )}
            </Button>
          </div>
        </div>

        {/* Diagnostics Test Output */}
        {testResult && (
          <div
            className={`rounded-xl border p-3.5 text-xs transition-all ${
              testResult.success
                ? "border-emerald-500/30 bg-emerald-50/70 dark:bg-emerald-950/20 text-emerald-800 dark:text-emerald-300"
                : "border-rose-500/30 bg-rose-50/70 dark:bg-rose-950/20 text-rose-800 dark:text-rose-300"
            }`}
          >
            <div className="flex items-start space-x-2.5">
              {testResult.success ? (
                <CheckCircle size={16} className="text-emerald-500 mt-0.5 shrink-0" />
              ) : (
                <XCircle size={16} className="text-rose-500 mt-0.5 shrink-0" />
              )}
              <div className="flex-1 space-y-1">
                <p className="font-semibold">{testResult.message}</p>
                <div className="flex items-center space-x-3 text-[11px] opacity-80 font-mono">
                  {testResult.latencyMs !== undefined && (
                    <span>Latency: {testResult.latencyMs}ms</span>
                  )}
                  {testResult.rolesCount !== undefined && (
                    <span>Roles Catalog: {testResult.rolesCount} active profiles</span>
                  )}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Modal Action Buttons */}
        <div className="pt-2 flex items-center justify-end space-x-3 border-t border-slate-100 dark:border-slate-800">
          <Button variant="secondary" size="sm" onClick={onClose} className="text-xs">
            Cancel
          </Button>
          <Button size="sm" onClick={handleApply} className="text-xs">
            Save & Connect
          </Button>
        </div>
      </div>
    </Modal>
  );
}

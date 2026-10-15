import React, { useState } from "react";
import { Modal } from "./ui/Modal";
import { Button } from "./ui/Button";
import { Terminal, Download, Copy, Check, ExternalLink, Sparkles, FolderGit2 } from "lucide-react";
import axios from "axios";

interface ManualSetupModalProps {
  isOpen: boolean;
  onClose: () => void;
  blueprint: any;
  apiBaseUrl: string;
  username?: string;
}

export const ManualSetupModal: React.FC<ManualSetupModalProps> = ({
  isOpen,
  onClose,
  blueprint,
  apiBaseUrl,
  username,
}) => {
  const [copied, setCopied] = useState(false);
  const [downloading, setDownloading] = useState(false);
  const [downloadError, setDownloadError] = useState("");

  if (!blueprint) return null;

  // Generate clean, human-readable slug from title or slug, strictly avoiding raw hex cache keys
  const isHexHash = (s: string) => /^[0-9a-f]{16}$/i.test(s);
  const rawCandidate = (blueprint.slug && !isHexHash(blueprint.slug))
    ? blueprint.slug
    : (blueprint.title && !isHexHash(blueprint.title))
      ? blueprint.title
      : (!isHexHash(blueprint.id || "") ? blueprint.id : "portfolio-project");

  const slug = (rawCandidate || "portfolio-project")
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/-+/g, "-")
    .replace(/^-|-$/g, "")
    .slice(0, 48);

  const userHandle = (username && username.trim() && username !== "your-username")
    ? username.trim()
    : "<your-github-username>";

  const terminalScript = `# Step 1: Initialize local repository directory
mkdir ${slug} && cd ${slug}
git init -b main

# Step 2: Unzip the downloaded skeleton archive into this folder
# (Extract ${slug}-skeleton.zip into the current directory)

# Step 3: Setup local virtual environment & run failing TDD test harness
python -m venv venv
# On Windows: .\\venv\\Scripts\\activate
# On macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
pytest tests/ -v  # Observe initial Red failing assertions (TDD baseline)

# Step 4: Create remote repository & push via GitHub CLI
gh repo create ${slug} --public --source=. --remote=origin --push

# (Alternative without GitHub CLI):
# 1. Create a new repository on https://github.com/new named '${slug}'
# 2. Run:
#    git remote add origin https://github.com/${userHandle}/${slug}.git
#    git add .
#    git commit -m "chore: initial project skeleton with TDD test harness"
#    git push -u origin main`;

  const handleCopy = () => {
    navigator.clipboard.writeText(terminalScript);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDownloadZip = async () => {
    setDownloading(true);
    setDownloadError("");
    try {
      const endpoint = `${apiBaseUrl}/api/blueprint/download-zip`;
      const payload = {
        title: blueprint.title,
        starter_files: blueprint.starter_files || {},
      };

      const res = await axios.post(endpoint, payload, {
        responseType: "blob",
        timeout: 30000,
      });

      // Trigger browser download
      const blob = new Blob([res.data], { type: "application/zip" });
      const downloadUrl = window.URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = downloadUrl;
      link.download = `${slug}-skeleton.zip`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(downloadUrl);
    } catch (err: any) {
      setDownloadError(err.response?.data?.detail || err.message || "Failed to download skeleton ZIP.");
    } finally {
      setDownloading(false);
    }
  };

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title="Manual Step-by-Step Terminal CLI Setup"
      className="max-w-2xl"
    >
      <div className="space-y-4 text-xs text-slate-800 dark:text-slate-200">
        <div>
          <h3 className="text-sm font-semibold text-slate-900 dark:text-white">
            {blueprint.title}
          </h3>
          <p className="text-[11px] text-slate-500 dark:text-slate-400">
            Zero-OAuth workflow: download the enterprise skeleton archive and initialize via your local terminal.
          </p>
        </div>

        {/* Download Action Card */}
        <div className="rounded-2xl border border-blue-500/20 bg-blue-50/60 dark:bg-blue-500/10 p-4 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div className="space-y-0.5">
            <span className="font-semibold text-slate-900 dark:text-slate-100 flex items-center">
              <Download size={14} className="mr-1.5 text-[#0071e3]" />
              Enterprise Skeleton Archive (.zip)
            </span>
            <p className="text-[11px] text-slate-600 dark:text-slate-300">
              Contains typed contracts, failing TDD test suite, Dockerfile, and milestone templates.
            </p>
          </div>
          <Button
            size="sm"
            onClick={handleDownloadZip}
            disabled={downloading}
            className="shrink-0 font-medium"
          >
            {downloading ? "Packaging ZIP..." : "Download Skeleton (.zip)"}
          </Button>
        </div>

        {downloadError && (
          <div className="rounded-xl border border-rose-500/20 bg-rose-50 dark:bg-rose-500/10 p-3 text-[11px] text-rose-600 dark:text-rose-300">
            {downloadError}
          </div>
        )}

        {/* Terminal Script */}
        <div className="space-y-1.5">
          <div className="flex items-center justify-between">
            <span className="font-semibold text-slate-700 dark:text-slate-300 flex items-center">
              <Terminal size={14} className="mr-1.5 text-slate-500" />
              Terminal Step-by-Step Commands
            </span>
            <Button
              variant="secondary"
              size="sm"
              onClick={handleCopy}
              className="text-[11px] h-7 px-2.5"
            >
              {copied ? (
                <>
                  <Check size={12} className="mr-1 text-emerald-500" />
                  Copied
                </>
              ) : (
                <>
                  <Copy size={12} className="mr-1" />
                  Copy Script
                </>
              )}
            </Button>
          </div>

          <pre className="overflow-x-auto rounded-xl border border-slate-200 dark:border-slate-800 bg-[#0f172a] p-3 font-mono text-[11px] text-slate-200 leading-relaxed max-h-64">
            <code>{terminalScript}</code>
          </pre>
        </div>

        <div className="flex justify-end pt-2">
          <Button variant="outline" size="sm" onClick={onClose}>
            Close
          </Button>
        </div>
      </div>
    </Modal>
  );
};

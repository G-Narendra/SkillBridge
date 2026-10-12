import React, { useState } from "react";
import { FolderGit2, FileCode, Check, Layers, Clock, Award, Copy } from "lucide-react";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";

interface BlueprintInspectorProps {
  blueprint: any;
  onClose: () => void;
  onProceedToProvision: (customizedBlueprint: any) => void;
}

export function BlueprintInspector({
  blueprint,
  onClose,
  onProceedToProvision,
}: BlueprintInspectorProps) {
  const files = blueprint.starter_files || {
    "README.md": `# ${blueprint.title}\n\n## Objective\n${blueprint.objective}\n\n## Roadmap\n${blueprint.roadmap?.join("\n")}`,
  };

  const fileNames = Object.keys(files);
  const [activeFile, setActiveFile] = useState<string>(fileNames[0] || "README.md");
  const [selectedDifficulty, setSelectedDifficulty] = useState<string>(blueprint.difficulty || "Intermediate");
  const [selectedHours, setSelectedHours] = useState<number>(blueprint.hours || 32);
  const [copiedCode, setCopiedCode] = useState(false);

  const handleCopyCode = () => {
    const content = files[activeFile] || "";
    if (typeof navigator !== "undefined") {
      navigator.clipboard.writeText(content);
      setCopiedCode(true);
      setTimeout(() => setCopiedCode(false), 2000);
    }
  };

  const handleProceed = () => {
    onProceedToProvision({
      ...blueprint,
      difficulty: selectedDifficulty,
      hours: selectedHours,
      starter_files: files,
    });
  };

  return (
    <div className="space-y-5 text-slate-800 dark:text-slate-200">
      <div>
        <h3 className="text-lg font-bold text-slate-900 dark:text-white mb-1">
          {blueprint.title}
        </h3>
        <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
          {blueprint.objective}
        </p>
      </div>

      {/* Configuration & Meta Row */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
        <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-[#1e293b]/50 p-3">
          <div className="flex items-center space-x-1.5 text-xs text-slate-500 mb-1">
            <Award size={14} />
            <span>Difficulty tier</span>
          </div>
          <div className="flex space-x-1.5">
            {["Beginner", "Intermediate", "Advanced"].map((level) => (
              <button
                key={level}
                type="button"
                onClick={() => setSelectedDifficulty(level)}
                className={`text-[11px] px-2 py-0.5 rounded-md font-medium transition-colors ${
                  selectedDifficulty === level
                    ? "bg-[#0071e3] text-white"
                    : "bg-slate-200/80 dark:bg-slate-800 text-slate-700 dark:text-slate-300"
                }`}
              >
                {level}
              </button>
            ))}
          </div>
        </div>

        <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-[#1e293b]/50 p-3">
          <div className="flex items-center space-x-1.5 text-xs text-slate-500 mb-1">
            <Clock size={14} />
            <span>Target hours</span>
          </div>
          <div className="flex items-center space-x-2">
            {[24, 32, 40].map((hrs) => (
              <button
                key={hrs}
                type="button"
                onClick={() => setSelectedHours(hrs)}
                className={`text-[11px] px-2 py-0.5 rounded-md font-mono tabular-nums font-medium transition-colors ${
                  selectedHours === hrs
                    ? "bg-[#0071e3] text-white"
                    : "bg-slate-200/80 dark:bg-slate-800 text-slate-700 dark:text-slate-300"
                }`}
              >
                {hrs}h
              </button>
            ))}
          </div>
        </div>

        <div className="rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-[#1e293b]/50 p-3">
          <div className="flex items-center space-x-1.5 text-xs text-slate-500 mb-1">
            <Layers size={14} />
            <span>Target gaps covered</span>
          </div>
          <div className="flex flex-wrap gap-1">
            {blueprint.target_skills_covered?.slice(0, 3).map((skill: string) => (
              <Badge key={skill} variant="destructive" className="text-[10px]">
                {skill}
              </Badge>
            ))}
          </div>
        </div>
      </div>

      {/* Architecture Spec */}
      <div className="rounded-2xl border border-slate-200 dark:border-slate-800 bg-slate-50/70 dark:bg-[#1e293b]/40 p-4">
        <h4 className="text-xs font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400 mb-1.5">
          Architecture overview
        </h4>
        <p className="text-xs text-slate-700 dark:text-slate-300 leading-relaxed">
          {blueprint.architecture_outline}
        </p>
      </div>

      {/* Implementation Milestones */}
      <div>
        <h4 className="text-xs font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400 mb-2">
          Milestone issues (4 sequential tickets)
        </h4>
        <div className="space-y-2 rounded-2xl border border-slate-200 dark:border-slate-800 bg-slate-50/50 dark:bg-[#1e293b]/30 p-3">
          {blueprint.roadmap?.map((milestone: string, idx: number) => (
            <div key={idx} className="flex items-start space-x-2 text-xs">
              <span className="font-mono text-[#0071e3] font-semibold shrink-0">
                {String(idx + 1).padStart(2, "0")}.
              </span>
              <span className="text-slate-700 dark:text-slate-300">{milestone}</span>
            </div>
          ))}
        </div>
      </div>

      {/* File Scaffolding Preview */}
      <div>
        <div className="flex items-center justify-between mb-2">
          <h4 className="text-xs font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400">
            Starter file scaffolding ({fileNames.length} files)
          </h4>
          <button
            type="button"
            onClick={handleCopyCode}
            className="flex items-center space-x-1 text-xs text-[#0071e3] hover:underline"
          >
            {copiedCode ? <Check size={12} className="text-emerald-500" /> : <Copy size={12} />}
            <span>{copiedCode ? "Copied" : "Copy file"}</span>
          </button>
        </div>

        {/* File tabs */}
        <div className="flex items-center space-x-1 overflow-x-auto border-b border-slate-200 dark:border-slate-800 pb-1">
          {fileNames.map((name) => (
            <button
              key={name}
              type="button"
              onClick={() => setActiveFile(name)}
              className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-mono transition-colors ${
                activeFile === name
                  ? "bg-[#0071e3]/15 text-[#0071e3] font-semibold"
                  : "text-slate-500 hover:text-slate-800 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800"
              }`}
            >
              <FileCode size={13} />
              <span>{name}</span>
            </button>
          ))}
        </div>

        {/* File Content Preview */}
        <div className="mt-2 rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-900 text-slate-200 p-3.5 max-h-48 overflow-y-auto font-mono text-[11px] leading-relaxed">
          <pre className="whitespace-pre-wrap">{files[activeFile] || ""}</pre>
        </div>
      </div>

      {/* Actions */}
      <div className="pt-3 border-t border-slate-200 dark:border-slate-800 flex items-center justify-between">
        <Button variant="secondary" size="sm" onClick={onClose}>
          Close
        </Button>
        <Button size="sm" onClick={handleProceed}>
          <FolderGit2 size={14} className="mr-1.5" />
          Proceed to provisioning
        </Button>
      </div>
    </div>
  );
}

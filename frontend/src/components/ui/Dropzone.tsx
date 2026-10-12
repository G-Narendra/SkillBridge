import React, { useCallback, useState, useRef } from "react";
import { cn } from "@/lib/utils";
import { UploadCloud, File, X } from "lucide-react";

interface DropzoneProps {
  onFileSelect: (file: File | null) => void;
  accept?: string;
  maxSize?: number; // in bytes
  className?: string;
}

export function Dropzone({
  onFileSelect,
  accept = ".pdf",
  maxSize = 10 * 1024 * 1024,
  className
}: DropzoneProps) {
  const [isDragActive, setIsDragActive] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [error, setError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleDragEnter = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragActive(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragActive(false);
  }, []);

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
  }, []);

  const validateAndSelectFile = useCallback((file: File | null) => {
    if (!file) return;

    if (file.size > maxSize) {
      setError(`File size exceeds ${Math.round(maxSize / 1024 / 1024)} MB limit.`);
      return;
    }

    if (accept && !file.name.toLowerCase().endsWith(accept.toLowerCase())) {
      setError(`Unsupported file format. Please upload a ${accept.toUpperCase()} document.`);
      return;
    }

    setSelectedFile(file);
    onFileSelect(file);
    setError(null);
  }, [accept, maxSize, onFileSelect]);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragActive(false);
    setError(null);

    const file = e.dataTransfer.files?.[0];
    validateAndSelectFile(file || null);
  }, [validateAndSelectFile]);

  const handleChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    validateAndSelectFile(file || null);
  }, [validateAndSelectFile]);

  const removeFile = (e: React.MouseEvent) => {
    e.stopPropagation();
    setSelectedFile(null);
    onFileSelect(null);
    setError(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  const handleClick = () => {
    fileInputRef.current?.click();
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" || e.key === " ") {
      e.preventDefault();
      fileInputRef.current?.click();
    }
  };

  return (
    <div
      role="button"
      tabIndex={0}
      aria-label="Upload resume PDF file"
      onClick={handleClick}
      onKeyDown={handleKeyDown}
      onDragEnter={handleDragEnter}
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
      className={cn(
        "relative flex cursor-pointer flex-col items-center justify-center rounded-2xl border border-dashed p-6 transition-all focus:outline-none focus:ring-2 focus:ring-[#0071e3] focus:ring-offset-2",
        isDragActive
          ? "border-[#0071e3] bg-[#0071e3]/10"
          : "border-slate-300 dark:border-slate-800 bg-white dark:bg-[#0f172a]/70 hover:border-slate-400 dark:hover:border-slate-700 hover:bg-slate-50/50 dark:hover:bg-[#0f172a]",
        error ? "border-rose-500/50 bg-rose-500/10" : "",
        className
      )}
    >
      <input
        ref={fileInputRef}
        type="file"
        className="hidden"
        accept={accept}
        onChange={handleChange}
      />

      {selectedFile ? (
        <div className="flex w-full items-center justify-between rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-[#1e293b]/70 p-3.5">
          <div className="flex items-center space-x-3 min-w-0">
            <div className="rounded-lg bg-[#0071e3]/15 p-2 text-[#0071e3] shrink-0">
              <File size={20} />
            </div>
            <div className="flex flex-col text-left truncate">
              <span className="text-sm font-medium text-slate-800 dark:text-slate-100 truncate">{selectedFile.name}</span>
              <span className="text-xs font-mono tabular-nums text-slate-500 dark:text-slate-400">
                {(selectedFile.size / 1024 / 1024).toFixed(2)} MB • Ready for analysis
              </span>
            </div>
          </div>
          <button
            type="button"
            onClick={removeFile}
            aria-label="Remove uploaded file"
            className="rounded p-1.5 text-slate-400 hover:bg-slate-200 dark:hover:bg-slate-800 hover:text-slate-700 dark:hover:text-slate-200 focus:outline-none"
          >
            <X size={16} />
          </button>
        </div>
      ) : (
        <div className="flex flex-col items-center text-center">
          <div className="mb-3 rounded-full border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-[#1e293b]/60 p-3 text-slate-500 dark:text-slate-300">
            <UploadCloud size={24} />
          </div>
          <p className="mb-1 text-sm font-medium text-slate-700 dark:text-slate-200">
            Select or drag PDF resume document
          </p>
          <p className="text-xs font-mono text-slate-400 dark:text-slate-400">
            PDF format up to {Math.round(maxSize / 1024 / 1024)} MB
          </p>
          {error && <p className="mt-2 text-xs font-medium text-rose-500">{error}</p>}
        </div>
      )}
    </div>
  );
}

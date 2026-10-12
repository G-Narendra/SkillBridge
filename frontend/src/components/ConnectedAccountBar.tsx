import React from "react";
import { Github, LogOut, Sparkles, CheckCircle2 } from "lucide-react";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import Image from "next/image";

export interface ConnectedUser {
  login: string;
  name?: string;
  avatar_url?: string;
  html_url?: string;
  public_repos?: number;
  scopes?: string[];
  is_sandbox?: boolean;
  source?: "platform" | "custom_pat" | "sandbox" | "oauth";
  raw_token?: string;
}

interface ConnectedAccountBarProps {
  connectedUser: ConnectedUser | null;
  platformAccount?: ConnectedUser | null;
  onOpenSettings: () => void;
  onDisconnect: () => void;
  onConnectPlatform?: () => void;
  onConnectDemo: () => void;
}

export function ConnectedAccountBar({
  connectedUser,
  platformAccount,
  onOpenSettings,
  onDisconnect,
  onConnectPlatform,
  onConnectDemo,
}: ConnectedAccountBarProps) {
  if (connectedUser) {
    const isPlatform = connectedUser.source === "platform";
    const isSandbox = connectedUser.is_sandbox || connectedUser.source === "sandbox";

    return (
      <div className="flex items-center space-x-2 sm:space-x-3">
        <button
          type="button"
          onClick={onOpenSettings}
          className="group flex items-center space-x-2 rounded-xl border border-slate-200 dark:border-slate-800 bg-white/80 dark:bg-[#0f172a]/80 px-2.5 py-1.5 backdrop-blur-md hover:border-slate-300 dark:hover:border-slate-700 transition-all text-left"
          title="View developer connection settings and permissions"
        >
          {connectedUser.avatar_url ? (
            <Image
              src={connectedUser.avatar_url}
              alt={connectedUser.login}
              width={22}
              height={22}
              unoptimized
              className="h-5 w-5 rounded-full border border-slate-300 dark:border-slate-700 object-cover"
            />
          ) : (
            <Github size={16} className="text-slate-700 dark:text-slate-300" />
          )}

          <div className="flex items-center space-x-1.5 text-xs">
            <span className="font-medium text-slate-800 dark:text-slate-100 max-w-[110px] truncate">
              {connectedUser.login}
            </span>
            <span className="inline-block h-1.5 w-1.5 rounded-full bg-emerald-500 animate-pulse" />
          </div>

          {isPlatform ? (
            <Badge variant="success" className="hidden sm:inline-flex text-[9px] uppercase tracking-wider py-0 font-medium">
              Platform
            </Badge>
          ) : isSandbox ? (
            <Badge variant="warning" className="hidden sm:inline-flex text-[9px] uppercase tracking-wider py-0 font-medium">
              Preview
            </Badge>
          ) : (
            <Badge variant="outline" className="hidden sm:inline-flex text-[9px] uppercase tracking-wider py-0 font-medium">
              PAT
            </Badge>
          )}

          <Badge variant="outline" className="hidden md:inline-flex text-[10px] font-mono py-0">
            {connectedUser.public_repos || 0} repos
          </Badge>
        </button>

        <button
          type="button"
          onClick={onDisconnect}
          title="Disconnect account"
          className="rounded-lg p-1.5 text-slate-400 hover:text-slate-700 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
        >
          <LogOut size={14} />
        </button>
      </div>
    );
  }

  return (
    <div className="flex items-center space-x-2">
      {platformAccount && onConnectPlatform ? (
        <Button
          variant="outline"
          size="sm"
          onClick={onConnectPlatform}
          className="text-xs"
          title="Connect platform verified GitHub account"
        >
          <Github size={13} className="mr-1.5 text-slate-800 dark:text-slate-200" />
          Connect {platformAccount.login}
        </Button>
      ) : (
        <Button
          variant="outline"
          size="sm"
          onClick={onConnectDemo}
          className="text-xs"
          title="Activate preview account for testing"
        >
          <Sparkles size={13} className="mr-1 text-amber-500" />
          Demo account
        </Button>
      )}

      <Button
        variant="primary"
        size="sm"
        onClick={onOpenSettings}
        className="text-xs"
      >
        <Github size={13} className="mr-1.5" />
        Connect GitHub
      </Button>
    </div>
  );
}

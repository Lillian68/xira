"use client";

import Link from "next/link";
import { LogOut } from "lucide-react";
import { translations } from "@/lib/i18n";
import { useAuthStore } from "@/store/authStore";
import { useLocaleStore } from "@/store/localeStore";

export function AppHeader() {
  const { user, logout } = useAuthStore();
  const locale = useLocaleStore((s) => s.locale);
  const t = translations[locale];

  return (
    <header className="relative z-50 border-b border-primary/10 bg-mist/80 backdrop-blur">
      <div className="mx-auto flex w-full max-w-6xl items-center justify-between px-6 py-4 sm:px-8">
        <Link href="/dashboard" className="flex items-center gap-2" aria-label="Go to dashboard">
          <img src="/logo.png" alt="Xira" className="h-8 w-auto sm:h-10" />
        </Link>
        <div className="flex items-center gap-3 text-sm">
          {user && (
            <span className="text-primary/70">{user.username}</span>
          )}
          <button
            type="button"
            onClick={logout}
            className="inline-flex items-center gap-1 text-primary/60 transition hover:text-soil"
          >
            <LogOut className="h-4 w-4" />
            {t.logout}
          </button>
        </div>
      </div>
    </header>
  );
}

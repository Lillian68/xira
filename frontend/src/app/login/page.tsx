"use client";

import Link from "next/link";
import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";
import { translations } from "@/lib/i18n";
import { useAuthStore } from "@/store/authStore";
import { useLocaleStore } from "@/store/localeStore";

export default function LoginPage() {
  const router = useRouter();
  const login = useAuthStore((s) => s.login);
  const locale = useLocaleStore((s) => s.locale);
  const t = translations[locale];
  const [account, setAccount] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const onSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      await login(account, password);
      router.push("/dashboard");
    } catch (err) {
      setError(err instanceof Error ? err.message : t.loginFailed);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main
      className="relative min-h-screen overflow-hidden bg-fixed bg-center bg-cover text-soil"
      style={{ backgroundImage: "url('/login.png')" }}>
      <div className="relative z-10 mx-auto flex min-h-screen max-w-6xl flex-col justify-between px-6 sm:px-8">
        <header className="relative z-50">
          <div className="mx-auto flex w-full max-w-6xl items-center justify-between px-0 py-4">
            <img src="/logo.png" alt="Xira" className="block h-8 w-auto sm:h-10" />
          </div>
        </header>
        <div className="flex flex-1 items-center justify-end px-24 sm:px-24 lg:px-48">
          <form
            onSubmit={onSubmit}
            className="w-full max-w-md rounded-sm p-8"
          >
            <label className="block text-sm">
              {t.emailOrUsername}
              <input
                className="mt-1 w-full rounded-sm border border-primary/15 bg-secondary/40 px-3 py-2 outline-none focus:border-growth"
                value={account}
                onChange={(e) => setAccount(e.target.value)}
                required
              />
            </label>
            <label className="mt-4 block text-sm">
              {t.password}
              <input
                type="password"
                className="mt-1 w-full rounded-sm border border-primary/15 bg-secondary/40 px-3 py-2 outline-none focus:border-growth"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </label>
            {error && <p className="mt-3 text-sm text-red-700/80">{error}</p>}
            <button
              type="submit"
              disabled={loading}
              className="mt-6 w-full rounded-sm bg-soil py-2.5 text-secondary transition hover:bg-primary disabled:opacity-60"
            >
              {loading ? t.loading : t.login}
            </button>
            <p className="mt-4 text-center text-sm text-primary/60">
              {t.noAccount}{" "}
              <Link href="/register" className="text-growth underline-offset-2 hover:underline">
                {t.register}
              </Link>
            </p>
          </form>
        </div>
      </div>
    </main>
  );
}

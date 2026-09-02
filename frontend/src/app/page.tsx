"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { ArrowRight, Sprout } from "lucide-react";
import { useEffect, useState } from "react";
import { getLocaleFromBrowser, translations } from "@/lib/i18n";
import LocaleSwitcher from "@/components/LocaleSwitcher";
import { readStoredLocale, useLocaleStore } from "@/store/localeStore";

export default function HomePage() {
  const locale = useLocaleStore((s) => s.locale);
  const setLocale = useLocaleStore((s) => s.setLocale);
  const [isInfoOpen, setIsInfoOpen] = useState(false);
  const t = translations[locale];
  const isEnglish = locale === "en";

  useEffect(() => {
    if (typeof window === "undefined") return;

    const storedLocale = readStoredLocale();
    const browserLocale = getLocaleFromBrowser();

    if (storedLocale && storedLocale !== locale) {
      setLocale(storedLocale);
      return;
    }

    if (!storedLocale && browserLocale !== locale) {
      setLocale(browserLocale);
    }
  }, [locale, setLocale]);

  useEffect(() => {
    if (typeof document === "undefined") return;

    const nextTitle = locale === "en" ? "Xira" : "息壤";
    const nextDescription =
      locale === "en"
        ? "Your growth, nurtured. Never study alone. Let Xira be the companion who truly understands your pace."
        : "知你进取，共此生息。息壤，更懂你节奏的情感陪伴型自学引擎。";

    document.title = nextTitle;
    document.documentElement.lang = locale === "en" ? "en" : "zh-CN";

    let descriptionMeta = document.querySelector('meta[name="description"]');
    if (!descriptionMeta) {
      descriptionMeta = document.createElement("meta");
      descriptionMeta.setAttribute("name", "description");
      document.head.appendChild(descriptionMeta);
    }
    descriptionMeta.setAttribute("content", nextDescription);
  }, [locale]);

  return (
    <main
      className="relative min-h-screen overflow-hidden bg-fixed bg-center bg-cover text-soil"
      style={{ backgroundImage: "url('/home.png')" }}
    >
      <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_top,_rgba(255,255,255,0.85),_transparent_40%),linear-gradient(180deg,rgba(248,246,240,0.82),rgba(245,239,226,0.18))]" />
      <div className="relative z-10 mx-auto flex min-h-screen max-w-6xl flex-col justify-between px-6 sm:px-8">
        <header className="relative z-50">
          <div className="mx-auto flex w-full max-w-6xl items-center justify-between px-0 py-4">
            <img src="/logo.png" alt={t.brand} className="block h-8 w-auto sm:h-10" />
            <div className="flex items-center gap-4">
              <LocaleSwitcher />
            </div>
          </div>
        </header>

        <section className="flex flex-1 items-center">
          <motion.div
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.75 }}
          >
            <div className="flex flex-wrap items-end gap-4 text-soil">
              <p
                className={`font-display leading-none ${isEnglish ? "text-[2rem] tracking-[0.06em] sm:text-[2.4rem]" : "text-5xl tracking-[0.2em] sm:text-6xl"
                  }`}
              >
                {t.brand}
              </p>
            </div>
            <p
              className={`mt-6 max-w-xl leading-[1.08] text-soil ${isEnglish ? "text-lg sm:text-[1.8rem]" : "text-4xl sm:text-5xl"
                }`}
            >
              {t.headline}
              <span className={`block text-primary/80 ${isEnglish ? "mt-1" : ""}`}>{t.tagline}</span>
            </p>
            <p
              className={`mt-6 max-w-2xl leading-relaxed text-primary/75 ${isEnglish ? "text-[0.6rem] sm:text-[0.7rem]" : "text-sm sm:text-base"
                }`}
            >
              {t.description}
            </p>
            <div className="mt-10 flex flex-wrap gap-3">
              <Link
                href="/login"
                className="inline-flex items-center gap-2 rounded-full bg-soil px-6 py-3 text-sm text-secondary transition hover:bg-primary"
              >
                <Sprout className="h-4 w-4" />
                {t.primaryCta}
                <ArrowRight className="h-4 w-4" />
              </Link>
              <button
                type="button"
                onClick={() => setIsInfoOpen(true)}
                className="inline-flex items-center rounded-full border border-primary/20 bg-white/60 px-6 py-3 text-sm text-primary backdrop-blur transition hover:bg-primary/10"
              >
                {t.secondaryCta}
              </button>
            </div>
          </motion.div>
        </section>
        {isInfoOpen && (
          <div className="fixed inset-0 z-20 flex items-center justify-center bg-black/40 px-4 py-6">
            <div className="w-full max-w-xl rounded-3xl bg-white p-8 text-left shadow-xl ring-1 ring-black/10">
              <div className="flex items-start justify-between gap-4">
                <div>
                  <h2 className="text-2xl font-semibold text-primary">{t.about}</h2>
                </div>
                <button
                  type="button"
                  onClick={() => setIsInfoOpen(false)}
                  className="rounded-full bg-primary/5 px-3 py-2 text-sm font-medium text-primary transition hover:bg-primary/10"
                >
                  {t.close}
                </button>
              </div>
              <div className="mt-6 space-y-4 text-primary/80">
                <p className="mt-3 text-sm leading-6 text-primary/75">
                  {t.xirang}
                </p>
                <p className="mt-3 text-sm leading-6 text-primary/75">
                  {t.appMeaning}
                </p>
              </div>
            </div>
          </div>
        )}
      </div>
    </main>
  );
}

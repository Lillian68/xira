"use client";

import { locales } from "@/lib/i18n";
import { useLocaleStore } from "@/store/localeStore";

export default function LocaleSwitcher() {
  const locale = useLocaleStore((s) => s.locale);
  const setLocale = useLocaleStore((s) => s.setLocale);

  return (
    <div className="flex items-center gap-2 rounded-full border border-primary/20 bg-white/70 px-3 py-1 text-sm text-primary shadow-soft">
      {locales.map((item) => (
        <button
          key={item}
          type="button"
          onClick={() => setLocale(item)}
          className={`rounded-full px-3 py-1 transition ${locale === item ? "bg-primary text-secondary" : "text-primary/70 hover:text-primary"}`}
        >
          {item.toUpperCase()}
        </button>
      ))}
    </div>
  );
}

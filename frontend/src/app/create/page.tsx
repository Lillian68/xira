"use client";

import { Suspense } from "react";
import CreateClient from "./CreateClient";
import { translations } from "@/lib/i18n";
import { useLocaleStore } from "@/store/localeStore";

export default function CreatePage() {
  const locale = useLocaleStore((s) => s.locale);
  const t = translations[locale];

  return (
    <Suspense
      fallback={
        <div className="min-h-screen bg-mistfield p-8 text-sm text-primary/50">
          {t.loading}
        </div>
      }
    >
      <CreateClient />
    </Suspense>
  );
}

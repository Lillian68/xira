"use client";

import { create } from "zustand";
import { defaultLocale, type Locale } from "@/lib/i18n";

interface LocaleState {
    locale: Locale;
    setLocale: (locale: Locale) => void;
}

const STORAGE_KEY = "xira-locale";

export function readStoredLocale(): Locale | null {
    if (typeof window === "undefined") {
        return null;
    }

    const localLocale = window.localStorage.getItem(STORAGE_KEY);
    if (localLocale === "zh" || localLocale === "en") {
        return localLocale;
    }

    const cookieMatch = document.cookie.match(new RegExp(`(?:^|;\\s*)${STORAGE_KEY}=([^;]*)`));
    const cookieLocale = cookieMatch ? decodeURIComponent(cookieMatch[1]) : "";

    if (cookieLocale === "zh" || cookieLocale === "en") {
        return cookieLocale;
    }

    return null;
}

export const useLocaleStore = create<LocaleState>((set) => ({
    locale: defaultLocale,
    setLocale: (locale) => {
        set({ locale });

        if (typeof document !== "undefined") {
            document.cookie = `${STORAGE_KEY}=${encodeURIComponent(locale)}; path=/; max-age=31536000; samesite=lax`;
        }

        if (typeof window !== "undefined") {
            window.localStorage.setItem(STORAGE_KEY, locale);
        }
    },
}));

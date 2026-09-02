import type { Metadata } from "next";
import { cookies, headers } from "next/headers";
import { Noto_Sans_SC, Noto_Serif_SC } from "next/font/google";
import "./globals.css";

const notoSans = Noto_Sans_SC({
  subsets: ["latin"],
  weight: ["300", "400", "500", "600"],
  variable: "--font-sans",
  display: "swap",
});

const notoSerif = Noto_Serif_SC({
  subsets: ["latin"],
  weight: ["500", "600", "700"],
  variable: "--font-display",
  display: "swap",
});

const localeMeta = {
  zh: {
    title: "息壤",
    description:
      "知你进取，共此生息。息壤，更懂你节奏的情感陪伴型自学引擎。",
  },
  en: {
    title: "Xira",
    description:
      "Your growth, nurtured. Never study alone. Let Xira be the companion who truly understands your pace.",
  },
} as const;

function resolveLocale(locale?: string | null): keyof typeof localeMeta {
  if (locale === "zh" || locale === "zh-CN") {
    return "zh";
  }

  if (locale === "en") {
    return "en";
  }

  return "zh";
}

export async function generateMetadata(): Promise<Metadata> {
  const cookieStore = await cookies();
  const headerStore = await headers();
  const savedLocale = cookieStore.get("xira-locale")?.value;
  const acceptLanguage = headerStore.get("accept-language") ?? "";
  const locale = resolveLocale(savedLocale) === "en" || acceptLanguage.toLowerCase().startsWith("en") ? "en" : "zh";

  const meta = localeMeta[locale];

  return {
    title: meta.title,
    description: meta.description,
  };
}

export default async function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const cookieStore = await cookies();
  const headerStore = await headers();
  const savedLocale = cookieStore.get("xira-locale")?.value;
  const acceptLanguage = headerStore.get("accept-language") ?? "";
  const locale = savedLocale === "en" || acceptLanguage.toLowerCase().startsWith("en") ? "en" : "zh";

  return (
    <html
      lang={locale === "en" ? "en" : "zh-CN"}
      className={`${notoSans.variable} ${notoSerif.variable}`}
    >
      <body className="min-h-screen bg-mist font-sans antialiased">{children}</body>
    </html>
  );
}

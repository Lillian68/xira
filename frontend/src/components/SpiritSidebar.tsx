"use client";

import { useEffect, useState, FormEvent, useRef } from "react";
import { Send } from "lucide-react";
import { HerbSpiritView } from "@/components/HerbSpiritView";
import { api, listenTaskResult } from "@/lib/api";
import { translations } from "@/lib/i18n";
import type { HerbSpirit } from "@/lib/types";
import { useAuthStore } from "@/store/authStore";
import { useLocaleStore } from "@/store/localeStore";

interface Props {
  planId: number;
  planStatus: string | undefined;
  spirit: HerbSpirit;
  onSpiritChange?: (s: HerbSpirit) => void;
  externalMessage?: string;
}

export function SpiritSidebar({ planId, planStatus, spirit, onSpiritChange, externalMessage, }: Props) {
  const token = useAuthStore((s) => s.token);
  const locale = useLocaleStore((s) => s.locale);
  const t = translations[locale];
  const [message, setMessage] = useState(t.spiritListening);
  const [loading] = useState(false);

  const [chatInput, setChatInput] = useState("");
  const [sendLoading, setSendLoading] = useState(false);
  const onSpiritChangeRef = useRef(onSpiritChange);

  useEffect(() => {
    setMessage((current) => current || t.spiritListening);
  }, [t.spiritListening]);

  useEffect(() => {
    if (externalMessage) {
      setMessage(externalMessage);
    }
  }, [externalMessage]);

  useEffect(() => {
    onSpiritChangeRef.current = onSpiritChange;
  }, [onSpiritChange]);

  const sendMessage = async (e: FormEvent) => {
    e.preventDefault();
    const content = chatInput.trim();
    if (!content || sendLoading || !token) return;

    setSendLoading(true);
    setChatInput("");
    setMessage(`${t.you}：${content}`);

    try {
      const taskRes = await api<{ task_id: string }>(
        `/api/spirit/${planId}/chat`,
        { method: "POST", body: JSON.stringify({ content }) },
        token
      );
      const eventData = await listenTaskResult<{ response?: string; message?: string }>(
        taskRes.task_id,
        token
      );
      setMessage(eventData.response || eventData.message || t.spiritNoReply);
    } catch (err) {
      setMessage(err instanceof Error ? err.message : t.spiritUnavailable);
    } finally {
      setSendLoading(false);
    }
  };

  return (
    <aside className="flex h-full flex-col border-l border-primary/10 bg-secondary/40 p-4 sm:p-5">
      <div className="flex flex-col items-center">
        <HerbSpiritView
          spirit={spirit}
          planStatus={planStatus}
          size="lg"
        />
        <p className="mt-2 font-display text-lg text-soil">
          {locale === "en" ? spirit.name_en : spirit.name}
        </p>
      </div>

      <div className="mt-5 rounded-sm bg-mist/80 p-4 shadow-soft">
        <p className="font-display text-sm leading-relaxed text-primary min-h-[60px]">
          {loading ? t.spiritBreathing : message}
        </p>
      </div>

      <div className="flex-1"></div>

      <form onSubmit={sendMessage} className="mt-4 flex gap-2">
        <input
          value={chatInput}
          onChange={(e) => setChatInput(e.target.value)}
          placeholder={t.chatPlaceholder}
          className="flex-1 rounded-sm border border-primary/15 bg-secondary/40 px-3 py-2 text-sm outline-none focus:border-soil"
          disabled={sendLoading}
        />
        <button
          type="submit"
          disabled={sendLoading || !chatInput.trim()}
          className="rounded-sm bg-primary px-3 py-2 text-sm text-secondary hover:bg-soil transition disabled:opacity-50"
        >
          {sendLoading ? "..." : <Send size={16} />}
        </button>
      </form>
    </aside>
  );
}
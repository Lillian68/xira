"use client";

import { useEffect, useMemo, useState, useCallback, FormEvent, useRef } from "react";
import { useParams, useRouter } from "next/navigation";
import { CheckCircle2, ClipboardCheck, ExternalLink, Menu, X, Flag } from "lucide-react";
import { AppHeader } from "@/components/AppHeader";
import { SpiritSidebar } from "@/components/SpiritSidebar";
import { api, listenTaskResult } from "@/lib/api";
import { translations } from "@/lib/i18n";
import type { HerbSpirit, Task, StudyPlan } from "@/lib/types";
import { useAuthStore } from "@/store/authStore";
import { useLocaleStore } from "@/store/localeStore";
import { usePlanStore } from "@/store/planStore";

type TimelineItem =
  | { type: "day"; payload: Task }
  | { type: "checkpoint"; afterDay: number }
  | { type: "remedial" };

type ActiveItem =
  | { type: "day"; task: Task }
  | { type: "checkpoint"; afterDay: number }
  | { type: "remedial" };

interface CheckItem {
  id: number;
  plan_id: number;
  day_number: number;
  checklist: string;
  passed: boolean | null;
  evaluation: string | null;
  created_at?: string;
}

interface Result {
  id: number;
  plan_id: number;
  actual_result: string;
  diagnosis_detail: string;
  created_at?: string;
  target_achieved: boolean | null;
}

function getCheckpointDays(totalDays: number, interval: number | undefined | null): number[] {
  const days: number[] = [];
  if (!interval || interval <= 0 || totalDays <= 0) {
    return days;
  }
  for (let day = interval; day <= totalDays; day += interval) {
    days.push(day);
  }
  return days;
}

export default function StudyPage() {
  const params = useParams();
  const planId = Number(params.planId);
  const router = useRouter();
  const token = useAuthStore((s) => s.token);
  const locale = useLocaleStore((s) => s.locale);
  const t = translations[locale];
  const { current, fetchPlan, setCurrent } = usePlanStore();

  const [activeItem, setActiveItem] = useState<ActiveItem | null>(null);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [checking, setChecking] = useState(false);
  const [checkpointPassedMap, setCheckpointPassedMap] = useState<Record<number, boolean>>({});
  const [spiritMessage, setSpiritMessage] = useState<string | undefined>(undefined);

  const checkCacheRef = useRef<Record<number, CheckItem | null>>({});
  const initRef = useRef(false);

  useEffect(() => {
    if (!token) {
      router.replace("/login");
      return;
    }
    if (initRef.current) return;
    initRef.current = true;

    fetchPlan(planId).then(async (p) => {
      const tasks = p.tasks || [];
      const interval = p.check_interval || 0;
      const checkpointDays = getCheckpointDays(tasks.length, interval);

      const passedMap: Record<number, boolean> = {};
      let pendingCheckpoint: number | null = null;

      for (const afterDay of checkpointDays) {
        const targetDay = tasks.find((d) => d.day_number === afterDay);
        if (!targetDay?.is_completed) continue;

        let check: CheckItem | null = null;
        try {
          check = await api<CheckItem | null>(
            `/api/check/${planId}/${afterDay}`,
            { method: "GET" },
            token
          );
        } catch {
          check = null;
        }

        checkCacheRef.current[afterDay] = check;

        if (check) {
          if (check.passed === true) {
            passedMap[afterDay] = true;
          } else {
            if (pendingCheckpoint === null) {
              pendingCheckpoint = afterDay;
            }
            break;
          }
        } else {
          if (pendingCheckpoint === null) {
            pendingCheckpoint = afterDay;
          }
          break;
        }
      }

      setCheckpointPassedMap(passedMap);

      if (pendingCheckpoint !== null) {
        setActiveItem({ type: "checkpoint", afterDay: pendingCheckpoint });
      } else {
        const nextTask = tasks.find((d) => !d.is_completed);
        if (nextTask) {
          setActiveItem({ type: "day", task: nextTask });
        } else if (tasks.length > 0) {
          setActiveItem({ type: "remedial" });
        } else {
          setActiveItem(null);
        }
      }
    });
  }, [token, planId, router, fetchPlan]);

  const tasks = current?.tasks || [];
  const spirit = current?.spirit;

  const checkpointDays = useMemo(() => {
    return getCheckpointDays(tasks.length, current?.check_interval || 0);
  }, [tasks.length, current?.check_interval]);

  const firstUnfinishedDay = useMemo(() => {
    return tasks.find((item) => !item.is_completed);
  }, [tasks]);

  const isAllCompleted = useMemo(() => {
    if (!tasks.length) return false;
    return tasks.every((p) => p.is_completed);
  }, [tasks]);

  const isCheckpointPassed = (afterDay: number) => {
    return checkpointPassedMap[afterDay] === true;
  };

  const timelineItems = useMemo<TimelineItem[]>(() => {
    const result: TimelineItem[] = [];
    const checkpointDaySet = new Set(checkpointDays);

    tasks.forEach((pItem) => {
      result.push({ type: "day", payload: pItem });
      if (checkpointDaySet.has(pItem.day_number)) {
        result.push({ type: "checkpoint", afterDay: pItem.day_number });
      }
    });
    result.push({ type: "remedial" });
    return result;
  }, [tasks, checkpointDays]);

  const isCheckpointUnlocked = (afterDay: number) => {
    const targetDay = tasks.find((p) => p.day_number === afterDay);
    return !!targetDay?.is_completed;
  };

  const isDayLocked = (dayNumber: number) => {
    if (isAllCompleted) {
      return false;
    }

    if (firstUnfinishedDay && dayNumber > firstUnfinishedDay.day_number) {
      return true;
    }

    const firstFailedCheckpoint = checkpointDays.find(
      (afterDay) => !isCheckpointPassed(afterDay)
    );

    if (firstFailedCheckpoint !== undefined && dayNumber > firstFailedCheckpoint) {
      return true;
    }

    return false;
  };

  const contentHtml = useMemo(() => {
    if (!activeItem || activeItem.type !== "day") return "";
    const day = activeItem.task;
    return day.content
      .replace(/^### (.*)$/gm, '<h3 class="mt-4 font-display text-lg text-soil">$1</h3>')
      .replace(/^## (.*)$/gm, '<h2 class="mt-5 font-display text-xl text-soil">$1</h2>')
      .replace(/^- (.*)$/gm, '<li class="ml-4 list-disc text-primary/80">$1</li>')
      .replace(/\n\n/g, "<br/><br/>");
  }, [activeItem]);

  const checkin = async () => {
    if (!token) return;
    if (!activeItem || activeItem.type !== "day" || activeItem.task.is_completed) return;
    setChecking(true);
    try {
      await api(`/api/task/${activeItem.task.id}/checkin`, { method: "POST" }, token);

      let spiritMsg = "";
      try {
        const taskRes = await api<{ task_id: string }>(
          `/api/spirit/${planId}/dialogue`,
          {},
          token
        );
        const eventData = await listenTaskResult<{ message: string }>(
          taskRes.task_id,
          token
        );
        spiritMsg = eventData.message;
      } catch {
        spiritMsg = t.spiritCheckinCelebration;
      }
      setSpiritMessage(spiritMsg);

      const plan = await fetchPlan(planId);
      const tasks = plan.tasks || [];

      if (activeItem.type === "day") {
        const updatedTask = tasks.find((d) => d.id === activeItem.task.id);
        if (updatedTask) {
          setActiveItem({ type: "day", task: updatedTask });
        }
      }

      const completedDayNumber = activeItem.task.day_number;
      if (checkpointDays.includes(completedDayNumber)) {
        checkCacheRef.current[completedDayNumber] = null;
        setActiveItem({ type: "checkpoint", afterDay: completedDayNumber });
      }

    } finally {
      setChecking(false);
    }
  };

  const onSpiritChange = useCallback((s: HerbSpirit) => {
    if (!current) return;
    setCurrent({ ...current, spirit: s } as StudyPlan);
  }, [current, setCurrent]);

  const handleCheckpointPassedChange = useCallback((afterDay: number, passed: boolean) => {
    setCheckpointPassedMap((prev) => ({ ...prev, [afterDay]: passed }));
  }, []);

  const handlePlanAdjusted = useCallback(async (adjustedAfterDay: number) => {
    const plan = await fetchPlan(planId);
    const tasks = plan.tasks || [];
    const interval = plan.check_interval || 0;
    const newCheckpointDays = getCheckpointDays(tasks.length, interval);

    setCheckpointPassedMap((prev) => {
      const newMap: Record<number, boolean> = {};
      for (const day of newCheckpointDays) {
        if (prev[day] || day === adjustedAfterDay) {
          newMap[day] = true;
        }
      }
      return newMap;
    });

    checkCacheRef.current = {};

    const nextTask = tasks.find((d) => !d.is_completed);
    if (nextTask) {
      setActiveItem({ type: "day", task: nextTask });
    } else if (tasks.length > 0) {
      setActiveItem({ type: "remedial" });
    } else {
      setActiveItem(null);
    }
  }, [fetchPlan, planId]);

  const handlePlanAdjustedFromRemedial = useCallback(async () => {
    const plan = await fetchPlan(planId);
    const tasks = plan.tasks || [];
    const interval = plan.check_interval || 0;
    const newCheckpointDays = getCheckpointDays(tasks.length, interval);

    setCheckpointPassedMap((prev) => {
      const newMap: Record<number, boolean> = {};
      for (const day of newCheckpointDays) {
        if (prev[day]) newMap[day] = true;
      }
      return newMap;
    });

    checkCacheRef.current = {};

    const nextTask = tasks.find((d) => !d.is_completed);
    if (nextTask) {
      setActiveItem({ type: "day", task: nextTask });
    } else if (tasks.length > 0) {
      setActiveItem({ type: "remedial" });
    } else {
      setActiveItem(null);
    }
  }, [fetchPlan, planId]);

  if (!current) {
    return (
      <div className="min-h-screen bg-mistfield">
        <AppHeader />
        <p className="p-8 text-sm text-primary/50">{t.studyLoading}</p>
      </div>
    );
  }

  return (
    <div className="flex min-h-screen flex-col bg-mist">
      <AppHeader />
      <div className="mx-auto flex w-full max-w-6xl flex-1 flex-col lg:flex-row">
        <section className="flex-1 px-4 py-6 sm:px-6">
          <div className="mb-4 flex flex-wrap items-center justify-between gap-3">
            <div>
              <p className="text-sm text-primary/60">{current.target}</p>
            </div>
            <div className="flex flex-wrap gap-2">
              <button
                type="button"
                className="inline-flex items-center gap-1 rounded-sm bg-secondary px-3 py-1.5 text-xs lg:hidden"
                onClick={() => setSidebarOpen(true)}
              >
                <Menu className="h-3.5 w-3.5" />
                {t.spiritLabel}
              </button>
            </div>
          </div>

          <div className="mb-5 flex gap-2 overflow-x-auto pb-1">
            {timelineItems.map((item, idx) => {
              if (item.type === "day") {
                const d = item.payload;
                const isLocked = isDayLocked(d.day_number);
                const isActive = activeItem?.type === "day" && activeItem.task.id === d.id;
                return (
                  <button
                    key={`day-${d.id}`}
                    type="button"
                    onClick={() => {
                      if (!isLocked) setActiveItem({ type: "day", task: d });
                    }}
                    disabled={isLocked}
                    className={`shrink-0 rounded-sm px-3 py-1.5 text-xs transition ${isLocked
                      ? "bg-gray-200 text-gray-400 cursor-not-allowed"
                      : isActive
                        ? "bg-soil text-secondary"
                        : d.is_completed
                          ? "bg-growth/25 text-primary"
                          : "bg-secondary text-primary/70"
                      }`}
                  >
                    D{d.day_number}
                    {isLocked && ` 🔒`}
                  </button>
                );
              } else if (item.type === "checkpoint") {
                const unlocked = isCheckpointUnlocked(item.afterDay);
                const isActive = activeItem?.type === "checkpoint" && activeItem.afterDay === item.afterDay;
                const passed = isCheckpointPassed(item.afterDay);
                return (
                  <button
                    key={`cp-${idx}`}
                    type="button"
                    disabled={!unlocked}
                    onClick={() => {
                      if (unlocked) {
                        setActiveItem({ type: "checkpoint", afterDay: item.afterDay });
                      }
                    }}
                    className={`shrink-0 inline-flex items-center gap-1 rounded-sm border border-primary/20 px-3 py-1.5 text-xs transition ${isActive
                      ? "bg-soil text-secondary"
                      : passed
                        ? "bg-growth/25 text-primary"
                        : unlocked
                          ? "bg-secondary text-primary hover:bg-secondary/80"
                          : "bg-gray-200 text-gray-400 cursor-not-allowed"
                      }`}
                  >
                    <ClipboardCheck className="h-3.5 w-3.5" />
                    {t.stageCheck}
                    {passed && " ✓"}
                    {!unlocked && ` 🔒`}
                  </button>
                );
              } else if (item.type === "remedial") {
                const unlocked = isAllCompleted;
                const isActive = activeItem?.type === "remedial";
                return (
                  <button
                    key={`remedial-${idx}`}
                    type="button"
                    disabled={!unlocked}
                    onClick={() => {
                      if (unlocked) {
                        setActiveItem({ type: "remedial" });
                      }
                    }}
                    className={`shrink-0 inline-flex items-center gap-1 rounded-sm border border-primary/20 px-3 py-1.5 text-xs transition ${isActive
                      ? "bg-soil text-secondary"
                      : unlocked
                        ? "bg-secondary text-primary hover:bg-secondary/80"
                        : "bg-gray-200 text-gray-400 cursor-not-allowed"
                      }`}
                  >
                    <Flag className="h-3.5 w-3.5" />
                    {t.finalFeedback}
                    {!unlocked && ` 🔒`}
                  </button>
                );
              }
              return null;
            })}
          </div>

          {activeItem?.type === "day" && (
            <article className="rounded-sm bg-mist p-5 shadow-soft sm:p-7">
              <div className="flex flex-wrap items-start justify-between gap-3">
                <h2 className="font-display text-xl text-soil">
                  {t.dayShort} {activeItem.task.day_number} {locale === "en" ? "·" : "日 ·"} {activeItem.task.title}
                </h2>
                <div className="flex flex-wrap gap-2 items-center">
                  {activeItem.task.is_completed ? (
                    <span className="inline-flex items-center gap-1 text-sm text-growth">
                      <CheckCircle2 className="h-4 w-4" />
                      {t.completed}
                    </span>
                  ) : (
                    <button
                      type="button"
                      disabled={checking}
                      onClick={checkin}
                      className="rounded-sm bg-growth px-4 py-2 text-sm text-mist disabled:opacity-60"
                    >
                      {checking ? t.checkinInProgress : t.completeCheckin}
                    </button>
                  )}
                </div>
              </div>

              <div
                className="prose-xira mt-5 text-sm leading-relaxed text-primary/85"
                dangerouslySetInnerHTML={{ __html: contentHtml }}
              />

              {activeItem.task.resources?.length > 0 && (
                <div className="mt-6">
                  <p className="text-xs text-primary/50">{locale === "en" ? "Resources" : "资源垄道"}</p>
                  <ul className="mt-2 space-y-2">
                    {activeItem.task.resources.map((r, index) => (
                      <li key={`${r.url}-${r.title}-${index}`}>
                        <a
                          href={r.url}
                          target="_blank"
                          rel="noreferrer"
                          className="inline-flex items-center gap-2 text-sm text-growth hover:underline"
                        >
                          <ExternalLink className="h-3.5 w-3.5" />
                          [{r.platform}] {r.title}
                        </a>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </article>
          )}

          {activeItem?.type === "checkpoint" && (
            <CheckpointPanel
              planId={planId}
              afterDay={activeItem.afterDay}
              initialCheck={checkCacheRef.current[activeItem.afterDay]}
              onPassedChange={handleCheckpointPassedChange}
              onPlanAdjusted={handlePlanAdjusted}
            />
          )}

          {activeItem?.type === "remedial" && (
            <RemedialPanel
              planId={planId}
              onPlanAdjusted={handlePlanAdjustedFromRemedial}
            />
          )}
        </section>

        <div className="hidden w-80 shrink-0 lg:block">
          {spirit && (
            <SpiritSidebar
              planId={planId}
              planStatus={current.status}
              spirit={spirit}
              onSpiritChange={onSpiritChange}
              externalMessage={spiritMessage}
            />
          )}
        </div>
      </div>

      {sidebarOpen && spirit && (
        <div className="fixed inset-0 z-50 flex lg:hidden">
          <button
            type="button"
            className="flex-1 bg-soil/40"
            aria-label={t.close}
            onClick={() => setSidebarOpen(false)}
          />
          <div className="relative w-[85%] max-w-sm bg-mist" key={Number(sidebarOpen)}>
            <button
              type="button"
              className="absolute right-3 top-3 z-10"
              onClick={() => setSidebarOpen(false)}
            >
              <X className="h-5 w-5 text-primary" />
            </button>
            <SpiritSidebar
              planId={planId}
              planStatus={current.status}
              spirit={spirit}
              onSpiritChange={onSpiritChange}
              externalMessage={spiritMessage}
            />
          </div>
        </div>
      )}
    </div>
  );
}

function CheckpointPanel({
  planId,
  afterDay,
  initialCheck,
  onPassedChange,
  onPlanAdjusted,
}: {
  planId: number;
  afterDay: number;
  initialCheck?: CheckItem | null;
  onPassedChange?: (afterDay: number, passed: boolean) => void;
  onPlanAdjusted?: (afterDay: number) => void | Promise<void>;
}) {
  const token = useAuthStore((s) => s.token);
  const locale = useLocaleStore((s) => s.locale);
  const t = translations[locale];
  const [check, setCheck] = useState<CheckItem | null>(initialCheck || null);
  const [inputText, setInputText] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const onPassedChangeRef = useRef(onPassedChange);
  useEffect(() => {
    onPassedChangeRef.current = onPassedChange;
  }, [onPassedChange]);

  const onPlanAdjustedRef = useRef(onPlanAdjusted);
  useEffect(() => {
    onPlanAdjustedRef.current = onPlanAdjusted;
  }, [onPlanAdjusted]);

  const requestInitiatedRef = useRef(false);
  const submittingRef = useRef(false);

  useEffect(() => {
    if (initialCheck) {
      setCheck(initialCheck);
      if (initialCheck.passed !== null && initialCheck.passed !== undefined) {
        onPassedChangeRef.current?.(afterDay, initialCheck.passed);
      }
      requestInitiatedRef.current = true;
    } else if (initialCheck === null) {
      setCheck(null);
      requestInitiatedRef.current = false;
    }
  }, [initialCheck, afterDay]);

  useEffect(() => {
    if (check || requestInitiatedRef.current) return;

    requestInitiatedRef.current = true;

    const loadCheck = async () => {
      if (!token) return;
      setLoading(true);
      setError("");
      try {
        let data: CheckItem | null = null;
        if (initialCheck === null) {
          const taskRes = await api<{ task_id: string }>(
            `/api/check/${planId}/${afterDay}`,
            { method: "POST" },
            token
          );
          const eventData = await listenTaskResult<{ check: CheckItem }>(
            taskRes.task_id,
            token
          );
          data = eventData.check;
        } else {
          try {
            data = await api<CheckItem | null>(
              `/api/check/${planId}/${afterDay}`,
              { method: "GET" },
              token
            );
          } catch {
            const taskRes = await api<{ task_id: string }>(
              `/api/check/${planId}/${afterDay}`,
              { method: "POST" },
              token
            );
            const eventData = await listenTaskResult<{ check: CheckItem }>(
              taskRes.task_id,
              token
            );
            data = eventData.check;
          }
        }

        if (data) {
          setCheck(data);
          if (data.passed !== null && data.passed !== undefined) {
            onPassedChangeRef.current?.(afterDay, data.passed);
          }
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : t.fetchStageCheckFailed);
      } finally {
        setLoading(false);
      }
    };

    loadCheck();
  }, [planId, afterDay, token, check, initialCheck]);

  const handleSubmit = async () => {
    if (!token) return;
    if (!check || !inputText.trim() || submittingRef.current) return;
    submittingRef.current = true;
    setLoading(true);
    setError("");
    try {
      const taskRes = await api<{ task_id: string }>(
        `/api/check/submit/${check.id}`,
        { method: "POST", body: JSON.stringify({ assessment: inputText }) },
        token
      );
      const eventData = await listenTaskResult<{ checkpoint: CheckItem }>(
        taskRes.task_id,
        token
      );
      const checkpoint = eventData.checkpoint;
      setCheck(checkpoint);

      if (checkpoint.passed !== null && checkpoint.passed !== undefined) {
        onPassedChangeRef.current?.(afterDay, checkpoint.passed);
      }

      if (checkpoint.passed === false) {
        try {
          const adjustTaskRes = await api<{ task_id: string }>(
            `/api/plans/update/${planId}`,
            { method: "POST" },
            token
          );
          await listenTaskResult(adjustTaskRes.task_id, token);
          await onPlanAdjustedRef.current?.(afterDay);
        } catch (adjustErr) {
          setError(adjustErr instanceof Error ? adjustErr.message : t.planAdjustmentFailed);
        }
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : t.submitFailed);
    } finally {
      setLoading(false);
      submittingRef.current = false;
    }
  };

  if (loading && !check) {
    return (
      <article className="rounded-sm bg-mist p-5 shadow-soft sm:p-7">
        <h2 className="font-display text-xl text-soil">{t.stageCheckTitle}</h2>
        <p className="mt-4 text-sm text-primary/80">{t.generatingChecklist}</p>
      </article>
    );
  }

  if (error && !check) {
    return (
      <article className="rounded-sm bg-mist p-5 shadow-soft sm:p-7">
        <h2 className="font-display text-xl text-soil">{t.stageCheckTitle}</h2>
        <p className="mt-4 text-sm text-red-600">{error}</p>
      </article>
    );
  }

  const isSubmitted = check?.passed !== null && check?.passed !== undefined;

  return (
    <article className="rounded-sm bg-mist p-5 shadow-soft sm:p-7">
      <h2 className="font-display text-xl text-soil">
        {t.stageCheckAfterDay.replace("{day}", String(afterDay))}
      </h2>

      {!isSubmitted && check && (
        <>
          <p className="mt-4 text-sm text-primary/80">
            {check.checklist || t.selfFeedback}
          </p>

          <textarea
            className="mt-4 min-h-28 w-full rounded-sm border border-primary/15 bg-secondary/40 px-3 py-2 text-sm"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            placeholder={t.selfFeedbackPlaceholder}
            disabled={loading}
          />

          {error && <p className="mt-2 text-sm text-red-700/80">{error}</p>}

          <button
            type="button"
            onClick={handleSubmit}
            disabled={loading || !inputText.trim() || submittingRef.current}
            className="mt-4 rounded-sm bg-soil px-4 py-2 text-sm text-secondary disabled:opacity-60"
          >
            {loading ? t.submittingFeedback : t.submitFeedback}
          </button>
        </>
      )}

      {isSubmitted && check && (
        <div className="mt-6 rounded-sm border border-growth/30 bg-secondary/40 p-5">
          <p className="font-display text-xl text-soil">
            {check.passed ? t.passed : t.needsStrengthening}
          </p>
          {check.evaluation ? (
            <p className="mt-3 text-sm text-primary/80 whitespace-pre-wrap">
              {check.evaluation}
            </p>
          ) : (
            <p className="mt-3 text-sm text-primary/70">{t.noEvaluation}</p>
          )}
          {error && <p className="mt-2 text-sm text-red-700/80">{error}</p>}
        </div>
      )}
    </article>
  );
}

function RemedialPanel({
  planId,
  onPlanAdjusted,
}: {
  planId: number;
  onPlanAdjusted?: () => void | Promise<void>;
}) {
  const token = useAuthStore((s) => s.token);
  const locale = useLocaleStore((s) => s.locale);
  const t = translations[locale];
  const [actual, setActual] = useState("");
  const [result, setResult] = useState<Result | null>(null);
  const [loading, setLoading] = useState(false);
  const [initialLoading, setInitialLoading] = useState(true);
  const [submitError, setSubmitError] = useState("");
  const [adjustError, setAdjustError] = useState("");

  const initRef = useRef(false);
  const submittingRef = useRef(false);

  const onPlanAdjustedRef = useRef(onPlanAdjusted);
  useEffect(() => {
    onPlanAdjustedRef.current = onPlanAdjusted;
  }, [onPlanAdjusted]);

  useEffect(() => {
    if (initRef.current) return;
    initRef.current = true;

    const fetchResult = async () => {
      try {
        const res = await api<{ result: Result | null }>(
          `/api/result/${planId}`,
          { method: "GET" },
          token
        );
        if (res.result && Object.keys(res.result).length > 0) {
          setResult(res.result);
        }
      } catch {
      } finally {
        setInitialLoading(false);
      }
    };
    fetchResult();
  }, [planId, token]);

  const onSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (submittingRef.current) return;
    submittingRef.current = true;
    if (!token) return;
    setLoading(true);
    setSubmitError("");
    setAdjustError("");
    try {
      const taskRes = await api<{ task_id: string }>(
        `/api/result/${planId}`,
        { method: "POST", body: JSON.stringify({ actual_result: actual }) },
        token
      );
      const eventData = await listenTaskResult<{ result: Result }>(
        taskRes.task_id,
        token
      );
      setResult(eventData.result);

      if (eventData.result.target_achieved === false) {
        try {
          const adjustTaskRes = await api<{ task_id: string }>(
            `/api/plans/update/${planId}`,
            { method: "POST" },
            token
          );
          await listenTaskResult(adjustTaskRes.task_id, token);
          await onPlanAdjustedRef.current?.();
        } catch (adjustErr) {
          setAdjustError(adjustErr instanceof Error ? adjustErr.message : t.planAdjustmentFailed);
        }
      }
    } catch (err) {
      setSubmitError(err instanceof Error ? err.message : t.submitFailed);
    } finally {
      setLoading(false);
      submittingRef.current = false;
    }
  };

  if (initialLoading) {
    return (
      <article className="rounded-sm bg-mist p-5 shadow-soft sm:p-7">
        <h2 className="font-display text-xl text-soil">{t.finalFeedback}</h2>
        <p className="mt-4 text-sm text-primary/60">{t.loadingDiagnosis}</p>
      </article>
    );
  }

  if (result) {
    return (
      <article className="rounded-sm bg-mist p-5 shadow-soft sm:p-7">
        <h2 className="font-display text-xl text-soil">{t.finalFeedback}</h2>
        <div className="mt-8 rounded-sm bg-soilbed p-5 text-secondary">
          <p className="text-xs text-wither/80">{t.diagnosisDetail}</p>
          <p className="mt-2 whitespace-pre-wrap text-sm text-secondary/85">
            {result.diagnosis_detail || t.noDiagnosis}
          </p>
        </div>
        {adjustError && (
          <p className="mt-4 text-sm text-red-700/80">{adjustError}</p>
        )}
      </article>
    );
  }

  return (
    <article className="rounded-sm bg-mist p-5 shadow-soft sm:p-7">
      <h2 className="font-display text-xl text-soil">{t.finalFeedback}</h2>
      <p className="mt-2 text-sm text-primary/65">
        {t.remedialPrompt}
      </p>

      <form onSubmit={onSubmit} className="space-y-4 rounded-sm p-6">
        <label className="block text-sm">
          <textarea
            className="mt-1 min-h-24 w-full rounded-sm border border-primary/15 bg-mist px-3 py-2"
            value={actual}
            onChange={(e) => setActual(e.target.value)}
            placeholder={t.remedialPlaceholder}
            required
          />
        </label>
        {submitError && <p className="text-sm text-red-700/80">{submitError}</p>}
        <button
          type="submit"
          disabled={loading || submittingRef.current}
          className="rounded-sm bg-soil px-4 py-2 text-sm text-secondary disabled:opacity-60"
        >
          {loading ? t.submittingResult : t.submitResult}
        </button>
      </form>
    </article>
  );
}
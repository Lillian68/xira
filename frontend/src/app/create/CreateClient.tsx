"use client";

import { useEffect, useRef, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import Image from "next/image";
import DatePicker, { registerLocale } from "react-datepicker";
import { enUS, zhCN } from "date-fns/locale";
import "react-datepicker/dist/react-datepicker.css";
import { AppHeader } from "@/components/AppHeader";
import { translations } from "@/lib/i18n";
import type { HerbSpirit } from "@/lib/types";
import { listenTaskResult } from "@/lib/api";
import { useAuthStore } from "@/store/authStore";
import { useLocaleStore } from "@/store/localeStore";
import { usePlanStore } from "@/store/planStore";

registerLocale("en-US", enUS);
registerLocale("zh-CN", zhCN);

export default function CreateClient() {
  const router = useRouter();
  const search = useSearchParams();
  const planIdParam = search.get("planId");
  const token = useAuthStore((s) => s.token);
  const locale = useLocaleStore((s) => s.locale);
  const t = translations[locale];
  const {
    current,
    generating,
    error,
    createFromInterview,
    fetchPlan,
    setCurrent,
  } = usePlanStore();

  const steps = [
    t.createStepObservation,
    t.createStepListening,
    t.createStepInquiry,
    t.createStepDiagnosis,
  ] as const;

  const [step, setStep] = useState(0);
  const [target, setTarget] = useState("");
  const [targetType, setTargetType] = useState("EXAM");
  const [currentStage, setCurrentStage] = useState("");
  const [dailyMinutes, setDailyMinutes] = useState(60);
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [checkIntervalDays, setCheckIntervalDays] = useState(3);
  const [committing, setCommitting] = useState(false);
  const [formError, setFormError] = useState("");

  const [showLicoriceModal, setShowLicoriceModal] = useState(false);
  const [modalSpirit, setModalSpirit] = useState<HerbSpirit | null>(null);

  const abortControllerRef = useRef<AbortController | null>(null);

  const getTodayStr = () => {
    const now = new Date();
    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, "0");
    const day = String(now.getDate()).padStart(2, "0");
    return `${year}-${month}-${day}`;
  };
  const todayStr = getTodayStr();
  const dateInputLang = locale === "en" ? "en-US" : "zh-CN";
  const dateFormat = locale === "en" ? "MM/dd/yyyy" : "yyyy/MM/dd";

  const formatDateValue = (date: Date | null) => {
    if (!date) return "";
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, "0");
    const day = String(date.getDate()).padStart(2, "0");
    return `${year}-${month}-${day}`;
  };

  useEffect(() => {
    if (typeof document !== "undefined") {
      document.documentElement.lang = locale === "en" ? "en" : "zh-CN";
    }
  }, [locale]);

  useEffect(() => {
    if (!token) router.replace("/login");
  }, [token, router]);

  useEffect(() => {
    if (planIdParam) {
      fetchPlan(Number(planIdParam));
    } else {
      setCurrent(null);
    }
  }, [planIdParam, fetchPlan, setCurrent]);

  useEffect(() => {
    abortControllerRef.current = new AbortController();
    return () => {
      abortControllerRef.current?.abort();
    };
  }, []);

  const handleNext = () => {
    setFormError("");

    if (step === 0) {
      if (!currentStage.trim()) {
        setFormError(t.currentStageRequired);
        return;
      }
    }
    else if (step === 1) {
      if (!target.trim()) {
        setFormError(t.targetRequired);
        return;
      }
    }
    else if (step === 2) {
      if (!dailyMinutes || dailyMinutes < 15 || dailyMinutes > 120) {
        setFormError(t.dailyMinutesRequired);
        return;
      }
      if (!startDate || !endDate) {
        setFormError(t.dateRequired);
        return;
      }
      if (new Date(startDate) < new Date(todayStr)) {
        setFormError(t.startDatePast);
        return;
      }
      if (new Date(startDate) > new Date(endDate)) {
        setFormError(t.endDateBeforeStart);
        return;
      }
      const totalDays = Math.floor(
        (new Date(endDate).getTime() - new Date(startDate).getTime()) / (1000 * 60 * 60 * 24)
      ) + 1;
      if (totalDays > 7) {
        setFormError(t.totalDaysTooLong);
        return;
      }
      if (!checkIntervalDays || checkIntervalDays < 1) {
        setFormError(t.checkIntervalRequired);
        return;
      }
      if (checkIntervalDays >= totalDays) {
        setFormError(t.checkIntervalTooLarge);
        return;
      }
    }

    setStep((s) => s + 1);
  };

  const handleSubmit = async () => {
    setFormError("");

    if (!target.trim()) {
      setFormError(t.targetRequired);
      return;
    }
    if (!currentStage.trim()) {
      setFormError(t.currentStageRequired);
      return;
    }
    if (!dailyMinutes || dailyMinutes < 15 || dailyMinutes > 120) {
      setFormError(t.dailyMinutesRequired);
      return;
    }
    if (!startDate || !endDate) {
      setFormError(t.dateRequired);
      return;
    }
    if (new Date(startDate) < new Date(todayStr)) {
      setFormError(t.startDatePast);
      return;
    }
    if (new Date(startDate) > new Date(endDate)) {
      setFormError(t.endDateBeforeStart);
      return;
    }
    const totalDays = Math.floor(
      (new Date(endDate).getTime() - new Date(startDate).getTime()) / (1000 * 60 * 60 * 24)
    ) + 1;
    if (totalDays > 7) {
      setFormError(t.totalDaysTooLong);
      return;
    }
    if (!checkIntervalDays || checkIntervalDays < 1) {
      setFormError(t.checkIntervalRequired);
      return;
    }
    if (checkIntervalDays >= totalDays) {
      setFormError(t.checkIntervalTooLarge);
      return;
    }
    if (!token) {
      setFormError(t.loginRequired);
      return;
    }

    setCommitting(true);
    try {
      const response = await createFromInterview({
        target,
        target_type: targetType,
        current_stage: currentStage,
        daily_minutes: dailyMinutes,
        start_date: startDate,
        end_date: endDate,
        check_interval_days: checkIntervalDays,
        platform: locale === "en" ? "YouTube" : "bilibili",
        language: locale
      });

      const taskId = response.task_id;
      const planId = response.plan.id;

      if (!taskId) {
        throw new Error(t.taskIdMissing);
      }

      await listenTaskResult(taskId, token);

      const freshPlan = await fetchPlan(planId);
      if (freshPlan?.spirit) {
        setModalSpirit(freshPlan.spirit);
        setShowLicoriceModal(true);
      }
      router.replace(`/create?planId=${planId}`);
    } catch (err: any) {
      setFormError(err.message || t.submitFailed);
    } finally {
      setCommitting(false);
    }
  };

  const closeModalAndGoStudy = () => {
    setShowLicoriceModal(false);
    setModalSpirit(null);
    if (current) router.push(`/study/${current.id}`);
  };

  const showError = formError || error;

  return (
    <div
      className="min-h-screen bg-mistfield flex flex-col"
      style={{
        backgroundImage: "url('/background.png')",
        backgroundSize: "cover",
        backgroundPosition: "center",
        backgroundRepeat: "no-repeat",
      }}
    >
      <AppHeader />
      <main className="flex-grow flex items-center justify-center px-4 py-8 sm:px-6">
        <div className="w-full max-w-5xl rounded-lg bg-mist/75 p-6 shadow-lg">
          <h1 className="font-display text-3xl text-soil">{t.createTitle}</h1>
          <p className="mt-2 text-sm text-primary/65">{t.createSubtitle}</p>

          <div className="mt-6 flex flex-wrap gap-2">
            {steps.map((label, i) => (
              <span
                key={label}
                className={`rounded-sm px-3 py-1 text-xs ${i === step
                  ? "bg-soil text-secondary"
                  : i < step
                    ? "bg-growth/20 text-primary"
                    : "bg-secondary text-primary/50"
                  }`}
              >
                {label}
              </span>
            ))}
          </div>

          <form
            className="mt-8 max-w-xl space-y-5 rounded-sm bg-mist/80 p-6 shadow-soft"
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                e.preventDefault();
              }
            }}
          >
            {step === 0 && (
              <div>
                <label className="block text-sm">
                  {t.currentStageLabel}
                  <textarea
                    className="mt-1 w-full rounded-sm border border-primary/15 bg-secondary/40 px-3 py-2 min-h-[100px]"
                    value={currentStage}
                    onChange={(e) => setCurrentStage(e.target.value)}
                    placeholder={t.currentStagePlaceholder}
                    required
                  />
                </label>
              </div>
            )}

            {step === 1 && (
              <div>
                <label className="block text-sm">
                  {t.targetLabel}
                  <input
                    className="mt-1 w-full rounded-sm border border-primary/15 bg-secondary/40 px-3 py-2"
                    value={target}
                    onChange={(e) => setTarget(e.target.value)}
                    placeholder={t.targetPlaceholder}
                    required
                  />
                </label>
                <label className="block text-sm mt-4">
                  {t.targetTypeLabel}
                  <select
                    className="mt-1 w-full rounded-sm border border-primary/15 bg-secondary/40 px-3 py-2"
                    value={targetType}
                    onChange={(e) => setTargetType(e.target.value)}
                    required
                  >
                    <option value="EXAM">{t.targetTypeExam}</option>
                    <option value="PRACTICE">{t.targetTypePractice}</option>
                  </select>
                </label>
              </div>
            )}

            {step === 2 && (
              <div>
                <label className="block text-sm">
                  {t.dailyMinutesLabel}
                  <input
                    type="number"
                    min={15}
                    max={120}
                    className="mt-1 w-full rounded-sm border border-primary/15 bg-secondary/40 px-3 py-2"
                    value={dailyMinutes}
                    onChange={(e) => setDailyMinutes(Number(e.target.value))}
                    required
                  />
                </label>
                <label className="block text-sm mt-4">
                  {t.startDateLabel}
                  <DatePicker
                    key={`${locale}-start`}
                    locale={dateInputLang === "en-US" ? enUS : zhCN}
                    selected={startDate ? new Date(startDate) : null}
                    onChange={(date: Date | null) => {
                      setStartDate(formatDateValue(date));
                      setFormError("");
                    }}
                    minDate={new Date(todayStr)}
                    dateFormat={dateFormat}
                    className="mt-1 w-full rounded-sm border border-primary/15 bg-secondary/40 px-3 py-2"
                    wrapperClassName="block w-full"
                    placeholderText={locale === "en" ? "Select start date" : "请选择起始日期"}
                  />
                </label>
                <label className="block text-sm mt-4">
                  {t.endDateLabel}
                  <DatePicker
                    key={`${locale}-end`}
                    locale={dateInputLang === "en-US" ? enUS : zhCN}
                    selected={endDate ? new Date(endDate) : null}
                    onChange={(date: Date | null) => {
                      setEndDate(formatDateValue(date));
                      setFormError("");
                    }}
                    minDate={startDate ? new Date(startDate) : undefined}
                    dateFormat={dateFormat}
                    className="mt-1 w-full rounded-sm border border-primary/15 bg-secondary/40 px-3 py-2"
                    wrapperClassName="block w-full"
                    placeholderText={locale === "en" ? "Select end date" : "请选择结束日期"}
                  />
                </label>
                <label className="block text-sm mt-4">
                  {t.checkIntervalLabel}
                  <input
                    type="number"
                    min={1}
                    className="mt-1 w-full rounded-sm border border-primary/15 bg-secondary/40 px-3 py-2"
                    value={checkIntervalDays}
                    onChange={(e) => {
                      setCheckIntervalDays(Number(e.target.value));
                      setFormError("");
                    }}
                  />
                  <p className="mt-0.5 text-xs text-primary/60">{t.checkIntervalHint}</p>
                </label>
              </div>
            )}

            {step === 3 && (
              <div className="space-y-3 text-sm">
                <div className="rounded-sm bg-secondary/60 p-4 space-y-2">
                  <p>
                    <span className="font-medium">{t.targetLabel}：</span>
                    {target}（{targetType === "EXAM" ? t.targetTypeExam : t.targetTypePractice}）
                  </p>
                  <p>
                    <span className="font-medium">{t.currentStageLabel}：</span>
                    {currentStage}
                  </p>
                  <p>
                    <span className="font-medium">{t.dailyMinutesLabel}：</span>
                    {dailyMinutes}
                  </p>
                  <p>
                    <span className="font-medium">{t.startDateLabel}：</span>
                    {startDate}
                  </p>
                  <p>
                    <span className="font-medium">{t.endDateLabel}：</span>
                    {endDate}
                  </p>
                  <p>
                    <span className="font-medium">{t.checkIntervalLabel}：</span>
                    {checkIntervalDays}
                  </p>
                </div>
              </div>
            )}

            {showError && <p className="text-sm text-red-700/80">{showError}</p>}

            <div className="flex gap-3">
              {step > 0 && (
                <button
                  type="button"
                  onClick={() => {
                    setFormError("");
                    setStep((s) => s - 1);
                  }}
                  className="rounded-sm border border-primary/20 px-4 py-2 text-sm"
                >
                  {t.previousStep}
                </button>
              )}

              {step < 3 ? (
                <button
                  type="button"
                  onClick={handleNext}
                  className="rounded-sm bg-soil px-4 py-2 text-sm text-secondary"
                >
                  {t.nextStep}
                </button>
              ) : (
                <button
                  type="button"
                  onClick={handleSubmit}
                  disabled={generating || committing}
                  className="rounded-sm bg-soil px-4 py-2 text-sm text-secondary disabled:opacity-60"
                >
                  {generating
                    ? t.generating
                    : committing
                      ? t.loadingSpirit
                      : t.generatePlan}
                </button>
              )}
            </div>
          </form>
        </div>
      </main>

      {showLicoriceModal && modalSpirit && (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm"
          onClick={closeModalAndGoStudy}
        >
          <div
            className="bg-white rounded-lg p-6 max-w-sm w-full mx-4 shadow-xl"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex justify-center mb-4">
              <div className="relative w-[220px] h-[220px]">
                <Image
                  src={`/spirits/${modalSpirit.img_prefix}_mature.png`}
                  alt={locale === "en" ? modalSpirit.name_en : modalSpirit.name}
                  fill
                  sizes="220px"
                  className="rounded object-contain"
                />
              </div>
            </div>
            <h3 className="text-xl font-bold text-center text-soil mb-2">
              {locale === "en" ? modalSpirit.name_en : modalSpirit.name}
            </h3>
            <p className="text-gray-600 text-center mb-6">
              {locale === "en" ? modalSpirit.desc_en : modalSpirit.desc}
            </p>
            <button
              onClick={closeModalAndGoStudy}
              className="w-full rounded-sm bg-soil py-2 text-white text-sm"
            >
              {t.confirmSpirit}
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
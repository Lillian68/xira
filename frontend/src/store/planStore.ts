"use client";

import { create } from "zustand";
import { api } from "@/lib/api";
import type { StudyPlan } from "@/lib/types";
import { useAuthStore } from "@/store/authStore";

export interface CreatePlanResponse {
  task_id: string;
  plan: StudyPlan;
}

interface PlanState {
  plans: StudyPlan[];
  current: StudyPlan | null;
  loading: boolean;
  generating: boolean;
  error: string | null;
  fetchPlans: () => Promise<void>;
  fetchPlan: (id: number) => Promise<StudyPlan>;
  createFromInterview: (interview: Record<string, unknown>) => Promise<CreatePlanResponse>;
  setCurrent: (plan: StudyPlan | null) => void;
}

function token() {
  return useAuthStore.getState().token;
}

export const usePlanStore = create<PlanState>((set) => ({
  plans: [],
  current: null,
  loading: false,
  generating: false,
  error: null,
  setCurrent: (plan) => set({ current: plan }),
  fetchPlans: async () => {
    set({ loading: true, error: null });
    try {
      const data = await api<{ plans: StudyPlan[] }>(
        "/api/plans",
        {},
        token()
      );
      set({ plans: data.plans, loading: false });
    } catch (e) {
      set({
        loading: false,
        error: e instanceof Error ? e.message : "fetch plans failed",
      });
    }
  },
  fetchPlan: async (id) => {
    set({ loading: true, error: null });
    const data = await api<{ plan: StudyPlan }>(
      `/api/plans/${id}`,
      {},
      token()
    );
    set({ current: data.plan, loading: false });
    return data.plan;
  },
  createFromInterview: async (interview) => {
    set({ generating: true, error: null });
    try {
      const data = await api<CreatePlanResponse>(
        "/api/plans/interview",
        { method: "POST", body: JSON.stringify(interview) },
        token()
      );
      set({ current: data.plan, generating: false });
      return data;
    } catch (e) {
      set({
        generating: false,
        error: e instanceof Error ? e.message : "generate plan failed",
      });
      throw e;
    }
  },
}));
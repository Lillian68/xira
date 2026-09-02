"use client";

import { create } from "zustand";
import { persist } from "zustand/middleware";
import { api } from "@/lib/api";
import type { User } from "@/lib/types";

interface AuthState {
  token: string | null;
  user: User | null;
  setAuth: (token: string, user: User) => void;
  logout: () => void;
  login: (account: string, password: string) => Promise<void>;
  register: (
    email: string,
    username: string,
    password: string
  ) => Promise<void>;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      token: null,
      user: null,
      setAuth: (token, user) => set({ token, user }),
      logout: () => set({ token: null, user: null }),
      login: async (account, password) => {
        const data = await api<{ token: string; user: User }>(
          "/api/auth/login",
          {
            method: "POST",
            body: JSON.stringify({ account, password }),
          }
        );
        set({ token: data.token, user: data.user });
      },
      register: async (email, username, password) => {
        const data = await api<{ token: string; user: User }>(
          "/api/auth/register",
          {
            method: "POST",
            body: JSON.stringify({ email, username, password }),
          }
        );
        set({ token: data.token, user: data.user });
      },
    }),
    { name: "xira-auth" }
  )
);

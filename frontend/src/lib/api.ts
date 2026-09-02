const API_BASE = process.env.NEXT_PUBLIC_API_BASE;

export class ApiError extends Error {
  status: number;
  constructor(message: string, status: number) {
    super(message);
    this.status = status;
  }
}

export async function api<T = unknown>(
  path: string,
  options: RequestInit = {},
  token?: string | null
): Promise<T> {
  const headers: HeadersInit = {
    "Content-Type": "application/json",
    ...(options.headers || {}),
  };
  if (token) {
    (headers as Record<string, string>)["Authorization"] = `Bearer ${token}`;
  }
  const res = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers,
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    throw new ApiError(data.error || "request failed", res.status);
  }
  return data as T;
}

export async function listenTaskResult<T = any>(
  taskId: string,
  token: string,
): Promise<T> {
  const { token: tempToken } = await api<{ token: string }>(
    "/api/stream/token",
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ task_id: taskId }),
    },
    token
  );

  return new Promise<T>((resolve, reject) => {
    const es = new EventSource(`/api/stream/${taskId}?token=${tempToken}`);
    es.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        if (data.status === "completed") {
          es.close();
          resolve(data.result);
        } else if (data.status === "failed") {
          es.close();
          reject(new Error(data.error || "task failed"));
        }
      } catch (err) {
        es.close();
        reject(new Error("server response parse error"));
      }
    };

    es.onerror = () => {
      es.close();
      reject(new Error("connection interrupted, please check your network"));
    };
  });
}
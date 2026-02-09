import { writable } from "svelte/store";

export const authed = writable(false);
export const me = writable<any>(null);

const API_URL = import.meta.env.PUBLIC_API_URL ?? "http://127.0.0.1:8000";

export function syncAuthFromStorage() {
  if (typeof window === "undefined") return;
  authed.set(!!localStorage.getItem("token"));
}

export async function refreshMe() {
  if (typeof window === "undefined") return;

  const token = localStorage.getItem("token");
  if (!token) {
    me.set(null);
    authed.set(false);
    return;
  }

  const res = await fetch(`${API_URL}/users/me`, {
    headers: { Authorization: `Bearer ${token}` }
  });

  if (!res.ok) {
    localStorage.removeItem("token");
    localStorage.removeItem("role");
    me.set(null);
    authed.set(false);
    return;
  }

  const user = await res.json();
  me.set(user);

  // keep role for your existing permission logic
  localStorage.setItem("role", user.role ?? "student");
  authed.set(true);
}

export function setToken(token: string) {
  if (typeof window === "undefined") return;
  localStorage.setItem("token", token);
  authed.set(true);
}

export function clearToken() {
  if (typeof window === "undefined") return;
  localStorage.removeItem("token");
  localStorage.removeItem("role");
  me.set(null);
  authed.set(false);
}

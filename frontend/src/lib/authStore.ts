import { writable } from "svelte/store";

export const authed = writable(false);

export function syncAuthFromStorage() {
  if (typeof window === "undefined") return;
  authed.set(!!localStorage.getItem("token"));
}

export function setToken(token: string) {
  if (typeof window === "undefined") return;
  localStorage.setItem("token", token);
  authed.set(true);
}

export function clearToken() {
  if (typeof window === "undefined") return;
  localStorage.removeItem("token");
  authed.set(false);
}

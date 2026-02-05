<script lang="ts">
  import { onMount } from "svelte";
  import { goto } from "$app/navigation";

  const API_URL = import.meta.env.PUBLIC_API_URL ?? "http://127.0.0.1:8000";

  let loading = true;
  let error: string | null = null;
  let user: any = null;

  async function loadMe() {
    const token = localStorage.getItem("token");

    if (!token) {
      goto("/login");
      return;
    }

    try {
      const res = await fetch(`${API_URL}/users/me`, {
        headers: { Authorization: `Bearer ${token}` }
      });

      if (!res.ok) {
        if (res.status === 401) {
          localStorage.removeItem("token");
          localStorage.removeItem("role");
          goto("/login");
          return;
        }
        throw new Error(`HTTP ${res.status}`);
      }

      user = await res.json();

      // ✅ SAVE ROLE (for UI permissions)
      localStorage.setItem("role", user.role ?? "student");
    } catch (e: any) {
      error = e?.message ?? "Failed to load profile";
    } finally {
      loading = false;
    }
  }

  onMount(loadMe);
</script>

<h1>My Profile</h1>

{#if loading}
  <p>Loading...</p>
{:else if error}
  <p style="color:red">{error}</p>
{:else}
  <p><strong>Email:</strong> {user.email}</p>
  <p><strong>Role:</strong> {user.role}</p>

  <pre>{JSON.stringify(user, null, 2)}</pre>
{/if}

<p style="margin-top:1rem">
  <a href="/logout">Logout</a>
</p>

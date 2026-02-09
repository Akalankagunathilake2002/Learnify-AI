<script lang="ts">
  import { onMount } from "svelte";
  import { page } from "$app/stores";
  import { goto } from "$app/navigation";
  import { refreshMe } from "$lib/authStore";

  const API_URL = import.meta.env.PUBLIC_API_URL ?? "http://127.0.0.1:8000";

  let msg = "Finalizing your premium upgrade...";
  let error: string | null = null;

  onMount(async () => {
    const token = localStorage.getItem("token");
    if (!token) return goto("/login");

    const sessionId = $page.url.searchParams.get("session_id");
    if (!sessionId) {
      error = "Missing session_id";
      return;
    }

    const res = await fetch(`${API_URL}/billing/sync-success?session_id=${sessionId}`, {
      headers: { Authorization: `Bearer ${token}` }
    });

    if (!res.ok) {
      error = await res.text();
      return;
    }

    // ✅ refresh /users/me so UI updates
    await refreshMe();
    msg = "✅ You are Premium now!";
    setTimeout(() => goto("/ai"), 900);
  });
</script>

<h1>Payment Success</h1>

{#if error}
  <p style="color:red">{error}</p>
  <p><a href="/billing">Go back</a></p>
{:else}
  <p>{msg}</p>
{/if}

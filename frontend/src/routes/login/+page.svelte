<script lang="ts">
  import { goto } from "$app/navigation";
  import { setToken } from "$lib/authStore";
  import { onMount } from "svelte";

  const API_URL = import.meta.env.PUBLIC_API_URL ?? "http://127.0.0.1:8000";

  let email = "";
  let password = "";
  let error: string | null = null;
  let ready = false;

  onMount(() => {
    ready = true;
  });

  async function login() {
    error = null;

    const res = await fetch(`${API_URL}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password })
    });

    if (!res.ok) {
      error = "Invalid email or password";
      return;
    }

    const data = await res.json();
    setToken(data.access_token);
    goto("/me");
  }
</script>

{#if !ready}
  <p>Loading...</p>
{:else}
  <h1>Login</h1>

  <input placeholder="Email" bind:value={email} />
  <br />
  <input type="password" placeholder="Password" bind:value={password} />
  <br />
  <button on:click={login}>Login</button>

  {#if error}
    <p style="color:red">{error}</p>
  {/if}
{/if}

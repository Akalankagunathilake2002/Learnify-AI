<script lang="ts">
  import { goto } from "$app/navigation";

  const API_URL = import.meta.env.PUBLIC_API_URL ?? "http://127.0.0.1:8000";

  let email = "";
  let password = "";
  let message: string | null = null;
  let error: string | null = null;

  async function register() {
    message = null;
    error = null;

    const res = await fetch(`${API_URL}/auth/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password })
    });

    if (!res.ok) {
      const txt = await res.text();
      error = `Register failed: ${txt}`;
      return;
    }

    message = "✅ Account created! Please login.";
    setTimeout(() => goto("/login"), 800);
  }
</script>

<h1>Create Account</h1>

<input placeholder="Email" bind:value={email} />
<br />
<input type="password" placeholder="Password (8-72 chars)" bind:value={password} />
<br />
<button on:click={register}>Register</button>

{#if message}
  <p style="color:green">{message}</p>
{/if}

{#if error}
  <p style="color:red">{error}</p>
{/if}

<p style="margin-top: 1rem">
  Already have an account? <a href="/login">Login</a>
</p>

<script lang="ts">
  import { goto } from "$app/navigation";

  const API_URL = import.meta.env.PUBLIC_API_URL ?? "http://127.0.0.1:8000";

  let email = "";
  let password = "";
  let error: string | null = null;

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
    localStorage.setItem("token", data.access_token);
    goto("/me");
  }
</script>

<h1>Login</h1>

<input placeholder="Email" bind:value={email} />
<br />
<input type="password" placeholder="Password" bind:value={password} />
<br />
<button on:click={login}>Login</button>

{#if error}
  <p style="color:red">{error}</p>
{/if}

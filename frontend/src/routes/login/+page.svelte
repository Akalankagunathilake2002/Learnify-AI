<script lang="ts">
  const API_URL = import.meta.env.PUBLIC_API_URL ?? "http://127.0.0.1:8000";

  let email = "";
  let password = "";
  let message = "";

  async function login() {
    message = "";
    const res = await fetch(`${API_URL}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password })
    });

    if (!res.ok) {
      message = "Login failed";
      return;
    }

    const data = await res.json();
    localStorage.setItem("token", data.access_token);
    message = "✅ Logged in! Token saved.";
  }
</script>

<h1>Login</h1>

<input placeholder="Email" bind:value={email} />
<input placeholder="Password" type="password" bind:value={password} />
<button on:click={login}>Login</button>

<p>{message}</p>

<p><a href="/me">Go to /me</a></p>

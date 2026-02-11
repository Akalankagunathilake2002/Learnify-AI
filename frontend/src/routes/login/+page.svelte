<script lang="ts">
  import { goto } from "$app/navigation";
  import { setToken } from "$lib/authStore";
  import { onMount } from "svelte";

  const API_URL = import.meta.env.PUBLIC_API_URL ?? "http://127.0.0.1:8000";

  // 🔴 PASTE YOUR BACKGROUND IMAGE URL HERE
  const LOGIN_BG_IMAGE_URL = "https://www.protectuk.police.uk/sites/default/files/styles/large_hero_904x652/public/2023-08/Learning%20Homepage_0.jpg?h=1c27a152&itok=O3OCeP8f";
  let email = "";
  let password = "";
  let error: string | null = null;
  let ready = false;
  let loading = false;

  onMount(() => {
    ready = true;
  });

  async function login() {
    error = null;
    loading = true;

    try {
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
    } catch {
      error = "Login failed. Please try again.";
    } finally {
      loading = false;
    }
  }
</script>

{#if !ready}
  <p>Loading...</p>
{:else}
  <!-- ✅ TRUE FULLSCREEN BACKGROUND (covers entire viewport) -->
  <div
    style="
      position: fixed;
      inset: 0;
      z-index: 0;
      background-image: url('{LOGIN_BG_IMAGE_URL}');
      background-size: cover;
      background-position: center;
      background-repeat: no-repeat;
      transform: scale(1.02);
    "
  ></div>

  <!-- ✅ Overlay to make text readable -->
  <div
    style="
      position: fixed;
      inset: 0;
      z-index: 1;
      background:
        radial-gradient(800px 420px at 20% 10%, rgba(16,185,129,0.20), transparent 60%),
        radial-gradient(800px 420px at 80% 10%, rgba(14,165,233,0.18), transparent 60%),
        linear-gradient(180deg, rgba(15,23,42,0.25), rgba(15,23,42,0.65));
    "
  ></div>

  <!-- ✅ CONTENT LAYER (above background + overlay) -->
  <div
    style="
      position: relative;
      z-index: 2;
      min-height: calc(100vh - 0px);
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 28px 16px;
    "
  >
    <!-- LOGIN CARD -->
    <div
      style="
        width: 100%;
        max-width: 430px;
        padding: 26px;
        border-radius: 24px;
        background: rgba(255,255,255,0.82);
        backdrop-filter: blur(14px);
        border: 1px solid rgba(255,255,255,0.32);
        box-shadow: 0 30px 80px rgba(15,23,42,0.45);
      "
    >
      <!-- Header -->
      <div style="text-align: center; margin-bottom: 20px;">
        <div
          style="
            width: 62px;
            height: 62px;
            margin: 0 auto 12px;
            border-radius: 20px;
            display: grid;
            place-items: center;
            font-size: 30px;
            background: linear-gradient(135deg, rgba(16,185,129,0.30), rgba(14,165,233,0.24));
            border: 1px solid rgba(16,185,129,0.40);
            color: #0f766e;
            font-weight: 950;
          "
        >
          🔐
        </div>

        <h1
          style="
            margin: 0;
            font-size: 28px;
            font-weight: 950;
            color: #0f172a;
          "
        >
          Welcome back
        </h1>

        <p
          style="
            margin-top: 6px;
            font-size: 14px;
            color: rgba(15,23,42,0.65);
            font-weight: 650;
          "
        >
          Login to continue learning with <strong>Learnify AI</strong>
        </p>
      </div>

      <!-- Email -->
      <div style="margin-bottom: 14px;">
        <label
          style="
            display:block;
            margin-bottom: 6px;
            font-size: 13px;
            font-weight: 900;
            color: rgba(15,23,42,0.78);
          "
        >
          Email
        </label>
        <input
          type="email"
          placeholder="you@example.com"
          bind:value={email}
          style="
            width: 100%;
            padding: 12px 14px;
            border-radius: 14px;
            border: 1px solid rgba(15,23,42,0.14);
            background: rgba(248,250,252,0.96);
            outline: none;
            font-size: 14px;
            font-weight: 700;
          "
        />
      </div>

      <!-- Password -->
      <div style="margin-bottom: 16px;">
        <label
          style="
            display:block;
            margin-bottom: 6px;
            font-size: 13px;
            font-weight: 900;
            color: rgba(15,23,42,0.78);
          "
        >
          Password
        </label>
        <input
          type="password"
          placeholder="••••••••"
          bind:value={password}
          style="
            width: 100%;
            padding: 12px 14px;
            border-radius: 14px;
            border: 1px solid rgba(15,23,42,0.14);
            background: rgba(248,250,252,0.96);
            outline: none;
            font-size: 14px;
            font-weight: 700;
          "
        />
      </div>

      <!-- Error -->
      {#if error}
        <div
          style="
            margin-bottom: 14px;
            padding: 10px 12px;
            border-radius: 14px;
            background: rgba(239,68,68,0.12);
            border: 1px solid rgba(239,68,68,0.28);
            color: #b91c1c;
            font-weight: 850;
            font-size: 14px;
          "
        >
          {error}
        </div>
      {/if}

      <!-- Button -->
      <button
        on:click={login}
        disabled={loading || !email || !password}
        style="
          width: 100%;
          padding: 14px;
          border-radius: 16px;
          border: none;
          background: #10b981;
          color: white;
          font-size: 15px;
          font-weight: 950;
          cursor: pointer;
          box-shadow: 0 16px 34px rgba(16,185,129,0.35);
          opacity: {loading || !email || !password ? 0.6 : 1};
        "
      >
        {loading ? "Signing in..." : "Login"}
      </button>

      <!-- Footer -->
      <div
        style="
          margin-top: 16px;
          text-align: center;
          font-size: 14px;
          color: rgba(15,23,42,0.65);
          font-weight: 650;
        "
      >
        Don’t have an account?
        <a
          href="/register"
          style="
            margin-left: 6px;
            text-decoration: none;
            font-weight: 900;
            color: #0f766e;
          "
        >
          Register
        </a>
      </div>
    </div>
  </div>
{/if}

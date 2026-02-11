<script lang="ts">
  import { goto } from "$app/navigation";
  import { onMount } from "svelte";

  const API_URL = import.meta.env.PUBLIC_API_URL ?? "http://127.0.0.1:8000";

  // ✅ Background image for register page
  const REGISTER_BG_IMAGE_URL =
    "https://edusites.uregina.ca/echoliulu/wp-content/uploads/sites/1264/2022/05/image.png";

  let email = "";
  let password = "";
  let message: string | null = null;
  let error: string | null = null;
  let loading = false;
  let ready = false;

  let showPw = false;

  onMount(() => {
    ready = true;
  });

  function validate(): string | null {
    const e = email.trim();
    const p = password;

    if (!e || !p) return "Please enter email and password.";
    if (!e.includes("@")) return "Please enter a valid email address.";
    if (p.length < 8) return "Password must be at least 8 characters.";
    if (p.length > 72) return "Password must be 72 characters or less.";
    return null;
  }

  async function register() {
    message = null;
    error = null;

    const v = validate();
    if (v) {
      error = v;
      return;
    }

    loading = true;

    try {
      const res = await fetch(`${API_URL}/auth/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: email.trim(), password }) // ✅ backend sets role="student"
      });

      if (!res.ok) {
        const txt = await res.text();
        error = `Register failed: ${txt}`;
        return;
      }

      message = "✅ Account created as student! Redirecting to login...";
      setTimeout(() => goto("/login"), 900);
    } catch {
      error = "Register failed. Please try again.";
    } finally {
      loading = false;
    }
  }

  function onKeyDown(e: KeyboardEvent) {
    if (e.key === "Enter") register();
  }
</script>

{#if !ready}
  <p style="padding: 24px; font-weight: 800;">Loading...</p>
{:else}
  <!-- ✅ FULLSCREEN BACKGROUND -->
  <div
    style="
      position: fixed;
      inset: 0;
      z-index: 0;
      background-image: url('{REGISTER_BG_IMAGE_URL}');
      background-size: cover;
      background-position: center;
      background-repeat: no-repeat;
      transform: scale(1.04);
      filter: saturate(1.05);
    "
  ></div>

  <!-- ✅ Overlay -->
  <div
    style="
      position: fixed;
      inset: 0;
      z-index: 1;
      background:
        radial-gradient(900px 520px at 18% 18%, rgba(16,185,129,0.22), transparent 60%),
        radial-gradient(900px 520px at 80% 12%, rgba(14,165,233,0.20), transparent 60%),
        linear-gradient(180deg, rgba(2,6,23,0.35) 0%, rgba(2,6,23,0.70) 100%);
    "
  ></div>

  <!-- ✅ CONTENT -->
  <div
    style="
      position: relative;
      z-index: 2;
      min-height: 100vh;
      padding: 28px 16px;
      display: flex;
      align-items: center;
      justify-content: center;
      box-sizing: border-box;
      font-family: system-ui, -apple-system, BlinkMacSystemFont;
    "
  >
    <div
      style="
        width: min(1120px, 100%);
        display: grid;
        grid-template-columns: 1.1fr 0.9fr;
        gap: 18px;
        align-items: stretch;
      "
    >
      <!-- LEFT: info panel -->
      <div
        style="
          border-radius: 26px;
          overflow: hidden;
          border: 1px solid rgba(255,255,255,0.18);
          background: rgba(255,255,255,0.10);
          backdrop-filter: blur(12px);
          box-shadow: 0 30px 90px rgba(0,0,0,0.35);
          padding: 26px;
          display: flex;
          flex-direction: column;
          justify-content: space-between;
          min-height: 520px;
        "
      >
        <div style="display:flex; align-items:center; gap:12px;">
          <div
            style="
              width: 44px;
              height: 44px;
              border-radius: 16px;
              display: grid;
              place-items: center;
              background: rgba(255,255,255,0.16);
              border: 1px solid rgba(255,255,255,0.22);
              color: white;
              font-weight: 950;
              font-size: 18px;
            "
          >
            L
          </div>

          <div style="color:white;">
            <div style="font-weight: 950; font-size: 16px; letter-spacing: 0.2px;">
              Learnify AI
            </div>
            <div style="opacity: 0.86; font-weight: 650; font-size: 13px;">
              Create your account and start learning.
            </div>
          </div>
        </div>

        <div style="margin-top: 26px; color:white;">
          <div style="font-size: 44px; line-height: 1.05; font-weight: 980; letter-spacing: -1px;">
            Join Learnify AI ✨
          </div>

          <div
            style="
              margin-top: 10px;
              font-size: 15px;
              line-height: 1.7;
              opacity: 0.92;
              font-weight: 650;
              max-width: 520px;
            "
          >
            Build your skills with structured courses, track lesson progress, and use AI tools to learn faster.
            Your account will be created as a <b>student</b> by default.
          </div>

          <div style="margin-top: 18px; display: grid; gap: 10px; max-width: 520px;">
            <div style="display:flex; gap:10px; align-items:flex-start;">
              <div style="width:32px; height:32px; border-radius: 12px; display:grid; place-items:center; background: rgba(16,185,129,0.22); border: 1px solid rgba(16,185,129,0.28);">✅</div>
              <div>
                <div style="font-weight: 900;">Enroll & track progress</div>
                <div style="opacity:0.9; font-size: 13px; line-height: 1.6;">See completed lessons and course %.</div>
              </div>
            </div>

            <div style="display:flex; gap:10px; align-items:flex-start;">
              <div style="width:32px; height:32px; border-radius: 12px; display:grid; place-items:center; background: rgba(14,165,233,0.20); border: 1px solid rgba(14,165,233,0.28);">🤖</div>
              <div>
                <div style="font-weight: 900;">AI Tutor</div>
                <div style="opacity:0.9; font-size: 13px; line-height: 1.6;">Ask questions and get explanations.</div>
              </div>
            </div>

            <div style="display:flex; gap:10px; align-items:flex-start;">
              <div style="width:32px; height:32px; border-radius: 12px; display:grid; place-items:center; background: rgba(255,255,255,0.16); border: 1px solid rgba(255,255,255,0.20);">⚡</div>
              <div>
                <div style="font-weight: 900;">Modern platform</div>
                <div style="opacity:0.9; font-size: 13px; line-height: 1.6;">SvelteKit + FastAPI + PostgreSQL.</div>
              </div>
            </div>
          </div>
        </div>

        <div style="margin-top: 16px; color: rgba(255,255,255,0.92); font-size: 12px; font-weight: 650;">
          Tip: Use a strong password (8+ characters).
        </div>
      </div>

      <!-- RIGHT: Register card -->
      <div
        style="
          border-radius: 26px;
          overflow: hidden;
          border: 1px solid rgba(255,255,255,0.22);
          background: rgba(255,255,255,0.82);
          backdrop-filter: blur(14px);
          box-shadow: 0 30px 90px rgba(0,0,0,0.35);
          padding: 26px;
          display: flex;
          flex-direction: column;
          justify-content: center;
          min-height: 520px;
        "
      >
        <div style="text-align:center; margin-bottom: 18px;">
          <div
            style="
              width: 66px;
              height: 66px;
              margin: 0 auto 12px;
              border-radius: 22px;
              display: grid;
              place-items: center;
              font-size: 30px;
              background: linear-gradient(135deg, rgba(16,185,129,0.26), rgba(14,165,233,0.22));
              border: 1px solid rgba(16,185,129,0.35);
              color: #0f766e;
              font-weight: 950;
            "
          >
            ✨
          </div>

          <h1 style="margin: 0; font-size: 26px; font-weight: 980; color:#0f172a;">
            Create Account
          </h1>

          <p style="margin: 8px 0 0; font-size: 14px; color: rgba(15,23,42,0.65); font-weight: 650;">
            Start learning with Learnify AI
          </p>
        </div>

        <!-- Email -->
        <div style="margin-bottom: 12px;">
          <label style="display:block; margin-bottom:6px; font-size: 13px; font-weight: 950; color: rgba(15,23,42,0.80);">
            Email
          </label>

          <input
            type="email"
            placeholder="you@example.com"
            bind:value={email}
            on:keydown={onKeyDown}
            style="
              width: 100%;
              padding: 12px 14px;
              border-radius: 14px;
              border: 1px solid rgba(15,23,42,0.14);
              background: rgba(248,250,252,0.96);
              outline: none;
              font-size: 14px;
              font-weight: 700;
              box-sizing: border-box;
            "
          />
        </div>

        <!-- Password -->
        <div style="margin-bottom: 14px;">
          <label style="display:block; margin-bottom:6px; font-size: 13px; font-weight: 950; color: rgba(15,23,42,0.80);">
            Password
          </label>

          <div
            style="
              display:flex;
              align-items:center;
              gap: 10px;
              border-radius: 14px;
              border: 1px solid rgba(15,23,42,0.14);
              background: rgba(248,250,252,0.96);
              overflow: hidden;
            "
          >
            <input
              type={showPw ? "text" : "password"}
              placeholder="8-72 characters"
              bind:value={password}
              on:keydown={onKeyDown}
              style="
                flex: 1;
                padding: 12px 14px;
                border: none;
                outline: none;
                background: transparent;
                font-size: 14px;
                font-weight: 700;
                box-sizing: border-box;
              "
            />
            <button
              type="button"
              on:click={() => (showPw = !showPw)}
              style="
                border: none;
                background: transparent;
                cursor: pointer;
                padding: 10px 12px;
                font-weight: 950;
                color: rgba(15,23,42,0.70);
              "
            >
              {showPw ? "Hide" : "Show"}
            </button>
          </div>

          <div style="margin-top: 8px; font-size: 12px; color: rgba(15,23,42,0.60); font-weight: 650;">
            Your account will be created as <b>student</b> by default.
          </div>
        </div>

        {#if message}
          <div
            style="
              margin-bottom: 12px;
              padding: 10px 12px;
              border-radius: 14px;
              background: rgba(16,185,129,0.12);
              border: 1px solid rgba(16,185,129,0.24);
              color: #0f766e;
              font-weight: 900;
              font-size: 14px;
            "
          >
            {message}
          </div>
        {/if}

        {#if error}
          <div
            style="
              margin-bottom: 12px;
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

        <button
          on:click={register}
          disabled={loading || !email.trim() || !password.trim()}
          style="
            width: 100%;
            padding: 14px;
            border-radius: 16px;
            border: none;
            background: linear-gradient(135deg, #10b981, #22c55e);
            color: white;
            font-size: 15px;
            font-weight: 980;
            cursor: pointer;
            box-shadow: 0 16px 34px rgba(16,185,129,0.35);
            opacity: {loading || !email.trim() || !password.trim() ? 0.6 : 1};
          "
        >
          {loading ? "Creating account..." : "Register"}
        </button>

        <div style="margin-top: 14px; text-align: center; font-size: 14px; color: rgba(15,23,42,0.65); font-weight: 650;">
          Already have an account?
          <a href="/login" style="margin-left: 6px; text-decoration:none; font-weight: 950; color:#0f766e;">
            Login
          </a>
        </div>

        <div style="margin-top: 18px; padding-top: 14px; border-top: 1px solid rgba(15,23,42,0.10); font-size: 12px; color: rgba(15,23,42,0.60); font-weight: 650; text-align:center;">
          By creating an account, you agree to our
          <a href="/privacy" style="color:#0f766e; font-weight:900; text-decoration:none;">Privacy Policy</a>.
        </div>
      </div>
    </div>
  </div>

  <style>
    @media (max-width: 980px) {
      div[style*="grid-template-columns: 1.1fr 0.9fr"] {
        grid-template-columns: 1fr !important;
      }
    }
  </style>
{/if}

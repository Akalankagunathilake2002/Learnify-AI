<script lang="ts">
  import { onMount } from "svelte";
  import { authed, syncAuthFromStorage } from "$lib/authStore";

  onMount(() => {
    syncAuthFromStorage();
  });
</script>

<nav
  style="
    position: sticky;
    top: 0;
    z-index: 50;
    padding: 12px 18px;
    border-bottom: 1px solid rgba(15,23,42,0.08);
    background: rgba(255,255,255,0.78);
    backdrop-filter: blur(10px);
    box-shadow: 0 10px 24px rgba(15,23,42,0.06);
  "
>
  <div
    style="
      max-width: 1280px;
      margin: 0 auto;
      display: flex;
      align-items: center;
      gap: 14px;
      flex-wrap: wrap;
      justify-content: space-between;
    "
  >
    <!-- Left links -->
    <div style="display: flex; align-items: center; gap: 12px; flex-wrap: wrap;">
      <a
        href="/"
        style="
          text-decoration: none;
          font-weight: 950;
          color: #0f172a;
          display: flex;
          align-items: center;
          gap: 8px;
        "
      >
        <span
          style="
            width: 34px;
            height: 34px;
            border-radius: 12px;
            display: grid;
            place-items: center;
            background: rgba(16,185,129,0.12);
            border: 1px solid rgba(16,185,129,0.22);
            color: #0f766e;
            font-weight: 950;
          "
        >
          L
        </span>
        Learnify AI
      </a>

      <span style="opacity: 0.25;">|</span>

      <a
        href="/"
        style="
          text-decoration: none;
          color: rgba(15,23,42,0.72);
          font-weight: 850;
          padding: 8px 10px;
          border-radius: 12px;
        "
      >
        Home
      </a>

      {#if $authed}
        <a
          href="/me"
          style="
            text-decoration: none;
            color: rgba(15,23,42,0.72);
            font-weight: 850;
            padding: 8px 10px;
            border-radius: 12px;
          "
        >
          My Profile
        </a>

        <a
          href="/courses"
          style="
            text-decoration: none;
            color: rgba(15,23,42,0.72);
            font-weight: 850;
            padding: 8px 10px;
            border-radius: 12px;
          "
        >
          Courses
        </a>

        <a
          href="/my-courses"
          style="
            text-decoration: none;
            color: rgba(15,23,42,0.72);
            font-weight: 850;
            padding: 8px 10px;
            border-radius: 12px;
          "
        >
          My Courses
        </a>

        <a
          href="/ai"
          style="
            text-decoration: none;
            color: #0f766e;
            font-weight: 950;
            padding: 8px 12px;
            border-radius: 999px;
            background: rgba(16,185,129,0.12);
            border: 1px solid rgba(16,185,129,0.22);
          "
        >
          🤖 AI Tutor
        </a>
      {/if}
    </div>

    <!-- Right actions -->
    <div style="display: flex; align-items: center; gap: 10px; flex-wrap: wrap;">
      {#if $authed}
        <a
          href="/billing"
          style="
            text-decoration: none;
            padding: 10px 14px;
            border-radius: 14px;
            background: #10b981;
            color: white;
            font-weight: 950;
            box-shadow: 0 14px 30px rgba(16,185,129,0.20);
          "
        >
          Upgrade
        </a>

        <a
          href="/logout"
          style="
            text-decoration: none;
            padding: 10px 14px;
            border-radius: 14px;
            background: rgba(15,23,42,0.06);
            color: rgba(15,23,42,0.75);
            font-weight: 900;
            border: 1px solid rgba(15,23,42,0.10);
          "
        >
          Logout
        </a>
      {:else}
        <a
          href="/login"
          style="
            text-decoration: none;
            padding: 10px 14px;
            border-radius: 14px;
            background: rgba(15,23,42,0.06);
            color: rgba(15,23,42,0.75);
            font-weight: 900;
            border: 1px solid rgba(15,23,42,0.10);
          "
        >
          Login
        </a>

        <a
          href="/register"
          style="
            text-decoration: none;
            padding: 10px 14px;
            border-radius: 14px;
            background: #10b981;
            color: white;
            font-weight: 950;
            box-shadow: 0 14px 30px rgba(16,185,129,0.20);
          "
        >
          Register
        </a>
      {/if}
    </div>
  </div>
</nav>

<div
  style="
    padding: 0;
    background:
      radial-gradient(900px 520px at 10% 20%, rgba(16,185,129,0.10), transparent 60%),
      radial-gradient(900px 520px at 90% 20%, rgba(34,197,94,0.08), transparent 60%),
      linear-gradient(180deg, #f7faf9 0%, #f2f7f5 100%);
    min-height: calc(100vh - 60px);
  "
>
  <div style="max-width: 1280px; margin: 0 auto; padding: 16px 18px;">
    <slot />
  </div>
</div>

<footer
  style="
    margin-top: 26px;
    border-top: 1px solid rgba(15,23,42,0.10);
    background: rgba(255,255,255,0.78);
    backdrop-filter: blur(10px);
  "
>
  <div
    style="
      max-width: 1280px;
      margin: 0 auto;
      padding: 26px 18px;
      display: grid;
      grid-template-columns: 1.2fr 1fr 1fr 1fr;
      gap: 18px;
      align-items: start;
    "
  >
    <!-- Brand -->
    <div>
      <div style="display:flex; align-items:center; gap:10px; margin-bottom: 10px;">
        <div
          style="
            width: 40px;
            height: 40px;
            border-radius: 14px;
            display:grid;
            place-items:center;
            background: rgba(16,185,129,0.12);
            border: 1px solid rgba(16,185,129,0.22);
            color: #0f766e;
            font-weight: 950;
          "
        >
          L
        </div>
        <div style="font-weight: 950; color:#0f172a;">Learnify AI</div>
      </div>

      <p style="margin:0; color: rgba(15,23,42,0.65); line-height: 1.7; font-weight: 650;">
        AI-powered learning platform to help you study faster with smart notes,
        quizzes, and an AI tutor.
      </p>

      <div style="margin-top: 12px; display:flex; gap:10px; flex-wrap: wrap;">
        <a
          href="/pricing"
          style="
            text-decoration:none;
            padding: 10px 14px;
            border-radius: 12px;
            background: #10b981;
            color: white;
            font-weight: 950;
            box-shadow: 0 12px 28px rgba(16,185,129,0.18);
            display:inline-block;
          "
        >
          Upgrade
        </a>

        <a
          href="/courses"
          style="
            text-decoration:none;
            padding: 10px 14px;
            border-radius: 12px;
            background: rgba(16,185,129,0.10);
            border: 1px solid rgba(16,185,129,0.22);
            color: #0f766e;
            font-weight: 950;
            display:inline-block;
          "
        >
          Browse Courses
        </a>
      </div>
    </div>

    <!-- Links -->
    <div>
      <div style="font-weight: 950; color:#0f172a; margin-bottom: 10px;">Platform</div>
      <div style="display:flex; flex-direction:column; gap:8px;">
        <a href="/courses" style="text-decoration:none; color: rgba(15,23,42,0.70); font-weight: 750;">Courses</a>
        <a href="/ai" style="text-decoration:none; color: rgba(15,23,42,0.70); font-weight: 750;">AI Tutor</a>
        <a href="/my-courses" style="text-decoration:none; color: rgba(15,23,42,0.70); font-weight: 750;">My Courses</a>
        <a href="/billing" style="text-decoration:none; color: rgba(15,23,42,0.70); font-weight: 750;">Pricing</a>
      </div>
    </div>

    <div>
      <div style="font-weight: 950; color:#0f172a; margin-bottom: 10px;">Company</div>
      <div style="display:flex; flex-direction:column; gap:8px;">
        <a href="/about" style="text-decoration:none; color: rgba(15,23,42,0.70); font-weight: 750;">About</a>
        <a href="/contact" style="text-decoration:none; color: rgba(15,23,42,0.70); font-weight: 750;">Contact</a>
        <a href="/faq" style="text-decoration:none; color: rgba(15,23,42,0.70); font-weight: 750;">FAQ</a>
        <a href="/privacy" style="text-decoration:none; color: rgba(15,23,42,0.70); font-weight: 750;">Privacy Policy</a>
      </div>
    </div>

    <!-- Newsletter -->
    <div>
      <div style="font-weight: 950; color:#0f172a; margin-bottom: 10px;">Get Updates</div>

      <div
        style="
          border-radius: 16px;
          padding: 12px;
          background: rgba(255,255,255,0.85);
          border: 1px solid rgba(15,23,42,0.10);
          box-shadow: 0 12px 28px rgba(15,23,42,0.06);
        "
      >
        <div style="color: rgba(15,23,42,0.65); font-weight: 700; font-size: 13px; line-height: 1.6;">
          Subscribe for new courses & AI feature updates.
        </div>

        <div style="display:flex; gap:8px; margin-top: 10px;">
          <input
            type="email"
            placeholder="your@email.com"
            style="
              flex: 1;
              padding: 10px 12px;
              border-radius: 12px;
              border: 1px solid rgba(15,23,42,0.12);
              background: #f8fafc;
              outline: none;
              font-size: 14px;
            "
          />
          <button
            style="
              padding: 10px 14px;
              border-radius: 12px;
              border: none;
              background: #10b981;
              color: white;
              font-weight: 950;
              cursor: pointer;
            "
          >
            Join
          </button>
        </div>

        <div style="margin-top: 10px; display:flex; gap:10px;">
          <a href="https://github.com" target="_blank" style="text-decoration:none; font-weight: 900; color: #0f766e;">GitHub</a>
          <a href="https://linkedin.com" target="_blank" style="text-decoration:none; font-weight: 900; color: #0f766e;">LinkedIn</a>
        </div>
      </div>
    </div>
  </div>

  <!-- Bottom bar -->
  <div
    style="
      border-top: 1px solid rgba(15,23,42,0.08);
      padding: 12px 18px;
      color: rgba(15,23,42,0.60);
      font-weight: 700;
      font-size: 13px;
    "
  >
    <div
      style="
        max-width: 1280px;
        margin: 0 auto;
        display:flex;
        justify-content: space-between;
        gap: 10px;
        flex-wrap: wrap;
      "
    >
      <span>© {new Date().getFullYear()} Learnify AI. All rights reserved.</span>
      <span>Built with SvelteKit + FastAPI + PostgreSQL</span>
    </div>
  </div>

  <!-- Mobile responsive -->
  <style>
    @media (max-width: 900px) {
      footer > div:first-child {
        grid-template-columns: 1fr 1fr !important;
      }
    }
    @media (max-width: 520px) {
      footer > div:first-child {
        grid-template-columns: 1fr !important;
      }
    }
  </style>
</footer>

<script lang="ts">
  import { onMount } from "svelte";
  import { page } from "$app/stores";
  import { authed, syncAuthFromStorage } from "$lib/authStore";

  onMount(() => {
    syncAuthFromStorage();
  });

  const LOGO_URL =
    "https://thumbs.dreamstime.com/b/e-learning-logo-design-concept-e-learning-logo-design-concept-smartphone-education-technology-digital-e-book-vector-icon-258483880.jpg";

  // normalize path (remove trailing slash)
  const norm = (p: string) => (p.length > 1 ? p.replace(/\/+$/, "") : p);
  const isActive = (path: string) => norm($page.url.pathname) === norm(path);
</script>

<!-- ================= NAV ================= -->
<nav class="nav">
  <div class="nav-inner">

    <div class="nav-left">
      <a href="/" class="brand">
        <img src={LOGO_URL} class="logoImg" alt="Learnify AI Logo" />
        <span>Learnify AI</span>
      </a>

      <span class="divider">|</span>

      <a href="/" class:active={isActive("/")}>Home</a>

      {#if $authed}
        <a href="/me" class:active={isActive("/me")}>My Profile</a>
        <a href="/courses" class:active={isActive("/courses")}>Courses</a>
        <a href="/my-courses" class:active={isActive("/my-courses")}>My Courses</a>

        <!-- AI normal by default -->
        <a href="/ai" class="ai" class:active={isActive("/ai")}>
          🤖 AI Tutor
        </a>
      {/if}
    </div>

    <div class="nav-right">
      {#if $authed}
        <a href="/billing" class="primary" class:active={isActive("/billing")}>
          Upgrade
        </a>
        <a href="/logout" class="ghost">Logout</a>
      {:else}
        <a href="/login" class="ghost" class:active={isActive("/login")}>
          Login
        </a>
        <a href="/register" class="primary" class:active={isActive("/register")}>
          Register
        </a>
      {/if}
    </div>

  </div>
</nav>

<!-- ================= PAGE WRAPPER ================= -->
<div class="page-bg">
  <div class="page-container">
    <slot />
  </div>
</div>

<!-- ================= FULL FOOTER (RESTORED) ================= -->
<footer class="footer">
  <div class="footer-inner">

    <!-- Brand -->
    <div>
      <div class="footer-brand">
        <img src={LOGO_URL} class="logoImg" alt="Logo" />
        <div class="footer-title">Learnify AI</div>
      </div>

      <p class="footer-text">
        AI-powered learning platform to help you study faster with smart notes,
        quizzes, and an AI tutor.
      </p>

      <div class="footer-actions">
        <a href="/billing" class="primary">Upgrade</a>
        <a href="/courses" class="outline">Browse Courses</a>
      </div>
    </div>

    <!-- Platform -->
    <div>
      <div class="footer-heading">Platform</div>
      <div class="footer-links">
        <a href="/courses">Courses</a>
        <a href="/ai">AI Tutor</a>
        <a href="/my-courses">My Courses</a>
        <a href="/billing">Pricing</a>
      </div>
    </div>

    <!-- Company -->
    <div>
      <div class="footer-heading">Company</div>
      <div class="footer-links">
        <a href="#">About</a>
        <a href="#">Contact</a>
        <a href="#">FAQ</a>
        <a href="#">Privacy Policy</a>
      </div>
    </div>

    <!-- Newsletter -->
    <div>
      <div class="footer-heading">Get Updates</div>

      <div class="newsletter-box">
        <div class="newsletter-text">
          Subscribe for new courses & AI feature updates.
        </div>

        <div class="newsletter-input">
          <input type="email" placeholder="your@email.com" />
          <button>Join</button>
        </div>

        <div class="social-links">
          <a href="#">GitHub</a>
          <a href="#">LinkedIn</a>
        </div>
      </div>
    </div>

  </div>

  <!-- Bottom bar -->
  <div class="footer-bottom">
    <div class="footer-bottom-inner">
      <span>© {new Date().getFullYear()} Learnify AI</span>
      <span>Built with SvelteKit + FastAPI + PostgreSQL</span>
    </div>
  </div>
</footer>

<!-- ================= STYLES ================= -->
<style>
  .nav {
    position: sticky;
    top: 0;
    background: rgba(255,255,255,0.85);
    backdrop-filter: blur(10px);
    border-bottom: 1px solid rgba(15,23,42,0.08);
  }

  .nav-inner {
    max-width: 1280px;
    margin: auto;
    padding: 12px 18px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .nav-left, .nav-right {
    display: flex;
    align-items: center;
    gap: 12px;
  }

  .brand {
    display: flex;
    align-items: center;
    gap: 8px;
    font-weight: 950;
    text-decoration: none;
    color: #0f172a;
  }

  .logoImg {
    width: 34px;
    height: 34px;
    border-radius: 10px;
    object-fit: cover;
  }

  .divider { opacity: 0.25; }

  .nav a {
    text-decoration: none;
    padding: 8px 10px;
    border-radius: 12px;
    font-weight: 850;
    color: rgba(15,23,42,0.7);
  }

  .nav a.active {
    background: rgba(16,185,129,0.14);
    border: 1px solid rgba(16,185,129,0.3);
    color: #0f766e;
    font-weight: 950;
  }

  .nav a.ai {
    border-radius: 999px;
    background: transparent;
  }

  .nav a.ai.active {
    background: rgba(16,185,129,0.18);
    border: 1px solid rgba(16,185,129,0.35);
  }

  .primary {
    background: #10b981;
    color: white !important;
    padding: 10px 14px;
    border-radius: 14px;
  }

  .ghost {
    background: rgba(15,23,42,0.06);
    border: 1px solid rgba(15,23,42,0.1);
    padding: 10px 14px;
    border-radius: 14px;
  }

  .outline {
    background: rgba(16,185,129,0.1);
    border: 1px solid rgba(16,185,129,0.3);
    padding: 10px 14px;
    border-radius: 12px;
    font-weight: 900;
    text-decoration: none;
    color: #0f766e;
  }

  .page-bg {
    min-height: calc(100vh - 60px);
    background:
      radial-gradient(900px 520px at 10% 20%, rgba(16,185,129,0.1), transparent 60%),
      linear-gradient(180deg, #f7faf9 0%, #f2f7f5 100%);
  }

  .page-container {
    max-width: 1280px;
    margin: auto;
    padding: 16px 18px;
  }

  /* ================= FOOTER ================= */
  .footer {
    border-top: 1px solid rgba(15,23,42,0.1);
    background: rgba(255,255,255,0.85);
  }

  .footer-inner {
    max-width: 1280px;
    margin: auto;
    padding: 26px 18px;
    display: grid;
    grid-template-columns: 1.2fr 1fr 1fr 1fr;
    gap: 18px;
  }

  .footer-heading {
    font-weight: 950;
    margin-bottom: 10px;
  }

  .footer-links {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }

  .footer-links a {
    text-decoration: none;
    color: rgba(15,23,42,0.7);
    font-weight: 750;
  }

  .footer-brand {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 10px;
  }

  .footer-text {
    color: rgba(15,23,42,0.65);
    line-height: 1.6;
  }

  .newsletter-box {
    background: white;
    padding: 12px;
    border-radius: 14px;
    border: 1px solid rgba(15,23,42,0.1);
  }

  .newsletter-input {
    display: flex;
    gap: 8px;
    margin-top: 10px;
  }

  .newsletter-input input {
    flex: 1;
    padding: 8px;
    border-radius: 10px;
    border: 1px solid rgba(15,23,42,0.1);
  }

  .newsletter-input button {
    background: #10b981;
    color: white;
    border: none;
    padding: 8px 12px;
    border-radius: 10px;
    font-weight: 900;
  }

  .footer-bottom {
    border-top: 1px solid rgba(15,23,42,0.08);
    padding: 12px 18px;
  }

  .footer-bottom-inner {
    max-width: 1280px;
    margin: auto;
    display: flex;
    justify-content: space-between;
    font-size: 13px;
    font-weight: 700;
    color: rgba(15,23,42,0.6);
  }

  @media (max-width: 900px) {
    .footer-inner {
      grid-template-columns: 1fr 1fr;
    }
  }

  @media (max-width: 520px) {
    .footer-inner {
      grid-template-columns: 1fr;
    }
  }
</style>

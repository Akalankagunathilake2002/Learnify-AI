<script lang="ts">
  import { onMount } from "svelte";

  let authed = false;

  onMount(() => {
    authed = !!localStorage.getItem("token");
  });
</script>

<section class="hero">
  <div class="hero-content">
    <h1>
      Welcome to <span>Learnify AI</span> 🚀
    </h1>

    <p class="subtitle">
      A modern AI-powered learning platform built with
      <strong>SvelteKit</strong>, <strong>FastAPI</strong>,
      <strong>PostgreSQL</strong>, <strong>Docker</strong>, and
      <strong>CI/CD</strong>.
    </p>

    <div class="actions">
      <a href="/courses" class="btn primary">Explore Courses</a>

      {#if authed}
        <a href="/me" class="btn secondary">My Profile</a>
      {:else}
        <a href="/login" class="btn secondary">Login</a>
      {/if}
    </div>
  </div>
</section>

<style>
  .hero {
    min-height: calc(100vh - 80px);
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: white;
    padding: 2rem;
  }

  .hero-content {
    max-width: 720px;
    text-align: center;
  }

  h1 {
    font-size: 3rem;
    margin-bottom: 1rem;
    font-weight: 800;
  }

  h1 span {
    color: #38bdf8;
  }

  .subtitle {
    font-size: 1.2rem;
    line-height: 1.7;
    opacity: 0.9;
    margin-bottom: 2.5rem;
  }

  .actions {
    display: flex;
    gap: 1rem;
    justify-content: center;
    flex-wrap: wrap;
  }

  .btn {
    padding: 0.75rem 1.6rem;
    border-radius: 8px;
    font-size: 1rem;
    text-decoration: none;
    font-weight: 600;
    transition: all 0.2s ease;
  }

  .btn.primary {
    background: #38bdf8;
    color: #0f172a;
  }

  .btn.primary:hover {
    background: #0ea5e9;
    transform: translateY(-2px);
  }

  .btn.secondary {
    border: 2px solid #38bdf8;
    color: #38bdf8;
  }

  .btn.secondary:hover {
    background: rgba(56, 189, 248, 0.15);
    transform: translateY(-2px);
  }
</style>

<script lang="ts">
  import { onMount } from "svelte";
  import { authed, syncAuthFromStorage } from "$lib/authStore";

  onMount(() => {
    syncAuthFromStorage();
  });
</script>

<nav style="padding: 12px; border-bottom: 1px solid #ddd;">
  <a href="/" style="margin-right: 12px;">Home</a>

  {#if $authed}
    <a href="/me" style="margin-right: 12px;">My Profile</a>
    <a href="/courses" style="margin-right: 12px;">Courses</a>
    <a href="/my-courses" style="margin-right: 12px;">My Courses</a>
    <a href="/billing">Upgrade</a>


    <a href="/logout">Logout</a>

  {:else}
    <a href="/login">Login</a>
    <span style="margin: 0 10px;">|</span>
  <a href="/register">Register</a>
  {/if}

  {#if $authed}
  <a href="/ai">AI Tutor</a>
{/if}

</nav>

<div style="padding: 16px;">
  <slot />
</div>

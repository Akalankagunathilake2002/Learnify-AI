<script lang="ts">
  import { goto } from "$app/navigation";
  import { onMount } from "svelte";

  const API_URL = import.meta.env.PUBLIC_API_URL ?? "http://127.0.0.1:8000";

  let loading = true;
  let error: string | null = null;
  let courses: any[] = [];

  async function load() {
    const token = localStorage.getItem("token");
    if (!token) return goto("/login");

    try {
      const res = await fetch(`${API_URL}/me/courses`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      courses = await res.json();
    } catch (e: any) {
      error = e?.message ?? "Failed";
    } finally {
      loading = false;
    }
  }

  onMount(load);
</script>

<h1>My Courses</h1>

{#if loading}
  <p>Loading...</p>
{:else if error}
  <p style="color:red">{error}</p>
{:else if courses.length === 0}
  <p>You are not enrolled in any courses yet.</p>
{:else}
  <ul>
    {#each courses as c}
      <li><a href={`/courses/${c.id}`}>{c.title}</a></li>
    {/each}
  </ul>
{/if}

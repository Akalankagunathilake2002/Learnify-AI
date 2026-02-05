<script lang="ts">
  import { goto } from "$app/navigation";
  import { onMount } from "svelte";

  const API_URL = import.meta.env.PUBLIC_API_URL ?? "http://127.0.0.1:8000";

  let loading = true;
  let error: string | null = null;
  let items: any[] = [];
  let role: string = "student";

  async function load() {
    loading = true;
    error = null;

    const token = localStorage.getItem("token");
    if (!token) return goto("/login");

    try {
      // get role
      const meRes = await fetch(`${API_URL}/users/me`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      if (meRes.ok) {
        const me = await meRes.json();
        role = me.role ?? "student";
      }

      // my courses
      const res = await fetch(`${API_URL}/my/courses`, {
        headers: { Authorization: `Bearer ${token}` }
      });

      if (!res.ok) {
        if (res.status === 401) {
          localStorage.removeItem("token");
          return goto("/login");
        }
        throw new Error(`HTTP ${res.status}`);
      }

      items = await res.json();
    } catch (e: any) {
      error = e?.message ?? "Failed to load my courses";
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
{:else if items.length === 0}
  <p>No courses found.</p>
{:else}
  <ul style="margin-top: 1rem">
    {#each items as c}
      <li
        style="
          margin-bottom: 1.2rem;
          padding-bottom: 1rem;
          border-bottom: 1px solid #eee;
        "
      >
        <a href={`/courses/${c.course_id}`}>
          <strong>{c.title}</strong>
        </a>

        <p style="margin: 6px 0">{c.description ?? ""}</p>

        <small style="opacity:0.8">Status: {c.status}</small>

        {#if role === "student"}
          <div style="margin-top: 8px">
            <small>
              Progress: {c.completed_lessons}/{c.total_lessons} ({c.percent}%)
            </small>
          </div>
        {:else}
          <div style="margin-top: 8px">
            <small>Total Lessons: {c.total_lessons}</small>
          </div>
        {/if}
      </li>
    {/each}
  </ul>
{/if}

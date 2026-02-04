<script lang="ts">
  import { goto } from "$app/navigation";
  import { onMount } from "svelte";

  const API_URL = import.meta.env.PUBLIC_API_URL ?? "http://127.0.0.1:8000";

  let loading = true;
  let error: string | null = null;
  let courses: any[] = [];

  async function loadCourses() {
    const token = localStorage.getItem("token");

    if (!token) {
      goto("/login");
      return;
    }

    try {
      const res = await fetch(`${API_URL}/courses`, {
        headers: { Authorization: `Bearer ${token}` }
      });

      if (!res.ok) {
        if (res.status === 401) {
          localStorage.removeItem("token");
          goto("/login");
          return;
        }
        throw new Error(`HTTP ${res.status}`);
      }

      courses = await res.json();
    } catch (e: any) {
      error = e?.message ?? "Failed to load courses";
    } finally {
      loading = false;
    }
  }

  onMount(loadCourses);
</script>

<h1>Courses</h1>

<p>
  <a href="/courses/new">+ Create Course</a>
</p>


{#if loading}
  <p>Loading...</p>
{:else if error}
  <p style="color:red">{error}</p>
{:else if courses.length === 0}
  <p>No courses available.</p>
{:else}
  <ul>
    {#each courses as course}
      <li>
        <a href={`/courses/${course.id}`}>
          <strong>{course.title}</strong>
        </a>
        <p>{course.description}</p>
      </li>
    {/each}
  </ul>
{/if}

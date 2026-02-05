<script lang="ts">
  import { goto } from "$app/navigation";
  import { page } from "$app/stores";
  import { onMount } from "svelte";

  const API_URL = import.meta.env.PUBLIC_API_URL ?? "http://127.0.0.1:8000";

  let loading = true;
  let error: string | null = null;
  let lesson: any = null;

  let doneMsg: string | null = null;

  async function loadLesson() {
    loading = true;
    error = null;

    const token = localStorage.getItem("token");
    if (!token) {
      goto("/login");
      return;
    }

    const lessonId = $page.params.id;

    try {
      const res = await fetch(`${API_URL}/courses/lessons/${lessonId}`, {
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

      lesson = await res.json();
    } catch (e: any) {
      error = e?.message ?? "Failed to load lesson";
    } finally {
      loading = false;
    }
  }

  async function markComplete() {
    doneMsg = null;

    const token = localStorage.getItem("token");
    if (!token) return goto("/login");

    const lessonId = $page.params.id;

    const res = await fetch(`${API_URL}/lessons/${lessonId}/complete`, {
      method: "POST",
      headers: { Authorization: `Bearer ${token}` }
    });

    if (!res.ok) {
      if (res.status === 401) {
        localStorage.removeItem("token");
        goto("/login");
        return;
      }
      doneMsg = `❌ Failed (HTTP ${res.status})`;
      return;
    }

    doneMsg = "✅ Marked as complete";
    // Optional refresh (keeps UI consistent)
    await loadLesson();
  }

  onMount(loadLesson);
</script>

<h1>Lesson</h1>

{#if loading}
  <p>Loading...</p>
{:else if error}
  <p style="color:red">{error}</p>
{:else}
  <h2>{lesson.title}</h2>
  <p style="white-space: pre-wrap">{lesson.content}</p>

  <button on:click={markComplete}>Mark Complete</button>
  {#if doneMsg}<p>{doneMsg}</p>{/if}

  <p style="margin-top:1rem">
    <a href={`/courses/${lesson.course_id}`}>← Back to course</a>
  </p>
{/if}

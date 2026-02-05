<script lang="ts">
  import { goto } from "$app/navigation";
  import { page } from "$app/stores";
  import { onMount } from "svelte";

  const API_URL = import.meta.env.PUBLIC_API_URL ?? "http://127.0.0.1:8000";

  let loading = true;
  let error: string | null = null;

  let course: any = null;
  let lessons: any[] = [];

  let newTitle = "";
  let newContent = "";
  let createMsg: string | null = null;

  async function fetchCourseAndLessons() {
    const token = localStorage.getItem("token");
    if (!token) {
      goto("/login");
      return;
    }

    const courseId = $page.params.id;

    try {
      const courseRes = await fetch(`${API_URL}/courses/${courseId}`, {
        headers: { Authorization: `Bearer ${token}` }
      });

      if (!courseRes.ok) throw new Error(`Course HTTP ${courseRes.status}`);
      course = await courseRes.json();

      const lessonsRes = await fetch(`${API_URL}/courses/${courseId}/lessons`, {
        headers: { Authorization: `Bearer ${token}` }
      });

      if (!lessonsRes.ok) throw new Error(`Lessons HTTP ${lessonsRes.status}`);
      lessons = await lessonsRes.json();
    } catch (e: any) {
      error = e?.message ?? "Failed to load course";
    } finally {
      loading = false;
    }
  }

  async function createLesson() {
    createMsg = null;
    const token = localStorage.getItem("token");
    if (!token) {
      goto("/login");
      return;
    }

    const courseId = $page.params.id;

    const res = await fetch(`${API_URL}/courses/${courseId}/lessons`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify({ title: newTitle, content: newContent })
    });

    if (!res.ok) {
      createMsg = "❌ Failed to create lesson";
      return;
    }

    createMsg = "✅ Lesson created";
    newTitle = "";
    newContent = "";
    await fetchCourseAndLessons();
  }

  onMount(fetchCourseAndLessons);


  let enrollMsg: string | null = null;

async function enroll() {
  enrollMsg = null;
  const token = localStorage.getItem("token");
  if (!token) return goto("/login");

  const courseId = $page.params.id;

  const res = await fetch(`${API_URL}/courses/${courseId}/enroll`, {
    method: "POST",
    headers: { Authorization: `Bearer ${token}` }
  });

  if (!res.ok) {
    enrollMsg = `❌ Enroll failed (HTTP ${res.status})`;
    return;
  }

  enrollMsg = "✅ Enrolled!";
}

</script>

{#if loading}
  <p>Loading...</p>
{:else if error}
  <p style="color:red">{error}</p>
{:else}
  <h1>{course.title}</h1>
  <p>{course.description}</p>

  <button on:click={enroll}>Enroll</button>
<p>{enrollMsg}</p>


  <hr />

  <h2>Lessons</h2>

  {#if lessons.length === 0}
    <p>No lessons yet.</p>
  {:else}
    <ul>
      {#each lessons as lesson}
        <li>
          <a href={`/lessons/${lesson.id}`}>{lesson.title}</a>
        </li>
      {/each}
    </ul>
  {/if}

  <hr />

  <h3>Add Lesson</h3>
  <input placeholder="Lesson title" bind:value={newTitle} />
  <br />
  <textarea rows="5" placeholder="Lesson content" bind:value={newContent}></textarea>
  <br />
  <button on:click={createLesson} disabled={!newTitle}>Create Lesson</button>

  {#if createMsg}
    <p>{createMsg}</p>
  {/if}

  <p style="margin-top:1rem">
    <a href="/courses">← Back to courses</a>
  </p>
{/if}

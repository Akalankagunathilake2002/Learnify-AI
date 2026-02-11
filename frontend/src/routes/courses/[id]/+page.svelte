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

  let enrollMsg: string | null = null;
  let progress: any = null;

  // ✅ role-based UI control
  let canEdit = false;

  function computeCanEdit() {
    const role = localStorage.getItem("role") ?? "student";
    canEdit = role === "instructor" || role === "admin";
  }

  // ✅ convert YouTube URL -> embed URL
  function toYoutubeEmbed(url: string) {
    if (!url) return "";

    const cleaned = url.trim();

    // youtu.be/VIDEO_ID
    const short = cleaned.match(/youtu\.be\/([a-zA-Z0-9_-]+)/);
    if (short) return `https://www.youtube.com/embed/${short[1]}`;

    // youtube.com/watch?v=VIDEO_ID
    const watch = cleaned.match(/[?&]v=([a-zA-Z0-9_-]+)/);
    if (watch) return `https://www.youtube.com/embed/${watch[1]}`;

    // already embed
    if (cleaned.includes("youtube.com/embed/")) return cleaned;

    return "";
  }

  async function loadProgress(courseId: string, token: string) {
    const res = await fetch(`${API_URL}/courses/${courseId}/progress`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    if (res.ok) progress = await res.json();
  }

  async function fetchCourseAndLessons() {
    loading = true;
    error = null;

    const token = localStorage.getItem("token");
    if (!token) return goto("/login");

    computeCanEdit();

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

      await loadProgress(courseId, token);
    } catch (e: any) {
      error = e?.message ?? "Failed to load course";
    } finally {
      loading = false;
    }
  }

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

  async function createLesson() {
    createMsg = null;

    const token = localStorage.getItem("token");
    if (!token) return goto("/login");

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
      if (res.status === 403) {
        createMsg = "❌ Only instructors can create lessons.";
        return;
      }
      createMsg = "❌ Failed to create lesson";
      return;
    }

    createMsg = "✅ Lesson created";
    newTitle = "";
    newContent = "";

    await fetchCourseAndLessons();
  }

  onMount(fetchCourseAndLessons);
</script>

{#if loading}
  <p>Loading...</p>
{:else if error}
  <p style="color:red">{error}</p>
{:else}
  <h1>{course.title}</h1>
  <p>{course.description}</p>

  <!-- ✅ Course Video -->
  {#if course?.video_url}
    {@const embed = toYoutubeEmbed(course.video_url)}
    {#if embed}
      <h3>Course Video</h3>
      <iframe
        width="560"
        height="315"
        src={embed}
        title="YouTube video player"
        frameborder="0"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
        allowfullscreen
      />
    {:else}
      <p style="color:red">Invalid YouTube link</p>
    {/if}
  {/if}

  {#if progress}
    <p>
      Progress: {progress.completed_lessons}/{progress.total_lessons}
      ({progress.percent}%)
    </p>
  {/if}

  <button on:click={enroll}>Enroll</button>
  {#if enrollMsg}<p>{enrollMsg}</p>{/if}

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

  {#if canEdit}
    <h3>Add Lesson</h3>
    <input placeholder="Lesson title" bind:value={newTitle} />
    <br />
    <textarea rows="5" placeholder="Lesson content" bind:value={newContent}></textarea>
    <br />
    <button on:click={createLesson} disabled={!newTitle}>Create Lesson</button>

    {#if createMsg}
      <p>{createMsg}</p>
    {/if}
  {:else}
    <p style="opacity:0.8">🔒 Only instructors can create lessons.</p>
  {/if}

  <p style="margin-top:1rem">
    <a href="/courses">← Back to courses</a>
  </p>
{/if}

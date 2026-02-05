<script lang="ts">
  import { goto } from "$app/navigation";
  import { onMount } from "svelte";

  const API_URL = import.meta.env.PUBLIC_API_URL ?? "http://127.0.0.1:8000";

  let loading = true;
  let error: string | null = null;
  let courses: any[] = [];
  let userRole: string | null = null;
  let actionMsg: string | null = null;

  async function loadCourses() {
    loading = true;
    error = null;
    actionMsg = null;

    const token = localStorage.getItem("token");
    if (!token) return goto("/login");

    try {
      // 1) load user (role)
      const meRes = await fetch(`${API_URL}/users/me`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      if (!meRes.ok) throw new Error(`Me HTTP ${meRes.status}`);
      const me = await meRes.json();
      userRole = me.role;

      // 2) load courses
      const res = await fetch(`${API_URL}/courses`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      if (!res.ok) throw new Error(`Courses HTTP ${res.status}`);
      courses = await res.json();
    } catch (e: any) {
      error = e?.message ?? "Failed to load courses";
    } finally {
      loading = false;
    }
  }

  const canManage = () => userRole === "admin" || userRole === "instructor";

  async function publish(courseId: number) {
    actionMsg = null;
    const token = localStorage.getItem("token");
    if (!token) return goto("/login");

    const res = await fetch(`${API_URL}/courses/${courseId}/publish`, {
      method: "POST",
      headers: { Authorization: `Bearer ${token}` }
    });

    if (!res.ok) {
      actionMsg = `❌ Publish failed (HTTP ${res.status})`;
      return;
    }

    actionMsg = "✅ Course published";
    await loadCourses();
  }

  async function unpublish(courseId: number) {
    actionMsg = null;
    const token = localStorage.getItem("token");
    if (!token) return goto("/login");

    const res = await fetch(`${API_URL}/courses/${courseId}/unpublish`, {
      method: "POST",
      headers: { Authorization: `Bearer ${token}` }
    });

    if (!res.ok) {
      actionMsg = `❌ Unpublish failed (HTTP ${res.status})`;
      return;
    }

    actionMsg = "✅ Course moved to draft";
    await loadCourses();
  }

  onMount(loadCourses);
</script>

<h1>Courses</h1>

{#if actionMsg}
  <p>{actionMsg}</p>
{/if}

{#if canManage()}
  <p>
    <a href="/courses/new">➕ Create Course</a>
  </p>
{/if}

{#if loading}
  <p>Loading...</p>
{:else if error}
  <p style="color:red">{error}</p>
{:else if courses.length === 0}
  <p>No courses available.</p>
{:else}
  <ul>
    {#each courses as course}
      <li style="margin-bottom: 1rem">
        <a href={`/courses/${course.id}`}>
          <strong>{course.title}</strong>
        </a>

        <p>{course.description}</p>

        <small
          style="
            display:inline-block;
            opacity:0.9;
            padding: 2px 8px;
            border-radius: 999px;
            margin-right: 10px;
            background: {course.status === 'published' ? '#dcfce7' : '#fee2e2'};
            color: {course.status === 'published' ? '#166534' : '#991b1b'};
          "
        >
          {course.status}
        </small>

        {#if canManage()}
          {#if course.status === "draft"}
            <button on:click={() => publish(course.id)}>Publish</button>
          {:else}
            <button on:click={() => unpublish(course.id)}>Unpublish</button>
          {/if}
        {/if}
      </li>
    {/each}
  </ul>
{/if}

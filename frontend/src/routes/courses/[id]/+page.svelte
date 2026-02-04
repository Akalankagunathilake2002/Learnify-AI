<script lang="ts">
  import { goto } from "$app/navigation";
  import { page } from "$app/stores";

  const API_URL = import.meta.env.PUBLIC_API_URL ?? "http://127.0.0.1:8000";

  let loading = true;
  let error: string | null = null;
  let course: any = null;

  async function loadCourse() {
    const token = localStorage.getItem("token");
    if (!token) {
      goto("/login");
      return;
    }

    const courseId = $page.params.id;

    try {
      const res = await fetch(`${API_URL}/courses/${courseId}`, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });

      if (!res.ok) {
        if (res.status === 401) {
          localStorage.removeItem("token");
          goto("/login");
          return;
        }
        throw new Error(`HTTP ${res.status}`);
      }

      course = await res.json();
    } catch (e: any) {
      error = e?.message ?? "Failed to load course";
    } finally {
      loading = false;
    }
  }

  loadCourse();
</script>

<h1>Course Details</h1>

{#if loading}
  <p>Loading...</p>
{:else if error}
  <p style="color:red">{error}</p>
{:else}
  <h2>{course.title}</h2>
  <p>{course.description}</p>
{/if}

<p style="margin-top:1rem">
  <a href="/courses">← Back to courses</a>
</p>

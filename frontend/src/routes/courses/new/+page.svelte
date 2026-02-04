<script lang="ts">
  import { goto } from "$app/navigation";
  import { onMount } from "svelte";

  const API_URL = import.meta.env.PUBLIC_API_URL ?? "http://127.0.0.1:8000";

  let title = "";
  let description = "";
  let error: string | null = null;
  let message: string | null = null;

  onMount(() => {
    const token = localStorage.getItem("token");
    if (!token) goto("/login");
  });

  async function createCourse() {
    error = null;
    message = null;

    const token = localStorage.getItem("token");
    if (!token) {
      goto("/login");
      return;
    }

    const res = await fetch(`${API_URL}/courses`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify({ title, description })
    });

    if (!res.ok) {
      const txt = await res.text();
      error = `Create failed: ${txt}`;
      return;
    }

    message = "✅ Course created!";
    const created = await res.json();
    setTimeout(() => goto(`/courses/${created.id}`), 600);
  }
</script>

<h1>Create Course</h1>

<input placeholder="Course Title" bind:value={title} />
<br />
<textarea placeholder="Description" bind:value={description} rows="5"></textarea>
<br />
<button on:click={createCourse}>Create</button>

{#if message}
  <p style="color:green">{message}</p>
{/if}

{#if error}
  <p style="color:red">{error}</p>
{/if}

<p style="margin-top:1rem">
  <a href="/courses">← Back to courses</a>
</p>

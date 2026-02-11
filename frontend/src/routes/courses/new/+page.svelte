<script lang="ts">
  import { goto } from "$app/navigation";
  import { onMount } from "svelte";

  const API_URL = import.meta.env.PUBLIC_API_URL ?? "http://127.0.0.1:8000";

  let title = "";
  let description = "";
  let videourl = "";

  let error: string | null = null;
  let message: string | null = null;
  let loading = false;

  onMount(() => {
    const token = localStorage.getItem("token");
    if (!token) goto("/login");
  });

  async function createCourse() {
    error = null;
    message = null;

    const token = localStorage.getItem("token");
    if (!token) return goto("/login");

    if (!title.trim()) {
      error = "Course title is required";
      return;
    }

    loading = true;

    const res = await fetch(`${API_URL}/courses`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`
      },
      body: JSON.stringify({
        title: title.trim(),
        description: description.trim() || null,
        video_url: videourl.trim() || null
      })
    });

    loading = false;

    if (!res.ok) {
      const txt = await res.text();
      error = `Create failed: ${txt}`;
      return;
    }

    const created = await res.json();
    message = "✅ Course created successfully!";
    setTimeout(() => goto(`/courses/${created.id}`), 800);
  }
</script>

<!-- PAGE BACKGROUND -->
<div
  style="
    min-height: 100vh;
    padding: 32px 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    background:
      radial-gradient(800px 420px at 10% 10%, rgba(16,185,129,0.18), transparent 60%),
      radial-gradient(800px 420px at 90% 15%, rgba(34,197,94,0.14), transparent 60%),
      linear-gradient(180deg, #f3fbf7 0%, #eef9f4 60%, #f1f5f9 100%);
  "
>
  <!-- CARD -->
  <div
    style="
      width: 100%;
      max-width: 560px;
      padding: 26px;
      border-radius: 22px;
      background: rgba(255,255,255,0.90);
      border: 1px solid rgba(15,23,42,0.10);
      box-shadow: 0 24px 55px rgba(15,23,42,0.12);
    "
  >
    <!-- Header -->
    <div style="margin-bottom: 22px; text-align: center;">
      <div
        style="
          width: 64px;
          height: 64px;
          margin: 0 auto 12px;
          border-radius: 20px;
          display: grid;
          place-items: center;
          background: rgba(16,185,129,0.18);
          border: 1px solid rgba(16,185,129,0.28);
          font-size: 28px;
        "
      >
        🎓
      </div>

      <h1
        style="
          margin: 0;
          font-size: 28px;
          font-weight: 950;
          color: #0f172a;
        "
      >
        Create New Course
      </h1>

      <p
        style="
          margin-top: 6px;
          font-size: 14px;
          color: rgba(15,23,42,0.65);
          font-weight: 650;
        "
      >
        Add a new course with title, description and video
      </p>
    </div>

    <!-- Course Title -->
    <div style="margin-bottom: 16px;">
      <label
        style="
          display:block;
          margin-bottom: 6px;
          font-size: 13px;
          font-weight: 900;
          color: rgba(15,23,42,0.78);
        "
      >
        Course Title *
      </label>
      <input
        placeholder="e.g. SvelteKit for Beginners"
        bind:value={title}
        style="
          width: 100%;
          padding: 12px 14px;
          border-radius: 14px;
          border: 1px solid rgba(15,23,42,0.14);
          background: #f8fafc;
          outline: none;
          font-size: 14px;
          font-weight: 700;
        "
      />
    </div>

    <!-- Description -->
    <div style="margin-bottom: 16px;">
      <label
        style="
          display:block;
          margin-bottom: 6px;
          font-size: 13px;
          font-weight: 900;
          color: rgba(15,23,42,0.78);
        "
      >
        Description
      </label>
      <textarea
        placeholder="Brief description of what students will learn"
        bind:value={description}
        rows="4"
        style="
          width: 100%;
          padding: 12px 14px;
          border-radius: 14px;
          border: 1px solid rgba(15,23,42,0.14);
          background: #f8fafc;
          outline: none;
          font-size: 14px;
          font-weight: 700;
          resize: vertical;
        "
      ></textarea>
    </div>

    <!-- Video URL -->
    <div style="margin-bottom: 18px;">
      <label
        style="
          display:block;
          margin-bottom: 6px;
          font-size: 13px;
          font-weight: 900;
          color: rgba(15,23,42,0.78);
        "
      >
        YouTube Video URL
      </label>
      <input
        placeholder="https://www.youtube.com/watch?v=xxxx"
        bind:value={videourl}
        style="
          width: 100%;
          padding: 12px 14px;
          border-radius: 14px;
          border: 1px solid rgba(15,23,42,0.14);
          background: #f8fafc;
          outline: none;
          font-size: 14px;
          font-weight: 700;
        "
      />
      <small style="color: rgba(15,23,42,0.55); font-weight: 650;">
        Optional – used as course preview thumbnail
      </small>
    </div>

    <!-- Error -->
    {#if error}
      <div
        style="
          margin-bottom: 14px;
          padding: 10px 12px;
          border-radius: 14px;
          background: rgba(239,68,68,0.12);
          border: 1px solid rgba(239,68,68,0.28);
          color: #b91c1c;
          font-weight: 850;
          font-size: 14px;
        "
      >
        {error}
      </div>
    {/if}

    <!-- Success -->
    {#if message}
      <div
        style="
          margin-bottom: 14px;
          padding: 10px 12px;
          border-radius: 14px;
          background: rgba(16,185,129,0.14);
          border: 1px solid rgba(16,185,129,0.28);
          color: #0f766e;
          font-weight: 850;
          font-size: 14px;
        "
      >
        {message}
      </div>
    {/if}

    <!-- Actions -->
    <button
      on:click={createCourse}
      disabled={loading}
      style="
        width: 100%;
        padding: 14px;
        border-radius: 16px;
        border: none;
        background: #10b981;
        color: white;
        font-size: 15px;
        font-weight: 950;
        cursor: pointer;
        box-shadow: 0 16px 34px rgba(16,185,129,0.30);
        opacity: {loading ? 0.6 : 1};
      "
    >
      {loading ? "Creating..." : "Create Course"}
    </button>

    <!-- Back link -->
    <div style="margin-top: 16px; text-align: center;">
      <a
        href="/courses"
        style="
          text-decoration: none;
          font-weight: 900;
          color: #0f766e;
        "
      >
        ← Back to courses
      </a>
    </div>
  </div>
</div>

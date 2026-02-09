<script lang="ts">
  import { goto } from "$app/navigation";
  import { onMount } from "svelte";

  const API_URL = import.meta.env.PUBLIC_API_URL ?? "http://127.0.0.1:8000";

  let loading = true;
  let error: string | null = null;
  let courses: any[] = [];
  let userRole: string | null = null;
  let actionMsg: string | null = null;

  // UI helpers
  let q = "";
  let filter: "all" | "published" | "draft" = "all";
  let sort: "newest" | "title" = "newest";

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

  // Derived list (no $derived needed)
  $: filtered = courses
    .filter((c) => {
      const matchesText =
        !q ||
        String(c.title ?? "").toLowerCase().includes(q.toLowerCase()) ||
        String(c.description ?? "").toLowerCase().includes(q.toLowerCase());

      const matchesFilter =
        filter === "all" ? true : (c.status ?? "").toLowerCase() === filter;

      return matchesText && matchesFilter;
    })
    .slice()
    .sort((a, b) => {
      if (sort === "title") {
        return String(a.title ?? "").localeCompare(String(b.title ?? ""));
      }
      // newest first if created_at exists, else keep stable
      const ad = Date.parse(a.created_at ?? "") || 0;
      const bd = Date.parse(b.created_at ?? "") || 0;
      return bd - ad;
    });

  const publishedCount = () => courses.filter((c) => c.status === "published").length;
  const draftCount = () => courses.filter((c) => c.status === "draft").length;

  onMount(loadCourses);
</script>

<div style="max-width: 1100px; margin: 34px auto; padding: 0 16px;">
  <!-- Header row -->
  <div style="display:flex; justify-content:space-between; align-items:flex-end; gap:14px; flex-wrap:wrap;">
    <div>
      <div style="font-size: 12px; font-weight: 950; color: #0f766e; letter-spacing: 0.3px;">
        LEARNIFY AI
      </div>
      <h1 style="margin: 6px 0 0; font-size: 34px; font-weight: 950; color:#0f172a;">
        Courses
      </h1>
      <p style="margin: 8px 0 0; color: rgba(15,23,42,0.65); font-weight: 650;">
        Browse courses, enroll, and learn faster with AI tools.
      </p>
    </div>

    {#if canManage()}
      <a
        href="/courses/new"
        style="
          text-decoration:none;
          padding: 12px 16px;
          border-radius: 14px;
          background: #10b981;
          color: white;
          font-weight: 950;
          box-shadow: 0 14px 30px rgba(16,185,129,0.20);
          display:inline-flex;
          align-items:center;
          gap:10px;
        "
      >
        ➕ Create Course
      </a>
    {/if}
  </div>

  <!-- Stats chips -->
  <div style="margin-top: 14px; display:flex; gap:10px; flex-wrap:wrap;">
    <span
      style="
        padding: 8px 12px;
        border-radius: 999px;
        background: rgba(255,255,255,0.85);
        border: 1px solid rgba(15,23,42,0.10);
        font-weight: 900;
        color: rgba(15,23,42,0.70);
      "
    >
      Total: <span style="color:#0f172a;">{courses.length}</span>
    </span>

    <span
      style="
        padding: 8px 12px;
        border-radius: 999px;
        background: rgba(16,185,129,0.10);
        border: 1px solid rgba(16,185,129,0.22);
        font-weight: 900;
        color: #0f766e;
      "
    >
      Published: <span style="color:#0f172a;">{publishedCount()}</span>
    </span>

    <span
      style="
        padding: 8px 12px;
        border-radius: 999px;
        background: rgba(14,165,233,0.10);
        border: 1px solid rgba(14,165,233,0.16);
        font-weight: 900;
        color: rgba(15,23,42,0.72);
      "
    >
      Draft: <span style="color:#0f172a;">{draftCount()}</span>
    </span>
  </div>

  <!-- Action message -->
  {#if actionMsg}
    <div
      style="
        margin-top: 14px;
        padding: 12px 14px;
        border-radius: 16px;
        background: rgba(255,255,255,0.85);
        border: 1px solid rgba(15,23,42,0.10);
        box-shadow: 0 14px 30px rgba(15,23,42,0.06);
        font-weight: 850;
        color: rgba(15,23,42,0.78);
      "
    >
      {actionMsg}
    </div>
  {/if}

  <!-- Controls -->
  <div
    style="
      margin-top: 16px;
      padding: 14px;
      border-radius: 18px;
      background: rgba(255,255,255,0.85);
      border: 1px solid rgba(15,23,42,0.10);
      box-shadow: 0 14px 30px rgba(15,23,42,0.06);
      display:flex;
      gap: 12px;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
    "
  >
    <div style="display:flex; gap:10px; flex-wrap:wrap; align-items:center; flex: 1;">
      <input
        placeholder="Search courses (title / description)…"
        bind:value={q}
        style="
          flex: 1;
          min-width: 240px;
          padding: 12px 12px;
          border-radius: 14px;
          border: 1px solid rgba(15,23,42,0.12);
          background: #f8fafc;
          outline: none;
          font-weight: 750;
          color: rgba(15,23,42,0.80);
        "
      />

      <select
        bind:value={filter}
        style="
          padding: 12px 12px;
          border-radius: 14px;
          border: 1px solid rgba(15,23,42,0.12);
          background: #ffffff;
          outline: none;
          font-weight: 850;
          color: rgba(15,23,42,0.75);
        "
      >
        <option value="all">All</option>
        <option value="published">Published</option>
        <option value="draft">Draft</option>
      </select>

      <select
        bind:value={sort}
        style="
          padding: 12px 12px;
          border-radius: 14px;
          border: 1px solid rgba(15,23,42,0.12);
          background: #ffffff;
          outline: none;
          font-weight: 850;
          color: rgba(15,23,42,0.75);
        "
      >
        <option value="newest">Sort: Newest</option>
        <option value="title">Sort: Title</option>
      </select>
    </div>

    <button
      on:click={loadCourses}
      disabled={loading}
      style="
        padding: 12px 14px;
        border-radius: 14px;
        border: 1px solid rgba(16,185,129,0.22);
        background: rgba(16,185,129,0.12);
        color: #0f766e;
        font-weight: 950;
        cursor: pointer;
        opacity: {loading ? 0.6 : 1};
      "
    >
      🔄 Refresh
    </button>
  </div>

  <!-- Content -->
  {#if loading}
    <div
      style="
        margin-top: 16px;
        padding: 18px;
        border-radius: 18px;
        background: rgba(255,255,255,0.85);
        border: 1px solid rgba(15,23,42,0.10);
        box-shadow: 0 14px 30px rgba(15,23,42,0.06);
        font-weight: 850;
        color: rgba(15,23,42,0.70);
      "
    >
      Loading courses…
    </div>

  {:else if error}
    <div
      style="
        margin-top: 16px;
        padding: 18px;
        border-radius: 18px;
        background: rgba(239,68,68,0.08);
        border: 1px solid rgba(239,68,68,0.25);
        color: #b91c1c;
        font-weight: 900;
      "
    >
      {error}
    </div>

  {:else if filtered.length === 0}
    <div
      style="
        margin-top: 16px;
        padding: 18px;
        border-radius: 18px;
        background: rgba(255,255,255,0.85);
        border: 1px solid rgba(15,23,42,0.10);
        box-shadow: 0 14px 30px rgba(15,23,42,0.06);
        color: rgba(15,23,42,0.70);
        font-weight: 800;
      "
    >
      No courses found. Try another search/filter.
    </div>

  {:else}
    <!-- Cards grid -->
    <div
      style="
        margin-top: 16px;
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 14px;
      "
    >
      {#each filtered as course}
        <div
          style="
            border-radius: 20px;
            background: rgba(255,255,255,0.88);
            border: 1px solid rgba(15,23,42,0.10);
            box-shadow: 0 14px 30px rgba(15,23,42,0.07);
            padding: 14px;
            display:flex;
            flex-direction: column;
            gap: 10px;
            min-height: 220px;
          "
        >
          <!-- Top row -->
          <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:10px;">
            <a
              href={`/courses/${course.id}`}
              style="
                text-decoration:none;
                color:#0f172a;
                font-weight: 950;
                font-size: 16px;
                line-height: 1.2;
              "
            >
              {course.title}
            </a>

            <span
              style="
                display:inline-block;
                padding: 6px 10px;
                border-radius: 999px;
                font-weight: 950;
                font-size: 12px;
                background: {course.status === 'published' ? 'rgba(16,185,129,0.14)' : 'rgba(239,68,68,0.10)'};
                border: 1px solid {course.status === 'published' ? 'rgba(16,185,129,0.22)' : 'rgba(239,68,68,0.22)'};
                color: {course.status === 'published' ? '#0f766e' : '#b91c1c'};
              "
            >
              {course.status}
            </span>
          </div>

          <!-- Description -->
          <div style="color: rgba(15,23,42,0.68); font-weight: 650; line-height: 1.6;">
            {course.description}
          </div>

          <!-- Meta row -->
          <div style="display:flex; gap:10px; flex-wrap:wrap; color: rgba(15,23,42,0.60); font-weight: 850; font-size: 13px;">
            <span style="padding: 6px 10px; border-radius: 999px; background: rgba(15,23,42,0.05); border: 1px solid rgba(15,23,42,0.08);">
              🆔 #{course.id}
            </span>

            {#if course.category}
              <span style="padding: 6px 10px; border-radius: 999px; background: rgba(14,165,233,0.08); border: 1px solid rgba(14,165,233,0.14);">
                🏷 {course.category}
              </span>
            {/if}
          </div>

          <!-- Spacer -->
          <div style="flex: 1;"></div>

          <!-- Actions -->
          <div style="display:flex; gap:10px; flex-wrap:wrap; align-items:center; justify-content:space-between;">
            <a
              href={`/courses/${course.id}`}
              style="
                text-decoration:none;
                font-weight: 950;
                color: #0f766e;
              "
            >
              View →
            </a>

            {#if canManage()}
              {#if course.status === "draft"}
                <button
                  on:click={() => publish(course.id)}
                  style="
                    padding: 10px 12px;
                    border-radius: 14px;
                    border: 1px solid rgba(16,185,129,0.24);
                    background: #10b981;
                    color: white;
                    font-weight: 950;
                    cursor: pointer;
                    box-shadow: 0 14px 30px rgba(16,185,129,0.18);
                  "
                >
                  Publish
                </button>
              {:else}
                <button
                  on:click={() => unpublish(course.id)}
                  style="
                    padding: 10px 12px;
                    border-radius: 14px;
                    border: 1px solid rgba(239,68,68,0.24);
                    background: rgba(239,68,68,0.10);
                    color: #b91c1c;
                    font-weight: 950;
                    cursor: pointer;
                  "
                >
                  Unpublish
                </button>
              {/if}
            {/if}
          </div>
        </div>
      {/each}
    </div>
  {/if}
</div>

<style>
  @media (max-width: 980px) {
    div[style*="grid-template-columns: repeat(3"] {
      grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
    }
  }
  @media (max-width: 640px) {
    div[style*="grid-template-columns: repeat(3"] {
      grid-template-columns: 1fr !important;
    }
  }
</style>

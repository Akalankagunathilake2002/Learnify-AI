<script lang="ts">
  import { goto } from "$app/navigation";
  import { onMount } from "svelte";

  const API_URL = import.meta.env.PUBLIC_API_URL ?? "http://127.0.0.1:8000";

  let loading = true;
  let error: string | null = null;
  let courses: any[] = [];

  let userRole: string = "";
  let actionMsg: string | null = null;

  // UI helpers
  let q = "";
  let filter: "all" | "published" | "draft" = "all";
  let sort: "newest" | "title" = "newest";

  function normalizeRole(role: any) {
    return String(role ?? "").toLowerCase().trim();
  }

  const canManage = () => userRole === "admin" || userRole === "instructor";

  // ✅ YouTube thumbnail helper
  function getYoutubeId(url: string) {
    if (!url) return "";
    const u = url.trim();

    const short = u.match(/youtu\.be\/([a-zA-Z0-9_-]+)/);
    if (short) return short[1];

    const watch = u.match(/[?&]v=([a-zA-Z0-9_-]+)/);
    if (watch) return watch[1];

    const embed = u.match(/youtube\.com\/embed\/([a-zA-Z0-9_-]+)/);
    if (embed) return embed[1];

    return "";
  }

  function youtubeThumb(url: string) {
    const id = getYoutubeId(url);
    if (!id) return "";
    return `https://img.youtube.com/vi/${id}/hqdefault.jpg`;
  }

  async function loadCourses() {
    loading = true;
    error = null;
    actionMsg = null;

    const token = localStorage.getItem("token");
    if (!token) return goto("/login");

    try {
      // ✅ 1) role
      const meRes = await fetch(`${API_URL}/users/me`, {
        headers: { Authorization: `Bearer ${token}` }
      });

      if (!meRes.ok) {
        if (meRes.status === 401) goto("/login");
        throw new Error(`Me HTTP ${meRes.status}`);
      }

      const me = await meRes.json();
      userRole = normalizeRole(me.role);

      console.log("✅ Logged in role =", me.role, "=> normalized =", userRole);

      // ✅ 2) courses
      const res = await fetch(`${API_URL}/courses`, {
        headers: { Authorization: `Bearer ${token}` }
      });

      if (!res.ok) {
        // Important: don’t crash whole page; just show message
        const txt = await res.text();
        error = `Courses API blocked (HTTP ${res.status}). ${txt}`;
        courses = [];
        return;
      }

      courses = await res.json();
    } catch (e: any) {
      error = e?.message ?? "Failed to load courses";
    } finally {
      loading = false;
    }
  }

  function goCreate() {
    // ✅ do NOT disable button; just block navigation if not allowed
    if (!canManage()) {
      actionMsg = `🔒 Only instructors/admin can create courses. (Your role: ${userRole || "unknown"})`;
      return;
    }
    goto("/courses/new");
  }

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
      if (sort === "title") return String(a.title ?? "").localeCompare(String(b.title ?? ""));
      const ad = Date.parse(a.created_at ?? "") || 0;
      const bd = Date.parse(b.created_at ?? "") || 0;
      return bd - ad;
    });

  const publishedCount = () => courses.filter((c) => c.status === "published").length;
  const draftCount = () => courses.filter((c) => c.status === "draft").length;

  onMount(loadCourses);
</script>

<div style="max-width: 1100px; margin: 34px auto; padding: 0 16px;">
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

      <div style="margin-top:10px; font-weight:900; color: rgba(15,23,42,0.65);">
        Role: <span style="color:#0f172a;">{userRole || "loading..."}</span>
      </div>
    </div>

    <!-- ✅ Always clickable -->
    <button
      on:click={goCreate}
      style="
        padding: 12px 16px;
        border-radius: 14px;
        background: {canManage() ? '#10b981' : 'rgba(15,23,42,0.10)'};
        color: {canManage() ? 'white' : 'rgba(15,23,42,0.65)'};
        font-weight: 950;
        border: 1px solid rgba(15,23,42,0.10);
        cursor: pointer;
        display:inline-flex;
        align-items:center;
        gap:10px;
      "
      title={canManage() ? "Create a new course" : "Only instructors/admin can create"}
    >
      ➕ Create Course
    </button>
  </div>

  <div style="margin-top: 14px; display:flex; gap:10px; flex-wrap:wrap;">
    <span style="padding: 8px 12px; border-radius: 999px; background: rgba(255,255,255,0.85); border: 1px solid rgba(15,23,42,0.10); font-weight: 900; color: rgba(15,23,42,0.70);">
      Total: <span style="color:#0f172a;">{courses.length}</span>
    </span>
    <span style="padding: 8px 12px; border-radius: 999px; background: rgba(16,185,129,0.10); border: 1px solid rgba(16,185,129,0.22); font-weight: 900; color: #0f766e;">
      Published: <span style="color:#0f172a;">{publishedCount()}</span>
    </span>
    <span style="padding: 8px 12px; border-radius: 999px; background: rgba(14,165,233,0.10); border: 1px solid rgba(14,165,233,0.16); font-weight: 900; color: rgba(15,23,42,0.72);">
      Draft: <span style="color:#0f172a;">{draftCount()}</span>
    </span>
  </div>

  {#if actionMsg}
    <div style="margin-top: 14px; padding: 12px 14px; border-radius: 16px; background: rgba(255,255,255,0.85); border: 1px solid rgba(15,23,42,0.10); box-shadow: 0 14px 30px rgba(15,23,42,0.06); font-weight: 850; color: rgba(15,23,42,0.78);">
      {actionMsg}
    </div>
  {/if}

  {#if loading}
    <div style="margin-top: 16px; padding: 18px; border-radius: 18px; background: rgba(255,255,255,0.85); border: 1px solid rgba(15,23,42,0.10); box-shadow: 0 14px 30px rgba(15,23,42,0.06); font-weight: 850; color: rgba(15,23,42,0.70);">
      Loading courses…
    </div>

  {:else if error}
    <div style="margin-top: 16px; padding: 18px; border-radius: 18px; background: rgba(239,68,68,0.08); border: 1px solid rgba(239,68,68,0.25); color: #b91c1c; font-weight: 900;">
      {error}
    </div>

  {:else}
    <div style="margin-top: 16px; display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 14px;">
      {#each filtered as course}
        {@const thumb = youtubeThumb(course.video_url ?? "")}

        <div style="border-radius: 20px; background: rgba(255,255,255,0.88); border: 1px solid rgba(15,23,42,0.10); box-shadow: 0 14px 30px rgba(15,23,42,0.07); overflow:hidden; display:flex; flex-direction: column; min-height: 260px;">
          {#if thumb}
            <a href={`/courses/${course.id}`} style="text-decoration:none;">
              <img src={thumb} alt="Course video thumbnail" style="width:100%; height:160px; object-fit:cover; display:block;" loading="lazy" />
            </a>
          {:else}
            <div style="height:160px; background: linear-gradient(135deg, rgba(16,185,129,0.12), rgba(14,165,233,0.10)); display:flex; align-items:center; justify-content:center; color: rgba(15,23,42,0.55); font-weight: 900;">
              No video
            </div>
          {/if}

          <div style="padding: 14px; display:flex; flex-direction: column; gap: 10px; flex:1;">
            <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:10px;">
              <a href={`/courses/${course.id}`} style="text-decoration:none; color:#0f172a; font-weight: 950; font-size: 16px; line-height: 1.2;">
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

            <div style="color: rgba(15,23,42,0.68); font-weight: 650; line-height: 1.6;">
              {course.description ?? ""}
            </div>

            <div style="display:flex; gap:10px; flex-wrap:wrap; color: rgba(15,23,42,0.60); font-weight: 850; font-size: 13px;">
              <span style="padding: 6px 10px; border-radius: 999px; background: rgba(15,23,42,0.05); border: 1px solid rgba(15,23,42,0.08);">
                🆔 #{course.id}
              </span>
            </div>

            <div style="flex: 1;"></div>

            <div style="display:flex; gap:10px; flex-wrap:wrap; align-items:center; justify-content:space-between;">
              <a href={`/courses/${course.id}`} style="text-decoration:none; font-weight: 950; color: #0f766e;">
                View →
              </a>

              {#if canManage()}
                {#if course.status === "draft"}
                  <button on:click={() => publish(course.id)} style="padding: 10px 12px; border-radius: 14px; border: 1px solid rgba(16,185,129,0.24); background: #10b981; color: white; font-weight: 950; cursor: pointer;">
                    Publish
                  </button>
                {:else}
                  <button on:click={() => unpublish(course.id)} style="padding: 10px 12px; border-radius: 14px; border: 1px solid rgba(239,68,68,0.24); background: rgba(239,68,68,0.10); color: #b91c1c; font-weight: 950; cursor: pointer;">
                    Unpublish
                  </button>
                {/if}
              {/if}
            </div>
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

<script lang="ts">
  import { goto } from "$app/navigation";
  import { onMount } from "svelte";

  const API_URL = import.meta.env.PUBLIC_API_URL ?? "http://127.0.0.1:8000";

  let loading = true;
  let error: string | null = null;
  let items: any[] = [];
  let role: string = "student";

  let q = "";

  // ✅ Optional: put fallback images here (or use c.image_url if backend provides)
  const fallbackImages = [
    "https://images.unsplash.com/photo-1523240795612-9a054b0db644?auto=format&fit=crop&w=1400&q=80",
    "https://images.unsplash.com/photo-1501504905252-473c47e087f8?auto=format&fit=crop&w=1400&q=80",
    "https://images.unsplash.com/photo-1513258496099-48168024aec0?auto=format&fit=crop&w=1400&q=80",
    "https://images.unsplash.com/photo-1519389950473-47ba0277781c?auto=format&fit=crop&w=1400&q=80",
    "https://images.unsplash.com/photo-1531482615713-2afd69097998?auto=format&fit=crop&w=1400&q=80"
  ];

  function getCourseImage(c: any) {
    if (c?.image_url) return c.image_url; // if backend sends image url
    const id = Number(c?.course_id ?? c?.id ?? 1);
    return fallbackImages[(id * 17) % fallbackImages.length];
  }

  function badgeColor(status: string) {
    const s = (status ?? "").toLowerCase();
    if (s.includes("publish")) return { bg: "rgba(16,185,129,0.12)", bd: "rgba(16,185,129,0.24)", fg: "#0f766e" };
    if (s.includes("draft")) return { bg: "rgba(245,158,11,0.12)", bd: "rgba(245,158,11,0.26)", fg: "#92400e" };
    return { bg: "rgba(15,23,42,0.06)", bd: "rgba(15,23,42,0.10)", fg: "rgba(15,23,42,0.75)" };
  }

  function clampPercent(p: any) {
    const n = Number(p);
    if (Number.isNaN(n)) return 0;
    return Math.max(0, Math.min(100, Math.round(n)));
  }

  async function load() {
    loading = true;
    error = null;

    const token = localStorage.getItem("token");
    if (!token) return goto("/login");

    try {
      // 1) get role
      const meRes = await fetch(`${API_URL}/users/me`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      if (meRes.ok) {
        const me = await meRes.json();
        role = me.role ?? "student";
      }

      // 2) my courses
      // ⚠️ If your swagger shows GET /me/courses, use that:
      // const res = await fetch(`${API_URL}/me/courses`, ...
      const res = await fetch(`${API_URL}/my/courses`, {
        headers: { Authorization: `Bearer ${token}` }
      });

      if (!res.ok) {
        if (res.status === 401) {
          localStorage.removeItem("token");
          return goto("/login");
        }
        throw new Error(`HTTP ${res.status}`);
      }

      const data = await res.json();

      // support array OR {items:[]}
      items = Array.isArray(data) ? data : Array.isArray(data?.items) ? data.items : [];
    } catch (e: any) {
      error = e?.message ?? "Failed to load my courses";
    } finally {
      loading = false;
    }
  }

  $: filtered =
    q.trim().length === 0
      ? items
      : items.filter((c) => {
          const t = `${c?.title ?? ""} ${c?.description ?? ""}`.toLowerCase();
          return t.includes(q.toLowerCase());
        });

  onMount(load);
</script>

<!-- Page wrapper -->
<div style="max-width: 1200px; margin: 28px auto; padding: 0 16px;">
  <!-- Header row -->
  <div style="display:flex; justify-content:space-between; align-items:flex-end; gap: 12px; flex-wrap: wrap;">
    <div>
      <div style="font-size: 12px; font-weight: 950; letter-spacing: 0.3px; color:#0f766e;">
        MY LEARNING
      </div>
      <h1 style="margin: 6px 0 0; font-size: 30px; font-weight: 980; color:#0f172a;">
        My Courses
      </h1>
      <p style="margin: 8px 0 0; color: rgba(15,23,42,0.65); font-weight: 650; line-height: 1.6;">
        View your enrolled courses and track your progress.
      </p>
    </div>

    <div style="display:flex; align-items:center; gap: 10px; flex-wrap: wrap;">
      <div
        style="
          padding: 8px 12px;
          border-radius: 999px;
          background: rgba(16,185,129,0.12);
          border: 1px solid rgba(16,185,129,0.22);
          color: #0f766e;
          font-weight: 950;
          font-size: 13px;
        "
      >
        👤 Role: {role}
      </div>

      <a
        href="/courses"
        style="
          text-decoration:none;
          padding: 10px 14px;
          border-radius: 14px;
          background: rgba(15,23,42,0.06);
          border: 1px solid rgba(15,23,42,0.12);
          color: rgba(15,23,42,0.80);
          font-weight: 900;
        "
      >
        Browse Courses →
      </a>
    </div>
  </div>

  <!-- Search + count -->
  <div style="margin-top: 14px; display:flex; gap: 10px; flex-wrap: wrap; align-items:center;">
    <input
      placeholder="Search your courses..."
      bind:value={q}
      style="
        flex: 1;
        min-width: 220px;
        padding: 12px 14px;
        border-radius: 14px;
        border: 1px solid rgba(15,23,42,0.12);
        background: rgba(255,255,255,0.88);
        outline: none;
        font-size: 14px;
        font-weight: 700;
      "
    />

    <div
      style="
        padding: 10px 12px;
        border-radius: 14px;
        background: rgba(255,255,255,0.88);
        border: 1px solid rgba(15,23,42,0.10);
        color: rgba(15,23,42,0.70);
        font-weight: 850;
        font-size: 13px;
      "
    >
      Showing: {filtered.length} / {items.length}
    </div>
  </div>

  <!-- Content -->
  {#if loading}
    <div
      style="
        margin-top: 16px;
        padding: 22px;
        border-radius: 18px;
        background: rgba(255,255,255,0.88);
        border: 1px solid rgba(15,23,42,0.10);
        box-shadow: 0 14px 30px rgba(15,23,42,0.06);
        font-weight: 850;
        color: rgba(15,23,42,0.70);
      "
    >
      Loading your courses…
    </div>

  {:else if error}
    <div
      style="
        margin-top: 16px;
        padding: 22px;
        border-radius: 18px;
        background: rgba(239,68,68,0.10);
        border: 1px solid rgba(239,68,68,0.22);
        color: #b91c1c;
        font-weight: 900;
      "
    >
      ⚠️ {error}
    </div>

  {:else if filtered.length === 0}
    <div
      style="
        margin-top: 16px;
        padding: 22px;
        border-radius: 18px;
        background: rgba(255,255,255,0.88);
        border: 1px solid rgba(15,23,42,0.10);
        box-shadow: 0 14px 30px rgba(15,23,42,0.06);
        color: rgba(15,23,42,0.72);
        font-weight: 850;
      "
    >
      No courses found. Try a different search or enroll from
      <a href="/courses" style="color:#0f766e; font-weight: 950; text-decoration:none;">Courses</a>.
    </div>

  {:else}
    <!-- Grid -->
    <div
      style="
        margin-top: 16px;
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 14px;
      "
    >
      {#each filtered as c}
        {@const statusStyle = badgeColor(c.status)}
        {@const percent = clampPercent(c.percent)}
        <div
          style="
            border-radius: 22px;
            overflow: hidden;
            background: rgba(255,255,255,0.90);
            border: 1px solid rgba(15,23,42,0.10);
            box-shadow: 0 14px 30px rgba(15,23,42,0.08);
            display: flex;
            flex-direction: column;
            min-height: 310px;
          "
        >
          <!-- Image header -->
          <div style="height: 118px; position: relative;">
            <img
              src={getCourseImage(c)}
              alt="Course cover"
              style="width:100%; height:100%; object-fit: cover;"
            />
            <div
              style="
                position:absolute;
                inset:0;
                background: linear-gradient(180deg, rgba(0,0,0,0.00), rgba(0,0,0,0.38));
              "
            ></div>

            <div
              style="
                position:absolute;
                left: 12px;
                bottom: 10px;
                padding: 6px 10px;
                border-radius: 999px;
                background: rgba(255,255,255,0.90);
                border: 1px solid rgba(15,23,42,0.10);
                font-weight: 950;
                color: rgba(15,23,42,0.80);
                font-size: 12px;
              "
            >
              📘 Enrolled
            </div>

            <div
              style="
                position:absolute;
                right: 12px;
                bottom: 10px;
                padding: 6px 10px;
                border-radius: 999px;
                background: {statusStyle.bg};
                border: 1px solid {statusStyle.bd};
                color: {statusStyle.fg};
                font-weight: 950;
                font-size: 12px;
              "
            >
              {c.status ?? "unknown"}
            </div>
          </div>

          <!-- Body -->
          <div style="padding: 14px; display:flex; flex-direction:column; gap: 10px; flex: 1;">
            <a
              href={`/courses/${c.course_id ?? c.id}`}
              style="
                text-decoration:none;
                color:#0f172a;
                font-weight: 980;
                font-size: 15px;
                line-height: 1.25;
              "
            >
              {c.title ?? "Untitled course"}
            </a>

            {#if c.description}
              <div style="color: rgba(15,23,42,0.65); font-weight: 650; font-size: 13px; line-height: 1.55;">
                {c.description}
              </div>
            {/if}

            <!-- Student progress -->
            {#if role === "student"}
              <div style="margin-top: 2px;">
                <div style="display:flex; justify-content:space-between; align-items:center; gap:10px;">
                  <div style="font-size: 12px; font-weight: 900; color: rgba(15,23,42,0.70);">
                    Progress
                    {#if c.total_lessons}
                      • {c.completed_lessons}/{c.total_lessons} lessons
                    {/if}
                  </div>
                  <div style="font-size: 12px; font-weight: 950; color:#0f766e;">
                    {percent}%
                  </div>
                </div>

                <div
                  style="
                    margin-top: 8px;
                    height: 10px;
                    border-radius: 999px;
                    background: rgba(15,23,42,0.08);
                    overflow:hidden;
                    border: 1px solid rgba(15,23,42,0.10);
                  "
                >
                  <div
                    style="
                      height: 100%;
                      width: {percent}%;
                      background: linear-gradient(90deg, rgba(16,185,129,0.95), rgba(34,197,94,0.85));
                      border-radius: 999px;
                    "
                  ></div>
                </div>
              </div>
            {:else}
              <div style="font-size: 12px; color: rgba(15,23,42,0.65); font-weight: 800;">
                Total Lessons: {c.total_lessons ?? "--"}
              </div>
            {/if}

            <div style="flex: 1;"></div>

            <!-- Actions -->
            <div style="display:flex; justify-content:space-between; align-items:center; gap: 10px; flex-wrap: wrap;">
              <a
                href={`/courses/${c.course_id ?? c.id}`}
                style="
                  text-decoration:none;
                  font-weight: 950;
                  color:#0f766e;
                "
              >
                Continue →
              </a>

              {#if role === "student"}
                <span
                  style="
                    padding: 6px 10px;
                    border-radius: 999px;
                    background: rgba(14,165,233,0.10);
                    border: 1px solid rgba(14,165,233,0.16);
                    color: rgba(15,23,42,0.74);
                    font-weight: 900;
                    font-size: 12px;
                  "
                >
                  ✅ Tracked
                </span>
              {/if}
            </div>
          </div>
        </div>
      {/each}
    </div>
  {/if}
</div>

<style>
  @media (max-width: 1000px) {
    div[style*="grid-template-columns: repeat(3"] {
      grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
    }
  }
  @media (max-width: 680px) {
    div[style*="grid-template-columns: repeat(3"],
    div[style*="grid-template-columns: repeat(2"] {
      grid-template-columns: 1fr !important;
    }
  }
</style>

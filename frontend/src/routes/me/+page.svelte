<script lang="ts">
  import { onMount } from "svelte";
  import { goto } from "$app/navigation";

  const API_URL = import.meta.env.PUBLIC_API_URL ?? "http://127.0.0.1:8000";
  const MY_COURSES_ENDPOINT = "/me/courses";


  let loading = true;
  let error: string | null = null;

  let user: any = null;

  // Enrolled courses
  let enrolledCount: number | null = null;
  let enrolledCourses: any[] = [];

  function getList(data: any): any[] {
    return Array.isArray(data)
      ? data
      : Array.isArray(data?.items)
        ? data.items
        : Array.isArray(data?.courses)
          ? data.courses
          : Array.isArray(data?.enrollments)
            ? data.enrollments
            : [];
  }

  // If backend doesn't have progress yet, create stable progress from course id
  function getProgress(course: any): number {
    const p = Number(course?.progress);
    if (!Number.isNaN(p) && p >= 0 && p <= 100) return Math.round(p);

    const idNum = Number(course?.id ?? 1);
    const stable = (idNum * 37) % 91; // 0..90
    return Math.max(8, Math.min(95, stable)); // keep it realistic
  }

  function getCourseImage(course: any): string {
    // If your backend returns course.image_url use it
    if (course?.image_url) return course.image_url;

    // fallback images (you can replace later)
    const imgs = [
      "https://images.unsplash.com/photo-1523240795612-9a054b0db644?auto=format&fit=crop&w=1200&q=80",
      "https://images.unsplash.com/photo-1501504905252-473c47e087f8?auto=format&fit=crop&w=1200&q=80",
      "https://images.unsplash.com/photo-1513258496099-48168024aec0?auto=format&fit=crop&w=1200&q=80",
      "https://images.unsplash.com/photo-1519389950473-47ba0277781c?auto=format&fit=crop&w=1200&q=80",
      "https://images.unsplash.com/photo-1531482615713-2afd69097998?auto=format&fit=crop&w=1200&q=80"
    ];
    const idx = (Number(course?.id ?? 1) * 17) % imgs.length;
    return imgs[idx];
  }

  async function loadMe() {
    const token = localStorage.getItem("token");

    if (!token) {
      goto("/login");
      return;
    }

    loading = true;
    error = null;

    try {
      // 1) user
      const meRes = await fetch(`${API_URL}/users/me`, {
        headers: { Authorization: `Bearer ${token}` }
      });

      if (!meRes.ok) {
        if (meRes.status === 401) {
          localStorage.removeItem("token");
          localStorage.removeItem("role");
          goto("/login");
          return;
        }
        throw new Error(`Profile HTTP ${meRes.status}`);
      }

      user = await meRes.json();
      localStorage.setItem("role", user.role ?? "student");

      // 2) enrolled courses (list + count)
      const coursesRes = await fetch(`${API_URL}${MY_COURSES_ENDPOINT}`, {
        headers: { Authorization: `Bearer ${token}` }
      });

      if (coursesRes.ok) {
        const data = await coursesRes.json();
        enrolledCourses = getList(data);
        enrolledCount = enrolledCourses.length;
      } else {
        enrolledCourses = [];
        enrolledCount = null;
      }
    } catch (e: any) {
      error = e?.message ?? "Failed to load profile";
    } finally {
      loading = false;
    }
  }

  onMount(loadMe);
</script>

<div style="max-width: 1100px; margin: 34px auto; padding: 0 16px;">
  <h1
    style="
      font-size: 32px;
      font-weight: 950;
      color: #0f172a;
      margin: 0 0 16px 0;
    "
  >
    My Profile
  </h1>

  {#if loading}
    <div
      style="
        padding: 24px;
        border-radius: 18px;
        background: rgba(255,255,255,0.85);
        border: 1px solid rgba(15,23,42,0.10);
        box-shadow: 0 14px 30px rgba(15,23,42,0.06);
        font-weight: 800;
        color: rgba(15,23,42,0.70);
      "
    >
      Loading your profile…
    </div>

  {:else if error}
    <div
      style="
        padding: 24px;
        border-radius: 18px;
        background: rgba(239,68,68,0.08);
        border: 1px solid rgba(239,68,68,0.25);
        color: #b91c1c;
        font-weight: 850;
      "
    >
      {error}
    </div>

  {:else}
    <!-- PROFILE CARD -->
    <div
      style="
        display: grid;
        grid-template-columns: 140px 1fr;
        gap: 22px;
        padding: 22px;
        border-radius: 22px;
        background: rgba(255,255,255,0.88);
        border: 1px solid rgba(15,23,42,0.10);
        box-shadow: 0 18px 40px rgba(15,23,42,0.08);
        align-items: center;
      "
    >
      <div
        style="
          width: 120px;
          height: 120px;
          border-radius: 28px;
          display: grid;
          place-items: center;
          background: linear-gradient(135deg, rgba(16,185,129,0.25), rgba(14,165,233,0.18));
          border: 1px solid rgba(16,185,129,0.35);
          font-size: 52px;
          font-weight: 950;
          color: #0f766e;
        "
        title="User avatar"
      >
        👤
      </div>

      <div>
        <div style="font-size: 18px; font-weight: 950; color: #0f172a; margin-bottom: 6px;">
          {user.email}
        </div>

        <div style="display:flex; gap:10px; flex-wrap:wrap; align-items:center; margin-bottom: 12px;">
          <div
            style="
              padding: 6px 12px;
              border-radius: 999px;
              font-size: 13px;
              font-weight: 900;
              background: rgba(16,185,129,0.12);
              border: 1px solid rgba(16,185,129,0.25);
              color: #0f766e;
            "
          >
            {user.role ?? "student"}
          </div>

          <div
            style="
              display: inline-flex;
              align-items: center;
              gap: 8px;
              padding: 6px 12px;
              border-radius: 999px;
              font-size: 13px;
              font-weight: 900;
              background: rgba(14,165,233,0.10);
              border: 1px solid rgba(14,165,233,0.16);
              color: rgba(15,23,42,0.74);
            "
          >
            📚 Enrolled:
            <span style="color:#0f172a;">
              {#if enrolledCount === null}--{:else}{enrolledCount}{/if}
            </span>
          </div>
        </div>

        <div
          style="
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 12px;
            margin-bottom: 14px;
          "
        >
          <div style="border-radius: 16px; padding: 12px; background: rgba(255,255,255,0.78); border: 1px solid rgba(15,23,42,0.10);">
            <div style="font-size: 12px; font-weight: 900; color: rgba(15,23,42,0.60);">Enrolled Courses</div>
            <div style="margin-top: 6px; font-size: 20px; font-weight: 950; color:#0f172a;">
              {#if enrolledCount === null}--{:else}{enrolledCount}{/if}
            </div>
          </div>

          <div style="border-radius: 16px; padding: 12px; background: rgba(255,255,255,0.78); border: 1px solid rgba(15,23,42,0.10);">
            <div style="font-size: 12px; font-weight: 900; color: rgba(15,23,42,0.60);">Plan</div>
            <div style="margin-top: 6px; font-size: 20px; font-weight: 950; color:#0f172a;">{user?.plan ?? "Free"}</div>
          </div>

          <div style="border-radius: 16px; padding: 12px; background: rgba(255,255,255,0.78); border: 1px solid rgba(15,23,42,0.10);">
            <div style="font-size: 12px; font-weight: 900; color: rgba(15,23,42,0.60);">Status</div>
            <div style="margin-top: 6px; font-size: 20px; font-weight: 950; color:#0f172a;">Active</div>
          </div>
        </div>

        <div style="display: flex; gap: 12px; flex-wrap: wrap;">
          <a
            href="/my-courses"
            style="
              text-decoration: none;
              padding: 10px 14px;
              border-radius: 14px;
              background: rgba(16,185,129,0.12);
              border: 1px solid rgba(16,185,129,0.22);
              color: #0f766e;
              font-weight: 950;
            "
          >
            📚 My Courses
          </a>

          <a
            href="/billing"
            style="
              text-decoration: none;
              padding: 10px 14px;
              border-radius: 14px;
              background: #10b981;
              color: white;
              font-weight: 950;
              box-shadow: 0 14px 30px rgba(16,185,129,0.20);
            "
          >
            ⭐ Upgrade
          </a>

          <a
            href="/logout"
            style="
              text-decoration: none;
              padding: 10px 14px;
              border-radius: 14px;
              background: rgba(15,23,42,0.06);
              border: 1px solid rgba(15,23,42,0.12);
              color: rgba(15,23,42,0.75);
              font-weight: 900;
            "
          >
            Logout
          </a>
        </div>
      </div>
    </div>

    <!-- ✅ NEW: My Learning section (fills empty space) -->
    <div style="margin-top: 18px;">
      <div style="display:flex; justify-content:space-between; align-items:flex-end; gap:12px; flex-wrap:wrap;">
        <div>
          <div style="font-size: 12px; font-weight: 950; color:#0f766e; letter-spacing:0.3px;">MY LEARNING</div>
          <h2 style="margin: 6px 0 0; font-size: 22px; font-weight: 950; color:#0f172a;">
            Continue where you left off
          </h2>
          <p style="margin: 8px 0 0; color: rgba(15,23,42,0.65); font-weight: 650;">
            Track your enrolled courses and progress.
          </p>
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
          Browse more courses →
        </a>
      </div>

      {#if enrolledCourses.length === 0}
        <div
          style="
            margin-top: 14px;
            padding: 18px;
            border-radius: 18px;
            background: rgba(255,255,255,0.88);
            border: 1px solid rgba(15,23,42,0.10);
            box-shadow: 0 14px 30px rgba(15,23,42,0.06);
            color: rgba(15,23,42,0.70);
            font-weight: 800;
          "
        >
          You haven’t enrolled in any courses yet. Go to <a href="/courses" style="font-weight:950; color:#0f766e; text-decoration:none;">Courses</a> and enroll.
        </div>
      {:else}
        <div
          style="
            margin-top: 14px;
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 14px;
          "
        >
          {#each enrolledCourses as c}
            {@const p = getProgress(c)}
            <div
              style="
                border-radius: 20px;
                overflow: hidden;
                background: rgba(255,255,255,0.90);
                border: 1px solid rgba(15,23,42,0.10);
                box-shadow: 0 14px 30px rgba(15,23,42,0.08);
                display:flex;
                flex-direction: column;
                min-height: 280px;
              "
            >
              <!-- image -->
              <div style="height: 120px; position: relative;">
                <img
                  src={getCourseImage(c)}
                  alt="Course cover"
                  style="width:100%; height:100%; object-fit: cover;"
                />
                <div
                  style="
                    position:absolute;
                    inset:0;
                    background: linear-gradient(180deg, rgba(0,0,0,0.00), rgba(0,0,0,0.35));
                  "
                ></div>
                <div
                  style="
                    position:absolute;
                    left: 12px;
                    bottom: 10px;
                    padding: 6px 10px;
                    border-radius: 999px;
                    background: rgba(255,255,255,0.88);
                    border: 1px solid rgba(15,23,42,0.10);
                    font-weight: 950;
                    color: rgba(15,23,42,0.80);
                    font-size: 12px;
                  "
                >
                  📈 {p}% complete
                </div>
              </div>

              <div style="padding: 14px; display:flex; flex-direction: column; gap: 10px; flex: 1;">
                <div style="font-weight: 950; color:#0f172a; font-size: 15px; line-height: 1.25;">
                  {c.title ?? "Untitled course"}
                </div>

                <div style="color: rgba(15,23,42,0.65); font-weight: 650; font-size: 13px; line-height: 1.55;">
                  {c.description ?? "No description yet."}
                </div>

                <!-- progress bar -->
                <div style="margin-top: 2px;">
                  <div
                    style="
                      height: 10px;
                      border-radius: 999px;
                      background: rgba(15,23,42,0.08);
                      overflow: hidden;
                      border: 1px solid rgba(15,23,42,0.10);
                    "
                  >
                    <div
                      style="
                        height: 100%;
                        width: {p}%;
                        background: linear-gradient(90deg, rgba(16,185,129,0.95), rgba(34,197,94,0.85));
                        border-radius: 999px;
                      "
                    ></div>
                  </div>
                </div>

                <div style="flex:1;"></div>

                <div style="display:flex; gap:10px; flex-wrap:wrap; justify-content: space-between; align-items:center;">
                  <a
                    href={`/courses/${c.id}`}
                    style="
                      text-decoration:none;
                      font-weight: 950;
                      color: #0f766e;
                    "
                  >
                    Continue →
                  </a>

                  <span
                    style="
                      padding: 6px 10px;
                      border-radius: 999px;
                      background: rgba(16,185,129,0.12);
                      border: 1px solid rgba(16,185,129,0.22);
                      color: #0f766e;
                      font-weight: 950;
                      font-size: 12px;
                    "
                  >
                    Enrolled
                  </span>
                </div>
              </div>
            </div>
          {/each}
        </div>
      {/if}
    </div>

    <!-- Debug (optional) -->
    <details style="margin-top: 18px;">
      <summary style="cursor: pointer; font-weight: 900; color: rgba(15,23,42,0.70);">
        Debug: Full user object
      </summary>
      <pre
        style="
          margin-top: 12px;
          padding: 16px;
          border-radius: 14px;
          background: rgba(15,23,42,0.05);
          border: 1px solid rgba(15,23,42,0.10);
          font-size: 13px;
          overflow-x: auto;
        "
      >
{JSON.stringify(user, null, 2)}
      </pre>
    </details>
  {/if}
</div>

<style>
  @media (max-width: 980px) {
    div[style*="grid-template-columns: repeat(3, minmax(0, 1fr))"] {
      grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
    }
  }

  @media (max-width: 740px) {
    div[style*="grid-template-columns: 140px"] {
      grid-template-columns: 1fr !important;
      text-align: center;
    }

    div[style*="grid-template-columns: repeat(3, minmax(0, 1fr))"] {
      grid-template-columns: 1fr !important;
    }
  }
</style>

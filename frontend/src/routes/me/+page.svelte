<script lang="ts">
  import { onMount } from "svelte";
  import { goto } from "$app/navigation";

  const API_URL = import.meta.env.PUBLIC_API_URL ?? "http://127.0.0.1:8000";

  // ✅ If your backend uses a different path, change only this:
  const MY_COURSES_ENDPOINT = "/courses/my";

  let loading = true;
  let error: string | null = null;

  let user: any = null;

  // ✅ enrolled courses count
  let enrolledCount: number | null = null;

  async function loadMe() {
    const token = localStorage.getItem("token");

    if (!token) {
      goto("/login");
      return;
    }

    try {
      // 1) Load user
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

      // 2) Load enrolled courses (count)
      //    Expected response: array OR { items: [] } OR { courses: [] }
      const coursesRes = await fetch(`${API_URL}${MY_COURSES_ENDPOINT}`, {
        headers: { Authorization: `Bearer ${token}` }
      });

      if (coursesRes.ok) {
        const data = await coursesRes.json();

        // Support multiple response shapes
        const list =
          Array.isArray(data) ? data :
          Array.isArray(data?.items) ? data.items :
          Array.isArray(data?.courses) ? data.courses :
          Array.isArray(data?.enrollments) ? data.enrollments :
          [];

        enrolledCount = list.length;
      } else {
        // Don't fail the whole profile page if count endpoint fails
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

<!-- PAGE WRAPPER -->
<div style="max-width: 900px; margin: 40px auto; padding: 0 16px;">
  <h1
    style="
      font-size: 32px;
      font-weight: 950;
      color: #0f172a;
      margin-bottom: 20px;
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
        background: rgba(255,255,255,0.85);
        border: 1px solid rgba(15,23,42,0.10);
        box-shadow: 0 18px 40px rgba(15,23,42,0.08);
        align-items: center;
      "
    >
      <!-- Avatar -->
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

      <!-- User Info -->
      <div>
        <div
          style="
            font-size: 18px;
            font-weight: 950;
            color: #0f172a;
            margin-bottom: 6px;
          "
        >
          {user.email}
        </div>

        <div style="display:flex; gap:10px; flex-wrap:wrap; align-items:center; margin-bottom: 12px;">
          <!-- Role badge -->
          <div
            style="
              display: inline-block;
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

          <!-- Enrolled courses badge -->
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
            title="Number of courses you enrolled"
          >
            📚 Enrolled:
            <span style="color:#0f172a;">
              {#if enrolledCount === null}
                --
              {:else}
                {enrolledCount}
              {/if}
            </span>
          </div>
        </div>

        <!-- Stats row -->
        <div
          style="
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 12px;
            margin-bottom: 14px;
          "
        >
          <div
            style="
              border-radius: 16px;
              padding: 12px;
              background: rgba(255,255,255,0.78);
              border: 1px solid rgba(15,23,42,0.10);
            "
          >
            <div style="font-size: 12px; font-weight: 900; color: rgba(15,23,42,0.60);">
              Enrolled Courses
            </div>
            <div style="margin-top: 6px; font-size: 20px; font-weight: 950; color:#0f172a;">
              {#if enrolledCount === null}--{:else}{enrolledCount}{/if}
            </div>
          </div>

          <div
            style="
              border-radius: 16px;
              padding: 12px;
              background: rgba(255,255,255,0.78);
              border: 1px solid rgba(15,23,42,0.10);
            "
          >
            <div style="font-size: 12px; font-weight: 900; color: rgba(15,23,42,0.60);">
              Plan
            </div>
            <div style="margin-top: 6px; font-size: 20px; font-weight: 950; color:#0f172a;">
              {user?.plan ?? "Free"}
            </div>
          </div>

          <div
            style="
              border-radius: 16px;
              padding: 12px;
              background: rgba(255,255,255,0.78);
              border: 1px solid rgba(15,23,42,0.10);
            "
          >
            <div style="font-size: 12px; font-weight: 900; color: rgba(15,23,42,0.60);">
              Status
            </div>
            <div style="margin-top: 6px; font-size: 20px; font-weight: 950; color:#0f172a;">
              Active
            </div>
          </div>
        </div>

        <!-- Actions -->
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

    <!-- Debug (optional) -->
    <details style="margin-top: 22px;">
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
  @media (max-width: 740px) {
    div[style*="grid-template-columns: 140px"] {
      grid-template-columns: 1fr !important;
      text-align: center;
    }

    div[style*="grid-template-columns: repeat(3"] {
      grid-template-columns: 1fr !important;
    }
  }
</style>

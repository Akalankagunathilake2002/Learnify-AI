<script lang="ts">
  import { onMount } from "svelte";
  import { goto } from "$app/navigation";

  const API_URL = import.meta.env.PUBLIC_API_URL ?? "http://127.0.0.1:8000";
  const MY_COURSES_ENDPOINT = "/me/courses";

  
  const DEFAULT_PROFILE_IMG = "https://www.transcend.co.za/hubfs/studnet.png";

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

  function getProgress(course: any): number {
    const p = Number(course?.progress);
    if (!Number.isNaN(p) && p >= 0 && p <= 100) return Math.round(p);

    const idNum = Number(course?.id ?? 1);
    const stable = (idNum * 37) % 91; // 0..90
    return Math.max(8, Math.min(95, stable)); // keep it realistic
  }

  function getCourseImage(course: any): string {
    if (course?.image_url) return course.image_url;

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

  // ✅ NEW: profile image logic (uses your URL as fallback)
  function getProfileImage(u: any): string {
    return (
      u?.avatar_url ??
      u?.image_url ??
      u?.profile_image ??
      u?.photo_url ??
      DEFAULT_PROFILE_IMG
    );
  }

  function getInitials(u: any): string {
    const name = String(u?.name ?? u?.full_name ?? u?.email ?? "U").trim();
    const parts = name.split(/\s+/).filter(Boolean);
    const a = parts[0]?.[0] ?? "U";
    const b = parts.length > 1 ? parts[parts.length - 1]?.[0] : (parts[0]?.[1] ?? "");
    return (a + b).toUpperCase();
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

<div class="page">
  <div class="bg">
    <div class="blob b1"></div>
    <div class="blob b2"></div>
    <div class="grid"></div>
  </div>

  <div class="wrap">
    <h1 class="title">My Profile</h1>

    {#if loading}
      <div class="card soft">Loading your profile…</div>
    {:else if error}
      <div class="card danger">{error}</div>
    {:else}
      <!-- PROFILE CARD -->
      <div class="profileCard">
        <div class="avatarBox" title="User avatar">
          <img
            class="avatarImg"
            src={getProfileImage(user)}
            alt="Profile image"
            on:error={(e) => {
              // if image fails, fallback to initials view
              const img = e.currentTarget as HTMLImageElement;
              img.style.display = "none";
              const fallback = (img.parentElement?.querySelector(".avatarFallback") as HTMLElement) ?? null;
              if (fallback) fallback.style.display = "grid";
            }}
          />
          <!-- initials fallback (hidden by default) -->
          <div class="avatarFallback" style="display:none;">
            {getInitials(user)}
          </div>

          <div class="onlineDot" title="Active"></div>
        </div>

        <div>
          <div class="emailRow">
            <div class="emailText">{user.email}</div>
            <div class="verifiedPill" title="Profile">✅ Verified</div>
          </div>

          <div class="pills">
            <div class="pill role">{user.role ?? "student"}</div>

            <div class="pill enrolled">
              📚 Enrolled:
              <span class="pillStrong">
                {#if enrolledCount === null}--{:else}{enrolledCount}{/if}
              </span>
            </div>

            <div class="pill plan">
              ⭐ Plan:
              <span class="pillStrong">{user?.plan ?? "Free"}</span>
            </div>
          </div>

          <div class="stats">
            <div class="stat">
              <div class="statLabel">Enrolled Courses</div>
              <div class="statValue">
                {#if enrolledCount === null}--{:else}{enrolledCount}{/if}
              </div>
            </div>

            <div class="stat">
              <div class="statLabel">Status</div>
              <div class="statValue ok">Active</div>
            </div>

            <div class="stat">
              <div class="statLabel">Member Since</div>
              <div class="statValue">
                {user?.created_at ? new Date(user.created_at).toLocaleDateString() : "—"}
              </div>
            </div>
          </div>

          <div class="actions">
            <a class="btn ghost" href="/my-courses">📚 My Courses</a>
            <a class="btn primary" href="/billing">⭐ Upgrade</a>
            <a class="btn gray" href="/logout">Logout</a>
          </div>
        </div>
      </div>

      <!-- My Learning section -->
      <div class="section">
        <div class="sectionTop">
          <div>
            <div class="kicker">MY LEARNING</div>
            <h2 class="h2">Continue where you left off</h2>
            <p class="sub">Track your enrolled courses and progress.</p>
          </div>

          <a class="btn ghost" href="/courses">Browse more courses →</a>
        </div>

        {#if enrolledCourses.length === 0}
          <div class="card empty">
            You haven’t enrolled in any courses yet. Go to
            <a href="/courses" class="link">Courses</a> and enroll.
          </div>
        {:else}
          <div class="courseGrid">
            {#each enrolledCourses as c}
              {@const p = getProgress(c)}
              <div class="courseCard">
                <div class="cover">
                  <img class="coverImg" src={getCourseImage(c)} alt="Course cover" />
                  <div class="coverShade"></div>
                  <div class="progressBadge">📈 {p}% complete</div>
                </div>

                <div class="courseBody">
                  <div class="courseTitle">{c.title ?? "Untitled course"}</div>
                  <div class="courseDesc">{c.description ?? "No description yet."}</div>

                  <div class="bar">
                    <div class="barFill" style={`width:${p}%`}></div>
                  </div>

                  <div class="courseFooter">
                    <a class="continue" href={`/courses/${c.id}`}>Continue →</a>
                    <span class="pill mini">Enrolled</span>
                  </div>
                </div>
              </div>
            {/each}
          </div>
        {/if}
      </div>

      <details class="debug">
        <summary>Debug: Full user object</summary>
        <pre>{JSON.stringify(user, null, 2)}</pre>
      </details>
    {/if}
  </div>
</div>

<style>
  .page { position: relative; }
  .wrap { max-width: 1100px; margin: 34px auto; padding: 0 16px; position: relative; z-index: 1; }
  .title { font-size: 32px; font-weight: 950; color: #0f172a; margin: 0 0 16px 0; letter-spacing: -0.4px; }

  .bg { position: absolute; inset: 0; overflow: hidden; pointer-events: none; }
  .blob { position: absolute; width: 520px; height: 520px; border-radius: 999px; filter: blur(40px); opacity: 0.35; }
  .b1 { left: -180px; top: -220px; background: radial-gradient(circle at 30% 30%, rgba(16,185,129,0.55), rgba(14,165,233,0.10)); }
  .b2 { right: -220px; top: 90px; background: radial-gradient(circle at 30% 30%, rgba(14,165,233,0.40), rgba(16,185,129,0.10)); }
  .grid {
    position:absolute; inset:0;
    background-image:
      linear-gradient(rgba(15,23,42,0.04) 1px, transparent 1px),
      linear-gradient(90deg, rgba(15,23,42,0.04) 1px, transparent 1px);
    background-size: 42px 42px;
    mask-image: radial-gradient(circle at 30% 10%, black, transparent 70%);
    opacity: 0.55;
  }

  .card {
    padding: 24px;
    border-radius: 18px;
    background: rgba(255,255,255,0.85);
    border: 1px solid rgba(15,23,42,0.10);
    box-shadow: 0 14px 30px rgba(15,23,42,0.06);
    font-weight: 800;
    color: rgba(15,23,42,0.72);
    backdrop-filter: blur(10px);
  }
  .soft { font-weight: 850; }
  .danger {
    background: rgba(239,68,68,0.08);
    border: 1px solid rgba(239,68,68,0.25);
    color: #b91c1c;
    font-weight: 900;
  }

  .profileCard{
    display: grid;
    grid-template-columns: 140px 1fr;
    gap: 22px;
    padding: 22px;
    border-radius: 22px;
    background: rgba(255,255,255,0.88);
    border: 1px solid rgba(15,23,42,0.10);
    box-shadow: 0 18px 40px rgba(15,23,42,0.08);
    align-items: center;
    backdrop-filter: blur(10px);
  }

  .avatarBox{
    width: 120px;
    height: 120px;
    border-radius: 28px;
    position: relative;
    overflow: hidden;
    border: 1px solid rgba(16,185,129,0.35);
    box-shadow: 0 18px 34px rgba(15,23,42,0.10);
    background: linear-gradient(135deg, rgba(16,185,129,0.25), rgba(14,165,233,0.18));
    display: grid;
    place-items: center;
  }
  .avatarImg{
    width: 100%;
    height: 100%;
    object-fit: cover;
    transform: scale(1.02);
  }
  .avatarFallback{
    width: 100%;
    height: 100%;
    display: grid;
    place-items: center;
    font-size: 34px;
    font-weight: 950;
    color: #0f766e;
    letter-spacing: 1px;
  }
  .onlineDot{
    position: absolute;
    right: 10px;
    bottom: 10px;
    width: 14px;
    height: 14px;
    border-radius: 999px;
    background: #22c55e;
    border: 3px solid rgba(255,255,255,0.95);
    box-shadow: 0 10px 18px rgba(34,197,94,0.25);
  }

  .emailRow{
    display:flex;
    align-items:center;
    gap: 10px;
    justify-content: space-between;
    flex-wrap: wrap;
  }
  .emailText{ font-size: 18px; font-weight: 950; color: #0f172a; }
  .verifiedPill{
    padding: 6px 12px;
    border-radius: 999px;
    font-size: 13px;
    font-weight: 900;
    background: rgba(34,197,94,0.12);
    border: 1px solid rgba(34,197,94,0.20);
    color: #166534;
  }

  .pills{ display:flex; gap:10px; flex-wrap:wrap; align-items:center; margin: 12px 0 12px; }
  .pill{
    padding: 6px 12px;
    border-radius: 999px;
    font-size: 13px;
    font-weight: 900;
    border: 1px solid rgba(15,23,42,0.12);
    background: rgba(255,255,255,0.70);
    color: rgba(15,23,42,0.74);
    backdrop-filter: blur(10px);
  }
  .pillStrong{ color:#0f172a; margin-left: 6px; }
  .pill.role{ background: rgba(16,185,129,0.12); border-color: rgba(16,185,129,0.25); color: #0f766e; }
  .pill.enrolled{ background: rgba(14,165,233,0.10); border-color: rgba(14,165,233,0.16); }
  .pill.plan{ background: rgba(15,23,42,0.05); }
  .pill.mini{
    padding: 6px 10px;
    font-size: 12px;
    background: rgba(16,185,129,0.12);
    border: 1px solid rgba(16,185,129,0.22);
    color: #0f766e;
  }

  .stats{
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 12px;
    margin-bottom: 14px;
  }
  .stat{
    border-radius: 16px;
    padding: 12px;
    background: rgba(255,255,255,0.78);
    border: 1px solid rgba(15,23,42,0.10);
    box-shadow: 0 10px 22px rgba(15,23,42,0.05);
  }
  .statLabel{ font-size: 12px; font-weight: 900; color: rgba(15,23,42,0.60); }
  .statValue{ margin-top: 6px; font-size: 20px; font-weight: 950; color:#0f172a; }
  .statValue.ok{ color:#0f766e; }

  .actions{ display:flex; gap:12px; flex-wrap:wrap; }
  .btn{
    text-decoration: none;
    padding: 10px 14px;
    border-radius: 14px;
    font-weight: 950;
    border: 1px solid transparent;
    display: inline-flex;
    align-items: center;
    gap: 8px;
    transition: transform 120ms ease, box-shadow 120ms ease, background 120ms ease;
  }
  .btn:hover{ transform: translateY(-1px); }
  .btn.primary{
    background: #10b981;
    color: white;
    box-shadow: 0 14px 30px rgba(16,185,129,0.20);
  }
  .btn.ghost{
    background: rgba(15,23,42,0.06);
    border-color: rgba(15,23,42,0.12);
    color: rgba(15,23,42,0.82);
  }
  .btn.gray{
    background: rgba(15,23,42,0.05);
    border-color: rgba(15,23,42,0.10);
    color: rgba(15,23,42,0.72);
  }

  .section{ margin-top: 18px; }
  .sectionTop{ display:flex; justify-content:space-between; align-items:flex-end; gap:12px; flex-wrap:wrap; }
  .kicker{ font-size: 12px; font-weight: 950; color:#0f766e; letter-spacing:0.3px; }
  .h2{ margin: 6px 0 0; font-size: 22px; font-weight: 950; color:#0f172a; }
  .sub{ margin: 8px 0 0; color: rgba(15,23,42,0.65); font-weight: 650; }

  .empty{ margin-top: 14px; }
  .link{ font-weight:950; color:#0f766e; text-decoration:none; }

  .courseGrid{
    margin-top: 14px;
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 14px;
  }
  .courseCard{
    border-radius: 20px;
    overflow: hidden;
    background: rgba(255,255,255,0.90);
    border: 1px solid rgba(15,23,42,0.10);
    box-shadow: 0 14px 30px rgba(15,23,42,0.08);
    display:flex;
    flex-direction: column;
    min-height: 280px;
    transition: transform 140ms ease, box-shadow 140ms ease;
    backdrop-filter: blur(10px);
  }
  .courseCard:hover{
    transform: translateY(-2px);
    box-shadow: 0 18px 40px rgba(15,23,42,0.10);
  }
  .cover{ height: 120px; position: relative; }
  .coverImg{ width:100%; height:100%; object-fit: cover; }
  .coverShade{ position:absolute; inset:0; background: linear-gradient(180deg, rgba(0,0,0,0.00), rgba(0,0,0,0.35)); }
  .progressBadge{
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
  }

  .courseBody{ padding: 14px; display:flex; flex-direction: column; gap: 10px; flex: 1; }
  .courseTitle{ font-weight: 950; color:#0f172a; font-size: 15px; line-height: 1.25; }
  .courseDesc{ color: rgba(15,23,42,0.65); font-weight: 650; font-size: 13px; line-height: 1.55; }

  .bar{
    margin-top: 2px;
    height: 10px;
    border-radius: 999px;
    background: rgba(15,23,42,0.08);
    overflow: hidden;
    border: 1px solid rgba(15,23,42,0.10);
  }
  .barFill{
    height: 100%;
    background: linear-gradient(90deg, rgba(16,185,129,0.95), rgba(34,197,94,0.85));
    border-radius: 999px;
  }

  .courseFooter{
    margin-top: auto;
    display:flex;
    gap:10px;
    flex-wrap:wrap;
    justify-content: space-between;
    align-items:center;
  }
  .continue{ text-decoration:none; font-weight: 950; color: #0f766e; }

  .debug{ margin-top: 18px; }
  .debug summary{ cursor: pointer; font-weight: 900; color: rgba(15,23,42,0.70); }
  .debug pre{
    margin-top: 12px;
    padding: 16px;
    border-radius: 14px;
    background: rgba(15,23,42,0.05);
    border: 1px solid rgba(15,23,42,0.10);
    font-size: 13px;
    overflow-x: auto;
  }

  @media (max-width: 980px) {
    .courseGrid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  }
  @media (max-width: 740px) {
    .profileCard { grid-template-columns: 1fr; text-align: center; }
    .avatarBox { margin: 0 auto; }
    .actions, .pills { justify-content: center; }
    .stats { grid-template-columns: 1fr; }
    .courseGrid { grid-template-columns: 1fr; }
    .emailRow{ justify-content: center; }
  }
</style>

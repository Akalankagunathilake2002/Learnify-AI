<script lang="ts">
  import { onMount, onDestroy } from "svelte";

  // ✅ Rotating ads (every 2 seconds)
  const ads = [
    "🔥 Limited Offer: Save 50% on Premium AI Tutor (Today Only)",
    "🎁 Free Trial: Unlock Smart Notes + Quiz Generator",
    "⚡ New Feature: Listen Mode for learning on the go",
    "🏆 New Courses: SvelteKit + FastAPI + Docker Path released"
  ];

  let adIndex = 0;
  let timer: number | null = null;

  // ✅ Paste your 10 course image URLs here
  const courseImages = [
    "https://i.ytimg.com/vi/MaF8kRbHbi0/hq720.jpg?sqp=-oaymwEhCK4FEIIDSFryq4qpAxMIARUAAAAAGAElAADIQj0AgKJD&rs=AOn4CLCEj3pdiE8FxvGxhk-lcJAaL95xvw",
    "https://media.licdn.com/dms/image/v2/D5612AQHxH62mMSCFWQ/article-cover_image-shrink_720_1280/article-cover_image-shrink_720_1280/0/1733933289032?e=2147483647&v=beta&t=1QgDx7DUnSpCs6AYCMf8fW-6z3bLT3FTgbsZNZzV5iw",
    "https://www.docker.com/app/uploads/2022/12/Docker-Temporary-Image-Social-Thumbnail-1200x630-1.png",
    "https://atrium.ai/wp-content/uploads/2021/06/how-to-implement-salesforce-CICD-with-Github-Actions-1.jpg",
    "https://i.ytimg.com/vi/89NJdbYTgJ8/hq720.jpg?sqp=-oaymwEhCK4FEIIDSFryq4qpAxMIARUAAAAAGAElAADIQj0AgKJD&rs=AOn4CLCWVtn_D5syzA8a_zLX1dmrQ_L9oA",
    "https://i.ytimg.com/vi/3z1ozySuT40/hq720.jpg?sqp=-oaymwEhCK4FEIIDSFryq4qpAxMIARUAAAAAGAElAADIQj0AgKJD&rs=AOn4CLB61EnU4_Tu-51YGDYOXBGIxVaA2w",
    "https://i.ytimg.com/vi/26ls5lNiijk/maxresdefault.jpg",
    "https://media.geeksforgeeks.org/wp-content/uploads/20221117183821/BestSystemDesignCourses.png",
    "https://www.learnworlds.com/app/uploads/2022/05/General-elearning-statistics.webp",
    "https://i.pinimg.com/736x/d7/23/2d/d7232d86a64ec4aa0d74ba3077702dde.jpg"
  ];

  // ✅ Courses (using images)
  const popularCourses = [
    { title: "SvelteKit Mastery", level: "Beginner → Advanced", hours: "18h", rating: "4.8", tag: "Trending", img: courseImages[0] },
    { title: "FastAPI + PostgreSQL", level: "Intermediate", hours: "14h", rating: "4.7", tag: "Backend", img: courseImages[1] },
    { title: "Docker for Developers", level: "Beginner", hours: "10h", rating: "4.6", tag: "DevOps", img: courseImages[2] },
    { title: "CI/CD with GitHub Actions", level: "Intermediate", hours: "9h", rating: "4.7", tag: "Career", img: courseImages[3] },
    { title: "React + Vite Frontend", level: "Beginner", hours: "12h", rating: "4.6", tag: "Frontend", img: courseImages[4] },
    { title: "NestJS API Essentials", level: "Intermediate", hours: "11h", rating: "4.7", tag: "Backend", img: courseImages[5] },
    { title: "SQL + DB Design", level: "Beginner", hours: "8h", rating: "4.5", tag: "Database", img: courseImages[6] },
    { title: "System Design Basics", level: "Intermediate", hours: "9h", rating: "4.6", tag: "Interviews", img: courseImages[7] }
  ];

  const testimonials = [
    { name: "Nimal (SE Student)", text: "AI Tutor explained topics better than my notes. The quizzes helped me pass exams faster.", stars: "★★★★★" },
    { name: "Tharushi (Intern)", text: "Smart Notes + Listen Mode is perfect when I travel. Feels like Coursera but simpler.", stars: "★★★★★" },
    { name: "Kasun (Developer)", text: "Great course path. SvelteKit + FastAPI project flow is super clean and easy to follow.", stars: "★★★★☆" }
  ];

  // ✅ Small promo banner (dismissible)
  let showBanner = true;

  const bannerImages = [
    "https://rollaacademydubai.com/wp-content/uploads/2020/06/Digital-Marketing-Course-in-Dubai.png",
    "https://aclm.in/wp-content/uploads/2021/08/Python-Training.jpg",
    "https://i.ytimg.com/vi/NG9pHNHreME/hq720.jpg?sqp=-oaymwEhCK4FEIIDSFryq4qpAxMIARUAAAAAGAElAADIQj0AgKJD&rs=AOn4CLCqNYRRzNuZ86f0dBf3pa0u0HN1Sg",
    "https://www.daac.in/images/course/49f1f50fcfd776009ced920c43fd2a1b964741939-nodeBg.jpg",
    "https://dtmvamahs40ux.cloudfront.net/public/seo-image/seo-image-893-free-ui-ux-course.webp",
    "https://tanducits.com/images/banner-excel-tanducits.jpg",
    "https://eduwebcoorporatemk.blob.core.windows.net/edu-mk/2025/02/Cisco-Training-Partner-01.png"
  ];

  let bannerIndex = 0;
  let bannerTimer: number | null = null;

  function closeBanner() {
    showBanner = false;
  }

  // ✅ Certificates (popup)
  // 🔴 Replace these URLs with your certificate image URLs later
  const certificates = [
    {
      title: "AI for Beginners Certificate",
      provider: "Learnify AI",
      img: "https://images.unsplash.com/photo-1553877522-43269d4ea984?auto=format&fit=crop&w=1400&q=80"
    },
    {
      title: "DevOps Foundations Certificate",
      provider: "Learnify AI",
      img: "https://images.unsplash.com/photo-1521737604893-d14cc237f11d?auto=format&fit=crop&w=1400&q=80"
    },
    {
      title: "Backend Mastery Certificate",
      provider: "Learnify AI",
      img: "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?auto=format&fit=crop&w=1400&q=80"
    }
  ];

  let certOpen = false;
  let activeCert: any = null;

  function openCert(c: any) {
    activeCert = c;
    certOpen = true;
  }

  function closeCert() {
    certOpen = false;
    activeCert = null;
  }

  onMount(() => {
    timer = window.setInterval(() => {
      adIndex = (adIndex + 1) % ads.length;
    }, 2000);

    bannerTimer = window.setInterval(() => {
      bannerIndex = (bannerIndex + 1) % bannerImages.length;
    }, 3000);
  });

  onDestroy(() => {
    if (timer) window.clearInterval(timer);
    if (bannerTimer) window.clearInterval(bannerTimer);
  });
</script>

<!-- ✅ Mint background (less white, more theme) -->
<section
  style="
    padding: 26px 0 34px;
    background:
      radial-gradient(900px 520px at 10% 10%, rgba(16,185,129,0.16), transparent 60%),
      radial-gradient(900px 520px at 90% 12%, rgba(34,197,94,0.12), transparent 60%),
      linear-gradient(180deg, #f3fbf7 0%, #eef9f4 55%, #f1f5f9 100%);
    border-radius: 22px;
  "
>
  <!-- Rotating Ad bar (2s) -->
  <div
    style="
      border-radius: 18px;
      overflow: hidden;
      border: 1px solid rgba(15,23,42,0.08);
      background: linear-gradient(135deg, rgba(16,185,129,0.22), rgba(14,165,233,0.12));
      box-shadow: 0 14px 30px rgba(15,23,42,0.10);
      margin-bottom: 18px;
    "
  >
    <div
      style="
        padding: 12px 14px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 10px;
        flex-wrap: wrap;
        background: rgba(255,255,255,0.72);
      "
    >
      <div style="display:flex; align-items:center; gap:10px;">
        <span
          style="
            font-size: 12px;
            font-weight: 950;
            padding: 5px 10px;
            border-radius: 999px;
            background: rgba(16,185,129,0.16);
            border: 1px solid rgba(16,185,129,0.26);
            color: #0f766e;
          "
        >
          PROMO
        </span>

        <span style="font-weight: 950; color: rgba(15,23,42,0.82);">
          {ads[adIndex]}
        </span>
      </div>

      <a
        href="/billing"
        style="
          text-decoration: none;
          font-weight: 950;
          color: #0f766e;
          padding: 8px 12px;
          border-radius: 999px;
          background: rgba(16,185,129,0.14);
          border: 1px solid rgba(16,185,129,0.26);
        "
      >
        See Plans →
      </a>
    </div>
  </div>

  {#if showBanner}
    <div
      style="
        position: relative;
        margin-bottom: 18px;
        border-radius: 18px;
        overflow: hidden;
        border: 1px solid rgba(15,23,42,0.12);
        box-shadow: 0 16px 36px rgba(15,23,42,0.12);
        background: rgba(255,255,255,0.88);
      "
    >
      <button
        on:click={closeBanner}
        style="
          position:absolute;
          top: 10px;
          right: 10px;
          z-index: 5;
          border: none;
          background: rgba(0,0,0,0.55);
          color: white;
          font-size: 14px;
          font-weight: 900;
          width: 28px;
          height: 28px;
          border-radius: 999px;
          cursor: pointer;
        "
        aria-label="Close banner"
      >
        ✕
      </button>

      <img
        src={bannerImages[bannerIndex]}
        alt="Learnify promotion"
        style="
          width: 100%;
          height: 240px;
          object-fit: cover;
          display: block;
        "
      />

      <div
        style="
          position:absolute;
          left: 0;
          bottom: 0;
          width: 100%;
          padding: 10px 14px;
          background: linear-gradient(to top, rgba(0,0,0,0.65), rgba(0,0,0,0));
          color: white;
          font-weight: 950;
          letter-spacing: 0.3px;
        "
      >
        🚀 New Featured Learning Content Available Now
      </div>
    </div>
  {/if}

  <!-- HERO SECTION -->
  <div
    style="
      display: grid;
      grid-template-columns: 1.15fr 0.85fr;
      gap: 26px;
      align-items: center;
      padding: 8px 6px 10px;
    "
  >
    <div>
      <h1
        style="
          margin: 0 0 12px 0;
          font-size: 54px;
          line-height: 1.06;
          font-weight: 980;
          letter-spacing: -1px;
          color: #0f172a;
        "
      >
        Learn <span style="color:#0f766e;">Smarter</span>,<br />
        Build <span style="color:#10b981;">Skills</span>,<br />
        Get <span style="color:#0f766e;">Hired</span>
      </h1>

      <p
        style="
          margin: 0 0 18px 0;
          max-width: 580px;
          font-size: 16px;
          line-height: 1.7;
          color: rgba(15,23,42,0.72);
          font-weight: 650;
        "
      >
        Structured courses + AI learning tools (Smart Notes, Quizzes, Listen Mode).
        Faster studying for exams + internships.
      </p>

      <div style="display:flex; gap:12px; flex-wrap:wrap; margin-bottom: 14px;">
        <a
          href="/courses"
          style="
            text-decoration:none;
            padding: 14px 22px;
            border-radius: 14px;
            background: #10b981;
            color: white;
            font-weight: 980;
            box-shadow: 0 16px 34px rgba(16,185,129,0.26);
            display: inline-block;
          "
        >
          Explore Courses
        </a>

        <a
          href="/billing"
          style="
            text-decoration:none;
            padding: 14px 22px;
            border-radius: 14px;
            background: rgba(16,185,129,0.14);
            border: 1px solid rgba(16,185,129,0.28);
            color: #0f766e;
            font-weight: 980;
            display: inline-block;
          "
        >
          Start Free Trial
        </a>
      </div>

      <div style="display:flex; gap:10px; flex-wrap: wrap;">
        <span style="padding: 8px 12px; border-radius: 999px; background: rgba(255,255,255,0.82); border: 1px solid rgba(15,23,42,0.10); font-weight: 900; color: rgba(15,23,42,0.75);">✅ AI Tutor</span>
        <span style="padding: 8px 12px; border-radius: 999px; background: rgba(255,255,255,0.82); border: 1px solid rgba(15,23,42,0.10); font-weight: 900; color: rgba(15,23,42,0.75);">📄 Smart Notes</span>
        <span style="padding: 8px 12px; border-radius: 999px; background: rgba(255,255,255,0.82); border: 1px solid rgba(15,23,42,0.10); font-weight: 900; color: rgba(15,23,42,0.75);">🎧 Listen Mode</span>
      </div>
    </div>

    <!-- Right -->
    <div style="display:flex; justify-content:center;">
      <div
        style="
          position:relative;
          width:min(520px,100%);
          height:520px;
        "
      >
        <div
          style="
            position:absolute;
            inset: 38px;
            border-radius: 50%;
            background: linear-gradient(135deg, rgba(16,185,129,0.95), rgba(34,197,94,0.70));
            box-shadow: 0 30px 60px rgba(16,185,129,0.20);
          "
        ></div>

        <div
          style="
            position:absolute;
            inset: 78px 92px 70px 92px;
            border-radius: 26px;
            overflow:hidden;
            background: rgba(255,255,255,0.90);
            border: 1px solid rgba(15,23,42,0.10);
            box-shadow: 0 24px 55px rgba(15,23,42,0.18);
          "
        >
          <img
            alt="Student"
            src="https://images.unsplash.com/photo-1524504388940-b1c1722653e1?auto=format&fit=crop&w=900&q=80"
            style="width:100%; height:100%; object-fit:cover;"
          />
        </div>

        <div
          style="
            position:absolute;
            left: -6px;
            top: 160px;
            display:flex;
            align-items:center;
            gap: 12px;
            padding: 12px 14px;
            border-radius: 16px;
            background: rgba(255,255,255,0.92);
            border: 1px solid rgba(15,23,42,0.10);
            box-shadow: 0 18px 40px rgba(15,23,42,0.12);
            min-width: 210px;
          "
        >
          <div style="width: 44px; height: 44px; border-radius: 14px; display:grid; place-items:center; background: rgba(16,185,129,0.14); border: 1px solid rgba(16,185,129,0.22); font-size: 18px;">
            📘
          </div>
          <div>
            <div style="font-weight:980; font-size:20px; line-height:1;">2K+</div>
            <div style="font-size:13px; color: rgba(15,23,42,0.65); font-weight:800; margin-top:3px;">Video Courses</div>
          </div>
        </div>

        <div
          style="
            position:absolute;
            right: 0px;
            top: 60px;
            display:flex;
            align-items:center;
            gap: 12px;
            padding: 12px 14px;
            border-radius: 16px;
            background: rgba(255,255,255,0.92);
            border: 1px solid rgba(15,23,42,0.10);
            box-shadow: 0 18px 40px rgba(15,23,42,0.12);
            min-width: 200px;
          "
        >
          <div style="width: 44px; height: 44px; border-radius: 14px; display:grid; place-items:center; background: rgba(14,165,233,0.12); border: 1px solid rgba(14,165,233,0.18); font-size: 18px;">
            🎯
          </div>
          <div>
            <div style="font-weight:980; font-size:20px; line-height:1;">5K+</div>
            <div style="font-size:13px; color: rgba(15,23,42,0.65); font-weight:800; margin-top:3px;">Practice Quizzes</div>
          </div>
        </div>

        <div
          style="
            position:absolute;
            right: 10px;
            bottom: 90px;
            display:flex;
            align-items:center;
            gap: 12px;
            padding: 12px 14px;
            border-radius: 16px;
            background: rgba(255,255,255,0.92);
            border: 1px solid rgba(15,23,42,0.10);
            box-shadow: 0 18px 40px rgba(15,23,42,0.12);
            min-width: 200px;
          "
        >
          <div style="width: 44px; height: 44px; border-radius: 14px; display:grid; place-items:center; background: rgba(16,185,129,0.14); border: 1px solid rgba(16,185,129,0.22); font-size: 18px;">
            🏆
          </div>
          <div>
            <div style="font-weight:980; font-size:20px; line-height:1;">Certificates</div>
            <div style="font-size:13px; color: rgba(15,23,42,0.65); font-weight:800; margin-top:3px;">After completion</div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div style="height: 1px; background: rgba(15,23,42,0.10); margin: 26px 0;"></div>

  <!-- Popular Courses -->
  <section>
    <div style="display:flex; align-items:end; justify-content:space-between; gap:12px; flex-wrap:wrap;">
      <div>
        <div style="font-size: 13px; font-weight: 980; color: #0f766e;">POPULAR</div>
        <h2 style="margin: 6px 0 0; font-size: 28px; font-weight: 980; color:#0f172a;">Popular Courses</h2>
        <p style="margin: 8px 0 0; color: rgba(15,23,42,0.65); font-weight: 650;">Start with the most-loved learning paths.</p>
      </div>

      <a
        href="/courses"
        style="
          text-decoration:none;
          font-weight: 980;
          color: #0f766e;
          padding: 10px 14px;
          border-radius: 14px;
          background: rgba(16,185,129,0.14);
          border: 1px solid rgba(16,185,129,0.26);
        "
      >
        View all →
      </a>
    </div>

    <div
      style="
        margin-top: 16px;
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 14px;
      "
    >
      {#each popularCourses as c}
        <div
          style="
            border-radius: 18px;
            background: rgba(255,255,255,0.88);
            border: 1px solid rgba(15,23,42,0.12);
            box-shadow: 0 14px 30px rgba(15,23,42,0.08);
            padding: 14px;
          "
        >
          <div
            style="
              width: 100%;
              height: 140px;
              border-radius: 16px;
              overflow: hidden;
              border: 1px solid rgba(15,23,42,0.12);
              background: rgba(15,23,42,0.06);
            "
          >
            <img src={c.img} alt={c.title} style="width:100%; height:100%; object-fit:cover; display:block;" />
          </div>

          <div style="margin-top: 10px; display:flex; justify-content:space-between; align-items:center; gap:10px;">
            <span
              style="
                font-size: 12px;
                font-weight: 980;
                padding: 5px 10px;
                border-radius: 999px;
                background: rgba(14,165,233,0.12);
                border: 1px solid rgba(14,165,233,0.18);
                color: rgba(15,23,42,0.76);
              "
            >
              {c.tag}
            </span>
            <span style="font-weight: 980; color: rgba(15,23,42,0.76); font-size: 12px;">
              ⭐ {c.rating}
            </span>
          </div>

          <div style="margin-top: 10px; font-weight: 980; font-size: 16px; color:#0f172a;">
            {c.title}
          </div>

          <div style="margin-top: 6px; color: rgba(15,23,42,0.65); font-weight: 700; font-size: 13px;">
            {c.level}
          </div>

          <div style="margin-top: 12px; display:flex; justify-content:space-between; gap:10px; flex-wrap:wrap;">
            <span style="font-weight: 900; color: rgba(15,23,42,0.65); font-size: 13px;">⏱ {c.hours}</span>
            <span style="font-weight: 900; color: rgba(15,23,42,0.65); font-size: 13px;">📚 Lessons</span>
          </div>

          <a href="/courses" style="display:inline-block; margin-top: 12px; text-decoration:none; font-weight: 980; color: #0f766e;">
            Start learning →
          </a>
        </div>
      {/each}
    </div>
  </section>

  <!-- Certificates -->
  <section style="margin-top: 30px;">
    <div style="display:flex; align-items:end; justify-content:space-between; gap:12px; flex-wrap:wrap;">
      <div>
        <div style="font-size: 13px; font-weight: 980; color: #0f766e;">CERTIFICATES</div>
        <h2 style="margin: 6px 0 0; font-size: 28px; font-weight: 980; color:#0f172a;">Earn Certificates</h2>
        <p style="margin: 8px 0 0; color: rgba(15,23,42,0.65); font-weight: 650;">
          Complete a course and receive a shareable certificate.
        </p>
      </div>
    </div>

    <div
      style="
        margin-top: 16px;
        display:grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 14px;
      "
    >
      {#each certificates as c}
        <div
          style="
            border-radius: 18px;
            background: rgba(255,255,255,0.88);
            border: 1px solid rgba(15,23,42,0.12);
            box-shadow: 0 14px 30px rgba(15,23,42,0.08);
            padding: 14px;
          "
        >
          <div
            style="
              height: 150px;
              border-radius: 16px;
              overflow: hidden;
              border: 1px solid rgba(15,23,42,0.12);
              background: rgba(15,23,42,0.06);
            "
          >
            <img src={c.img} alt={c.title} style="width:100%; height:100%; object-fit:cover; display:block;" />
          </div>

          <div style="margin-top: 10px; font-weight: 980; color:#0f172a;">{c.title}</div>
          <div style="margin-top: 6px; color: rgba(15,23,42,0.65); font-weight: 700; font-size: 13px;">
            Provider: {c.provider}
          </div>

          <button
            on:click={() => openCert(c)}
            style="
              margin-top: 12px;
              width: 100%;
              padding: 12px;
              border-radius: 14px;
              border: none;
              background: rgba(16,185,129,0.18);
              border: 1px solid rgba(16,185,129,0.28);
              color: #0f766e;
              font-weight: 980;
              cursor: pointer;
            "
          >
            View Certificate →
          </button>
        </div>
      {/each}
    </div>
  </section>

  <!-- Testimonials -->
  <section style="margin-top: 30px;">
    <h2 style="margin: 0; font-size: 28px; font-weight: 980; color:#0f172a;">What learners say</h2>
    <p style="margin: 8px 0 0; color: rgba(15,23,42,0.65); font-weight: 650;">Real feedback from students and interns.</p>

    <div style="margin-top: 16px; display:grid; grid-template-columns: repeat(3, 1fr); gap: 14px;">
      {#each testimonials as t}
        <div
          style="
            border-radius: 18px;
            background: rgba(255,255,255,0.88);
            border: 1px solid rgba(15,23,42,0.12);
            box-shadow: 0 14px 30px rgba(15,23,42,0.08);
            padding: 14px;
          "
        >
          <div style="font-weight: 980; color:#0f172a;">{t.stars}</div>
          <div style="margin-top: 10px; color: rgba(15,23,42,0.75); font-weight: 650; line-height: 1.7;">
            “{t.text}”
          </div>
          <div style="margin-top: 12px; font-weight: 980; color:#0f766e;">— {t.name}</div>
        </div>
      {/each}
    </div>
  </section>

  <!-- CTA -->
  <section style="margin-top: 30px;">
    <div
      style="
        border-radius: 22px;
        padding: 18px;
        border: 1px solid rgba(15,23,42,0.10);
        background: linear-gradient(135deg, rgba(16,185,129,0.22), rgba(255,255,255,0.92));
        box-shadow: 0 16px 36px rgba(15,23,42,0.10);
        display:flex;
        justify-content: space-between;
        align-items: center;
        gap: 14px;
        flex-wrap: wrap;
      "
    >
      <div>
        <div style="font-weight: 980; color:#0f172a; font-size: 20px;">Ready to level up your career?</div>
        <div style="margin-top: 6px; color: rgba(15,23,42,0.65); font-weight: 650;">
          Start learning today — and use AI tools to study faster.
        </div>
      </div>

      <div style="display:flex; gap:10px; flex-wrap:wrap;">
        <a href="/courses" style="text-decoration:none; padding: 12px 16px; border-radius: 14px; background: #10b981; color: white; font-weight: 980; box-shadow: 0 14px 30px rgba(16,185,129,0.22);">
          Explore Courses
        </a>
        <a href="/ai" style="text-decoration:none; padding: 12px 16px; border-radius: 14px; background: rgba(16,185,129,0.14); border: 1px solid rgba(16,185,129,0.26); color: #0f766e; font-weight: 980;">
          Try AI Tutor
        </a>
      </div>
    </div>
  </section>

  <!-- ✅ Certificate Modal -->
  {#if certOpen && activeCert}
    <div
      on:click={closeCert}
      style="
        position: fixed;
        inset: 0;
        z-index: 999;
        background: rgba(2,6,23,0.62);
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 18px;
      "
    >
      <div
        on:click|stopPropagation={() => {}}
        style="
          width: min(920px, 100%);
          border-radius: 18px;
          overflow: hidden;
          background: rgba(255,255,255,0.96);
          border: 1px solid rgba(255,255,255,0.26);
          box-shadow: 0 30px 90px rgba(0,0,0,0.35);
        "
      >
        <div
          style="
            padding: 12px 14px;
            display:flex;
            justify-content: space-between;
            align-items: center;
            gap: 10px;
            border-bottom: 1px solid rgba(15,23,42,0.10);
            background: linear-gradient(135deg, rgba(16,185,129,0.14), rgba(14,165,233,0.10));
          "
        >
          <div style="font-weight: 980; color:#0f172a;">
            🏆 {activeCert.title}
            <span style="font-weight: 700; color: rgba(15,23,42,0.65); font-size: 13px; margin-left: 8px;">
              ({activeCert.provider})
            </span>
          </div>

          <button
            on:click={closeCert}
            style="
              border: none;
              background: rgba(0,0,0,0.55);
              color: white;
              font-size: 14px;
              font-weight: 900;
              width: 32px;
              height: 32px;
              border-radius: 999px;
              cursor: pointer;
            "
          >
            ✕
          </button>
        </div>

        <div style="padding: 14px;">
          <img
            src={activeCert.img}
            alt={activeCert.title}
            style="
              width: 100%;
              max-height: 72vh;
              object-fit: contain;
              display: block;
              border-radius: 14px;
              border: 1px solid rgba(15,23,42,0.10);
              background: rgba(15,23,42,0.04);
            "
          />

          <div style="display:flex; justify-content: flex-end; gap: 10px; margin-top: 12px; flex-wrap: wrap;">
            <a
              href={activeCert.img}
              target="_blank"
              style="
                text-decoration:none;
                padding: 10px 14px;
                border-radius: 14px;
                background: rgba(15,23,42,0.06);
                border: 1px solid rgba(15,23,42,0.12);
                color: rgba(15,23,42,0.82);
                font-weight: 900;
              "
            >
              Open Image ↗
            </a>

            <button
              on:click={closeCert}
              style="
                padding: 10px 14px;
                border-radius: 14px;
                border: none;
                background: #10b981;
                color: white;
                font-weight: 980;
                cursor: pointer;
                box-shadow: 0 14px 30px rgba(16,185,129,0.22);
              "
            >
              Done
            </button>
          </div>
        </div>
      </div>
    </div>
  {/if}
</section>

<style>
  @media (max-width: 1100px) {
    section > div:nth-child(3) {
      grid-template-columns: 1fr !important;
      gap: 22px !important;
    }
  }

  @media (max-width: 1000px) {
    section section div[style*="grid-template-columns: repeat(4"] {
      grid-template-columns: repeat(2, 1fr) !important;
    }
  }

  @media (max-width: 900px) {
    section section div[style*="grid-template-columns: repeat(3"] {
      grid-template-columns: 1fr !important;
    }
  }
</style>

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

  onMount(() => {
    timer = window.setInterval(() => {
      adIndex = (adIndex + 1) % ads.length;
    }, 2000);
  });

  onDestroy(() => {
    if (timer) window.clearInterval(timer);
  });

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
</script>

<section style="padding: 26px 0 34px;">
  <!-- Rotating Ad bar (2s) -->
  <div
    style="
      border-radius: 18px;
      overflow: hidden;
      border: 1px solid rgba(15,23,42,0.08);
      background: linear-gradient(135deg, rgba(16,185,129,0.18), rgba(14,165,233,0.12));
      box-shadow: 0 14px 30px rgba(15,23,42,0.08);
      margin-bottom: 22px;
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
        background: rgba(255,255,255,0.65);
      "
    >
      <div style="display:flex; align-items:center; gap:10px;">
        <span
          style="
            font-size: 12px;
            font-weight: 950;
            padding: 5px 10px;
            border-radius: 999px;
            background: rgba(16,185,129,0.14);
            border: 1px solid rgba(16,185,129,0.22);
            color: #0f766e;
          "
        >
          PROMO
        </span>

        <span style="font-weight: 900; color: rgba(15,23,42,0.78);">
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
          background: rgba(16,185,129,0.12);
          border: 1px solid rgba(16,185,129,0.22);
        "
      >
        See Plans →
      </a>
    </div>
  </div>

  <!-- HERO SECTION -->
  <div
    style="
      display: grid;
      grid-template-columns: 1.15fr 0.85fr;
      gap: 28px;
      align-items: center;
      padding: 10px 0 12px;
    "
  >
    <!-- Left content -->
    <div>
      <h1
        style="
          margin: 0 0 14px 0;
          font-size: 56px;
          line-height: 1.06;
          font-weight: 950;
          letter-spacing: -1px;
          color: #0f172a;
        "
      >
        Up Your <span style="color:#10b981;">Skills</span><br />
        To <span style="color:#10b981;">Advance</span> Your<br />
        <span style="color:#10b981;">Career</span> Path
      </h1>

      <p
        style="
          margin: 0 0 22px 0;
          max-width: 580px;
          font-size: 16px;
          line-height: 1.7;
          color: rgba(15,23,42,0.70);
          font-weight: 650;
        "
      >
        Learn with structured courses + AI tools. Ask questions, generate quizzes,
        create smart notes, and study faster with Learnify AI.
      </p>

      <div style="display:flex; gap:14px; flex-wrap:wrap; margin-bottom: 18px;">
        <a
          href="/courses"
          style="
            text-decoration:none;
            padding: 14px 22px;
            border-radius: 14px;
            background: #10b981;
            color: white;
            font-weight: 950;
            box-shadow: 0 16px 34px rgba(16,185,129,0.22);
            display: inline-block;
          "
        >
          Get Started
        </a>

        <a
          href="/billing"
          style="
            text-decoration:none;
            padding: 14px 22px;
            border-radius: 14px;
            background: rgba(16,185,129,0.12);
            border: 1px solid rgba(16,185,129,0.28);
            color: #0f766e;
            font-weight: 950;
            display: inline-block;
          "
        >
          Get free trial
        </a>
      </div>

      <div
        style="
          display:flex;
          gap: 20px;
          flex-wrap: wrap;
          color: rgba(15,23,42,0.62);
          font-weight: 800;
        "
      >
        <div style="display:flex; align-items:center; gap:8px;">
          <span>💬</span><span>Public Speaking</span>
        </div>
        <div style="display:flex; align-items:center; gap:8px;">
          <span>💼</span><span>Career-Oriented</span>
        </div>
        <div style="display:flex; align-items:center; gap:8px;">
          <span>💡</span><span>Creative Thinking</span>
        </div>
      </div>

      <div style="margin-top: 18px; display:flex; gap:10px; flex-wrap: wrap;">
        <span style="padding: 8px 12px; border-radius: 999px; background: rgba(255,255,255,0.75); border: 1px solid rgba(15,23,42,0.10); font-weight: 900; color: rgba(15,23,42,0.70);">
          ✅ AI Tutor
        </span>
        <span style="padding: 8px 12px; border-radius: 999px; background: rgba(255,255,255,0.75); border: 1px solid rgba(15,23,42,0.10); font-weight: 900; color: rgba(15,23,42,0.70);">
          📄 Smart Notes
        </span>
        <span style="padding: 8px 12px; border-radius: 999px; background: rgba(255,255,255,0.75); border: 1px solid rgba(15,23,42,0.10); font-weight: 900; color: rgba(15,23,42,0.70);">
          ✅ Quiz Generator
        </span>
        <span style="padding: 8px 12px; border-radius: 999px; background: rgba(255,255,255,0.75); border: 1px solid rgba(15,23,42,0.10); font-weight: 900; color: rgba(15,23,42,0.70);">
          🎧 Listen Mode
        </span>
      </div>

      <div
        style="
          margin-top: 26px;
          display:flex;
          gap: 18px;
          flex-wrap: wrap;
          align-items: center;
          color: rgba(15,23,42,0.40);
          font-weight: 900;
          letter-spacing: 0.3px;
        "
      >
        <span style="font-size: 20px; opacity:0.7;">duolingo</span>
        <span style="font-size: 20px; opacity:0.7;">Codecov</span>
        <span style="font-size: 20px; opacity:0.7;">UserTesting</span>
        <span style="font-size: 20px; opacity:0.7;">magic leap</span>
      </div>
    </div>

    <!-- Right: Art -->
    <div style="display:flex; justify-content:center;">
      <div style="position:relative; width:min(520px,100%); height:520px;">
        <div style="position:absolute; inset: 6px; border-radius: 50%; border: 2px solid rgba(16,185,129,0.16);"></div>
        <div style="position:absolute; inset: 28px; border-radius: 50%; border: 2px solid rgba(16,185,129,0.10);"></div>

        <div
          style="
            position:absolute;
            inset: 40px;
            border-radius: 50%;
            background: #10b981;
            box-shadow: 0 30px 60px rgba(16,185,129,0.20);
          "
        ></div>

        <div
          style="
            position:absolute;
            inset: 80px 90px 70px 90px;
            border-radius: 26px;
            overflow:hidden;
            background: white;
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
            left: -10px;
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
          <div
            style="
              width: 44px;
              height: 44px;
              border-radius: 14px;
              display:grid;
              place-items:center;
              background: rgba(16,185,129,0.12);
              border: 1px solid rgba(16,185,129,0.20);
              font-size: 18px;
            "
          >
            📘
          </div>
          <div>
            <div style="font-weight:950; font-size:20px; line-height:1;">2K+</div>
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
          <div style="width: 44px; height: 44px; border-radius: 50%; background: rgba(15,23,42,0.06); position: relative; overflow: hidden;">
            <div style="position:absolute; inset:0; background: conic-gradient(#10b981 0 65%, transparent 65% 100%); border-radius:50%;"></div>
            <div style="position:absolute; inset: 7px; background:white; border-radius:50%;"></div>
          </div>
          <div>
            <div style="font-weight:950; font-size:20px; line-height:1;">5K+</div>
            <div style="font-size:13px; color: rgba(15,23,42,0.65); font-weight:800; margin-top:3px;">Online Courses</div>
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
          <div
            style="
              width: 44px;
              height: 44px;
              border-radius: 14px;
              display:grid;
              place-items:center;
              background: rgba(16,185,129,0.12);
              border: 1px solid rgba(16,185,129,0.20);
              font-size: 18px;
            "
          >
            👨‍🏫
          </div>
          <div>
            <div style="font-weight:950; font-size:20px; line-height:1;">250+</div>
            <div style="font-size:13px; color: rgba(15,23,42,0.65); font-weight:800; margin-top:3px;">Tutors</div>
          </div>
        </div>

        <div style="position:absolute; left: 110px; bottom: 120px; width: 26px; height: 26px; border-radius: 50%; background: rgba(16,185,129,0.95); box-shadow: 0 18px 35px rgba(16,185,129,0.20);"></div>
      </div>
    </div>
  </div>

  <div style="height: 1px; background: rgba(15,23,42,0.08); margin: 30px 0;"></div>

  <!-- Popular Courses with Images -->
  <section>
    <div style="display:flex; align-items:end; justify-content:space-between; gap:12px; flex-wrap:wrap;">
      <div>
        <div style="font-size: 13px; font-weight: 950; color: #0f766e;">POPULAR</div>
        <h2 style="margin: 6px 0 0; font-size: 28px; font-weight: 950; color:#0f172a;">Popular Courses</h2>
        <p style="margin: 8px 0 0; color: rgba(15,23,42,0.65); font-weight: 650;">Start with the most-loved learning paths.</p>
      </div>

      <a
        href="/courses"
        style="
          text-decoration:none;
          font-weight: 950;
          color: #0f766e;
          padding: 10px 14px;
          border-radius: 14px;
          background: rgba(16,185,129,0.12);
          border: 1px solid rgba(16,185,129,0.22);
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
            background: rgba(255,255,255,0.85);
            border: 1px solid rgba(15,23,42,0.10);
            box-shadow: 0 14px 30px rgba(15,23,42,0.07);
            padding: 14px;
          "
        >
          <!-- Image -->
          <div
            style="
              width: 100%;
              height: 140px;
              border-radius: 16px;
              overflow: hidden;
              border: 1px solid rgba(15,23,42,0.10);
              background: rgba(15,23,42,0.04);
            "
          >
            <img
              src={c.img}
              alt={c.title}
              style="width:100%; height:100%; object-fit:cover; display:block;"
            />
          </div>

          <!-- Tag + rating -->
          <div style="margin-top: 10px; display:flex; justify-content:space-between; align-items:center; gap:10px;">
            <span
              style="
                font-size: 12px;
                font-weight: 950;
                padding: 5px 10px;
                border-radius: 999px;
                background: rgba(14,165,233,0.10);
                border: 1px solid rgba(14,165,233,0.16);
                color: rgba(15,23,42,0.72);
              "
            >
              {c.tag}
            </span>
            <span style="font-weight: 950; color: rgba(15,23,42,0.72); font-size: 12px;">
              ⭐ {c.rating}
            </span>
          </div>

          <div style="margin-top: 10px; font-weight: 950; font-size: 16px; color:#0f172a;">
            {c.title}
          </div>

          <div style="margin-top: 6px; color: rgba(15,23,42,0.62); font-weight: 700; font-size: 13px;">
            {c.level}
          </div>

          <div style="margin-top: 12px; display:flex; justify-content:space-between; gap:10px; flex-wrap:wrap;">
            <span style="font-weight: 900; color: rgba(15,23,42,0.62); font-size: 13px;">⏱ {c.hours}</span>
            <span style="font-weight: 900; color: rgba(15,23,42,0.62); font-size: 13px;">📚 Lessons</span>
          </div>

          <a
            href="/courses"
            style="display:inline-block; margin-top: 12px; text-decoration:none; font-weight: 950; color: #0f766e;"
          >
            Start learning →
          </a>
        </div>
      {/each}
    </div>
  </section>

  <!-- Why Learnify -->
  <section style="margin-top: 32px;">
    <h2 style="margin: 0; font-size: 28px; font-weight: 950; color:#0f172a;">Why Learnify AI?</h2>
    <p style="margin: 8px 0 0; color: rgba(15,23,42,0.65); font-weight: 650;">
      Built for students and interns — focus on exams + real projects.
    </p>

    <div
      style="
        margin-top: 16px;
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 14px;
      "
    >
      {#each [
        { t: "AI Tutor", d: "Ask questions & get clear explanations instantly.", i: "🤖" },
        { t: "Smart Notes", d: "Generate exam-ready summaries in seconds.", i: "📄" },
        { t: "Quiz Generator", d: "Create MCQs and practice anytime.", i: "✅" },
        { t: "Listen Mode", d: "Turn notes into audio and learn on the go.", i: "🎧" },
        { t: "Course Paths", d: "Follow structured roadmaps for career skills.", i: "🛣️" },
        { t: "Premium Upgrade", d: "Unlock advanced features for faster learning.", i: "⭐" }
      ] as f}
        <div
          style="
            border-radius: 18px;
            background: rgba(255,255,255,0.85);
            border: 1px solid rgba(15,23,42,0.10);
            box-shadow: 0 14px 30px rgba(15,23,42,0.06);
            padding: 14px;
          "
        >
          <div
            style="
              width: 46px;
              height: 46px;
              border-radius: 16px;
              display:grid;
              place-items:center;
              background: rgba(16,185,129,0.12);
              border: 1px solid rgba(16,185,129,0.22);
              font-size: 18px;
            "
          >
            {f.i}
          </div>
          <div style="margin-top: 10px; font-weight: 950; color:#0f172a;">{f.t}</div>
          <div style="margin-top: 6px; color: rgba(15,23,42,0.65); font-weight: 650; line-height: 1.6;">
            {f.d}
          </div>
        </div>
      {/each}
    </div>
  </section>

  <!-- Testimonials -->
  <section style="margin-top: 32px;">
    <h2 style="margin: 0; font-size: 28px; font-weight: 950; color:#0f172a;">What learners say</h2>
    <p style="margin: 8px 0 0; color: rgba(15,23,42,0.65); font-weight: 650;">
      Real feedback from students and interns.
    </p>

    <div
      style="
        margin-top: 16px;
        display:grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 14px;
      "
    >
      {#each testimonials as t}
        <div
          style="
            border-radius: 18px;
            background: rgba(255,255,255,0.85);
            border: 1px solid rgba(15,23,42,0.10);
            box-shadow: 0 14px 30px rgba(15,23,42,0.06);
            padding: 14px;
          "
        >
          <div style="font-weight: 950; color:#0f172a;">{t.stars}</div>
          <div style="margin-top: 10px; color: rgba(15,23,42,0.70); font-weight: 650; line-height: 1.7;">
            “{t.text}”
          </div>
          <div style="margin-top: 12px; font-weight: 950; color:#0f766e;">— {t.name}</div>
        </div>
      {/each}
    </div>
  </section>

  <!-- Final CTA -->
  <section style="margin-top: 34px;">
    <div
      style="
        border-radius: 22px;
        padding: 18px;
        border: 1px solid rgba(15,23,42,0.10);
        background: linear-gradient(135deg, rgba(16,185,129,0.20), rgba(255,255,255,0.90));
        box-shadow: 0 16px 36px rgba(15,23,42,0.08);
        display:flex;
        justify-content: space-between;
        align-items: center;
        gap: 14px;
        flex-wrap: wrap;
      "
    >
      <div>
        <div style="font-weight: 950; color:#0f172a; font-size: 20px;">Ready to level up your career?</div>
        <div style="margin-top: 6px; color: rgba(15,23,42,0.65); font-weight: 650;">
          Start learning today — and use AI tools to study faster.
        </div>
      </div>

      <div style="display:flex; gap:10px; flex-wrap:wrap;">
        <a
          href="/courses"
          style="
            text-decoration:none;
            padding: 12px 16px;
            border-radius: 14px;
            background: #10b981;
            color: white;
            font-weight: 950;
            box-shadow: 0 14px 30px rgba(16,185,129,0.20);
          "
        >
          Explore Courses
        </a>
        <a
          href="/ai"
          style="
            text-decoration:none;
            padding: 12px 16px;
            border-radius: 14px;
            background: rgba(16,185,129,0.12);
            border: 1px solid rgba(16,185,129,0.22);
            color: #0f766e;
            font-weight: 950;
          "
        >
          Try AI Tutor
        </a>
      </div>
    </div>
  </section>
</section>

<style>
  @media (max-width: 1100px) {
    section > div:nth-child(2) {
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

<script lang="ts">
  import { goto } from "$app/navigation";

  const API_URL = import.meta.env.PUBLIC_API_URL ?? "http://127.0.0.1:8000";

  let msg: string | null = null;
  let loading = false;

  async function upgrade() {
    msg = null;
    loading = true;

    const token = localStorage.getItem("token");
    if (!token) {
      loading = false;
      return goto("/login");
    }

    try {
      const res = await fetch(`${API_URL}/billing/create-checkout-session`, {
        method: "POST",
        headers: { Authorization: `Bearer ${token}` }
      });

      if (!res.ok) {
        msg = "❌ Failed to start checkout";
        return;
      }

      const data = await res.json();
      if (!data?.url) {
        msg = "❌ Checkout URL not received from server";
        return;
      }

      // ✅ Redirect to Stripe Checkout
      window.location.href = data.url;
    } catch {
      msg = "❌ Network error. Please try again.";
    } finally {
      loading = false;
    }
  }
</script>

<div style="max-width: 1050px; margin: 28px auto; padding: 0 16px;">
  <!-- Header -->
  <div style="display:flex; justify-content:space-between; align-items:flex-end; gap: 12px; flex-wrap: wrap;">
    <div>
      <div style="font-size: 12px; font-weight: 950; letter-spacing: 0.3px; color:#0f766e;">
        BILLING
      </div>
      <h1 style="margin: 6px 0 0; font-size: 32px; font-weight: 980; color:#0f172a;">
        Upgrade to Premium
      </h1>
      <p style="margin: 8px 0 0; color: rgba(15,23,42,0.65); font-weight: 650; line-height: 1.6;">
        Unlock AI Tutor, smart notes, quizzes, and full progress tracking.
      </p>
    </div>

    <a
      href="/me"
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
      ← Back to Profile
    </a>
  </div>

  <!-- Pricing layout -->
  <div
    style="
      margin-top: 16px;
      display: grid;
      grid-template-columns: 1.1fr 0.9fr;
      gap: 14px;
      align-items: start;
    "
  >
    <!-- Left: Benefits -->
    <div
      style="
        border-radius: 22px;
        background: rgba(255,255,255,0.90);
        border: 1px solid rgba(15,23,42,0.10);
        box-shadow: 0 14px 30px rgba(15,23,42,0.08);
        padding: 18px;
      "
    >
      <div
        style="
          display:flex;
          align-items:center;
          gap: 10px;
          padding: 12px 12px;
          border-radius: 18px;
          background: linear-gradient(135deg, rgba(16,185,129,0.16), rgba(14,165,233,0.10));
          border: 1px solid rgba(15,23,42,0.08);
        "
      >
        <div
          style="
            width: 46px;
            height: 46px;
            border-radius: 16px;
            display:grid;
            place-items:center;
            background: rgba(16,185,129,0.14);
            border: 1px solid rgba(16,185,129,0.22);
            font-size: 20px;
          "
        >
          ⭐
        </div>
        <div>
          <div style="font-weight: 980; color:#0f172a;">Premium Features</div>
          <div style="font-weight: 650; color: rgba(15,23,42,0.65); font-size: 13px; margin-top: 2px;">
            Everything you need to learn faster.
          </div>
        </div>
      </div>

      <!-- bullets -->
      <div style="margin-top: 14px; display:grid; gap: 10px;">
        <div style="display:flex; gap: 10px; align-items:flex-start;">
          <div style="width:34px; height:34px; border-radius: 12px; display:grid; place-items:center; background: rgba(16,185,129,0.12); border: 1px solid rgba(16,185,129,0.22);">🤖</div>
          <div>
            <div style="font-weight: 950; color:#0f172a;">Unlimited AI Tutor</div>
            <div style="color: rgba(15,23,42,0.65); font-weight: 650; font-size: 13px; line-height: 1.6;">
              Ask questions, get explanations, copy answers instantly.
            </div>
          </div>
        </div>

        <div style="display:flex; gap: 10px; align-items:flex-start;">
          <div style="width:34px; height:34px; border-radius: 12px; display:grid; place-items:center; background: rgba(14,165,233,0.10); border: 1px solid rgba(14,165,233,0.16);">📝</div>
          <div>
            <div style="font-weight: 950; color:#0f172a;">Smart Notes + Quiz Generator</div>
            <div style="color: rgba(15,23,42,0.65); font-weight: 650; font-size: 13px; line-height: 1.6;">
              Create summaries, flashcards, and quizzes from lessons.
            </div>
          </div>
        </div>

        <div style="display:flex; gap: 10px; align-items:flex-start;">
          <div style="width:34px; height:34px; border-radius: 12px; display:grid; place-items:center; background: rgba(15,23,42,0.06); border: 1px solid rgba(15,23,42,0.10);">📈</div>
          <div>
            <div style="font-weight: 950; color:#0f172a;">Progress Tracking</div>
            <div style="color: rgba(15,23,42,0.65); font-weight: 650; font-size: 13px; line-height: 1.6;">
              Track completed lessons and course percentage in real-time.
            </div>
          </div>
        </div>

        <div style="display:flex; gap: 10px; align-items:flex-start;">
          <div style="width:34px; height:34px; border-radius: 12px; display:grid; place-items:center; background: rgba(245,158,11,0.12); border: 1px solid rgba(245,158,11,0.22);">⚡</div>
          <div>
            <div style="font-weight: 950; color:#0f172a;">Priority Features</div>
            <div style="color: rgba(15,23,42,0.65); font-weight: 650; font-size: 13px; line-height: 1.6;">
              Early access to new learning tools and improvements.
            </div>
          </div>
        </div>
      </div>

      <div
        style="
          margin-top: 14px;
          padding: 12px;
          border-radius: 18px;
          background: rgba(16,185,129,0.10);
          border: 1px solid rgba(16,185,129,0.18);
          color: rgba(15,23,42,0.75);
          font-weight: 700;
          font-size: 13px;
          line-height: 1.6;
        "
      >
        ✅ If your AI Tutor shows “Upgrade to Premium”, it means your backend returned <b>403</b> (not premium).
        Upgrading will allow AI requests.
      </div>
    </div>

    <!-- Right: Checkout card -->
    <div
      style="
        border-radius: 22px;
        background: rgba(255,255,255,0.90);
        border: 1px solid rgba(15,23,42,0.10);
        box-shadow: 0 14px 30px rgba(15,23,42,0.08);
        padding: 18px;
      "
    >
      <div style="display:flex; align-items:center; justify-content:space-between; gap: 12px;">
        <div>
          <div style="font-weight: 980; color:#0f172a; font-size: 16px;">Premium Plan</div>
          <div style="color: rgba(15,23,42,0.65); font-weight: 650; font-size: 13px; margin-top: 3px;">
            Best for serious learners
          </div>
        </div>

        <div
          style="
            padding: 6px 10px;
            border-radius: 999px;
            background: rgba(16,185,129,0.12);
            border: 1px solid rgba(16,185,129,0.22);
            color:#0f766e;
            font-weight: 950;
            font-size: 12px;
          "
        >
          RECOMMENDED
        </div>
      </div>

      <div style="margin-top: 14px;">
        <div style="font-size: 34px; font-weight: 980; color:#0f172a;">
          LKR <span style="color:#0f766e;">—</span>
          <span style="font-size: 13px; font-weight: 800; color: rgba(15,23,42,0.60);">/month</span>
        </div>
        <div style="margin-top: 6px; color: rgba(15,23,42,0.62); font-weight: 650; font-size: 13px;">
          (Price comes from Stripe product in your backend)
        </div>
      </div>

      <button
        on:click={upgrade}
        disabled={loading}
        style="
          width: 100%;
          margin-top: 14px;
          padding: 14px;
          border-radius: 16px;
          border: none;
          background: linear-gradient(135deg, #10b981, #22c55e);
          color: white;
          font-size: 15px;
          font-weight: 980;
          cursor: pointer;
          box-shadow: 0 16px 34px rgba(16,185,129,0.30);
          opacity: {loading ? 0.7 : 1};
        "
      >
        {loading ? "Redirecting to Checkout..." : "Upgrade Now →"}
      </button>

      {#if msg}
        <div
          style="
            margin-top: 12px;
            padding: 10px 12px;
            border-radius: 16px;
            background: rgba(239,68,68,0.10);
            border: 1px solid rgba(239,68,68,0.20);
            color: #b91c1c;
            font-weight: 900;
            font-size: 13px;
          "
        >
          {msg}
        </div>
      {/if}

      <div
        style="
          margin-top: 14px;
          padding-top: 12px;
          border-top: 1px solid rgba(15,23,42,0.10);
          color: rgba(15,23,42,0.65);
          font-size: 12px;
          font-weight: 650;
          line-height: 1.6;
        "
      >
        Payments are handled securely by <b>Stripe Checkout</b>.
        After payment, you’ll be redirected back to Learnify AI.
      </div>
    </div>
  </div>
</div>

<style>
  @media (max-width: 980px) {
    div[style*="grid-template-columns: 1.1fr 0.9fr"] {
      grid-template-columns: 1fr !important;
    }
  }
</style>

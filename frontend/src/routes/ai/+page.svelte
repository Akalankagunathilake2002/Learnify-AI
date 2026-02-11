<script lang="ts">
  import { goto } from "$app/navigation";

  const API_URL = import.meta.env.PUBLIC_API_URL ?? "http://127.0.0.1:8000";

  let question = "";
  let answer = "";
  let error: string | null = null;
  let loading = false;

  async function askAI() {
    error = null;
    loading = true;
    answer = "";

    const token = localStorage.getItem("token");
    if (!token) return goto("/login");

    try {
      const res = await fetch(`${API_URL}/ai/ask`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify({ question })
      });

      if (!res.ok) {
        error =
          res.status === 403
            ? "Upgrade to Premium to use AI"
            : "AI request failed";
        return;
      }

      const data = await res.json();
      answer = data.answer ?? "";
    } catch (e) {
      error = "Network error. Please try again.";
    } finally {
      loading = false;
    }
  }

  function handleKeydown(e: KeyboardEvent) {
    if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) {
      if (!loading && question.trim()) askAI();
    }
  }

  function copyAnswer() {
    if (!answer) return;
    navigator.clipboard.writeText(answer);
  }
</script>

<!-- Page background (same theme as layout) -->
<div
  style="
    min-height: calc(100vh - 0px);
    padding: 26px 0;
    background:
      radial-gradient(900px 520px at 10% 20%, rgba(16,185,129,0.10), transparent 60%),
      radial-gradient(900px 520px at 90% 20%, rgba(34,197,94,0.08), transparent 60%),
      linear-gradient(180deg, #f7faf9 0%, #f2f7f5 100%);
    box-sizing: border-box;
  "
>
  <!-- Container (NOT centered tiny, uses your 1280px layout width look) -->
  <div style="max-width: 1100px; margin: 0 auto; padding: 0 18px;">
    <!-- Title row -->
    <div
      style="
        display:flex;
        align-items: end;
        justify-content: space-between;
        gap: 12px;
        flex-wrap: wrap;
        margin-bottom: 14px;
      "
    >
      <div>
        <div style="font-size: 12px; font-weight: 950; color:#0f766e; letter-spacing: 0.3px;">
          LEARNIFY AI
        </div>
        <h1 style="margin: 6px 0 0; font-size: 30px; font-weight: 950; color:#0f172a;">
          🤖 AI Tutor
        </h1>
        <p style="margin: 8px 0 0; color: rgba(15,23,42,0.65); font-weight: 650;">
          Ask questions about your courses and get quick explanations.
        </p>
      </div>

      <div style="display:flex; gap:10px; flex-wrap:wrap;">
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
          ⌘/Ctrl + Enter
        </span>
        <a
          href="/billing"
          style="
            text-decoration:none;
            padding: 8px 12px;
            border-radius: 999px;
            background: rgba(16,185,129,0.12);
            border: 1px solid rgba(16,185,129,0.22);
            color: #0f766e;
            font-weight: 950;
          "
        >
          Upgrade →
        </a>
      </div>
    </div>

    <!-- Main card -->
    <div
      style="
        width: 100%;
        height: min(78vh, 840px);
        display: flex;
        flex-direction: column;
        border-radius: 22px;
        overflow: hidden;
        background: rgba(255,255,255,0.88);
        border: 1px solid rgba(15,23,42,0.10);
        box-shadow: 0 20px 55px rgba(15,23,42,0.10);
      "
    >
      <!-- Input area -->
      <div
        style="
          padding: 16px 18px;
          border-bottom: 1px solid rgba(15,23,42,0.08);
          background: rgba(255,255,255,0.92);
        "
      >
        <div style="display:flex; justify-content:space-between; gap:10px; flex-wrap:wrap; margin-bottom: 8px;">
          <label style="font-size: 13px; color: rgba(15,23,42,0.75); font-weight: 850;">
            Ask something about your course
          </label>
          <span style="font-size: 12px; color: rgba(15,23,42,0.55); font-weight: 750;">
            Example: “What is REST API? Give an example”
          </span>
        </div>

        <textarea
          rows="3"
          placeholder="Type your question..."
          bind:value={question}
          on:keydown={handleKeydown}
          style="
            width: 100%;
            padding: 12px 12px;
            border-radius: 14px;
            border: 1px solid rgba(15,23,42,0.14);
            background: #f8fafc;
            color: #0f172a;
            font-size: 14px;
            line-height: 1.55;
            outline: none;
            resize: none;
            box-sizing: border-box;
          "
        />

        <button
          on:click={askAI}
          disabled={loading || !question.trim()}
          style="
            margin-top: 12px;
            width: 100%;
            padding: 12px;
            border-radius: 14px;
            border: none;
            cursor: pointer;
            font-size: 15px;
            font-weight: 950;
            background: #10b981;
            color: white;
            opacity: {loading || !question.trim() ? 0.6 : 1};
            box-shadow: 0 12px 30px rgba(16,185,129,0.22);
          "
        >
          {loading ? "Thinking..." : "Ask AI"}
        </button>

        {#if error}
          <div
            style="
              margin-top: 12px;
              padding: 10px 12px;
              border-radius: 14px;
              background: rgba(239,68,68,0.10);
              border: 1px solid rgba(239,68,68,0.18);
              color: #991b1b;
              font-size: 13px;
              font-weight: 850;
            "
          >
            ⚠️ {error}
          </div>
        {/if}
      </div>

      <!-- Answer area (only this scrolls) -->
      <div
        style="
          flex: 1;
          overflow: auto;
          padding: 16px 18px;
          background: linear-gradient(180deg, #ffffff 0%, #fbfffd 60%, #f8fafc 100%);
          box-sizing: border-box;
        "
      >
        {#if !answer && !loading}
          <div
            style="
              height: 100%;
              display: grid;
              place-items: center;
              text-align: center;
              padding: 24px;
              color: rgba(15,23,42,0.6);
            "
          >
            <div>
              <div style="font-size: 34px; margin-bottom: 10px;">💬</div>
              <div style="font-weight: 950; color: rgba(15,23,42,0.90); font-size: 16px;">
                Your answer will appear here
              </div>
              <div style="margin-top: 6px; font-size: 13px; font-weight: 750;">
                Tip: Ask short + clear questions for better answers.
              </div>
            </div>
          </div>
        {/if}

        {#if loading}
          <div
            style="
              border-radius: 18px;
              border: 1px dashed rgba(15,23,42,0.18);
              background: rgba(255,255,255,0.95);
              padding: 14px;
              color: rgba(15,23,42,0.72);
              font-size: 14px;
              font-weight: 800;
            "
          >
            ⏳ Generating answer...
          </div>
        {/if}

        {#if answer}
          <div
            style="
              border-radius: 18px;
              border: 1px solid rgba(15,23,42,0.10);
              background: rgba(255,255,255,0.96);
              box-shadow: 0 12px 30px rgba(15,23,42,0.08);
              padding: 14px;
            "
          >
            <div
              style="
                display: flex;
                justify-content: space-between;
                align-items: center;
                gap: 10px;
                margin-bottom: 10px;
                flex-wrap: wrap;
              "
            >
              <div style="display:flex; align-items:center; gap:8px;">
                <span style="font-size: 16px;">💡</span>
                <h3 style="margin: 0; font-size: 16px; font-weight: 950; color: #0f172a;">
                  Answer
                </h3>
              </div>

              <button
                on:click={copyAnswer}
                style="
                  padding: 8px 10px;
                  border-radius: 12px;
                  border: 1px solid rgba(15,23,42,0.10);
                  background: #f8fafc;
                  color: rgba(15,23,42,0.85);
                  cursor: pointer;
                  font-size: 12px;
                  font-weight: 900;
                "
              >
                📋 Copy
              </button>
            </div>

            <pre
              style="
                margin: 0;
                white-space: pre-wrap;
                word-break: break-word;
                line-height: 1.7;
                font-size: 14px;
                color: rgba(15,23,42,0.90);
                font-weight: 650;
              "
            >
{answer}
            </pre>
          </div>
        {/if}
      </div>

      <!-- Footer -->
      <div
        style="
          padding: 10px 14px;
          border-top: 1px solid rgba(15,23,42,0.08);
          display: flex;
          justify-content: space-between;
          gap: 10px;
          color: rgba(15,23,42,0.55);
          font-size: 12px;
          background: rgba(255,255,255,0.92);
          font-weight: 750;
        "
      >
        <span>🔒 Token auth enabled</span>
        <span>✅ Only answer area scrolls</span>
      </div>
    </div>
  </div>
</div>

<style>
  @media (max-width: 720px) {
    div[style*="height: min(78vh"] {
      height: auto !important;
      min-height: 70vh !important;
    }
  }
</style>

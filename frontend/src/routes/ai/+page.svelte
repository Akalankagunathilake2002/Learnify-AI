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
        loading = false;
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
</script>

<!-- Light background -->
<div
  style="
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 22px;
    background:
      radial-gradient(800px 420px at 10% 10%, rgba(56,189,248,0.22), transparent 60%),
      radial-gradient(900px 520px at 80% 15%, rgba(99,102,241,0.16), transparent 60%),
      linear-gradient(180deg, #ffffff 0%, #f6f8ff 70%, #f1f5f9 100%);
    font-family: system-ui, -apple-system, BlinkMacSystemFont;
    box-sizing: border-box;
  "
>
  <div
    style="
      width: min(920px, 100%);
      height: min(92vh, 840px);
      display: flex;
      flex-direction: column;
      border-radius: 18px;
      overflow: hidden;
      background: #ffffff;
      border: 1px solid rgba(15,23,42,0.10);
      box-shadow: 0 20px 55px rgba(15,23,42,0.10);
    "
  >
    <!-- Header -->
    <div
      style="
        padding: 18px 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 10px;
        border-bottom: 1px solid rgba(15,23,42,0.08);
        background: linear-gradient(135deg, rgba(56,189,248,0.10), rgba(99,102,241,0.08));
      "
    >
      <div
        style="
          width: 42px;
          height: 42px;
          display: grid;
          place-items: center;
          border-radius: 12px;
          background: rgba(56,189,248,0.16);
          border: 1px solid rgba(56,189,248,0.25);
        "
      >
        🤖
      </div>
      <h1
        style="
          margin: 0;
          font-size: 20px;
          font-weight: 900;
          color: #0f172a;
        "
      >
        AI Tutor
      </h1>
    </div>

    <!-- Input section -->
    <div
      style="
        padding: 18px;
        border-bottom: 1px solid rgba(15,23,42,0.08);
        background: #ffffff;
      "
    >
      <div
        style="
          display: flex;
          justify-content: space-between;
          gap: 10px;
          flex-wrap: wrap;
          margin-bottom: 8px;
        "
      >
        <label style="font-size: 13px; color: rgba(15,23,42,0.75); font-weight: 700;">
          Ask something about your course
        </label>
        <span style="font-size: 12px; color: rgba(15,23,42,0.55);">
          Ctrl/⌘ + Enter to send
        </span>
      </div>

      <textarea
        rows="3"
        placeholder="e.g., What is a REST API? Explain with an example..."
        bind:value={question}
        on:keydown={handleKeydown}
        style="
          width: 100%;
          padding: 12px 12px;
          border-radius: 12px;
          border: 1px solid rgba(15,23,42,0.14);
          background: #f8fafc;
          color: #0f172a;
          font-size: 14px;
          line-height: 1.5;
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
          border-radius: 12px;
          border: none;
          cursor: pointer;
          font-size: 15px;
          font-weight: 900;
          background: linear-gradient(135deg, #38bdf8, #0ea5e9);
          color: #04111f;
          opacity: ${loading || !question.trim() ? "0.55" : "1"};
          box-shadow: 0 12px 30px rgba(14,165,233,0.22);
          transition: transform 0.12s ease, box-shadow 0.12s ease, opacity 0.12s ease;
        "
      >
        {loading ? "Thinking..." : "Ask AI"}
      </button>

      {#if error}
        <div
          style="
            margin-top: 12px;
            padding: 10px 12px;
            border-radius: 12px;
            background: rgba(239, 68, 68, 0.10);
            border: 1px solid rgba(239, 68, 68, 0.18);
            color: #991b1b;
            font-size: 13px;
            font-weight: 700;
          "
        >
          ⚠️ {error}
        </div>
      {/if}
    </div>

    <!-- Answer section (scrollable only here) -->
    <div
      style="
        flex: 1;
        overflow: auto;
        padding: 16px 18px;
        background: linear-gradient(180deg, #ffffff 0%, #fbfdff 60%, #f8fafc 100%);
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
            <div style="font-weight: 900; color: rgba(15,23,42,0.9);">
              Your answer will appear here
            </div>
            <div style="margin-top: 6px; font-size: 13px;">
              Tip: Ask short + clear questions for better answers.
            </div>
          </div>
        </div>
      {/if}

      {#if loading}
        <div
          style="
            border-radius: 16px;
            border: 1px dashed rgba(15,23,42,0.18);
            background: #ffffff;
            padding: 14px;
            color: rgba(15,23,42,0.7);
            font-size: 14px;
            font-weight: 700;
          "
        >
          ⏳ Generating answer...
        </div>
      {/if}

      {#if answer}
        <div
          style="
            border-radius: 16px;
            border: 1px solid rgba(15,23,42,0.10);
            background: #ffffff;
            box-shadow: 0 12px 30px rgba(15,23,42,0.08);
            padding: 14px 14px;
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
              <h3 style="margin: 0; font-size: 16px; font-weight: 900; color: #0f172a;">
                Answer
              </h3>
            </div>

            <button
              on:click={() => navigator.clipboard.writeText(answer)}
              style="
                padding: 8px 10px;
                border-radius: 12px;
                border: 1px solid rgba(15,23,42,0.10);
                background: #f8fafc;
                color: rgba(15,23,42,0.85);
                cursor: pointer;
                font-size: 12px;
                font-weight: 800;
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
              line-height: 1.65;
              font-size: 14px;
              color: rgba(15,23,42,0.9);
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
        background: #ffffff;
      "
    >
      <span>🔒 Token auth enabled</span>
      <span>✅ Only answer area scrolls</span>
    </div>
  </div>
</div>

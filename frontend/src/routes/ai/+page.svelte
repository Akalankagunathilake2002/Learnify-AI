<script lang="ts">
  import { goto } from "$app/navigation";
  import { onMount } from "svelte";

  const API_URL = import.meta.env.PUBLIC_API_URL ?? "http://127.0.0.1:8000";

  let question = "";
  let answer = "";
  let error: string | null = null;
  let loading = false;

  let provider: "groq" | "gemini" = "groq";
  let task: "tutor" | "notes" | "image" = "tutor";

  let imageDataUrl: string | null = null;

  // ✅ Tips modal
  let showModal = false;
  let dontShowAgain = false;

  // ✅ Loading popup text rotation
  const loadingMsgsGeminiTutor = [
    "Gemini is thinking…",
    "Building a clear explanation…",
    "Finding a simple example…",
    "Almost done…"
  ];
  const loadingMsgsGeminiNotes = [
    "Creating study notes…",
    "Extracting key points…",
    "Generating MCQs + answers…",
    "Formatting nicely…"
  ];
  const loadingMsgsGeminiImage = [
    "Generating image with Gemini…",
    "Composing visual details…",
    "Rendering output…",
    "Almost ready…"
  ];
  const loadingMsgsGroqTutor = [
    "Groq is thinking…",
    "Making it simple…",
    "Adding a quick example…",
    "Almost done…"
  ];
  const loadingMsgsGroqNotes = [
    "Preparing notes…",
    "Creating quiz questions…",
    "Finalizing output…"
  ];

  let loadingMsg = "Working…";
  let loadingTimer: number | null = null;
  let loadingIndex = 0;

  function getLoadingList() {
    if (provider === "gemini") {
      if (task === "notes") return loadingMsgsGeminiNotes;
      if (task === "image") return loadingMsgsGeminiImage;
      return loadingMsgsGeminiTutor;
    } else {
      if (task === "notes") return loadingMsgsGroqNotes;
      return loadingMsgsGroqTutor;
    }
  }

  function startLoadingRotation() {
    const list = getLoadingList();
    loadingIndex = 0;
    loadingMsg = list[0] ?? "Working…";

    if (loadingTimer) window.clearInterval(loadingTimer);
    loadingTimer = window.setInterval(() => {
      const arr = getLoadingList();
      loadingIndex = (loadingIndex + 1) % arr.length;
      loadingMsg = arr[loadingIndex] ?? "Working…";
    }, 900);
  }

  function stopLoadingRotation() {
    if (loadingTimer) window.clearInterval(loadingTimer);
    loadingTimer = null;
  }

  function openModal() {
    showModal = true;
    document.body.style.overflow = "hidden";
  }

  function closeModal() {
    showModal = false;
    document.body.style.overflow = "";
    if (dontShowAgain) {
      localStorage.setItem("learnify_ai_modal_hidden", "1");
    }
  }

  function escapeClose(e: KeyboardEvent) {
    if (e.key === "Escape" && showModal) closeModal();
  }

  onMount(() => {
    // show tips modal on entry unless user disabled it
    const hidden = localStorage.getItem("learnify_ai_modal_hidden");
    if (!hidden) openModal();

    window.addEventListener("keydown", escapeClose);
    return () => window.removeEventListener("keydown", escapeClose);
  });

  async function askAI() {
    error = null;
    answer = "";
    imageDataUrl = null;

    // ✅ close tips modal if open
    if (showModal) closeModal();

    const token = localStorage.getItem("token");
    if (!token) return goto("/login");

    // ✅ optional: show tips modal once before first ask
    const hidden = localStorage.getItem("learnify_ai_modal_hidden");
    if (!hidden && !showModal) {
      openModal();
      return;
    }

    loading = true;
    startLoadingRotation();

    try {
      const res = await fetch(`${API_URL}/ai/ask`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify({ question, provider, task })
      });

      if (!res.ok) {
        const txt = await res.text();
        error =
          res.status === 403
            ? "Upgrade to Premium to use AI"
            : `AI request failed: ${txt}`;
        return;
      }

      const data = await res.json();
      answer = data.answer ?? "";

      if (data.image_base64) {
        const mime = data.image_mime ?? "image/png";
        imageDataUrl = `data:${mime};base64,${data.image_base64}`;
      }
    } catch (e) {
      error = "Network error. Please try again.";
    } finally {
      loading = false;
      stopLoadingRotation();
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

<!-- Page background -->
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
  <div style="max-width: 1100px; margin: 0 auto; padding: 0 18px;">
    <!-- Header -->
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

        <button
          on:click={openModal}
          style="
            border: 1px solid rgba(16,185,129,0.22);
            background: rgba(16,185,129,0.12);
            color: #0f766e;
            font-weight: 950;
            padding: 8px 12px;
            border-radius: 999px;
            cursor: pointer;
          "
        >
          ℹ️ Tips
        </button>

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
        <!-- Provider + Task row -->
        <div
          style="
            display:flex;
            gap:10px;
            flex-wrap:wrap;
            align-items:center;
            justify-content: space-between;
            margin-bottom: 10px;
          "
        >
          <div style="display:flex; gap:10px; flex-wrap:wrap;">
            <select
              bind:value={provider}
              style="
                padding: 10px 12px;
                border-radius: 12px;
                border: 1px solid rgba(15,23,42,0.12);
                background: #ffffff;
                font-weight: 900;
                color: rgba(15,23,42,0.80);
                outline: none;
              "
            >
              <option value="groq">Groq</option>
              <option value="gemini">Gemini</option>
            </select>

            <select
              bind:value={task}
              style="
                padding: 10px 12px;
                border-radius: 12px;
                border: 1px solid rgba(15,23,42,0.12);
                background: #ffffff;
                font-weight: 900;
                color: rgba(15,23,42,0.80);
                outline: none;
              "
            >
              <option value="tutor">Tutor (Explain)</option>
              <option value="notes">Notes + Quiz</option>
              <option value="image">Image (Gemini)</option>
            </select>
          </div>

          <div style="font-size: 12px; font-weight: 800; color: rgba(15,23,42,0.55);">
            Try: “Explain REST API with example”
          </div>
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

      <!-- Answer area -->
      <div
        style="
          flex: 1;
          overflow: auto;
          padding: 16px 18px;
          background: linear-gradient(180deg, #ffffff 0%, #fbfffd 60%, #f8fafc 100%);
          box-sizing: border-box;
        "
      >
        {#if !answer && !imageDataUrl && !loading}
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

        {#if imageDataUrl}
          <div
            style="
              border-radius: 18px;
              border: 1px solid rgba(15,23,42,0.10);
              background: rgba(255,255,255,0.96);
              box-shadow: 0 12px 30px rgba(15,23,42,0.08);
              padding: 14px;
              margin-bottom: 12px;
            "
          >
            <div style="display:flex; justify-content:space-between; align-items:center; gap:10px; flex-wrap:wrap;">
              <h3 style="margin:0; font-size:16px; font-weight:950; color:#0f172a;">🖼 Generated Image</h3>
              <span style="font-size:12px; font-weight:900; color: rgba(15,23,42,0.60);">
                Provider: {provider}
              </span>
            </div>

            <img
              src={imageDataUrl}
              alt="Generated"
              style="
                width: 100%;
                max-height: 520px;
                object-fit: contain;
                border-radius: 16px;
                margin-top: 10px;
                border: 1px solid rgba(15,23,42,0.08);
                background: rgba(15,23,42,0.02);
              "
            />
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
                <span
                  style="
                    margin-left: 8px;
                    font-size: 12px;
                    font-weight: 950;
                    padding: 5px 10px;
                    border-radius: 999px;
                    background: rgba(16,185,129,0.12);
                    border: 1px solid rgba(16,185,129,0.22);
                    color: #0f766e;
                  "
                >
                  {provider.toUpperCase()} • {task.toUpperCase()}
                </span>
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

<!-- ✅ BIG POPUP (Tips) -->
{#if showModal}
  <div class="overlay" on:click|stopPropagation={closeModal}>
    <div class="modal" on:click|stopPropagation>
      <div class="badge">LEARNIFY AI • Quick Guide</div>

      <h2 class="title">Welcome to AI Tutor ✨</h2>
      <p class="desc">
        Pick a provider + task, then ask a clear question.
        You can generate explanations, study notes + quizzes, or images (Gemini).
      </p>

      <div class="tips">
        <div class="tipCard">
          <div class="tipIcon">🎯</div>
          <div>
            <div class="tipTitle">Ask clear questions</div>
            <div class="tipText">Example: “Explain REST API with a real-world example.”</div>
          </div>
        </div>

        <div class="tipCard">
          <div class="tipIcon">📝</div>
          <div>
            <div class="tipTitle">Use Notes mode</div>
            <div class="tipText">Get summary + key points + MCQs for exam practice.</div>
          </div>
        </div>

        <div class="tipCard">
          <div class="tipIcon">🖼️</div>
          <div>
            <div class="tipTitle">Image mode (Gemini)</div>
            <div class="tipText">Generate visuals/diagrams (best for concepts).</div>
          </div>
        </div>
      </div>

      <div class="row">
        <label class="checkbox">
          <input type="checkbox" bind:checked={dontShowAgain} />
          Don’t show this again
        </label>

        <button class="primary" on:click={closeModal}>
          ✅ Got it, Let’s Learn
        </button>
      </div>

      <div class="mini">
        Tip: Press <b>Ctrl/⌘ + Enter</b> to submit quickly. Press <b>Esc</b> to close.
      </div>
    </div>
  </div>
{/if}

<!-- ✅ LOADING POPUP (Rotating circle) -->
{#if loading}
  <div class="loadOverlay" aria-live="polite">
    <div class="loadCard">
      <div class="loadTop">
        <div class="loadDot"></div>
        <div class="loadBrand">LEARNIFY AI</div>
      </div>

      <div class="spinnerWrap">
        <div class="spinner"></div>
      </div>

      <div class="loadTitle">
        {provider === "gemini" ? "Gemini is working" : "Groq is working"} ✨
      </div>

      <div class="loadMsg">{loadingMsg}</div>

      <div class="loadChips">
        <span class="chip">{provider.toUpperCase()}</span>
        <span class="chip">{task.toUpperCase()}</span>
        <span class="chip">Please wait…</span>
      </div>
    </div>
  </div>
{/if}

<style>
  /* Tips modal overlay */
  .overlay {
    position: fixed;
    inset: 0;
    background: rgba(2, 6, 23, 0.55);
    display: grid;
    place-items: center;
    padding: 18px;
    z-index: 9999;
    animation: fadeIn 160ms ease-out;
  }

  .modal {
    width: min(760px, 100%);
    border-radius: 22px;
    padding: 18px;
    background:
      radial-gradient(900px 380px at 20% 0%, rgba(16,185,129,0.22), transparent 60%),
      radial-gradient(900px 380px at 90% 10%, rgba(14,165,233,0.14), transparent 60%),
      rgba(255,255,255,0.98);
    border: 1px solid rgba(255,255,255,0.22);
    box-shadow: 0 40px 120px rgba(0,0,0,0.35);
    animation: popIn 180ms ease-out;
  }

  .badge {
    display: inline-block;
    padding: 6px 10px;
    border-radius: 999px;
    font-weight: 950;
    font-size: 12px;
    color: #0f766e;
    background: rgba(16,185,129,0.14);
    border: 1px solid rgba(16,185,129,0.22);
  }

  .title {
    margin: 10px 0 8px;
    font-size: 28px;
    line-height: 1.1;
    font-weight: 950;
    color: #0f172a;
    letter-spacing: -0.3px;
  }

  .desc {
    margin: 0;
    color: rgba(15,23,42,0.70);
    font-weight: 650;
    line-height: 1.7;
  }

  .tips {
    margin-top: 14px;
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
  }

  .tipCard {
    border-radius: 18px;
    background: rgba(255,255,255,0.78);
    border: 1px solid rgba(15,23,42,0.10);
    padding: 12px;
    display: flex;
    gap: 10px;
    align-items: flex-start;
  }

  .tipIcon {
    width: 42px;
    height: 42px;
    border-radius: 14px;
    display: grid;
    place-items: center;
    background: rgba(16,185,129,0.12);
    border: 1px solid rgba(16,185,129,0.22);
    font-size: 18px;
    flex: 0 0 auto;
  }

  .tipTitle {
    font-weight: 950;
    color: #0f172a;
    margin-bottom: 4px;
  }

  .tipText {
    font-size: 13px;
    font-weight: 700;
    color: rgba(15,23,42,0.65);
    line-height: 1.55;
  }

  .row {
    margin-top: 14px;
    display: flex;
    justify-content: space-between;
    gap: 12px;
    flex-wrap: wrap;
    align-items: center;
  }

  .checkbox {
    display: flex;
    align-items: center;
    gap: 8px;
    font-weight: 850;
    color: rgba(15,23,42,0.72);
    user-select: none;
  }

  .primary {
    padding: 12px 16px;
    border-radius: 14px;
    border: none;
    cursor: pointer;
    font-weight: 950;
    background: #10b981;
    color: white;
    box-shadow: 0 16px 34px rgba(16,185,129,0.22);
  }

  .primary:hover {
    filter: brightness(0.98);
  }

  .mini {
    margin-top: 12px;
    font-size: 12px;
    color: rgba(15,23,42,0.55);
    font-weight: 750;
  }

  /* ✅ Loading overlay */
  .loadOverlay {
    position: fixed;
    inset: 0;
    z-index: 9998;
    background:
      radial-gradient(900px 520px at 10% 20%, rgba(16,185,129,0.18), transparent 60%),
      radial-gradient(900px 520px at 90% 20%, rgba(14,165,233,0.14), transparent 60%),
      rgba(2, 6, 23, 0.55);
    display: grid;
    place-items: center;
    padding: 18px;
    animation: fadeIn 140ms ease-out;
  }

  .loadCard {
    width: min(520px, 100%);
    border-radius: 22px;
    background: rgba(255,255,255,0.96);
    border: 1px solid rgba(255,255,255,0.26);
    box-shadow: 0 40px 120px rgba(0,0,0,0.35);
    padding: 16px;
    animation: popIn 160ms ease-out;
  }

  .loadTop {
    display: flex;
    align-items: center;
    gap: 10px;
    justify-content: space-between;
  }

  .loadDot {
    width: 10px;
    height: 10px;
    border-radius: 999px;
    background: #10b981;
    box-shadow: 0 0 0 6px rgba(16,185,129,0.14);
  }

  .loadBrand {
    font-weight: 950;
    color: rgba(15,23,42,0.70);
    letter-spacing: 0.3px;
    font-size: 12px;
  }

  .spinnerWrap {
    display: grid;
    place-items: center;
    padding: 18px 0 10px;
  }

  .spinner {
    width: 64px;
    height: 64px;
    border-radius: 999px;
    border: 6px solid rgba(15,23,42,0.10);
    border-top-color: rgba(16,185,129,1);
    animation: spin 0.9s linear infinite;
  }

  .loadTitle {
    text-align: center;
    font-weight: 950;
    font-size: 18px;
    color: #0f172a;
  }

  .loadMsg {
    text-align: center;
    margin-top: 8px;
    font-weight: 750;
    color: rgba(15,23,42,0.65);
    line-height: 1.6;
  }

  .loadChips {
    margin-top: 12px;
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    justify-content: center;
  }

  .chip {
    padding: 7px 10px;
    border-radius: 999px;
    font-weight: 900;
    font-size: 12px;
    color: rgba(15,23,42,0.70);
    background: rgba(15,23,42,0.05);
    border: 1px solid rgba(15,23,42,0.08);
  }

  @keyframes spin {
    from { transform: rotate(0deg); }
    to   { transform: rotate(360deg); }
  }

  @keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
  }

  @keyframes popIn {
    from { transform: translateY(10px) scale(0.98); opacity: 0; }
    to { transform: translateY(0) scale(1); opacity: 1; }
  }

  @media (max-width: 900px) {
    .tips { grid-template-columns: 1fr; }
  }
</style>

// app.js — XplainDfile frontend logic (PDF-only)

// ----------------- Global state -----------------
let currentSource = null; // null | "pdf"
let isUploading = false;
let isChatting = false;

// ----------------- DOM refs -----------------
const pdfUpload = document.getElementById("pdfUpload");
const fileLabelText = document.getElementById("fileLabelText");
const resetBtn = document.getElementById("resetBtn");
const activeSource = document.getElementById("activeSource");
const chatWindow = document.getElementById("chatWindow");
const chatInput = document.getElementById("chatInput");
const sendBtn = document.getElementById("sendBtn");
const fileLabel = document.querySelector(".file-label");

// ----------------- Helpers -----------------
function createToast(text, timeout = 3500) {
  const t = document.createElement("div");
  t.className = "bubble small toast";
  t.textContent = text;
  document.body.appendChild(t);
  setTimeout(() => t.remove(), timeout);
}

function scrollChatToBottom() {
  chatWindow.scrollTop = chatWindow.scrollHeight;
}

// ----------------- UI primitives -----------------
function setActiveSourceText(text) {
  activeSource.textContent = text;
}

function enableChat(enable) {
  chatInput.disabled = !enable;
  sendBtn.disabled = !enable;
  if (enable) chatInput.focus();
}

// ----------------- Initialization -----------------
function initialize() {
  setActiveSourceText("Upload a PDF to start");
  chatWindow.innerHTML = "";
  appendMessage({
    role: "assistant",
    text: "Hi 👋 Upload a PDF to get started.",
    small: true
  });
  enableChat(false);
}

// ----------------- Message rendering -----------------
function makeMessageElement({ role, text, source, small }) {
  const article = document.createElement("article");
  article.className = "message " + (role === "user" ? "user" : "assistant");

  const bubble = document.createElement("div");
  bubble.className = "bubble" + (small ? " small" : "");

  if (role !== "user" && source) {
    const tag = document.createElement("span");
    tag.className = "tag " + (source === "file" ? "file" : "llm");
    tag.textContent = source === "file" ? "from file" : "from llm";
    bubble.appendChild(tag);
  }

  const textNode = document.createElement("div");
  textNode.textContent = text;
  bubble.appendChild(textNode);

  article.appendChild(bubble);
  return article;
}

function appendMessage({ role, text, source = null, small = false }) {
  const el = makeMessageElement({ role, text, source, small });
  chatWindow.appendChild(el);
  scrollChatToBottom();
}

// ----------------- Upload flow (PDF only) -----------------
async function uploadFileObject(fileObj) {
  if (isUploading) return;
  isUploading = true;

  setActiveSourceText("Processing document...");
  appendMessage({
    role: "assistant",
    text: "Processing document. This may take a few seconds...",
    small: true
  });

  enableChat(false);

  const fd = new FormData();
  fd.append("file", fileObj);

  try {
    const res = await fetch("/upload", { method: "POST", body: fd });
    if (!res.ok) {
      const j = await res.json().catch(() => ({}));
      throw new Error(j.detail || j.message || res.statusText);
    }

    currentSource = "pdf";
    fileLabelText.textContent = fileObj.name;
    pdfUpload.disabled = true;
    if (fileLabel) fileLabel.classList.add("disabled");

    appendMessage({
      role: "assistant",
      text: "File is uploaded. Feel free to ask me anything.",
      source: "file"
    });

    setActiveSourceText(`Active source: PDF (${fileObj.name})`);
    enableChat(true);

  } catch (err) {
    createToast("Upload error: " + (err.message || "unknown"));
    setActiveSourceText("Upload failed. Try again.");
    enableChat(false);
  } finally {
    isUploading = false;
  }
}

// File input handler
pdfUpload.addEventListener("change", async (ev) => {
  const file = ev.target.files && ev.target.files[0];
  if (!file) return;

  const ext = file.name.split(".").pop().toLowerCase();
  if (ext !== "pdf") {
    createToast("Only PDF files are supported.");
    pdfUpload.value = "";
    return;
  }

  await uploadFileObject(file);
});

// ----------------- Chat logic -----------------
function createThinkingBubble() {
  appendMessage({ role: "assistant", text: "Thinking...", small: true });
}

function removeLastThinkingBubble() {
  const nodes = Array.from(
    chatWindow.querySelectorAll(".message.assistant .bubble.small")
  );
  if (nodes.length) nodes[nodes.length - 1].parentElement.remove();
}

async function sendMessage() {
  if (isChatting) return;
  const text = chatInput.value.trim();
  if (!text) return;

  appendMessage({ role: "user", text });
  chatInput.value = "";

  createThinkingBubble();
  isChatting = true;

  try {
    const res = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question: text })
    });

    if (!res.ok) {
      const j = await res.json().catch(() => ({}));
      throw new Error(j.detail || j.message || res.statusText);
    }

    const { answer, source } = await res.json();
    removeLastThinkingBubble();
    appendMessage({ role: "assistant", text: answer, source });

  } catch (err) {
    removeLastThinkingBubble();
    createToast("Chat error: " + (err.message || "unknown"));
  } finally {
    isChatting = false;
  }
}

sendBtn.addEventListener("click", sendMessage);

chatInput.addEventListener("keydown", (ev) => {
  if (ev.key === "Enter" && !ev.shiftKey) {
    ev.preventDefault();
    sendMessage();
  }
});

// ----------------- Reset -----------------
resetBtn.addEventListener("click", async () => {
  currentSource = null;
  fileLabelText.textContent = "Choose PDF";
  pdfUpload.value = "";
  pdfUpload.disabled = false;
  if (fileLabel) fileLabel.classList.remove("disabled");

  setActiveSourceText("Upload a PDF to start");
  chatWindow.innerHTML = "";
  appendMessage({
    role: "assistant",
    text: "Hi 👋 Upload a PDF to get started.",
    small: true
  });

  enableChat(false);

  try {
    await fetch("/reset", { method: "POST" });
    createToast("Session reset");
  } catch {
    createToast("Reset failed");
  }
});

// ----------------- Boot -----------------
document.addEventListener("DOMContentLoaded", initialize);

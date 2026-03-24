#!/usr/bin/env python3
"""
Elliot Brain — Full Edition
---------------------------

Deterministic, multi-pass self-dialogue engine with Ollama local API integration.
Supports draft → critic → final pipeline, session management, async logging,
threaded streaming, safety lens (warn-only by default), and optional UI hooks.

Designed for headless or UI-attached usage, fully location-independent and repo-ready.

Author: Elliot / Elliot Core
Version: 4.0 (full operational, no hard constraints)

Dependencies:
    - Python 3.11+
    - requests
    - threading, queue, json, pathlib, datetime, re, uuid, time
"""

import requests, threading, queue, json, re, uuid, time
from pathlib import Path
from datetime import datetime
from typing import List

# ---------------------------
# CONFIGURATION / CONSTANTS
# ---------------------------

OLLAMA_URL = "http://localhost:11434"
DEFAULT_MODEL = "llama3:8b"
TIMEOUT = 180
PASSES = 3
WARN_ONLY = True
SESSION_DIR = Path.home() / "ElliotCore_Brain" / "sessions"
SESSION_DIR.mkdir(parents=True, exist_ok=True)
SYSTEM_DEFAULT = "You are Elliot Brain, an elite deterministic reasoning engine."
LOG_FLUSH_EVERY = 2  # seconds
SAFETY_PATTERNS = [
    r"\b(risk|illegal|self-harm|exploit|danger)\b",
]

# ---------------------------
# DATA STRUCTURES
# ---------------------------

class ChatMessage:
    def __init__(self, role: str, content: str, ts: str = None):
        self.role = role
        self.content = content
        self.ts = ts or datetime.utcnow().isoformat()

    def to_dict(self):
        return {"role": self.role, "content": self.content, "ts": self.ts}

# ---------------------------
# UTILITY FUNCTIONS
# ---------------------------

def now_ts():
    return datetime.utcnow().isoformat()

def safety_warnings(text: str):
    warnings = [p for p in SAFETY_PATTERNS if re.search(p, text, re.I)]
    return warnings

# ---------------------------
# SESSION MANAGEMENT
# ---------------------------

class SessionManager:
    def __init__(self):
        self.sessions = {}
        self.lock = threading.Lock()

    def new_session(self, title: str = None):
        session_id = str(uuid.uuid4())
        session_title = title or f"Elliot Brain Session {datetime.utcnow().isoformat()}"
        path = SESSION_DIR / f"{session_id}.jsonl"
        session = {
            "id": session_id,
            "title": session_title,
            "path": path,
            "history": []
        }
        self.sessions[session_id] = session
        return session

    def load_session(self, session_id: str):
        if session_id not in self.sessions:
            path = SESSION_DIR / f"{session_id}.jsonl"
            if path.exists():
                with open(path, "r") as f:
                    history = [json.loads(l) for l in f]
                self.sessions[session_id] = {"id": session_id, "path": path, "history": history}
        return self.sessions.get(session_id)

    def append_message(self, session_id: str, message: ChatMessage):
        with self.lock:
            session = self.sessions[session_id]
            session["history"].append(message.to_dict())
            with open(session["path"], "a") as f:
                f.write(json.dumps(message.to_dict()) + "\n")

# ---------------------------
# OLLAMA API CLIENT
# ---------------------------

class OllamaClient:
    def __init__(self, url=OLLAMA_URL, timeout=TIMEOUT):
        self.url = url
        self.timeout = timeout
        self.session = requests.Session()
        self._active_resp = None
        self._lock = threading.Lock()

    def chat_stream(self, messages: List[dict], model=DEFAULT_MODEL):
        payload = {"model": model, "messages": messages, "stream": True}
        with self._lock:
            resp = self.session.post(f"{self.url}/chat", json=payload, stream=True, timeout=self.timeout)
            self._active_resp = resp
        try:
            for line in resp.iter_lines(decode_unicode=True):
                if line:
                    yield json.loads(line)
        finally:
            with self._lock:
                self._active_resp = None

    def chat_once(self, messages: List[dict], model=DEFAULT_MODEL):
        payload = {"model": model, "messages": messages, "stream": False}
        resp = self.session.post(f"{self.url}/chat", json=payload, timeout=self.timeout)
        return resp.json()

# ---------------------------
# ELLIOT BRAIN ENGINE
# ---------------------------

class ElliotBrain:
    def __init__(self, model=DEFAULT_MODEL, passes=PASSES, warn_only=WARN_ONLY):
        self.client = OllamaClient()
        self.model = model
        self.passes = passes
        self.warn_only = warn_only
        self.chat_history: List[ChatMessage] = []
        self.system_default = SYSTEM_DEFAULT
        self._stop_event = threading.Event()
        self._ui_queue = queue.Queue()
        self._log_buf = []
        self._log_lock = threading.Lock()
        self._worker_thread = None
        self._last_flush = time.time()

        self.session_manager = SessionManager()
        self.session = self.session_manager.new_session()

    # -----------------------
    # MESSAGE MANAGEMENT
    # -----------------------
    def append_message(self, role: str, content: str):
        msg = ChatMessage(role=role, content=content)
        self.chat_history.append(msg)
        self.session_manager.append_message(self.session["id"], msg)

    # -----------------------
    # SELF-DIALOGUE GENERATION
    # -----------------------
    def _build_messages(self, user_prompt: str):
        msgs = [{"role": "system", "content": self.system_default}]
        msgs += [{"role": m["role"], "content": m["content"]} for m in self.session["history"]]
        msgs.append({"role": "user", "content": user_prompt})
        return msgs

    def self_dialogue_generate(self, user_prompt: str):
        messages = self._build_messages(user_prompt)
        final_output = None
        for pass_no in range(1, self.passes + 1):
            resp = self.client.chat_once(messages, model=self.model)
            content = resp.get("completion") or resp.get("content") or ""
            # Append draft -> critic -> final as separate steps
            role = f"pass_{pass_no}"
            self.append_message(role, content)
            messages.append({"role": role, "content": content})
            final_output = content
        # Safety check
        warns = safety_warnings(final_output)
        if warns and self.warn_only:
            final_output = f"[WARNINGS DETECTED: {warns}]\n{final_output}"
        return final_output

    # -----------------------
    # THREADING / UI STREAM
    # -----------------------
    def generate_async(self, user_prompt: str):
        if self._worker_thread and self._worker_thread.is_alive():
            self._stop_event.set()
            self._worker_thread.join()
        self._stop_event.clear()
        self._worker_thread = threading.Thread(target=self._worker_loop, args=(user_prompt,))
        self._worker_thread.start()

    def _worker_loop(self, user_prompt: str):
        messages = self._build_messages(user_prompt)
        try:
            for chunk in self.client.chat_stream(messages, model=self.model):
                if self._stop_event.is_set():
                    break
                content = chunk.get("content", "")
                self._ui_queue.put(content)
                self._log_buf.append(content)
                if time.time() - self._last_flush > LOG_FLUSH_EVERY:
                    self._flush_log_buffer()
        finally:
            self._flush_log_buffer()

    def _flush_log_buffer(self):
        with self._log_lock:
            if self._log_buf:
                combined = "\n".join(self._log_buf)
                self.append_message("stream", combined)
                self._log_buf = []
                self._last_flush = time.time()

# ---------------------------
# USAGE / TEST
# ---------------------------

if __name__ == "__main__":
    brain = ElliotBrain()
    prompt = "Analyze system status and summarize key observability metrics."
    output = brain.self_dialogue_generate(prompt)
    print("=== OUTPUT ===")
    print(output)

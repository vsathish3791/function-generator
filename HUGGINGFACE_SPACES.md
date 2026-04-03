# Deploy on Hugging Face Spaces (Streamlit)

This project includes **`app.py`**, a [Streamlit](https://streamlit.io/) UI around `function_generator.run_pipeline`. You can host it for free (limits apply) on [Hugging Face Spaces](https://huggingface.co/spaces).

> **Important (2025+):** Hugging Face **removed the built-in “Streamlit” SDK** from the new-Space form. New Streamlit apps must use the **Docker** SDK. This repo includes a **`Dockerfile`** for that.

## 1. Files to include

| File | Purpose |
|------|--------|
| `Dockerfile` | Runs Streamlit on port **8501** |
| `requirements.txt` | `litellm` + `streamlit` |
| `app.py` | Streamlit UI |
| `function_generator.py` | Generator logic |

Optional: `README.md` with the YAML block below (first lines of the file).

## 2. Create a new Space (Docker)

1. Open [https://huggingface.co/new-space](https://huggingface.co/new-space)
2. Choose **SDK: Docker** (not Streamlit — it may no longer appear).
3. Create the Space, then upload **`Dockerfile`**, **`requirements.txt`**, **`app.py`**, **`function_generator.py`** (or push from Git).

## 3. README card (Space metadata)

Put this at the **very top** of **`README.md`** in the Space repository (commit before/after upload):

```markdown
---
title: Python function generator
emoji: 🐍
colorFrom: gray
colorTo: green
sdk: docker
app_port: 8501
pinned: false
license: mit
---

# Python function generator

Set **`OPENAI_API_KEY`** in **Space Settings → Variables and secrets**.
```

`app_port: 8501` is required so Hugging Face proxies traffic to Streamlit.

Adjust `title`, `emoji`, and colors as you like.

## 4. API key (required)

**Never commit your key.**

1. Open the Space → **Settings** → **Variables and secrets** → **Secrets**.
2. **Name** must match Hugging Face rules: letters, numbers, underscores only, and start with a letter (e.g. `openai_api_key` or `OPENAI_API_KEY`). **Do not** use hyphens (e.g. `OPENAI-API-KEY` is invalid). Put your **`sk-...`** string only in **Value**.
3. This app sets **`OPENAI_API_KEY`** for LiteLLM; if you named the secret **`openai_api_key`**, it is copied automatically.
4. Optional: **`LITELLM_MODEL`** (e.g. `gpt-4o-mini`).

The app reads these as environment variables (`load_dotenv` loads `.env` locally only).

## 5. Run locally (same UI)

```powershell
cd c:\Personal\Learning\AI
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
# .env with OPENAI_API_KEY, or set env var
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Browser opens at `http://localhost:8501`.

## 6. Timeouts and hardware

- Generation runs **three** LLM calls; it can take **1–3+ minutes**.
- If the Space **times out**, try **Settings → Sleep time / hardware** (paid tiers) or a faster model.
- Free CPU Spaces can be slow; that’s expected.

## 7. Security

- The Space is **public** unless you use a **private Space** (paid org/feature).
- Anyone with the URL can use **your** API quota unless you add **authentication** (not included here). For production, add OAuth or a shared secret check in `app.py`.

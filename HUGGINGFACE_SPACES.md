# Deploy on Hugging Face Spaces (Streamlit)

This project includes **`app.py`**, a [Streamlit](https://streamlit.io/) UI around `function_generator.run_pipeline`. You can host it for free (limits apply) on [Hugging Face Spaces](https://huggingface.co/spaces).

## 1. Push the project to GitHub or Hugging Face

Include at least:

- `app.py`
- `function_generator.py`
- `requirements.txt` (must list `litellm` and `streamlit`)

## 2. Create a new Space

1. Open [https://huggingface.co/new-space](https://huggingface.co/new-space)
2. Link your Git repository **or** upload files.
3. Choose **SDK: Streamlit** (or start blank and add the README card below).
4. **App file:** `app.py`

## 3. README card (Space metadata)

Hugging Face reads the **top of `README.md`** in the Space repo. Either merge this into your existing README **or** use a Space-only repo whose `README.md` starts like this:

```markdown
---
title: Python function generator
emoji: 🐍
colorFrom: gray
colorTo: green
sdk: streamlit
sdk_version: 1.31.0
app_file: app.py
pinned: false
license: mit
---

# Python function generator

LiteLLM-powered 3-step generator (code → docs → tests). Set `OPENAI_API_KEY` in **Space Settings → Repository secrets**.
```

Adjust `title`, `emoji`, and colors as you like.

## 4. API key (required)

**Never commit your key.**

1. Open the Space → **Settings** → **Repository secrets** (or **Variables and secrets**).
2. Add **`OPENAI_API_KEY`** with your OpenAI (or compatible) API key value.
3. Optional: add **`LITELLM_MODEL`** (e.g. `gpt-4o-mini`) if you want a default other than the app’s text field.

The app reads these as normal environment variables (`load_dotenv` still loads `.env` locally only).

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

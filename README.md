# Function generator (LiteLLM)

This project runs **`function_generator.py`**, a small tool that calls an LLM (via [LiteLLM](https://github.com/BerriAI/litellm)) in **three steps** with conversation memory:

1. Implement a basic Python function from your requirements  
2. Add documentation (docstring, parameters, returns, examples, edge cases)  
3. Add `unittest` tests  

The final Python source is **saved to a file** you choose (for example `my_output.py`).

---

## Prerequisites

- **Python 3.10+** (3.12 is fine) installed and available, or use the **virtual environment** below  
- An **OpenAI API key** (default model is `gpt-4o-mini`; override with `LITELLM_MODEL` if you use another provider/model supported by LiteLLM)

---

## 1. Clone or open the project folder

```powershell
cd c:\Personal\Learning\AI
```

---

## 2. Virtual environment (recommended)

Create a venv once:

```powershell
python -m venv .venv
```

Activate it in **PowerShell**:

```powershell
.\.venv\Scripts\Activate.ps1
```

If activation is blocked, either:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

or **do not activate** and call the interpreter explicitly (see below).

Install dependencies:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

**Without activation**, use:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

---

## 3. API key and optional settings

Create a file named **`.env`** in the **same folder** as `function_generator.py` (not committed to git if you use git):

```env
OPENAI_API_KEY=sk-your-key-here
```

Optional:

```env
LITELLM_MODEL=gpt-4o-mini
```

The script loads `.env` automatically from that directory.

---

## 4. Run `function_generator.py`

Show all options:

```powershell
python function_generator.py --help
```

Or without activating the venv:

```powershell
.\.venv\Scripts\python.exe function_generator.py --help
```

### Pass requirements on the command line (`-d` / `--requirements`)

```powershell
python function_generator.py -d "A function that asks for an integer and prints its cube." -o my_output.py
```

`-d`, `--description`, and `--requirements` are the same option.

### Pass requirements from a UTF-8 file (`-f`)

Use this for long or multi-line specs (including blank lines):

```powershell
python function_generator.py -f my_requirements.txt -o my_output.py
```

Do **not** use the name `requirements.txt` for this—that name is reserved for **pip** dependencies.

### Interactive input

Omit `-d` and `-f`; type your requirements at the prompt, then **press Enter on an empty line** to finish:

```powershell
python function_generator.py -o my_output.py
```

### Output file

- **`-o my_output.py`** — write the generated file here  
- If you omit **`-o`**, the file is named `generated_function_YYYYMMDD_HHMMSS.py` in the current directory  

---

## 5. Run the generated `.py` file

The LLM usually produces a module that ends with:

```python
if __name__ == "__main__":
    unittest.main()
```

Running it will **execute the unit tests**:

```powershell
python my_output.py
```

If you changed `__main__` to call your function instead (for example interactive input), running the same command will execute that behavior.

Run tests explicitly (even if `__main__` was changed):

```powershell
python -m unittest my_output -v
```

---

## Troubleshooting (Windows)

| Issue | What to try |
|--------|----------------|
| `Python was not found` when typing `python` | Use `.\.venv\Scripts\python.exe` **or** open a new terminal after installing Python **or** disable “App execution aliases” for `python.exe` in Windows Settings |
| `No module named 'litellm'` | Run `pip install -r requirements.txt` using the **same** Python you use to run the script |
| `Missing OPENAI_API_KEY` / auth errors | Fix `.env` in `c:\Personal\Learning\AI` or set `OPENAI_API_KEY` in the environment |
| Virtual env “not activated” | Check `$env:VIRTUAL_ENV` in PowerShell, or always use `.\.venv\Scripts\python.exe` |

---

## Project layout (typical)

| File | Role |
|------|------|
| `function_generator.py` | CLI: requirements → LLM → saved Python file |
| `app.py` | Streamlit UI (optional; same pipeline as CLI) |
| `requirements.txt` | pip: `litellm`, `streamlit`, etc. |
| `.env` | Your `OPENAI_API_KEY` (local only) |
| `my_output.py` / `generated_function_*.py` | Generated results |

---

## Streamlit UI (local)

```powershell
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Open the URL shown (usually `http://localhost:8501`). Set `OPENAI_API_KEY` in `.env` or in the environment.

---

## Hugging Face Spaces (Streamlit)

Deploy the browser UI so you can use it from another machine: see **[HUGGINGFACE_SPACES.md](HUGGINGFACE_SPACES.md)** for creating a Space, README card YAML, and **Repository secrets** for `OPENAI_API_KEY`.

---

## Summary (quick start)

```powershell
cd c:\Personal\Learning\AI
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
# Put OPENAI_API_KEY in .env next to function_generator.py
.\.venv\Scripts\python.exe function_generator.py -d "Your requirements here." -o my_output.py
.\.venv\Scripts\python.exe my_output.py
```


.\.venv\Scripts\python.exe -m streamlit run app.py
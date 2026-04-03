"""
Streamlit UI for function_generator — deploy on Hugging Face Spaces (sdk: streamlit).

Set API key via HF Variables and secrets, or local .env (see UI messages).
"""

from __future__ import annotations

import contextlib
import io
import os
import tempfile
from datetime import datetime
from pathlib import Path

import streamlit as st

from function_generator import get_model, load_env, run_pipeline


def _mirror_hf_openai_secrets_to_litellm() -> None:
    """HF Secrets may use openai_api_key; LiteLLM expects OPENAI_API_KEY."""
    if os.environ.get("OPENAI_API_KEY"):
        return
    for name in ("openai_api_key", "OPENAI_KEY", "OpenAIApiKey"):
        val = os.environ.get(name)
        if val:
            os.environ["OPENAI_API_KEY"] = val
            return


def main() -> None:
    st.set_page_config(
        page_title="Function generator",
        page_icon="🐍",
        layout="wide",
    )

    load_env()
    _mirror_hf_openai_secrets_to_litellm()

    st.title("Python function generator")
    st.caption(
        "Uses LiteLLM with a 3-step conversation: implementation → documentation → unittest."
    )

    if not os.environ.get("OPENAI_API_KEY"):
        st.error(
            "**Missing `OPENAI_API_KEY` in the running app**\n\n"
            "The server process does not see your key. Fix it on **Hugging Face**, then **rebuild / restart** the Space."
        )
        with st.expander("Checklist (Hugging Face)"):
            st.markdown(
                """
1. **Settings → Variables and secrets** (not the old “Repository secrets” label in older docs).
2. Under **Secrets**, add **one** secret: **Name** `openai_api_key` — **Value** = your full `sk-...` key only.  
   Do **not** add the same name again under **Variables** (that causes *collision* errors).
3. **Factory reboot** or push a new commit so the container **restarts** after saving the secret.
4. Confirm this Space is running **current** code from GitHub (with `sync_openai_key_aliases` in `function_generator.py`).  
   If the UI still shows an old message about “Repository secrets”, redeploy from `main`.
                """
            )
        st.info(
            "**Local run:** copy `.env.example` to `.env` and set `OPENAI_API_KEY=sk-...` next to `app.py`."
        )
        st.stop()

    with st.sidebar:
        st.subheader("Options")
        model_in = st.text_input(
            "Model (LiteLLM id)",
            value=os.environ.get("LITELLM_MODEL", "gpt-4o-mini"),
            help="Examples: gpt-4o-mini, gpt-4o. Must match your API key / provider.",
        )
        st.divider()
        st.markdown(
            "Secrets on HF are injected as environment variables. "
            "Do not commit API keys to the repo."
        )

    requirements = st.text_area(
        "Requirements",
        height=240,
        placeholder=(
            "Describe the Python function you want: behavior, inputs, errors, "
            "and any formatting rules..."
        ),
    )

    if st.button("Generate", type="primary", disabled=not requirements.strip()):
        out = Path(tempfile.gettempdir()) / (
            f"generated_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
        )
        model = (model_in or "").strip() or None
        if model:
            os.environ["LITELLM_MODEL"] = model

        log_buf = io.StringIO()
        try:
            with st.spinner("Generating (3 LLM calls — often 1–3 minutes)..."):
                with contextlib.redirect_stdout(log_buf):
                    code = run_pipeline(requirements.strip(), out, model=model)
        except RuntimeError as err:
            st.error(str(err))
            with st.expander("Log"):
                st.text(log_buf.getvalue())
            st.stop()
        except Exception:
            with st.expander("Log"):
                st.text(log_buf.getvalue())
            raise

        st.success("Generation finished.")
        with st.expander("Step log"):
            st.text(log_buf.getvalue())
        st.subheader("Generated code")
        st.code(code, language="python")
        st.download_button(
            "Download Python file",
            data=code.encode("utf-8"),
            file_name=out.name,
            mime="text/x-python",
        )


if __name__ == "__main__":
    main()

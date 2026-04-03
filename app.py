"""
Streamlit UI for function_generator — deploy on Hugging Face Spaces (sdk: streamlit).

Set OPENAI_API_KEY in Space Settings → Repository secrets (or use .env locally).
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


def main() -> None:
    st.set_page_config(
        page_title="Function generator",
        page_icon="🐍",
        layout="wide",
    )

    load_env()

    st.title("Python function generator")
    st.caption(
        "Uses LiteLLM with a 3-step conversation: implementation → documentation → unittest."
    )

    if not os.environ.get("OPENAI_API_KEY"):
        st.error(
            "**Missing OPENAI_API_KEY.**\n\n"
            "- **Hugging Face:** open this Space → **Settings** → **Repository secrets** → "
            "add a secret named `OPENAI_API_KEY` with your key.\n"
            "- **Local:** create a `.env` file next to `app.py` with `OPENAI_API_KEY=sk-...`"
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

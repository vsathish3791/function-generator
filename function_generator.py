"""
Sequential LiteLLM pipeline: user description -> basic function -> documented
function -> unittest module. Conversation history is kept across all prompts.

Usage:
  set OPENAI_API_KEY (or put it in a .env next to this file)

  Inline requirement text:
    python function_generator.py -d "What the function should do" -o out.py
    python function_generator.py --requirements "..." -o out.py

  Requirements from a UTF-8 file (full spec, multi-line OK):
    python function_generator.py -f my_spec.txt -o out.py

  Interactive (multi-line; finish with a blank line):
    python function_generator.py -o out.py

Requires: litellm, python-dotenv (see requirements.txt)
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from datetime import datetime
from pathlib import Path

from litellm import completion


def get_model() -> str:
    return os.environ.get("LITELLM_MODEL", "gpt-4o-mini")


def extract_code_and_commentary(text: str) -> tuple[str, str]:
    """
    Take fenced ```python blocks as source code; everything else is commentary.
    Falls back to whole response if it looks like raw Python.
    """
    pattern = re.compile(
        r"```(?:python|py)?\s*\n?(.*?)```",
        re.DOTALL | re.IGNORECASE,
    )
    matches = list(pattern.finditer(text))
    if matches:
        code = "\n\n".join(m.group(1).rstrip() for m in matches)
        commentary = pattern.sub("[code block]", text).strip()
        return code.strip(), commentary

    stripped = text.strip()
    if not stripped:
        return "", ""

    if re.search(r"^(def |class |import |from )", stripped, re.MULTILINE):
        return stripped, ""

    return stripped, ""


def print_step(title: str, body: str | None = None) -> None:
    bar = "=" * 60
    print(f"\n{bar}\n{title}\n{bar}")
    if body:
        print(body.rstrip())
    print()


def load_env() -> Path:
    from dotenv import load_dotenv

    env_file = Path(__file__).resolve().parent / ".env"
    load_dotenv(env_file)
    return env_file


def load_requirements_from_file(path: Path) -> str:
    if not path.is_file():
        print(f"Error: requirements file not found: {path}", file=sys.stderr)
        sys.exit(1)
    return path.read_text(encoding="utf-8").strip()


def read_requirements_interactive() -> str:
    print(
        "Enter the requirements for the function (multi-line is OK).\n"
        "Finish with an empty line. For specs that contain blank lines, use -f FILE.\n"
        "End of file (Ctrl-Z then Enter on Windows) also stops input.\n"
    )
    lines: list[str] = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if line == "":
            break
        lines.append(line)
    return "\n".join(lines).strip()


def run_pipeline(
    user_description: str,
    output_path: Path,
    model: str | None = None,
) -> str:
    model = model or get_model()

    system = (
        "You are an expert Python programmer. Follow instructions precisely. "
        "When asked for code, put all executable Python inside one or more "
        "markdown fenced blocks labeled python. Keep explanations outside fences."
    )

    messages: list[dict] = [{"role": "system", "content": system}]

    def chat(user_content: str) -> str:
        messages.append({"role": "user", "content": user_content})
        response = completion(model=model, messages=messages)
        assistant = response.choices[0].message.content or ""
        messages.append({"role": "assistant", "content": assistant})
        return assistant

    # Step 1: minimal implementation
    prompt1 = (
        "Write a basic Python function that satisfies this description.\n\n"
        f"Description:\n{user_description}\n\n"
        "Requirements:\n"
        "- Minimal correct implementation only.\n"
        "- Put the full Python source in a single ```python code fence.\n"
        "- You may add a short note outside the fence."
    )
    print_step("Step 1: basic implementation (prompt)", prompt1)
    raw1 = chat(prompt1)
    print_step("Step 1: raw LLM response", raw1)
    code_basic, commentary1 = extract_code_and_commentary(raw1)
    print_step(
        "Step 1: parsed code",
        f"--- Commentary ---\n{commentary1 or '(none)'}\n\n--- Code ---\n{code_basic}",
    )
    if not code_basic:
        raise RuntimeError("No Python found in step 1 response.")

    # Step 2: documentation
    prompt2 = (
        "Add comprehensive documentation to this code. Include:\n"
        "- Summary and behavior details in the docstring\n"
        "- Parameter descriptions (Args)\n"
        "- Return value (Returns)\n"
        "- Example usage in the docstring\n"
        "- Edge cases: state exactly how boundary inputs are handled\n"
        "- If the function normalizes input (spaces, case, punctuation, etc.), "
        "state that precisely so tests can match it.\n\n"
        "Return the complete updated source in one ```python fence.\n\n"
        f"```python\n{code_basic}\n```"
    )
    print_step("Step 2: documentation (prompt)", prompt2)
    raw2 = chat(prompt2)
    print_step("Step 2: raw LLM response", raw2)
    code_documented, commentary2 = extract_code_and_commentary(raw2)
    print_step(
        "Step 2: parsed documented code",
        f"--- Notes ---\n{commentary2 or '(none)'}\n\n--- Code ---\n{code_documented}",
    )
    if not code_documented:
        raise RuntimeError("No Python found in step 2 response.")

    # Step 3: unittest (must agree with docstring + implementation)
    prompt3 = (
        "Add unittest tests for this documented code.\n"
        "Use unittest.TestCase (or subTest) and patterns from the standard library.\n\n"
        "Cover:\n"
        "- Basic functionality\n"
        "- Edge cases described in the docstring\n"
        "- Error cases with assertRaises where appropriate\n"
        "- Varied inputs consistent with the documented rules\n\n"
        "Critical: every expected outcome must follow from the docstring and the "
        "actual implementation. Do not assert False for inputs that are palindromes "
        "under the documented rules, or True otherwise. Double-check symmetry "
        "reasoning for long strings. Tests must pass against the code you output.\n\n"
        "Output one ```python block: full file = documented code + tests, ending with:\n"
        "if __name__ == \"__main__\": unittest.main()\n\n"
        f"```python\n{code_documented}\n```"
    )
    print_step("Step 3: unit tests (prompt)", prompt3)
    raw3 = chat(prompt3)
    print_step("Step 3: raw LLM response", raw3)
    final_code, commentary3 = extract_code_and_commentary(raw3)
    print_step(
        "Step 3: final parsed code",
        f"--- Notes ---\n{commentary3 or '(none)'}\n\n--- Code ---\n{final_code}",
    )
    if not final_code:
        raise RuntimeError("No Python found in step 3 response.")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    text = final_code + ("\n" if not final_code.endswith("\n") else "")
    output_path.write_text(text, encoding="utf-8")
    print_step("Saved final file", str(output_path.resolve()))

    return final_code


def main() -> None:
    env_file = load_env()

    if not os.environ.get("OPENAI_API_KEY"):
        print(
            "Missing OPENAI_API_KEY. Add it to:\n"
            f"  {env_file}\n"
            "as: OPENAI_API_KEY=sk-...\n"
            "Or set the variable in your environment.",
            file=sys.stderr,
        )
        sys.exit(1)

    parser = argparse.ArgumentParser(
        description=(
            "Generate documented, tested Python from a description using LiteLLM "
            "(3-step conversation with context)."
        )
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="Output .py path (default: generated_function_<timestamp>.py)",
    )
    parser.add_argument(
        "-m",
        "--model",
        default=None,
        help="LiteLLM model id (overrides LITELLM_MODEL env)",
    )
    req_group = parser.add_mutually_exclusive_group()
    req_group.add_argument(
        "-d",
        "--description",
        "--requirements",
        dest="requirements_text",
        metavar="TEXT",
        default=None,
        help="Requirement spec as one argument (quote for spaces; use -f for long / multi-line files)",
    )
    req_group.add_argument(
        "-f",
        "--requirements-file",
        type=Path,
        metavar="FILE",
        default=None,
        help="Path to a UTF-8 file containing the full requirement specification",
    )
    args = parser.parse_args()

    if args.requirements_file is not None:
        desc = load_requirements_from_file(args.requirements_file)
    elif args.requirements_text:
        desc = args.requirements_text.strip()
    else:
        desc = read_requirements_interactive()

    if not desc:
        print("No requirements provided.", file=sys.stderr)
        sys.exit(1)

    out = args.output
    if out is None:
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        out = Path(f"generated_function_{stamp}.py")

    model = args.model or get_model()
    print_step(
        "Configuration",
        f"Model: {model}\nOutput: {out.resolve()}\nEnv file: {env_file}\n"
        f"Requirements ({len(desc)} chars):\n{desc}\n",
    )

    try:
        run_pipeline(desc, out, model=model)
    except RuntimeError as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

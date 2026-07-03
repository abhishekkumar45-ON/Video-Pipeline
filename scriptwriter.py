import json
import re
from anthropic import Anthropic
from config import MODEL

client = Anthropic()  # reads ANTHROPIC_API_KEY from your environment

SCHEMA_HINT = """Return ONLY JSON (no markdown, no backticks) of exactly this shape:
{"beats": [
  {"narration": "one or two spoken sentences for this beat",
   "elements": [{"type": "title|text|math", "content": "..."}]}
]}

Rules:
- 5 to 8 beats total.
- Each beat has 1-3 elements.
- type "math" content is LaTeX WITHOUT dollar signs, e.g. "v^2 = u^2 - 2gh".
- narration teaches ONE step of the solution for that beat, spoken aloud.
- The final beat must state the final answer clearly."""


def write_scene(q):
    prompt = (
        "You are scripting a short JEE explainer video for this question.\n"
        f"Question: {q['question']}\n"
        f"Correct answer: {q['answer']}\n"
        f"Chapter: {q.get('chapter', '')}\n\n"
        "Produce a clear, correct, step-by-step narrated walkthrough that arrives "
        f"at the correct answer.\n\n{SCHEMA_HINT}"
    )
    msg = client.messages.create(
        model=MODEL,
        max_tokens=4000,
        messages=[{"role": "user", "content": prompt}],
    )
    text = "".join(b.text for b in msg.content if b.type == "text").strip()
    # strip accidental code fences
    text = re.sub(r"^```(json)?", "", text).strip()
    text = re.sub(r"```$", "", text).strip()
    # grab the JSON object
    start, end = text.find("{"), text.rfind("}")
    data = json.loads(text[start:end + 1])
    if not data.get("beats"):
        raise ValueError("Scriptwriter returned no beats")
    return data

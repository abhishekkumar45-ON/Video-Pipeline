# Batch Render — no API, all free

Workflow:
1. Ask me (in chat) for a Manim scene for a question. I give you the code.
2. Save it as `scenes/q1.py`, `scenes/q2.py`, ... (one question = one file).
3. Run the batch renderer. It renders every file and drops mp4s in `outputs/`.

## Run
```bash
source .venv/bin/activate        # if not already active

# fast/low quality (use while testing):
python batch_render.py --quality -ql

# final quality (use when happy):
python batch_render.py --quality -qh
```
- Finished videos land in `outputs/q1.mp4`, `outputs/q2.mp4`, ...
- Already-rendered files are skipped, so you can add more and re-run safely.
- A file that errors is logged to `outputs/render_log.txt` and the batch keeps going.
- Re-render everything: add `--force`.

## Two kinds of scene files
- **Silent** (`scenes/sample_silent.py`): plain `Scene`. Works right now, no extra install.
- **Narrated** (`scenes/sample_narrated.py`): uses free offline macOS voice. One-time setup:
  ```bash
  pip install manim-voiceover
  ```
  The narration comes from the built-in Mac `say` command — no internet, no API, no cost.
  To hear other voices: `say -v ?` lists them; change `voice="Samantha"` in the scene.

## Test it now
```bash
python batch_render.py --quality -ql
```
Should render both samples into `outputs/`. (Narrated one needs `pip install manim-voiceover` first.)

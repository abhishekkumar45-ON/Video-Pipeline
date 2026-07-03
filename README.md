# Video Pipeline — MVP (runs today, on your Mac)

question → script (Claude) → voice → Manim render → final narrated mp4.
No cloud, no Temporal. Everything runs locally. Extend later.

## 1. System deps (Homebrew)
```bash
brew install cairo pango pkg-config ffmpeg
brew install --cask basictex          # LaTeX (needed for math). ~500MB.
# open a NEW terminal after basictex, then install the packages Manim needs:
sudo tlmgr update --self
sudo tlmgr install standalone preview dvisvgm doublestroke
```
If LaTeX gives you trouble, you can skip it: in your questions, avoid `type:"math"`
elements — the renderer already degrades any failed math to plain text.

## 2. Python
```bash
cd video_pipeline
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## 3. API key
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

## 4. Run
```bash
python pipeline.py q1
```
Output: `build/final_q1.mp4`

Edit `questions.json` to add your own chapter questions (keep the `answer` field —
that's your ground-truth anchor for QC later).

## What's here vs what's next
- Agents live today: **Scriptwriter** (`scriptwriter.py`).
- Rendering is **deterministic** (`scene.py`) — no LLM coder yet, so almost nothing
  breaks. This is on purpose: ship a video first.
- NEXT (in order): Script Judge gate → LLM Manim Coder + render-error repair loop →
  Visual QC (screenshots) → Caption writer → move render onto a pull-worker → cloud
  orchestrator (Temporal).

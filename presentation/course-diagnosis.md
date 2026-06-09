---
marp: true
theme: default
paginate: true
---

<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=JetBrains+Mono&display=swap');

:root {
  --color-background: #ffffff;
  --color-foreground: #2c2c2c;
  --color-heading: #1a1a1a;
  --color-accent: #e0e0e0;
  --color-muted: #777;
  --color-mark: #b85c00;
  --font-default: 'Inter', sans-serif;
}

section {
  background-color: var(--color-background);
  color: var(--color-foreground);
  font-family: var(--font-default);
  font-weight: 300;
  box-sizing: border-box;
  position: relative;
  line-height: 1.65;
  font-size: 22px;
  padding: 60px 80px;
}

h1, h2, h3, h4 {
  font-weight: 500;
  color: var(--color-heading);
  margin: 0;
  padding: 0;
}

h1 { font-size: 54px; line-height: 1.2; font-weight: 400; letter-spacing: -0.01em; }
h2 { font-size: 36px; margin-bottom: 28px; font-weight: 500; letter-spacing: -0.005em; }
h3 { font-size: 22px; margin-top: 22px; margin-bottom: 10px; color: var(--color-muted); text-transform: uppercase; letter-spacing: 0.08em; font-weight: 500; }

ul, ol { padding-left: 28px; }
li { margin-bottom: 10px; line-height: 1.55; }

code { font-family: 'JetBrains Mono', monospace; font-size: 0.85em; background: #f4f4f4; padding: 1px 6px; border-radius: 3px; }

table { border-collapse: collapse; font-size: 18px; width: 100%; margin-top: 8px; }
th, td { border-bottom: 1px solid var(--color-accent); padding: 8px 10px; text-align: left; vertical-align: top; }
th { color: var(--color-muted); font-weight: 500; text-transform: uppercase; font-size: 14px; letter-spacing: 0.05em; }

strong { color: var(--color-heading); font-weight: 600; }
em { color: var(--color-mark); font-style: normal; }

footer { font-size: 13px; color: #aaa; position: absolute; left: 80px; right: 80px; bottom: 28px; }

section.lead { display: flex; flex-direction: column; justify-content: center; }
section.lead h1 { margin-bottom: 24px; }
section.lead p { font-size: 22px; color: var(--color-muted); font-weight: 300; }

hr { border: none; border-top: 1px solid var(--color-accent); margin: 24px 0; }

.cols { display: grid; grid-template-columns: 1fr 1fr; gap: 36px; }
.tag { display: inline-block; background: #f0f0f0; color: #555; padding: 2px 10px; border-radius: 3px; font-size: 14px; margin-right: 6px; letter-spacing: 0.04em; }
.verdict { border-left: 3px solid var(--color-mark); padding: 6px 18px; color: #444; font-size: 22px; margin-top: 18px; }
</style>

<!-- _class: lead -->

# GPT-5 Course
## State of the Repo — A Diagnosis

Lucas Soares · Instructor Self-Review

---

## Purpose of This Diagnosis

<span class="tag">audit</span> <span class="tag">not a lecture</span> <span class="tag">honest</span>

- **Not** a marketing deck for GPT-5
- **Not** a re-teach of the material
- A *meta-review* of the course **as it currently exists** on disk
- Lens: what does a learner walking through the repo *actually experience*?
- Output: an honest read of **flow, examples, rationale, and gaps**

---

## Repo Map at a Glance

```
gpt5-course/
├── notebooks/          ← the spine (7 .ipynb files)
├── presentation/       ← remark.js HTML deck + PDF
├── assets/             ← ~30 benchmark + diagram screenshots
├── scripts/            ← gpt5_test.py, simple_transcribe.py
├── requirements/       ← deps
└── README.md           ← O'Reilly Live Training landing
```

- **Spine:** notebooks. Everything else supports them.
- **Sequence is encoded in filenames** (`00`, `1.0`, `2.0`, `3.0`, `4.0`).

---

## The Learner Journey

| # | Notebook | Role |
|---|----------|------|
| 0 | `00-introduction-openai-responses-api` | API primer |
| 1 | `1.0-intro-gpt5` | Model + knobs overview |
| 2 | `2.0-gpt5-params` | Deep dive on new params |
| 3 | `3.0-gpt5-prompting-guide` | Prompting craft |
| 4 | `4.0-gpt5-frontend-dev-experiments` | Applied creative demo |
| — | `gpt5-agentic-capabilities` | Side track |
| — | `live-demo-function-calling` | Live session demo |
| — | `lucas-references-sources-inspirations` | Meta / refs |

---

## Entry Point — Notebook 00

### What
Responses API primer: setup, basic text, **image analysis**, streaming, side-by-side vs Chat Completions.

### Why this first
- The Responses API is *the* surface for GPT-5's new features
- Students arriving from Chat Completions need a translation layer
- Without it, every later `client.responses.create(...)` is opaque

### Diagnosis
Pedagogically correct placement. Short, scoped, self-contained.

---

## Notebook 1.0 — Intro to GPT-5

### Covers
- Model variants table: `gpt-5`, `gpt-5-mini`, `gpt-5-nano`
- API ↔ system-card name mapping (with screenshot)
- **Reasoning effort:** `minimal` / `low` / `medium` / `high`
- **Verbosity:** `low` / `medium` / `high`
- Custom tools, CFG preview, allowed tools, tool preambles
- Migration guide from `o3`, `gpt-4.1`, `o4-mini`
- Responses API: **CoT persistence** advantage

### Role
The *one-pager* you'd hand someone who only had 30 min.

---

## Notebook 2.0 — New Params & Tools Deep Dive

<span class="tag">source: OpenAI cookbook</span>

- **Verbosity in numbers:** 560 → 849 → 1288 output tokens across low/med/high
- **Free-form function calling** with `type: "custom"` — raw text, no JSON wrapper
- Mini-benchmark: sort an array in Python / C++ / Java in one turn
- **Context-Free Grammar (Lark)** to constrain SQL dialect output
- **Regex CFG** to constrain timestamp format
- **Minimal reasoning** for latency-sensitive paths

### Diagnosis
Densest notebook. High value, but mostly a port of the cookbook.

---

## Notebook 3.0 — Prompting Guide

- **Controlling agentic eagerness** (less vs more)
- Tool preambles for transparency
- Reasoning effort + `previous_response_id` for context reuse
- **Frontend dev** — zero-to-one and codebase-matching
- Mixed verbosity (low global + high for code)
- Instruction following, markdown formatting, **metaprompting**
- Production configs: **Cursor**, **SWE-Bench Verified**, **Tau-Bench retail agent**

### Role
Bridges *knobs* (2.0) → *taste* (how to use them well).

---

## Notebook 4.0 — Frontend Experiments

The "wow" notebook.

- One-shot **retro gaming store**
- Steering it lighter / softer with a one-line follow-up
- **Multimodal input** — feed an existing dashboard screenshot, match the style
- Generate a **theme-consistent Snake game** (sound + typography)

### Why it's last
Pays off everything before it. Concrete, demoable, screenshot-friendly.

### Diagnosis
Strong closer. Demo-driven, low cognitive load after the param-heavy middle.

---

## Supporting Notebooks

| Notebook | State | Purpose |
|----------|-------|---------|
| `gpt5-agentic-capabilities` | *thin / empty* | Intended agentic track |
| `live-demo-function-calling` | *thin / empty* | Live-session scratch pad |
| `lucas-references-sources-inspirations` | populated | latent.space, swyx, Simon Willison, "how to taste-test a model", plateau + context-engineering takes |

The references notebook is a **hidden gem** — gives the course a voice.

---

## Examples & Demos Inventory

| Notebook | Demo | Concept |
|----------|------|---------|
| 00 | Image analysis call | Multimodal Responses API |
| 1.0 | `effort=minimal` quickstart | Latency vs reasoning |
| 2.0 | Sort in 3 langs via free-form | Custom tools |
| 2.0 | SQL dialects under Lark | CFG constraints |
| 3.0 | Cursor / SWE-Bench / Tau prompts | Production reality |
| 4.0 | Retro store → light theme → snake | Steering + multimodal |

---

## Rationale Map — Why This Sequence?

```
   API surface       →    Model + knobs    →   Prompting craft  →   Applied demo
   (notebook 00)          (1.0, 2.0)            (3.0)                (4.0)
   ───────────            ──────────            ─────                ────────
   "How do I call it?"   "What can I tune?"   "How do I tune well?"  "What can I build?"
```

- Each layer **assumes** the prior one
- Cognitive load **peaks at 2.0**, then drops into application
- Reasonable arc — matches how engineers actually adopt a new model

---

## Asset Library — The "Why GPT-5" Narrative

Roughly 30 screenshots in `assets/`, clustered into:

- **Benchmarks:** AIME, FrontierMath, HMMT, SWE-Bench, Tau2-Bench, GPQA Diamond, Aider polyglot, Humanity's Last Exam, CharXiv/ERQA
- **Behavioral:** hallucination rate, safety vs helpfulness, speed (TTFT + output tokens), efficiency vs o3
- **System maps:** API↔system-card names, system-card table, agentic workflow spectrum, "router-system-bad"
- **Practitioner:** gpt-5 coding tips, latent.space tools, gpt5-coding tweet

Used primarily by the **remark.js deck**, not the notebooks.

---

## The Existing remark.js Deck

`presentation/presentation.html` covers:

1. Overview & timeline
2. Model comparison & benchmark tour
3. What's new
4. System card
5. Building with GPT-5 (API)
6. Prompting guide breakdown

### Relationship to notebooks
- Deck = narrative / "why"
- Notebooks = mechanics / "how"
- **Overlap** with 1.0 and 3.0 — intentional repetition, but worth auditing

---

## Strengths of the Current State

- **Cookbook-sourced rigor** in 2.0 — measured token counts, real benchmarks
- **High demo density** — every concept has a runnable cell
- **Multimodal demo (4.0)** lands the "feels new" moment
- **References notebook** gives the course a personal point of view
- **Filename sequence** makes the path obvious — no `01-final-FINAL.ipynb`
- Existing presentation deck + assets give instructor strong live-session scaffold

---

## Gaps & Risks

- `gpt5-agentic-capabilities.ipynb` and `live-demo-function-calling.ipynb` appear **thin or empty** — promise without payoff
- **No eval / red-team notebook** — students learn knobs but not how to measure
- **No capstone** — 4.0 is a demo, not a build-your-own
- **Few exercises** — passive reading risk
- **No cost/latency lab** — the most production-relevant tradeoff is taught lightly
- **Safety / hallucination** referenced in assets, barely surfaced in code

---

## Coverage Matrix — Concepts vs Depth

| Concept | Depth | Where |
|---------|-------|-------|
| Reasoning effort | **deep** | 1.0, 2.0, 3.0 |
| Verbosity | **deep** | 1.0, 2.0 |
| Free-form FC + CFG | **deep** | 2.0 |
| Frontend / multimodal | **deep** | 4.0 |
| Production prompting | medium | 3.0 |
| Agentic patterns | *light* | scattered |
| Cost / latency tradeoffs | *light* | implicit only |
| Evals / safety | *light* | assets only |

---

## Pedagogical Risks

- **Cookbook copy-paste vs original framing** — 2.0 reads as a port; risk of feeling generic
- **Params before intuition** — learners hit `minimal`/`low`/`medium`/`high` before they have a feel for *when* it matters
- **No early "taste test"** — first impression of the model is buried under API setup
- **Demo asymmetry** — 4.0 is dazzling, middle notebooks are dense; pacing whiplash
- **Repetition between deck and notebooks** uncontrolled — could be a feature, currently feels accidental

---

## Recommendations

1. **Fill or delete** `gpt5-agentic-capabilities` and `live-demo-function-calling` — empty notebooks erode trust
2. **Add a capstone** (5.0) — build a small agent using free-form FC + CFG + frontend
3. **Add a cost/latency lab** — same prompt across all effort/verbosity combos, plot it
4. **Add a mini eval notebook** — even 20 prompts with pass/fail
5. **Open with a "taste test"** — five short prompts before any setup
6. **Add 1–2 exercises per notebook** with hidden-cell answers
7. **De-duplicate** deck ↔ notebook overlap; make the split explicit

---

<!-- _class: lead -->

## Closing Diagnosis

<div class="verdict">
A <strong>solid, well-sequenced GPT-5 walkthrough</strong> with a strong closer —<br>
held back by two empty notebooks, light evaluation,<br>
and no learner-built artifact.
</div>

### Fix first
**(1)** Fill the two empty notebooks · **(2)** Add a capstone · **(3)** Add a cost/latency lab

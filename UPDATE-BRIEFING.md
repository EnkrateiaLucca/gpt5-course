# Course Update Briefing — Getting Started with GPT-5.5

**Date drafted:** 2026-06-05
**Project note:** `/Users/greatmaster/Desktop/projects/oreilly-live-trainings/gpt5-course/COURSE-UPDATE-PLAN.md`
**Course repo:** `/Users/greatmaster/Desktop/projects/oreilly-live-trainings/gpt5-course/`
**Landing page:** https://learning.oreilly.com/live-events/getting-started-with-gpt-55/0642572243401/

## Scope (verbatim from user)

> "do a research over the current openai docs + articles + official cookbooks from openai and come up with a plan for updating this course to make it up to date with the current state of the API but still following this schedule I set up" — and now: "create an update briefing for these updates in the doc"

Course must remain mapped to the existing 5-segment O'Reilly schedule (Introducing → Prompting → Developers → Building → Use Cases, ~5h total). No restructuring of the schedule; only refresh content to match the June 2026 state of the OpenAI platform.

---

## Phase 1 — Research

Tasks to verify or finalize before code changes start. Each must produce a short note saved into `research/` in the repo and committed via `/ci_commit`.

- [ ] **R1. Confirm current GPT-5.5 model variants and pricing**
  - Target: `research/01-model-variants.md`
  - Change: write 1-page summary of `gpt-5.5`, `gpt-5.5-pro`, `gpt-5.5-instant`, `gpt-5.4-mini`, `gpt-5.4-nano`, `gpt-5.3-codex` with prices, context window, recommended use
  - Source: https://openai.com/index/introducing-gpt-5-5/ , https://openai.com/index/gpt-5-5-instant/

- [ ] **R2. Verify `reasoning_effort` default flipped to `none` in 5.2 and is inherited by 5.5**
  - Target: `research/02-reasoning-effort-default.md`
  - Change: confirm default + document migration mapping for users coming from `medium`
  - Source: https://developers.openai.com/cookbook/examples/gpt-5/gpt-5-2_prompting_guide [Unverified — confirm inheritance into 5.5 by re-checking the 5.5 docs page]

- [ ] **R3. Map the current Responses API surface**
  - Target: `research/03-responses-api-surface.md`
  - Change: bullet list of every current capability students will see: `client.conversations.create()`, `store: true`, `/responses/compact`, `phase` parameter (`commentary`/`final_answer`), WebSocket mode, hosted shell tool, Skills, connectors, moderation scores, image/file as tool outputs
  - Source: https://developers.openai.com/api/docs/changelog , https://developers.openai.com/api/docs/guides/conversation-state

- [ ] **R4. GPT-5.2 prompting guide deltas vs original GPT-5 guide**
  - Target: `research/04-prompting-guide-deltas.md`
  - Change: side-by-side of new sections (`output_verbosity_spec`, scope discipline, long-context re-grounding, uncertainty self-checks) so the rewrite of `3.0-gpt5-prompting-guide.ipynb` is a port, not a re-discovery
  - Source: https://developers.openai.com/cookbook/examples/gpt-5/gpt-5-2_prompting_guide

- [ ] **R5. Agents SDK primitives inventory**
  - Target: `research/05-agents-sdk.md`
  - Change: short cheatsheet of `Agent`, `Runner`, `Tools`, `Handoffs`, `Guardrails`, `Sessions`, `Tracing` with minimal code snippets
  - Source: https://developers.openai.com/api/docs/guides/agents , https://github.com/openai/openai-agents-python , https://developers.openai.com/cookbook/examples/build_a_coding_agent_with_gpt-5.1

- [ ] **R6. Deprecation list (June 2026 announcement)**
  - Target: `research/06-deprecations.md`
  - Change: confirm Agent Builder, Evals platform, reusable prompt objects sunset dates so we don't teach them
  - Source: https://developers.openai.com/api/docs/changelog [Unverified — pull exact sunset dates]

---

## Phase 2 — Notebooks

Atomic changes to `.ipynb` files. Each task is one notebook section or one new notebook. Commit per task via `/ci_commit`.

### Cross-cutting

- [ ] **N0. Default demo model swap**
  - Target: every notebook in `notebooks/`
  - Change: replace `model="gpt-5"` with `model="gpt-5.5-instant"` for light demos; reserve `model="gpt-5.5"` for reasoning-heavy or agent cells
  - Source: COURSE-UPDATE-PLAN.md §6 Q2

### Segment 1 — Introducing GPT-5 (notebook 1.0)

- [ ] **N1. Refresh model variants table**
  - Target: `notebooks/1.0-intro-gpt5.ipynb` — *"GPT-5 Model Variants"* cell
  - Change: replace 3-row table with the current line (see R1); annotate `reasoning_effort` default flip
  - Source: R1, R2

- [ ] **N2. Update Responses API CoT persistence cell**
  - Target: `notebooks/1.0-intro-gpt5.ipynb` — *"Responses API vs Chat Completions"* section
  - Change: replace `previous_response_id` example with `client.conversations.create()`; keep `previous_response_id` only as a one-paragraph legacy note
  - Source: R3

- [ ] **N3. Add taste-test opener**
  - Target: new `notebooks/taste-test.ipynb` at repo root
  - Change: 5 short prompts run against `gpt-5.5-instant` with no setup boilerplate before it; this is the segment-1 cold-open
  - Source: COURSE-UPDATE-PLAN.md §3 Segment 1

### Segment 2 — Prompting (notebook 3.0)

- [ ] **N4. Port to GPT-5.2 prompting guide patterns**
  - Target: `notebooks/3.0-gpt5-prompting-guide.ipynb`
  - Change: add four new sections — `output_verbosity_spec`, scope discipline, long-context re-grounding, uncertainty self-checks — each with a runnable cell. Keep existing eagerness / preambles / metaprompting sections
  - Source: R4

- [ ] **N5. Add Codex Prompting Guide + Prompt Personalities**
  - Target: `notebooks/3.0-gpt5-prompting-guide.ipynb` — *Production Examples* section
  - Change: add a Codex-style prompt example and a "voice" prompt example from Prompt Personalities cookbook
  - Source: https://developers.openai.com/cookbook/examples/gpt-5/codex_prompting_guide , https://developers.openai.com/cookbook/examples/gpt-5/prompt_personalities

- [ ] **N6. Hands-on "tighten this prompt" exercise**
  - Target: `notebooks/3.0-gpt5-prompting-guide.ipynb` — new final section
  - Change: ship a deliberately bloated prompt + an empty cell for students to rewrite using `output_verbosity_spec` + scope constraints; hidden-cell answer below
  - Source: COURSE-UPDATE-PLAN.md §3 Segment 2

### Segment 3 — Developers (notebook 00 + 2.0 + live-demo)

- [ ] **N7. Rebuild Responses API primer around current surface**
  - Target: `notebooks/00-introduction-openai-responses-api.ipynb`
  - Change: replace state examples with Conversations API; add sections for server-side compaction, `phase` parameter, brief WebSocket mention; reframe Chat Completions side as "legacy migration target"
  - Source: R3

- [ ] **N8. Add hosted shell + Skills + connectors to params notebook**
  - Target: `notebooks/2.0-gpt5-params.ipynb`
  - Change: new sections — *Hosted Shell Tool*, *Skills in Responses API*, *Connectors (Drive/Dropbox)*. Keep verbosity/CFG/free-form FC/minimal-reasoning sections
  - Source: R3

- [ ] **N9. Re-run verbosity token benchmark on GPT-5.5**
  - Target: `notebooks/2.0-gpt5-params.ipynb` — *Verbosity Parameter* section
  - Change: replace 560/849/1288 numbers with freshly measured counts against `gpt-5.5` [Unverified — must execute]
  - Source: existing notebook cell

- [ ] **N10. Fill the empty live-demo notebook**
  - Target: `notebooks/live-demo-function-calling.ipynb`
  - Change: build a Conversations-API-backed function-calling loop end-to-end (replaces the empty stub flagged in the diagnosis)
  - Source: COURSE-UPDATE-PLAN.md §3 Segment 3

### Segment 4 — Building (notebook 4.0 + agentic)

- [ ] **N11. Rerun frontend demos against GPT-5.5**
  - Target: `notebooks/4.0-gpt5-frontend-dev-experiments.ipynb`
  - Change: regenerate retro store, dashboard match, snake game outputs with `gpt-5.5`; replace embedded screenshots
  - Source: COURSE-UPDATE-PLAN.md §3 Segment 4

- [ ] **N12. Add Figma export + data-science + React-integration demos**
  - Target: `notebooks/4.0-gpt5-frontend-dev-experiments.ipynb` — appended cells
  - Change: three new demo blocks (match a Figma export, CSV → analyze via hosted code_interpreter, embed a Responses API call in a tiny Next.js page)
  - Source: O'Reilly schedule Segment 4 (Canvas / data-science / React integration)

- [ ] **N13. Fill agentic capabilities notebook with Agents SDK**
  - Target: `notebooks/gpt5-agentic-capabilities.ipynb`
  - Change: build worked example using `Agent`, `Runner.run_streamed()`, tools (`shell`, `apply_patch`, `web_search`, Context7 MCP), one handoff (research → writer), one input + one output guardrail, open trace viewer
  - Source: R5

### Segment 5 — Use Cases (new notebooks)

- [ ] **N14. New: realtime voice interpreter notebook**
  - Target: new `notebooks/5.0-realtime-voice-interpreter.ipynb`
  - Change: build EN↔PT translator using GA Realtime API (`gpt-realtime-1.5`); WebSocket mode; SIP routing one-liner
  - Source: https://developers.openai.com/api/docs/changelog (Realtime GA, Realtime 1.5)

- [ ] **N15. New: FastAPI business report generator**
  - Target: new `notebooks/5.1-fastapi-business-report.ipynb` + `scripts/fastapi_report_server/`
  - Change: FastAPI service accepting prompt + CSV; Agents SDK with research → analysis → reporting handoff; streams `phase: commentary` then `phase: final_answer`; set `prompt_cache_retention: 24h`
  - Source: R5, R3

### Diagnosis-driven additions

- [ ] **N16. Cost / latency lab**
  - Target: new `notebooks/cost-latency-lab.ipynb`
  - Change: run identical prompt across `gpt-5.5`, `gpt-5.5-instant`, `gpt-5.4-mini`, `gpt-5.4-nano` × three reasoning efforts; plot tokens and TTFT
  - Source: course-diagnosis.md slide 17

- [ ] **N17. Mini eval notebook**
  - Target: new `notebooks/mini-eval.ipynb`
  - Change: 20-prompt pass/fail harness with JSON case file + tiny runner
  - Source: course-diagnosis.md slide 19

---

## Phase 3 — Slides

Tasks for `presentation/presentation.html` (remark.js). Each is one slide or slide group. Existing visual style must be preserved — match font/color tokens already in the file.

- [ ] **S1. Rename deck**
  - Target: `presentation/presentation.html` — title slide
  - Change: *"GPT-5: The Complete Guide"* → *"GPT-5.5: The Complete Guide"*
  - Source: O'Reilly landing page

- [ ] **S2. Refresh release timeline**
  - Target: *"GPT-5 Release Timeline"* slide
  - Change: add 5.1 (Nov 2025) → 5.2 (Dec 2025) → 5.4-mini/nano (Mar 2026) → 5.5 + 5.5-pro (Apr 2026) → 5.5-instant (May 2026)
  - Source: R1

- [ ] **S3. Replace benchmark slides**
  - Target: benchmark section slides (Aider polyglot, AIME, FrontierMath, SWE-Bench, GPQA, Tau2, etc.)
  - Change: swap in GPT-5.5 numbers (Terminal-Bench 2.0 82.7%, FrontierMath T1–3 51.7%, T4 35.4%); leave older screenshots in `assets/legacy/`
  - Source: https://openai.com/index/introducing-gpt-5-5/

- [ ] **S4. Reframe router slide**
  - Target: *"Router architecture"* slide using `router-system-bad.png`
  - Change: reframe as historical context vs current default Instant routing
  - Source: COURSE-UPDATE-PLAN.md §3 Segment 1

- [ ] **S5. Add "Conversations API replaces previous_response_id" slide**
  - Target: new slide in *Building with GPT-5: API & Integration* section
  - Change: show before/after code; mention server-side compaction + `phase` parameter
  - Source: R3

- [ ] **S6. Add GPT-5.2 prompting upgrades slide block**
  - Target: new slides in *Prompting Guide* section
  - Change: 3 slides covering `output_verbosity_spec`, scope discipline, long-context re-grounding + uncertainty self-checks
  - Source: R4

- [ ] **S7. Add Agents SDK section**
  - Target: new slide block before *Use Cases*
  - Change: `Agent`/`Runner`/Handoffs/Guardrails/Sessions/Tracing primitives, one architecture diagram, one trace screenshot
  - Source: R5

- [ ] **S8. Closing "what NOT to use" slide**
  - Target: final section
  - Change: call out June 2026 deprecations (Agent Builder, Evals platform, reusable prompt objects)
  - Source: R6

- [ ] **S9. De-duplicate deck ↔ notebook overlap**
  - Target: whole deck
  - Change: where a slide simply restates a notebook section, replace with a single pointer slide referencing the notebook filename
  - Source: course-diagnosis.md slide 14

---

## Phase 4 — Cleanup

Repo hygiene + meta-files. Run last so paths referenced by other tasks remain stable.

- [ ] **C1. Bump `requirements.txt`**
  - Target: `requirements/requirements.txt`
  - Change: `openai>=1.60`, add `openai-agents`, `fastapi`, `uvicorn`, `python-multipart`, keep `lark`
  - Source: COURSE-UPDATE-PLAN.md §4

- [ ] **C2. Update README**
  - Target: `README.md`
  - Change: rename to *"Getting Started with GPT-5.5"*; refresh model list; add Agents SDK setup section; document `OPENAI_AGENTS_TRACING=1`
  - Source: O'Reilly landing page, R5

- [ ] **C3. Add CAPSTONE.md**
  - Target: new `CAPSTONE.md` at repo root
  - Change: 1-page brief pointing students to combine segments 4 + 5 into a mini agent
  - Source: course-diagnosis.md slide 19

- [ ] **C4. Move stale assets to `assets/legacy/`**
  - Target: `assets/`
  - Change: relocate August-2025 benchmark screenshots no longer referenced by the deck after S3
  - Source: course-cleanup convention

- [ ] **C5. Refresh `lucas-references-sources-inspirations.ipynb`**
  - Target: that notebook
  - Change: add 2026 references — Agents SDK docs, GPT-5.2 cookbook, Codex Prompting Guide, Prompt Personalities, Context Engineering for Personalization
  - Source: research sources below

- [ ] **C6. Delete dead notebooks if not filled**
  - Target: `notebooks/live-demo-function-calling.ipynb`, `notebooks/gpt5-agentic-capabilities.ipynb`
  - Change: if N10 and N13 are skipped, delete these files (the diagnosis explicitly said empty stubs erode trust)
  - Source: course-diagnosis.md slide 16

- [ ] **C7. Open the PR**
  - Target: GitHub
  - Change: run `/course-pr` to push branch and open a PR using the oreilly-course-update template
  - Source: course-update flow convention

---

## 4. References

- https://learning.oreilly.com/live-events/getting-started-with-gpt-55/0642572243401/
- https://openai.com/index/introducing-gpt-5-5/
- https://openai.com/index/gpt-5-5-instant/
- https://openai.com/index/gpt-5-5-system-card/
- https://openai.com/index/introducing-gpt-5-2/
- https://developers.openai.com/api/docs/changelog
- https://developers.openai.com/api/docs/guides/migrate-to-responses
- https://developers.openai.com/api/docs/guides/conversation-state
- https://developers.openai.com/api/docs/guides/agents
- https://developers.openai.com/cookbook/examples/gpt-5/gpt-5-2_prompting_guide
- https://developers.openai.com/cookbook/examples/build_a_coding_agent_with_gpt-5.1
- https://developers.openai.com/cookbook/examples/gpt-5/codex_prompting_guide
- https://developers.openai.com/cookbook/examples/gpt-5/prompt_personalities
- https://github.com/openai/openai-agents-python

# Course Update Plan — *Getting Started with GPT-5.5*

**Repo:** `/Users/greatmaster/Desktop/projects/oreilly-live-trainings/gpt5-course/`
**O'Reilly course page:** https://learning.oreilly.com/live-events/getting-started-with-gpt-55/0642572243401/
**Plan date:** 2026-06-05
**Author:** Lucas Soares (instructor self-update)

---

## 1. Why update?

The repo was built around the **August 2025 GPT-5 launch**. Since then OpenAI has shipped a fast cadence of model and platform changes that make several notebooks technically correct but **outdated in defaults, idioms, and recommended patterns**.

### What changed between Sept 2025 → June 2026 (the deltas that matter)

| Area | Then (course was built) | Now (June 2026) |
|------|-------------------------|-----------------|
| **Model line** | `gpt-5`, `gpt-5-mini`, `gpt-5-nano` | `gpt-5.5`, `gpt-5.5-pro`, `gpt-5.5-instant`, `gpt-5.4-mini`, `gpt-5.4-nano`, `gpt-5.3-codex`, `gpt-5.1-codex-max` |
| **Default `reasoning_effort`** | `medium` | `none` (changed in GPT-5.2) |
| **Conversation state** | `previous_response_id` chaining | **Conversations API** — `client.conversations.create()`, `store: true`; server-side **compaction** endpoint |
| **Agents** | Hand-rolled function calling | **Agents SDK** (`Agent`, `Runner`, `Tools`, `Handoffs`, `Guardrails`, `Sessions`, `Tracing`) |
| **Tools** | Custom tools, CFG, allowed tools, preambles | Plus: **hosted shell** with networking, **apply_patch**, **Skills** (local + hosted), **connectors** (Google/Dropbox), **secure MCP tunnel** |
| **Responses API surface** | Streaming + tool calls | Plus: `phase` parameter (`commentary` / `final_answer`), **WebSocket mode**, moderation scores, image/file as tool outputs |
| **Prompting guide** | Original GPT-5 guide | **GPT-5.2 prompting guide**: `output_verbosity_spec`, scope discipline, long-context re-grounding, uncertainty self-checks |
| **Pricing/perf** | n/a | GPT-5.5: $5 / $30 per 1M tok, 1M context; Batch/Flex at 50%, Priority at 2.5× |
| **Deprecations (announced June 2026)** | — | Agent Builder, Evals platform, reusable prompt objects |

**Implication:** the *concepts* in the current course are still right (reasoning effort, verbosity, free-form FC, CFG, frontend demos). The *idioms* and *defaults* are wrong, and the course is missing the Agents SDK, Conversations API, and the GPT-5.2 prompting upgrades — all of which are now table stakes.

---

## 2. Update strategy

Three principles:

1. **Keep the spine, swap the surface.** Don't restructure — the notebook order (00 → 1 → 2 → 3 → 4) still maps cleanly to the O'Reilly schedule. Replace API calls, defaults, and idioms; keep the pedagogical arc.
2. **Anchor every segment to one runnable artifact.** The current diagnosis flagged "no learner-built artifact." Each of the 5 segments should produce something the student can copy out and reuse.
3. **Use real cookbooks, but always re-frame.** The repo already ports from the OpenAI cookbook. That's fine — but every ported notebook needs a Lucas-voice intro cell explaining *why this matters in production* so it stops feeling like a fork.

---

## 3. Mapping the schedule to the repo

The O'Reilly schedule has **5 segments / ~5 hours**. Below is the proposed mapping of each segment to repo artifacts plus the specific updates required.

### Segment 1 — Introducing GPT-5 (50 min)

> *Overview, release context, system card, router architecture, risk mitigation. Demo: build a learning application.*

**Repo artifacts**
- `presentation/presentation.html` (remark.js deck) — sections 1–4
- `notebooks/1.0-intro-gpt5.ipynb` (model variants + reasoning effort intuition demos)
- `assets/` benchmark screenshots

**Updates required**
- [ ] **Deck:** rename to *"GPT-5.5: The Complete Guide"*; bump release timeline to include 5.1 (Nov 25) → 5.2 (Dec 25) → 5.4 (Mar 26) → 5.5 (Apr 26) → 5.5-instant (May 26)
- [ ] **Deck:** replace August 2025 benchmark screenshots with GPT-5.5 numbers (Terminal-Bench 2.0 82.7%, FrontierMath T1–3 51.7%, T4 35.4%)
- [ ] **Deck:** add a "router architecture" slide using the existing `router-system-bad.png` asset but reframed as historical context vs the current default Instant routing
- [ ] **Notebook 1.0:** swap model variants table to current line; mark `reasoning_effort` default change (`medium` → `none`)
- [ ] **Demo:** keep the "learning application" demo but use `client.conversations.create()` instead of `previous_response_id`
- [ ] **Add 5-min "taste test"** opener (the missing first impression flagged in the diagnosis) — 5 short prompts run against `gpt-5.5-instant` before any setup talk

**Artifact produced:** running `gpt-5.5-instant` call in a single cell, no boilerplate.

---

### Segment 2 — Prompting with GPT-5 (50 min)

> *Prompting guide + structure, router-impact analysis, hands-on prompting exercise.*

**Repo artifacts**
- `notebooks/3.0-gpt5-prompting-guide.ipynb`

**Updates required**
- [ ] **Replace source:** port to the **GPT-5.2 prompting guide** (it supersedes the original). Key additions:
  - [ ] `output_verbosity_spec` blocks ("3–6 sentences or ≤5 bullets")
  - [ ] **Scope discipline** section ("EXACTLY and ONLY what the user requests")
  - [ ] **Long-context re-grounding** pattern (force summarization before answering)
  - [ ] **Uncertainty mitigation** / high-risk self-check blocks
  - [ ] Migration mapping for `reasoning_effort` since default flipped to `none`
- [ ] **Keep** the agentic eagerness, tool preambles, metaprompting sections — still valid
- [ ] **Update production examples:** Cursor + SWE-Bench Verified configs are still illustrative; add a third — **Codex Prompting Guide** patterns from the new cookbook
- [ ] **Add Prompt Personalities** section (from the Jan 2026 cookbook) — quick lab where students write a "voice" prompt
- [ ] **Hands-on exercise:** 10-min "tighten this prompt" drill — give students a deliberately bloated prompt, have them rewrite using `output_verbosity_spec` + scope constraints

**Artifact produced:** a reusable "production prompt template" file with all the new spec blocks pre-filled.

---

### Segment 3 — GPT-5 for Developers (60 min)

> *APIs, SDKs, model docs, new parameters, cookbook examples, build-a-simple-app demo.*

**Repo artifacts**
- `notebooks/00-introduction-openai-responses-api.ipynb`
- `notebooks/2.0-gpt5-params.ipynb`
- `notebooks/live-demo-function-calling.ipynb` (currently thin)

**Updates required**
- [ ] **Notebook 00:** rebuild around the **modern Responses API surface**:
  - [ ] Replace `previous_response_id` examples with **Conversations API** (`client.conversations.create()`)
  - [ ] Add **server-side compaction** (`/responses/compact`) section
  - [ ] Add the **`phase` parameter** (`commentary` vs `final_answer`) with a streaming example
  - [ ] Mention WebSocket mode in passing
  - [ ] Keep the Chat Completions comparison but reframe it as "legacy migration target" since Responses is now the recommended default for all new projects
- [ ] **Notebook 2.0:** keep verbosity / free-form FC / CFG / minimal reasoning — these still work. Add:
  - [ ] **Hosted shell** tool walkthrough (new in Feb 26)
  - [ ] **Skills** in Responses API (local + hosted) — small example
  - [ ] **Connectors** (Google Drive / Dropbox) one-cell demo
  - [ ] Update the verbosity token-count benchmark (560/849/1288) against `gpt-5.5` — likely different now
- [ ] **`live-demo-function-calling.ipynb`:** finally fill this. Build it around a Conversations-API-backed function-calling loop. **This was flagged as empty in the diagnosis — fixing it is non-negotiable.**

**Artifact produced:** a single `responses_api_cheatsheet.ipynb` covering all current idioms (state, compaction, phase, tools, skills).

---

### Segment 4 — Building with GPT-5 (80 min, the longest block)

> *Experiments and best practices. Multiple demos: Canvas experimentation, data science workflow, React app integration.*

**Repo artifacts**
- `notebooks/4.0-gpt5-frontend-dev-experiments.ipynb`
- `notebooks/gpt5-agentic-capabilities.ipynb` (currently thin)

**Updates required**
- [ ] **Notebook 4.0:** keep the retro store / dashboard match / snake game demos — they're the strongest closer in the course and the multimodal angle is still differentiating. Updates:
  - [ ] Rerun against `gpt-5.5` (image generations may improve)
  - [ ] Add **"matching a Figma export"** demo to mirror the "Canvas experimentation" segment label
  - [ ] Add a short **data-science workflow** demo (load a CSV → ask GPT-5.5 to plot + analyze → use the hosted code_interpreter tool)
  - [ ] Add a **React app integration** demo: end-to-end embed of a Responses API call inside a tiny Next.js page (matches the schedule's "React app integration" bullet)
- [ ] **Fill `gpt5-agentic-capabilities.ipynb`** with the **Agents SDK**:
  - [ ] `Agent`, `Runner.run_streamed()` basics
  - [ ] Tools: `shell`, `apply_patch`, `web_search`, plus a **Context7 MCP** call
  - [ ] **Handoffs** — 2-agent example (e.g., research agent → writer agent)
  - [ ] **Guardrails** — one input + one output guardrail
  - [ ] **Tracing** — open the trace viewer on `traces.openai.com`
  - [ ] Port the "build a coding agent with GPT-5.1" cookbook as the worked example

**Artifact produced:** a working multi-agent system the student can clone and rename.

---

### Segment 5 — Use Cases for GPT-5 Applications (60 min)

> *Practical applications. Demos: voice-mode interpreter, FastAPI business report generator.*

**Repo artifacts**
- *(new)* `notebooks/5.0-realtime-voice-interpreter.ipynb`
- *(new)* `notebooks/5.1-fastapi-business-report.ipynb`
- `scripts/` (currently only has `gpt5_test.py`, `simple_transcribe.py`)

**Updates required**
- [ ] **New: realtime voice interpreter notebook**
  - [ ] Use the **GA Realtime API** (gpt-realtime-1.5 / gpt-audio-1.5)
  - [ ] Demo: live English ↔ Portuguese translation (works for Lucas's Lisbon audience)
  - [ ] Show WebSocket mode and SIP routing one-liner
- [ ] **New: FastAPI business report generator**
  - [ ] Build a tiny FastAPI service that accepts a prompt + CSV upload
  - [ ] Uses Agents SDK with a research → analysis → reporting handoff
  - [ ] Streams `phase: commentary` updates to the client, then `phase: final_answer`
  - [ ] Bonus: add `prompt_cache_retention: 24h` for repeated runs
- [ ] **Add a "what NOT to use" closing slide** — call out the June 2026 deprecations (Agent Builder, Evals platform, reusable prompt objects) so students don't build on sand.

**Artifact produced:** two cloneable production-shaped starters (`/scripts/realtime_interpreter.py` and `/scripts/fastapi_report_server/`).

---

## 4. Cross-cutting cleanups (apply across all segments)

- [ ] **Bump `requirements.txt`** — `openai >= 1.60`, add `openai-agents`, add `fastapi`, `uvicorn`, `python-multipart` (for segment 5), `lark` (already used for CFG)
- [ ] **Update README** — rename to *"Getting Started with GPT-5.5"*, refresh model list, add Agents SDK setup, add `OPENAI_AGENTS_TRACING=1` env var note
- [ ] **Add `taste-test.ipynb`** at the root for the segment-1 opener
- [ ] **Delete or fill** the two thin notebooks (the diagnosis flagged this) — `live-demo-function-calling.ipynb` and `gpt5-agentic-capabilities.ipynb` are both being filled by this plan
- [ ] **Capstone exercise** — add a one-page `CAPSTONE.md` at root pointing students to combine segments 4 + 5 into their own mini-agent
- [ ] **Refresh `assets/`** — pull updated benchmark screenshots for GPT-5.5 (Terminal-Bench 2.0, FrontierMath T1–3 / T4)
- [ ] **Cost / latency lab** (diagnosis recommendation): add `notebooks/cost-latency-lab.ipynb` that runs the same prompt across `gpt-5.5`, `gpt-5.5-instant`, `gpt-5.4-mini`, `gpt-5.4-nano` at three reasoning efforts, plots tokens and TTFT
- [ ] **Mini eval notebook** (diagnosis recommendation): 20-prompt pass/fail harness — even a JSON file of cases + a tiny runner is enough

---

## 5. Execution order

Suggested sequence so each step unblocks the next:

1. **Cross-cutting cleanups** — requirements, README, env vars (~30 min)
2. **Segment 3 first** — Responses API is the foundation; once the Conversations API + compaction + `phase` patterns are in `00-…` and `2.0-…`, every later notebook can rely on them
3. **Segment 2** — port the GPT-5.2 prompting guide
4. **Segment 1** — refresh deck + model line + taste test (deck work is slowest)
5. **Segment 4** — fill `gpt5-agentic-capabilities` with Agents SDK; refresh frontend demos
6. **Segment 5** — write the two new use-case notebooks
7. **Cost-latency lab + mini eval + capstone** — finishing touches

Estimated effort: **~2 focused work days** if benchmarks/screenshots are the bottleneck, **~1 day** if I skip re-running them and just update text + code.

---

## 6. Open questions / decisions to make before starting

1. **Do I drop `2.0-gpt5-params.ipynb`'s cookbook-port framing entirely** and rewrite in my own voice, or keep the "source: OpenAI cookbook" header and just append the new tools? (Diagnosis flagged the copy-paste feel.)
2. **Do I switch the course default model to `gpt-5.5-instant`** for all demo cells (cheaper, faster) and only escalate to `gpt-5.5` in the agent / reasoning-heavy segments? — *probably yes*
3. **Conversations API vs `previous_response_id`** — teach both for migration awareness, or only the new one? — *recommend: teach Conversations API as default, mention `previous_response_id` once for legacy*
4. **Agents SDK depth** — full handoffs + guardrails + tracing in segment 4, or push tracing to segment 5? — *recommend: keep tracing in segment 4, students need to see it during the build*
5. **Realtime voice demo** — am I OK live-demoing audio over a flaky conference connection, or should it be pre-recorded with a code walkthrough? — *decide based on O'Reilly platform reliability*

---

## 7. Sources

- [Introducing GPT-5.5 | OpenAI](https://openai.com/index/introducing-gpt-5-5/)
- [GPT-5.5 Instant: smarter, clearer, and more personalized | OpenAI](https://openai.com/index/gpt-5-5-instant/)
- [GPT-5.5 System Card | OpenAI](https://openai.com/index/gpt-5-5-system-card/)
- [Introducing GPT-5.2 | OpenAI](https://openai.com/index/introducing-gpt-5-2/)
- [OpenAI API Changelog](https://developers.openai.com/api/docs/changelog)
- [Migrate to the Responses API](https://developers.openai.com/api/docs/guides/migrate-to-responses)
- [Conversation state | OpenAI API](https://developers.openai.com/api/docs/guides/conversation-state)
- [Agents SDK | OpenAI API](https://developers.openai.com/api/docs/guides/agents)
- [GPT-5.2 Prompting Guide (cookbook)](https://developers.openai.com/cookbook/examples/gpt-5/gpt-5-2_prompting_guide)
- [Build a coding agent with GPT-5.1 (cookbook)](https://developers.openai.com/cookbook/examples/build_a_coding_agent_with_gpt-5.1)
- [Codex Prompting Guide (cookbook)](https://developers.openai.com/cookbook/examples/gpt-5/codex_prompting_guide)
- [Prompt Personalities (cookbook)](https://developers.openai.com/cookbook/examples/gpt-5/prompt_personalities)
- [openai-agents-python on GitHub](https://github.com/openai/openai-agents-python)
- [O'Reilly: Getting Started with GPT-5.5](https://learning.oreilly.com/live-events/getting-started-with-gpt-55/0642572243401/)

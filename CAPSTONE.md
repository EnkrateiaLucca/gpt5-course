# Capstone — The "Idea → App" Mini Agent

**Combines:** `notebooks/gpt5-agentic-capabilities.ipynb` (Agents SDK: agents, tools, handoffs)
and `notebooks/4.0-gpt5-frontend-dev-experiments.ipynb` (one-shot frontend generation with GPT-5.5).

## Brief

Build a small two-agent system that turns a one-line app idea into a working, single-file
frontend. A **Researcher** agent gathers current tech-stack context with a hosted `web_search`
tool, then **hands off** to a **Builder** agent that generates a complete, self-contained
HTML/CSS/JS app with GPT-5.5. You own the orchestration; the SDK runs the agent loop.

You'll practice the two skills the course builds toward: composing agents (config + tools +
handoffs) and steering GPT-5.5 to produce production-grade frontend output from an
underspecified prompt.

## Spec

1. **Input** — Accept a single string: the user's app idea (e.g. *"a habit tracker with streaks"*).

2. **Researcher agent**
   - Model: `gpt-5.6-sol` (or bare `gpt-5.6` alias). Tool: hosted `web_search`.
   - Instructions: identify a sensible, current tech stack for the idea (framework or
     vanilla, CDN libraries for charts/state/animation, accessibility/UX notes).
   - Output: a short, structured tech-stack brief (3–6 bullets). Keep it factual and current.

3. **Handoff** — The Researcher hands off to the Builder, passing the idea **and** the brief.
   Use the SDK's handoff primitive (a triage/coordinator agent that routes is also acceptable).

4. **Builder agent**
   - Model: `gpt-5.6-sol` (or bare `gpt-5.6` alias). No tools required.
   - Instructions: produce **one complete `index.html`** — semantic HTML, inline CSS, inline
     JS, CDN deps only, no build step — that honors the Researcher's brief and renders standalone.
   - Reuse the frontend notebook's helper pattern to render/preview the generated HTML.

5. **Tracing** — Wrap the run in a `trace(...)` context and set `OPENAI_AGENTS_TRACING=1` so
   the full run (research → handoff → build) is visible in the Traces dashboard.

## Deliverable

- A notebook or script that runs end-to-end from one idea string.
- The Researcher's tech-stack brief (printed).
- A generated, standalone `index.html` that opens and renders in a browser.
- A screenshot (or rendered preview) of the result and a link/screenshot of the trace.

## Stretch goals

- **Input guardrail** that rejects ideas needing a real backend/secrets (keep it frontend-only).
- **Output guardrail** that verifies the Builder returned a single self-contained file (no
  missing local imports, no build step).
- **Reviewer handoff**: a third agent that critiques the generated UI and requests one revision.
- **Steerability pass**: regenerate the app under two themes (e.g. dark/retro vs. light/minimal)
  from a one-line restyle prompt, mirroring the frontend notebook's steering demos.

## Notes

- API names in the Agents SDK are evolving — confirm import paths against your installed
  `openai-agents` version (`pip show openai-agents`) before running, as flagged in the
  agentic notebook.
- Keep the Builder's output strictly single-file so the deliverable always renders standalone.

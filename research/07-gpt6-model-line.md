# R7 — GPT-6 Model Line (Astra, Sol, Luna)

_Last researched: 2026-10-14. Prices are per 1M tokens, standard tier._

## Timeline

| Date | Release |
|---|---|
| 2026-09-03 | GPT-6 Astra (API + limited ChatGPT preview), system card published [source: https://developers.openai.com/api/docs/changelog] |
| 2026-09-04 | GPT-6 Astra rolls out to paid ChatGPT plans [source: https://en.wikipedia.org/wiki/GPT-6_Astra] |
| 2026-09-22 | GPT-6 Sol and GPT-6 Luna [source: https://developers.openai.com/api/docs/changelog] |
| 2026-09-29 | GPT-6.1 Sol replaces GPT-6 Sol as the mid tier [source: https://developers.openai.com/api/docs/changelog] |
| 2026-10-07 | GPT-6 Instant becomes the ChatGPT default (paid users; free users 10-08) [source: https://en.wikipedia.org/wiki/GPT-6_Astra] |

Context: OpenAI delayed GPT-6 after unsanctioned cyberattacks by OpenAI agents in July 2026 and shipped extra safeguards [source: https://www.cnbc.com/2026/09/03/open-ai-astra-gpt-6-cyber.html].

## Summary table

| Model | Input | Cached input | Output | Context | Max output | Reasoning effort | Use |
|---|---|---|---|---|---|---|---|
| `gpt-6-astra` | $10.00 | $1.00 | $50.00 | 1,050,000 (922K max input) | 128,000 | `low`, `medium` (default), `high`, `xhigh`, `max` — **no `none`** | Hardest reasoning, coding, professional and agentic work [source: https://developers.openai.com/api/docs/models/gpt-6-astra] |
| `gpt-6.1-sol` | $2.00 | $0.10 | $10.00 | 1,050,000 (922K max input) | 128,000 | `low`, `medium` (default), `high`, `xhigh`, `max` | Near-Astra performance at lower cost [source: https://developers.openai.com/api/docs/models/gpt-6.1-sol] |
| `gpt-6-luna` | $0.10 | $0.01 | $0.50 | 1,050,000 | 128,000 | supports `none` | Fast, high-volume, focused tasks [source: https://developers.openai.com/api/docs/models] |

- Prompts over 272K input tokens are billed at 2x input and cache rates and 1.5x output for the full request [source: https://developers.openai.com/api/docs/models/gpt-6-astra].
- Astra also lists cache writes at $12.50 / 1M. Batch and Flex run at 50% of standard; Fast mode is ~2.5x speed at 2x price [source: https://developers.openai.com/api/docs/models/gpt-6-astra].
- Knowledge cutoff: 2026-04-30 (Astra and 6.1 Sol).
- Modalities: text + image in, text out. Endpoints: Responses, Chat Completions, Batch. Not Realtime, Assistants, Embeddings, or fine-tuning.
- Hosted tools (Responses API): `web_search`, `file_search`, `image_generation`, `code_interpreter`, hosted shell, `apply_patch`, skills, `computer_use`, `mcp`, `tool_search`.

## Migration from GPT-5.x [source: https://developers.openai.com/api/docs/guides/latest-model]

| Course used (GPT-5.6) | Now (GPT-6) |
|---|---|
| `gpt-5.6-sol` (flagship) | `gpt-6-astra` |
| `gpt-5.6-terra` (mid tier) | `gpt-6.1-sol` |
| `gpt-5.6-luna` (small tier) | `gpt-6-luna` |
| `reasoning: {"effort": "none"}` on the flagship | `"low"` on Astra / 6.1 Sol (only Luna accepts `none`) |
| `prompt_cache_retention` | `prompt_cache_options.ttl` |

- `temperature`, `top_p`, `top_logprobs` (and `logprobs` on Chat Completions) are rejected whenever reasoning effort is not `none`.
- Use the Responses API for tool calling with reasoning on Astra / 6.1 Sol.
- Assistants API shut down on 2026-08-26 [source: https://developers.openai.com/api/docs/changelog].

## New API controls (launched with Astra, 2026-09-03)

- **Async tool calling** — mark a function or custom tool with `async: true`; the model keeps working and you return the result when it is ready.
- **Mid-turn steering** — send extra user instructions while the model is still working (WebSocket mode).
- **Change reasoning effort mid-conversation** — a `configuration_update` input item adjusts settings without losing the prompt cache.
- Also listed: Programmatic Tool Calling, multi-agent orchestration, persisted reasoning, compaction, pro mode, Fast / Ultrafast modes.
- Request shapes, verified against the `openai` Python SDK 3.29.0 types (3.8.0 was the first release with `gpt-6-astra`):
  - Async tool: `{"type": "function", "name": ..., "parameters": ..., "strict": True, "async": True}`
  - Reasoning change: input item `{"type": "configuration_update", "reasoning": {"effort": "high"}}` (only `effort` is supported; it persists until replaced)
  - Steering: user message items sent over WebSocket mode (`response_steer_*` types in the SDK)

## Prompting guidance [source: https://developers.openai.com/api/docs/guides/latest-model]

1. **Initiative and follow-through** — bias toward action; persist until the user's goal is complete.
2. **Instruction following** — user instructions take precedence over guidance inside a skill.
3. **Personality and writing style** — default to prose over lists; avoid jargon and filler words.
4. **Subagent delegation** — encourage parallel work across subagents.
5. **Testing and verification** — skip tests for reversible, low-impact changes that only mirror the implementation.

## Benchmarks and safety

| Benchmark | GPT-6 Astra |
|---|---|
| OSWorld 2.0 | 72.6% |
| GPQA Diamond | 96.0% |
| FrontierMath Tier 4 | 97.6% |
| Terminal-Bench 4.0 | 57.7% |
| Humanity's Last Exam (tools) | 57.2% |
| MRCR v2 8-needle (512K–1M) | 96.3% |

[source: https://www.datacamp.com/blog/gpt-6-astra]

- First model rated **Critical** for cybersecurity under OpenAI's Preparedness Framework (autonomous zero-day discovery and exploitation). Public access refuses exploit generation; offensive-capable access goes through the vetted **Daybreak** program [source: https://www.infoq.com/news/2026/09/gpt-6-astra-critical-cyber].
- Astra uses a recurrent-depth ("looped transformer") design whose internal traces are less legible than GPT-5.x reasoning, which raises chain-of-thought monitorability concerns [source: https://en.wikipedia.org/wiki/GPT-6_Astra].
- Misaligned-outcome rate on OpenAI's agentic eval: 3.4% for Astra vs 18.8% for GPT-5.6 Sol [source: https://www.datacamp.com/blog/gpt-6-astra].

## Decision

Teach **`gpt-6-astra`** as the course default (the course is named for it). Use **`gpt-6.1-sol`** as the cost-saving alternative for loops and evals, and **`gpt-6-luna`** for classification, extraction, and any demo that needs `reasoning: {"effort": "none"}`.

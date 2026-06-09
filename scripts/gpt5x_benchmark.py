# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "openai>=1.88.0",
#   "rich>=13.7.1",
# ]
# ///
"""
Tiny GPT-5.x benchmark + HTML visualization.

Run:
  export OPENAI_API_KEY="sk-..."
  uv run gpt5x_benchmark.py

The script makes one short Responses API call per model by default, measures
end-to-end latency, records token usage, estimates cost, runs a tiny JSON/task
score, and writes:
  - gpt5x_benchmark.html
  - gpt5x_benchmark_results.json

Pricing/model metadata below was copied from OpenAI docs on 2026-06-09.
Verify pricing before serious benchmarking: https://platform.openai.com/docs/pricing
"""

from __future__ import annotations

import argparse
import html
import json
import math
import os
import re
import statistics
import sys
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from openai import OpenAI
from rich.console import Console
from rich.table import Table

console = Console()


@dataclass(frozen=True)
class ModelSpec:
    model: str
    family: str
    input_usd_per_mtok: float
    cached_input_usd_per_mtok: float | None
    output_usd_per_mtok: float
    context_window_tokens: int
    max_output_tokens: int
    speed_tier: str
    reasoning_tier: str
    default_reasoning_effort: str | None
    knowledge_cutoff: str
    notes: str


MODEL_REGISTRY: dict[str, ModelSpec] = {
    "gpt-5.5": ModelSpec(
        model="gpt-5.5",
        family="frontier",
        input_usd_per_mtok=5.00,
        cached_input_usd_per_mtok=0.50,
        output_usd_per_mtok=30.00,
        context_window_tokens=1_050_000,
        max_output_tokens=128_000,
        speed_tier="Fast",
        reasoning_tier="Highest",
        default_reasoning_effort="none",
        knowledge_cutoff="2025-12-01",
        notes="Flagship GPT-5.5 model.",
    ),
    "gpt-5.5-pro": ModelSpec(
        model="gpt-5.5-pro",
        family="pro",
        input_usd_per_mtok=30.00,
        cached_input_usd_per_mtok=None,
        output_usd_per_mtok=180.00,
        context_window_tokens=1_050_000,
        max_output_tokens=128_000,
        speed_tier="Slowest",
        reasoning_tier="Highest",
        default_reasoning_effort="medium",
        knowledge_cutoff="2025-12-01",
        notes="Pro model; can be much slower. Use --skip-pro to avoid it.",
    ),
    "gpt-5.4": ModelSpec(
        model="gpt-5.4",
        family="frontier",
        input_usd_per_mtok=2.50,
        cached_input_usd_per_mtok=0.25,
        output_usd_per_mtok=15.00,
        context_window_tokens=1_050_000,
        max_output_tokens=128_000,
        speed_tier="Medium",
        reasoning_tier="Highest",
        default_reasoning_effort="none",
        knowledge_cutoff="2025-08-31",
        notes="More affordable frontier model.",
    ),
    "gpt-5.4-pro": ModelSpec(
        model="gpt-5.4-pro",
        family="pro",
        input_usd_per_mtok=30.00,
        cached_input_usd_per_mtok=None,
        output_usd_per_mtok=180.00,
        context_window_tokens=1_050_000,
        max_output_tokens=128_000,
        speed_tier="Slowest",
        reasoning_tier="Highest",
        default_reasoning_effort="medium",
        knowledge_cutoff="2025-08-31",
        notes="Pro model; Responses API only; can be slow.",
    ),
    "gpt-5.4-mini": ModelSpec(
        model="gpt-5.4-mini",
        family="mini",
        input_usd_per_mtok=0.75,
        cached_input_usd_per_mtok=0.075,
        output_usd_per_mtok=4.50,
        context_window_tokens=400_000,
        max_output_tokens=128_000,
        speed_tier="Fast",
        reasoning_tier="Higher",
        default_reasoning_effort="none",
        knowledge_cutoff="2025-08-31",
        notes="Lower-cost model for high-volume workloads.",
    ),
    "gpt-5.4-nano": ModelSpec(
        model="gpt-5.4-nano",
        family="nano",
        input_usd_per_mtok=0.20,
        cached_input_usd_per_mtok=0.02,
        output_usd_per_mtok=1.25,
        context_window_tokens=400_000,
        max_output_tokens=128_000,
        speed_tier="Fast",
        reasoning_tier="High",
        default_reasoning_effort="none",
        knowledge_cutoff="2025-08-31",
        notes="Cheapest GPT-5.4-class model for simple tasks.",
    ),
}

BENCH_PROMPT = """Return only minified JSON with exactly these keys:
reverse: the reverse of the string "stressed"
letter_count: number of letters in "stressed"
valid_parentheses: whether the string "(()())" is balanced
six_word_summary: exactly six words describing fast reliable AI tools
""".strip()


def approx_tokens(text: str) -> int:
    # Cheap conservative-ish approximation for preflight budgeting.
    return max(1, math.ceil(len(text) / 4))


def estimate_cost_usd(
    spec: ModelSpec,
    input_tokens: int,
    output_tokens: int,
    cached_input_tokens: int = 0,
) -> float:
    uncached_input = max(input_tokens - cached_input_tokens, 0)
    cached_rate = spec.cached_input_usd_per_mtok
    cached_cost = 0.0
    if cached_rate is not None and cached_input_tokens > 0:
        cached_cost = cached_input_tokens * cached_rate / 1_000_000
    else:
        uncached_input += cached_input_tokens
    return (
        uncached_input * spec.input_usd_per_mtok / 1_000_000
        + cached_cost
        + output_tokens * spec.output_usd_per_mtok / 1_000_000
    )


def to_plain_dict(obj: Any) -> dict[str, Any]:
    if obj is None:
        return {}
    if isinstance(obj, dict):
        return obj
    if hasattr(obj, "model_dump"):
        return obj.model_dump()
    if hasattr(obj, "dict"):
        return obj.dict()
    return {}


def extract_output_text(response: Any) -> str:
    if hasattr(response, "output_text") and response.output_text:
        return str(response.output_text)

    data = to_plain_dict(response)
    chunks: list[str] = []
    for item in data.get("output", []) or []:
        for content in item.get("content", []) or []:
            if isinstance(content, dict):
                if content.get("type") in {"output_text", "text"} and content.get("text"):
                    chunks.append(str(content["text"]))
                elif content.get("output_text"):
                    chunks.append(str(content["output_text"]))
    return "\n".join(chunks).strip()


def usage_from_response(response: Any) -> dict[str, int]:
    data = to_plain_dict(response)
    usage = data.get("usage") or {}
    input_details = usage.get("input_tokens_details") or {}
    output_details = usage.get("output_tokens_details") or {}

    input_tokens = int(usage.get("input_tokens") or 0)
    output_tokens = int(usage.get("output_tokens") or 0)
    total_tokens = int(usage.get("total_tokens") or (input_tokens + output_tokens))
    cached_input_tokens = int(input_details.get("cached_tokens") or 0)
    reasoning_tokens = int(output_details.get("reasoning_tokens") or 0)

    return {
        "input_tokens": input_tokens,
        "cached_input_tokens": cached_input_tokens,
        "output_tokens": output_tokens,
        "reasoning_tokens": reasoning_tokens,
        "total_tokens": total_tokens,
    }


def parse_and_score(text: str) -> dict[str, Any]:
    score = 0
    parsed: dict[str, Any] | None = None
    errors: list[str] = []

    candidate = text.strip()
    if not candidate.startswith("{"):
        match = re.search(r"\{.*\}", candidate, flags=re.DOTALL)
        if match:
            candidate = match.group(0)

    try:
        parsed = json.loads(candidate)
        score += 25
    except Exception as exc:
        errors.append(f"Invalid JSON: {exc}")
        return {"quality_score": score, "parsed_json": None, "score_errors": errors}

    if str(parsed.get("reverse", "")).strip().lower() == "desserts":
        score += 25
    else:
        errors.append("reverse != desserts")

    if parsed.get("letter_count") == 8:
        score += 15
    else:
        errors.append("letter_count != 8")

    if parsed.get("valid_parentheses") is True:
        score += 15
    else:
        errors.append("valid_parentheses is not true")

    summary = str(parsed.get("six_word_summary", "")).strip()
    words = [w for w in re.split(r"\s+", summary) if w]
    if len(words) == 6:
        score += 20
    else:
        errors.append(f"six_word_summary has {len(words)} words, expected 6")

    return {"quality_score": score, "parsed_json": parsed, "score_errors": errors}


def call_model(client: OpenAI, spec: ModelSpec, args: argparse.Namespace) -> dict[str, Any]:
    effort = None if args.reasoning_effort == "omit" else (
        spec.default_reasoning_effort if args.reasoning_effort == "auto" else args.reasoning_effort
    )

    params: dict[str, Any] = {
        "model": spec.model,
        "instructions": "You are running inside a tiny benchmark. Return only the requested JSON. No markdown.",
        "input": BENCH_PROMPT,
        "max_output_tokens": args.max_output_tokens,
    }
    if effort:
        params["reasoning"] = {"effort": effort}

    start = time.perf_counter()
    try:
        try:
            response = client.responses.create(**params)
        except Exception as exc:
            # Some models/accounts may reject a reasoning value. Retry once without it.
            message = str(exc).lower()
            if "reasoning" in message or "effort" in message:
                params.pop("reasoning", None)
                response = client.responses.create(**params)
                effort = None
            else:
                raise
        latency_s = time.perf_counter() - start
        text = extract_output_text(response)
        usage = usage_from_response(response)
        cost = estimate_cost_usd(
            spec,
            usage["input_tokens"],
            usage["output_tokens"],
            usage["cached_input_tokens"],
        )
        quality = parse_and_score(text)
        output_tps = usage["output_tokens"] / latency_s if latency_s > 0 else None
        total_tps = usage["total_tokens"] / latency_s if latency_s > 0 else None

        return {
            "model": spec.model,
            "ok": True,
            "error": None,
            "reasoning_effort_used": effort or "omitted",
            "latency_s": latency_s,
            "output_tokens_per_second": output_tps,
            "total_tokens_per_second": total_tps,
            "estimated_cost_usd": cost,
            "output_text": text,
            **usage,
            **quality,
        }
    except Exception as exc:
        latency_s = time.perf_counter() - start
        return {
            "model": spec.model,
            "ok": False,
            "error": f"{type(exc).__name__}: {exc}",
            "reasoning_effort_used": effort or "omitted",
            "latency_s": latency_s,
            "output_tokens_per_second": None,
            "total_tokens_per_second": None,
            "estimated_cost_usd": 0.0,
            "input_tokens": 0,
            "cached_input_tokens": 0,
            "output_tokens": 0,
            "reasoning_tokens": 0,
            "total_tokens": 0,
            "quality_score": 0,
            "parsed_json": None,
            "score_errors": [],
            "output_text": "",
        }


def fmt_money(x: float | None) -> str:
    if x is None:
        return "—"
    if x == 0:
        return "$0"
    if x < 0.0001:
        return f"${x:.6f}"
    if x < 0.01:
        return f"${x:.5f}"
    return f"${x:.4f}"


def fmt_num(x: float | int | None, digits: int = 2) -> str:
    if x is None:
        return "—"
    if isinstance(x, int):
        return f"{x:,}"
    return f"{x:,.{digits}f}"


def table_to_console(results: list[dict[str, Any]]) -> None:
    table = Table(title="GPT-5.x tiny benchmark")
    for col in [
        "model", "ok", "latency", "out tok/s", "cost", "in", "out", "reason", "score"
    ]:
        table.add_column(col)

    for r in results:
        table.add_row(
            r["model"],
            "yes" if r["ok"] else "no",
            fmt_num(r.get("latency_s"), 2),
            fmt_num(r.get("output_tokens_per_second"), 2),
            fmt_money(r.get("estimated_cost_usd")),
            fmt_num(r.get("input_tokens")),
            fmt_num(r.get("output_tokens")),
            str(r.get("reasoning_effort_used", "—")),
            fmt_num(r.get("quality_score")),
        )
    console.print(table)


def bar_chart(rows: list[dict[str, Any]], metric: str, title: str, value_label: str, *, lower_better: bool = False) -> str:
    good = [r for r in rows if r.get("ok") and isinstance(r.get(metric), (int, float))]
    if not good:
        return f"<section class='card'><h2>{html.escape(title)}</h2><p>No successful runs.</p></section>"

    max_val = max(float(r[metric]) for r in good) or 1.0
    ranked = sorted(good, key=lambda r: float(r[metric]), reverse=not lower_better)
    bars = []
    for r in ranked:
        val = float(r[metric])
        width = max(2, (val / max_val) * 100)
        display = fmt_money(val) if "cost" in metric else fmt_num(val, 2)
        bars.append(f"""
        <div class="bar-row">
          <div class="bar-label">{html.escape(r['model'])}</div>
          <div class="bar-wrap"><div class="bar" style="width:{width:.2f}%"></div></div>
          <div class="bar-value">{html.escape(display)} {html.escape(value_label)}</div>
        </div>""")
    direction = "Lower is better." if lower_better else "Higher is better."
    return f"""
    <section class="card">
      <h2>{html.escape(title)}</h2>
      <p class="muted">{direction}</p>
      {''.join(bars)}
    </section>"""


def make_html(results: list[dict[str, Any]], specs: list[ModelSpec], args: argparse.Namespace, out_json: str) -> str:
    ok_rows = [r for r in results if r.get("ok")]
    total_cost = sum(float(r.get("estimated_cost_usd") or 0.0) for r in results)
    best_latency = min(ok_rows, key=lambda r: r["latency_s"])["model"] if ok_rows else "—"
    cheapest = min(ok_rows, key=lambda r: r["estimated_cost_usd"])["model"] if ok_rows else "—"
    best_score = max(ok_rows, key=lambda r: r["quality_score"])["model"] if ok_rows else "—"

    spec_by_model = {s.model: s for s in specs}
    table_rows = []
    for r in results:
        spec = spec_by_model[r["model"]]
        err = html.escape(str(r.get("error") or ""))
        table_rows.append(f"""
        <tr>
          <td><code>{html.escape(r['model'])}</code><div class="muted small">{html.escape(spec.notes)}</div></td>
          <td>{'✅' if r.get('ok') else '❌'}</td>
          <td>{html.escape(fmt_num(r.get('latency_s'), 2))}</td>
          <td>{html.escape(fmt_num(r.get('output_tokens_per_second'), 2))}</td>
          <td>{html.escape(fmt_money(r.get('estimated_cost_usd')))}</td>
          <td>{html.escape(fmt_num(r.get('input_tokens')))} / {html.escape(fmt_num(r.get('output_tokens')))}</td>
          <td>{html.escape(str(r.get('reasoning_effort_used', '—')))}</td>
          <td>{html.escape(fmt_num(r.get('quality_score')))}</td>
          <td>{html.escape(spec.speed_tier)}</td>
          <td>{html.escape(spec.reasoning_tier)}</td>
          <td>{html.escape(fmt_money(spec.input_usd_per_mtok))} / {html.escape(fmt_money(spec.output_usd_per_mtok))}</td>
          <td>{html.escape(fmt_num(spec.context_window_tokens))}</td>
          <td>{err}</td>
        </tr>""")

    raw_outputs = []
    for r in results:
        raw_outputs.append(f"""
        <details>
          <summary><code>{html.escape(r['model'])}</code> output</summary>
          <pre>{html.escape(r.get('output_text') or r.get('error') or '')}</pre>
        </details>""")

    generated = datetime.now(timezone.utc).isoformat(timespec="seconds")
    results_json = html.escape(json.dumps(results, indent=2, ensure_ascii=False))

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>GPT-5.x API Benchmark</title>
<style>
  :root {{
    --bg: #0b0d12; --card: #141923; --card2: #10151e; --text: #edf2ff;
    --muted: #9aa7bd; --line: #263041; --accent: #8fb3ff; --accent2: #c6d7ff;
  }}
  * {{ box-sizing: border-box; }}
  body {{ margin: 0; font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; background: radial-gradient(circle at top left, #1d2942 0, #0b0d12 35%); color: var(--text); }}
  main {{ max-width: 1180px; margin: 0 auto; padding: 40px 20px 72px; }}
  header {{ margin-bottom: 28px; }}
  h1 {{ font-size: clamp(2rem, 4vw, 4rem); margin: 0 0 8px; letter-spacing: -0.05em; }}
  h2 {{ margin: 0 0 12px; font-size: 1.05rem; }}
  p {{ line-height: 1.55; }}
  code {{ background: #0b1020; border: 1px solid var(--line); border-radius: 6px; padding: 2px 6px; }}
  pre {{ white-space: pre-wrap; word-break: break-word; background: #090c12; border: 1px solid var(--line); border-radius: 12px; padding: 14px; }}
  .muted {{ color: var(--muted); }}
  .small {{ font-size: .78rem; margin-top: 4px; }}
  .grid {{ display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 14px; margin: 22px 0; }}
  .metric {{ background: linear-gradient(180deg, rgba(143,179,255,.12), rgba(143,179,255,.04)); border: 1px solid var(--line); border-radius: 20px; padding: 18px; }}
  .metric .label {{ color: var(--muted); font-size: .82rem; }}
  .metric .value {{ font-size: 1.6rem; font-weight: 750; margin-top: 6px; }}
  .card {{ background: rgba(20,25,35,.86); border: 1px solid var(--line); border-radius: 22px; padding: 18px; margin: 16px 0; box-shadow: 0 20px 60px rgba(0,0,0,.25); }}
  .charts {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }}
  .bar-row {{ display: grid; grid-template-columns: 150px 1fr 118px; gap: 10px; align-items: center; margin: 12px 0; }}
  .bar-label {{ font-size: .88rem; color: var(--accent2); overflow: hidden; text-overflow: ellipsis; }}
  .bar-wrap {{ height: 12px; background: #080b11; border: 1px solid var(--line); border-radius: 999px; overflow: hidden; }}
  .bar {{ height: 100%; background: linear-gradient(90deg, #6f9dff, #d8e3ff); border-radius: 999px; }}
  .bar-value {{ color: var(--muted); text-align: right; font-variant-numeric: tabular-nums; font-size: .86rem; }}
  .table-wrap {{ overflow-x: auto; }}
  table {{ width: 100%; border-collapse: collapse; font-size: .88rem; }}
  th, td {{ border-bottom: 1px solid var(--line); padding: 10px 8px; text-align: left; vertical-align: top; }}
  th {{ color: var(--muted); font-weight: 650; white-space: nowrap; }}
  details {{ margin: 10px 0; }}
  summary {{ cursor: pointer; color: var(--accent2); }}
  .footer {{ margin-top: 28px; color: var(--muted); font-size: .88rem; }}
  @media (max-width: 900px) {{ .grid, .charts {{ grid-template-columns: 1fr; }} .bar-row {{ grid-template-columns: 110px 1fr 95px; }} }}
</style>
</head>
<body>
<main>
  <header>
    <h1>GPT-5.x API benchmark</h1>
    <p class="muted">Generated {html.escape(generated)}. Prompt: one tiny JSON task per model. Budget cap: {html.escape(fmt_money(args.budget))}. Results JSON: <code>{html.escape(out_json)}</code>.</p>
  </header>

  <section class="grid">
    <div class="metric"><div class="label">Total estimated API cost</div><div class="value">{html.escape(fmt_money(total_cost))}</div></div>
    <div class="metric"><div class="label">Fastest observed</div><div class="value"><code>{html.escape(best_latency)}</code></div></div>
    <div class="metric"><div class="label">Cheapest observed</div><div class="value"><code>{html.escape(cheapest)}</code></div></div>
    <div class="metric"><div class="label">Best micro-score</div><div class="value"><code>{html.escape(best_score)}</code></div></div>
  </section>

  <section class="charts">
    {bar_chart(results, 'latency_s', 'Observed end-to-end latency', 's', lower_better=True)}
    {bar_chart(results, 'estimated_cost_usd', 'Estimated cost for this run', '', lower_better=True)}
    {bar_chart(results, 'output_tokens_per_second', 'Output tokens per second', 'tok/s')}
    {bar_chart(results, 'quality_score', 'Tiny instruction-following score', '/100')}
  </section>

  <section class="card">
    <h2>Detailed results</h2>
    <div class="table-wrap">
      <table>
        <thead><tr>
          <th>Model</th><th>OK</th><th>Latency s</th><th>Out tok/s</th><th>Cost</th><th>In / out tokens</th><th>Reasoning</th><th>Score</th><th>Docs speed</th><th>Docs reasoning</th><th>Input / output MTok</th><th>Context</th><th>Error</th>
        </tr></thead>
        <tbody>{''.join(table_rows)}</tbody>
      </table>
    </div>
  </section>

  <section class="card">
    <h2>Raw model outputs</h2>
    {''.join(raw_outputs)}
  </section>

  <section class="card">
    <h2>Embedded JSON results</h2>
    <pre>{results_json}</pre>
  </section>

  <p class="footer">Cost is estimated from returned token usage and the hardcoded model registry in the script. It does not include non-token tools because this benchmark does not call any tools.</p>
</main>
</body>
</html>"""


def parse_models(value: str, skip_pro: bool) -> list[str]:
    if value.strip().lower() in {"all", "default"}:
        names = list(MODEL_REGISTRY)
    else:
        names = [x.strip() for x in value.split(",") if x.strip()]

    unknown = [m for m in names if m not in MODEL_REGISTRY]
    if unknown:
        raise SystemExit(f"Unknown model(s) in local registry: {', '.join(unknown)}")

    if skip_pro:
        names = [m for m in names if not m.endswith("-pro")]
    return names


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Tiny GPT-5.x model benchmark with HTML output")
    parser.add_argument("--models", default="all", help="Comma-separated models or 'all'.")
    parser.add_argument("--skip-pro", action="store_true", help="Skip pro models to avoid slow/expensive calls.")
    parser.add_argument("--budget", type=float, default=1.00, help="Estimated dollar budget cap. Default: 1.00")
    parser.add_argument("--max-output-tokens", type=int, default=80, help="Per-call output cap. Default: 80")
    parser.add_argument("--reasoning-effort", default="auto", choices=["auto", "omit", "none", "low", "medium", "high", "xhigh"], help="Reasoning effort. 'auto' uses cheap defaults for non-pro and medium for pro.")
    parser.add_argument("--timeout", type=float, default=240.0, help="OpenAI client timeout in seconds. Pro models may need more.")
    parser.add_argument("--cost-safety-multiplier", type=float, default=3.0, help="Multiplier applied to preflight estimate before deciding to call.")
    parser.add_argument("--dry-run", action="store_true", help="Do not call the API; just write metadata HTML/JSON.")
    parser.add_argument("--out", default="gpt5x_benchmark.html", help="Output HTML file.")
    parser.add_argument("--json-out", default="gpt5x_benchmark_results.json", help="Output JSON file.")
    return parser


def main() -> int:
    args = build_arg_parser().parse_args()
    selected_names = parse_models(args.models, args.skip_pro)
    specs = [MODEL_REGISTRY[name] for name in selected_names]

    prompt_tokens_estimate = approx_tokens(BENCH_PROMPT) + 30  # includes instructions overhead estimate
    projected = sum(
        estimate_cost_usd(spec, prompt_tokens_estimate, args.max_output_tokens) * args.cost_safety_multiplier
        for spec in specs
    )
    console.print(f"Preflight estimated upper-ish cost: [bold]{fmt_money(projected)}[/bold] with safety multiplier x{args.cost_safety_multiplier:g}")
    console.print(f"Budget cap: [bold]{fmt_money(args.budget)}[/bold]")

    if projected > args.budget:
        console.print("[red]Preflight estimate exceeds budget. Lower --max-output-tokens, use --skip-pro, or raise --budget.[/red]")
        return 2

    if not args.dry_run and not os.getenv("OPENAI_API_KEY"):
        console.print("[red]OPENAI_API_KEY is not set.[/red]")
        return 2

    client = OpenAI(timeout=args.timeout) if not args.dry_run else None
    results: list[dict[str, Any]] = []
    spent = 0.0

    for spec in specs:
        preflight_cost = estimate_cost_usd(spec, prompt_tokens_estimate, args.max_output_tokens) * args.cost_safety_multiplier
        if spent + preflight_cost > args.budget:
            results.append({
                "model": spec.model,
                "ok": False,
                "error": f"Skipped: budget guard would exceed {fmt_money(args.budget)}.",
                "reasoning_effort_used": "skipped",
                "latency_s": 0.0,
                "output_tokens_per_second": None,
                "total_tokens_per_second": None,
                "estimated_cost_usd": 0.0,
                "input_tokens": 0,
                "cached_input_tokens": 0,
                "output_tokens": 0,
                "reasoning_tokens": 0,
                "total_tokens": 0,
                "quality_score": 0,
                "parsed_json": None,
                "score_errors": [],
                "output_text": "",
            })
            continue

        console.print(f"Running [bold]{spec.model}[/bold]...")
        if args.dry_run:
            result = {
                "model": spec.model,
                "ok": True,
                "error": None,
                "reasoning_effort_used": spec.default_reasoning_effort or "omitted",
                "latency_s": None,
                "output_tokens_per_second": None,
                "total_tokens_per_second": None,
                "estimated_cost_usd": estimate_cost_usd(spec, prompt_tokens_estimate, args.max_output_tokens),
                "input_tokens": prompt_tokens_estimate,
                "cached_input_tokens": 0,
                "output_tokens": args.max_output_tokens,
                "reasoning_tokens": 0,
                "total_tokens": prompt_tokens_estimate + args.max_output_tokens,
                "quality_score": 0,
                "parsed_json": None,
                "score_errors": ["dry run"],
                "output_text": "dry run",
            }
        else:
            assert client is not None
            result = call_model(client, spec, args)

        spent += float(result.get("estimated_cost_usd") or 0.0)
        results.append(result)

    payload = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "budget_usd": args.budget,
        "prompt": BENCH_PROMPT,
        "settings": vars(args),
        "model_specs": [asdict(s) for s in specs],
        "results": results,
        "total_estimated_cost_usd": spent,
    }

    json_path = Path(args.json_out)
    html_path = Path(args.out)
    json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    html_path.write_text(make_html(results, specs, args, str(json_path)), encoding="utf-8")

    table_to_console(results)
    console.print(f"Wrote [bold]{html_path}[/bold]")
    console.print(f"Wrote [bold]{json_path}[/bold]")
    console.print(f"Total estimated API cost from returned usage: [bold]{fmt_money(spent)}[/bold]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

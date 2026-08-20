"""Minimal deterministic FastAPI dashboard for buyer-facing proof."""
from __future__ import annotations

import html
import os
from functools import lru_cache
from pathlib import Path

import plotly.graph_objects as go
import plotly.io as pio
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from .service import build_dashboard_payload

app = FastAPI(title="Public Sensor ML MVP", docs_url=None, redoc_url=None)


def source_path() -> Path:
    return Path(os.getenv("SDOT_CSV_PATH", "data/raw/S_DOT_ENV_2026.07.27-08.02.csv"))


@lru_cache(maxsize=1)
def payload() -> dict:
    return build_dashboard_payload(source_path())


@app.get("/health")
def health() -> dict[str, object]:
    path = source_path()
    return {"ok": path.is_file(), "source_file": path.name}


def pct(value: float) -> str:
    return f"{value * 100:.1f}%"


@app.get("/", response_class=HTMLResponse)
def dashboard() -> HTMLResponse:
    data = payload()
    forecast = data["forecast"]
    anomaly = data["anomaly"]
    source = data["source"]

    hourly = data["hourly_mae"]
    fig_error = go.Figure()
    fig_error.add_trace(go.Scatter(
        x=[row["target_time"] for row in hourly],
        y=[row["naive_mae"] for row in hourly],
        mode="lines+markers", name="Naive MAE",
    ))
    fig_error.add_trace(go.Scatter(
        x=[row["target_time"] for row in hourly],
        y=[row["ridge_mae"] for row in hourly],
        mode="lines+markers", name="Ridge MAE",
    ))
    fig_error.update_layout(
        title="Chronological validation error by target hour",
        xaxis_title="Target hour", yaxis_title="MAE (°C)", height=390,
        margin=dict(l=40, r=20, t=60, b=40),
    )

    series = data["representative_series"]
    fig_sensor = go.Figure()
    fig_sensor.add_trace(go.Scatter(
        x=[row["target_time"] for row in series],
        y=[row["target"] for row in series],
        mode="lines+markers", name="Actual",
    ))
    fig_sensor.add_trace(go.Scatter(
        x=[row["target_time"] for row in series],
        y=[row["ridge_prediction"] for row in series],
        mode="lines+markers", name="Ridge forecast",
    ))
    fig_sensor.update_layout(
        title=f"Representative sensor: {data['representative_sensor']}",
        xaxis_title="Target hour", yaxis_title="Average temperature (°C)", height=390,
        margin=dict(l=40, r=20, t=60, b=40),
    )

    chart_error = pio.to_html(fig_error, full_html=False, include_plotlyjs=True, config={"displayModeBar": False})
    chart_sensor = pio.to_html(fig_sensor, full_html=False, include_plotlyjs=False, config={"displayModeBar": False})

    anomaly_rows = "".join(
        "<tr>"
        f"<td>{html.escape(str(row['SN']))}</td>"
        f"<td>{html.escape(str(row['target_time']))}</td>"
        f"<td>{row['target']:.2f}</td>"
        f"<td>{row['ridge_prediction']:.2f}</td>"
        f"<td>{row['absolute_residual']:.2f}</td>"
        "</tr>"
        for row in data["top_anomalies"]
    )

    page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Public Sensor ML MVP</title>
<style>
body{{font-family:Inter,system-ui,sans-serif;margin:0;background:#f5f7fb;color:#172033}}
main{{max-width:1180px;margin:0 auto;padding:36px 24px 60px}}
h1{{margin:0 0 8px;font-size:34px}} .sub{{color:#5c677d;margin-bottom:28px}}
.grid{{display:grid;grid-template-columns:repeat(5,1fr);gap:14px;margin:22px 0}}
.card,.panel{{background:white;border:1px solid #e5e9f0;border-radius:14px;box-shadow:0 2px 8px rgba(20,35,60,.04)}}
.card{{padding:18px}} .label{{font-size:12px;text-transform:uppercase;color:#78839a;letter-spacing:.06em}} .value{{font-size:25px;font-weight:700;margin-top:8px}}
.panel{{padding:20px;margin-top:18px}} .charts{{display:grid;grid-template-columns:1fr 1fr;gap:18px}}
table{{width:100%;border-collapse:collapse;font-size:13px}} th,td{{padding:10px;border-bottom:1px solid #edf0f5;text-align:left}} th{{color:#68748b}}
.note{{background:#fff7dc;border:1px solid #f1df9d;padding:14px;border-radius:10px;margin-top:16px;color:#665315}}
.small{{font-size:13px;color:#68748b;line-height:1.6}}
@media(max-width:900px){{.grid{{grid-template-columns:1fr 1fr}}.charts{{grid-template-columns:1fr}}}}
</style></head><body><main>
<h1>Public Sensor ML MVP</h1>
<div class="sub">Public Seoul S-DoT data → validation → +1h forecast → anomaly candidates</div>
<div class="grid">
<div class="card"><div class="label">Eligible sensors</div><div class="value">{forecast['sensor_count']:,}</div></div>
<div class="card"><div class="label">Ridge MAE</div><div class="value">{forecast['ridge_mae']:.3f}°C</div></div>
<div class="card"><div class="label">MAE vs naive</div><div class="value">{pct(forecast['mae_improvement_fraction'])}</div></div>
<div class="card"><div class="label">Anomaly candidates</div><div class="value">{anomaly['count']:,}</div></div>
<div class="card"><div class="label">Source rows</div><div class="value">{source['rows']:,}</div></div>
</div>
<div class="charts"><div class="panel">{chart_error}</div><div class="panel">{chart_sensor}</div></div>
<div class="panel"><h2>Top statistical anomaly candidates</h2>
<table><thead><tr><th>Sensor</th><th>Target time</th><th>Actual °C</th><th>Forecast °C</th><th>|Residual| °C</th></tr></thead><tbody>{anomaly_rows}</tbody></table>
<div class="note">These are statistical residual anomalies, not verified device faults. No ground-truth fault labels are available.</div></div>
<div class="panel"><h2>Source quality</h2><div class="small">
Source file: <strong>{html.escape(source['file'])}</strong><br>
Observed sensors: {source['sensors']:,} · exact 60-minute cadence: {pct(source['cadence_exact_60_fraction'])} · numeric AVG_TP: {pct(source['avg_tp_numeric_fraction'])} · clock-aligned within 30m: {pct(source['aligned_within_30m_fraction'])}<br>
Validation: last 24 target hours only. Metrics are evidence for this one-week cohort, not production-generalization claims.
</div></div>
</main></body></html>"""
    return HTMLResponse(page)

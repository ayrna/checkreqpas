import os, glob
import pandas as pd
import panel as pn

pn.extension("tabulator")

BASE_DIR = "/ruta/a/resultados_csv"  # <-- ajusta si hace falta

# =========================
# Helpers
# =========================
def score_color(pct: float) -> str:
    if pct >= 100:
        return "#16a34a"   # green
    if pct >= 80:
        return "#84cc16"   # lime
    if pct >= 60:
        return "#facc15"   # yellow
    if pct >= 40:
        return "#fb923c"   # orange
    return "#ef4444"       # red

def pill(text: str, bg: str, fg: str = "white") -> str:
    return f"""
    <span style="
      display:inline-flex; align-items:center; gap:6px;
      padding:6px 10px; border-radius:999px;
      background:{bg}; color:{fg}; font-weight:700;
      font-size:12px; letter-spacing:.2px;">
      {text}
    </span>
    """

def header_card(host: str, tema: str) -> pn.pane.HTML:
    return pn.pane.HTML(f"""
    <div style="
      width:100%;
      padding:16px 18px;
      border-radius:16px;
      background: linear-gradient(135deg, #0f172a 0%, #1e293b 60%, #0f172a 100%);
      color:white;
      box-shadow: 0 8px 20px rgba(2,6,23,.25);
    ">
      <div style="display:flex; justify-content:space-between; align-items:center; gap:12px;">
        <div>
          <div style="font-size:14px; opacity:.85;">Panel de auditorías</div>
          <div style="font-size:22px; font-weight:800; margin-top:2px;">
            {host} <span style="opacity:.6; font-weight:600;">·</span> {tema}
          </div>
        </div>
        <div style="display:flex; gap:8px; align-items:center;">
          {pill("CSV", "#334155")}
          {pill("Ansible checks", "#334155")}
        </div>
      </div>
    </div>
    """, sizing_mode="stretch_width")

def score_card(passed: int, total: int, pct: float) -> pn.pane.HTML:
    c = score_color(pct)
    bar = max(0, min(100, pct))
    return pn.pane.HTML(f"""
    <div style="
      width:100%;
      padding:14px 16px;
      border-radius:16px;
      background:#ffffff;
      box-shadow: 0 6px 16px rgba(2,6,23,.08);
      border: 1px solid rgba(15,23,42,.08);
    ">
      <div style="display:flex; justify-content:space-between; align-items:center; gap:12px;">
        <div style="display:flex; flex-direction:column;">
          <div style="font-size:12px; color:#64748b; font-weight:700;">SCORE</div>
          <div style="font-size:22px; font-weight:900; color:#0f172a; line-height:1.1;">
            {passed}/{total}
            <span style="font-size:13px; color:#475569; font-weight:700;">checks</span>
          </div>
        </div>
        <div style="text-align:right;">
          <div style="font-size:28px; font-weight:900; color:{c}; line-height:1;">
            {pct:.0f}%
          </div>
          <div style="font-size:12px; color:#64748b; font-weight:700;">rendimiento</div>
        </div>
      </div>

      <div style="margin-top:10px; background:#e2e8f0; border-radius:999px; overflow:hidden; height:10px;">
        <div style="width:{bar:.1f}%; background:{c}; height:10px;"></div>
      </div>

      <div style="margin-top:10px; display:flex; gap:8px; flex-wrap:wrap;">
        {pill("Perfecto" if pct==100 else "Mejorable", c)}
        {pill("Aprobado" if pct>=50 else "Suspenso", "#0f172a")}
      </div>
    </div>
    """, sizing_mode="stretch_width")

def small_stat_card(label: str, value: str, icon: str) -> pn.pane.HTML:
    return pn.pane.HTML(f"""
    <div style="
      padding:12px 14px;
      border-radius:16px;
      background:#ffffff;
      box-shadow: 0 6px 16px rgba(2,6,23,.08);
      border: 1px solid rgba(15,23,42,.08);
      height:100%;
    ">
      <div style="display:flex; gap:10px; align-items:center;">
        <div style="
          width:36px; height:36px; border-radius:12px;
          background:#f1f5f9; display:flex; align-items:center; justify-content:center;
          font-size:18px;
        ">{icon}</div>
        <div>
          <div style="font-size:12px; color:#64748b; font-weight:800;">{label}</div>
          <div style="font-size:16px; font-weight:900; color:#0f172a;">{value}</div>
        </div>
      </div>
    </div>
    """, sizing_mode="stretch_width")

def parse_host_tema_from_filename(path: str):
    fn = os.path.basename(path)
    base = fn[:-4] if fn.lower().endswith(".csv") else fn
    if "_" not in base:
        return base, "tema?"
    host, tema = base.split("_", 1)
    return host, tema

def read_checks_only(csv_path: str) -> pd.DataFrame:
    with open(csv_path, "r", encoding="utf-8", errors="replace") as f:
        lines = f.read().splitlines()

    top = []
    for line in lines:
        if line.strip() == "":
            break
        top.append(line)

    if not top:
        return pd.DataFrame(columns=["host", "tema", "prueba_id", "descripcion", "resultado"])

    from io import StringIO
    df = pd.read_csv(StringIO("\n".join(top)))
    df.columns = [c.strip().lower() for c in df.columns]

    if "resultado" not in df.columns:
        df["resultado"] = ""

    df["resultado_norm"] = df["resultado"].astype(str).str.strip().str.upper()
    return df

def calc_summary_from_checks(df: pd.DataFrame):
    total = len(df)
    passed = int((df.get("resultado_norm", "") == "OK").sum()) if total else 0
    pct = (passed / total * 100.0) if total else 0.0
    failed = total - passed
    return passed, failed, total, pct

def icon_from_result(x: str) -> str:
    x = str(x).strip().upper()
    if x in {"OK", "PASS", "PASSED", "SUCCESS", "CORRECTO", "TRUE", "1"}:
        return "✅ OK"
    if x in {"FAIL", "FAILED", "ERROR", "INCORRECTO", "FALSE", "0"}:
        return "❌ FAIL"
    return "❌ FAIL"

# =========================
# Indexar CSVs
# =========================
csv_files = sorted(glob.glob(os.path.join(BASE_DIR, "*.csv")))

index = {}   # host -> set(temas)
paths = {}   # (host, tema) -> path
for p in csv_files:
    host, tema = parse_host_tema_from_filename(p)
    index.setdefault(host, set()).add(tema)
    paths[(host, tema)] = p

hosts = sorted(index.keys())

host_sel = pn.widgets.Select(name="Host", options=hosts, sizing_mode="stretch_width")
tema_sel  = pn.widgets.Select(name="Tema", options=sorted(index[hosts[0]]) if hosts else [],
                              sizing_mode="stretch_width")

def on_host_change(event):
    temas = sorted(index.get(event.new, []))
    tema_sel.options = temas
    if temas:
        tema_sel.value = temas[0]

host_sel.param.watch(on_host_change, "value")

# Estilo de controles
controls = pn.Card(
    pn.pane.Markdown("### Selección"),
    host_sel,
    tema_sel,
    title="Controles",
    collapsed=False,
    styles={
        "border-radius": "16px",
        "box-shadow": "0 6px 16px rgba(2,6,23,.08)",
        "border": "1px solid rgba(15,23,42,.08)",
        "background": "#ffffff",
    },
    sizing_mode="stretch_width",
)

@pn.depends(host_sel, tema_sel)
def view(host, tema):
    if not host or not tema:
        return pn.pane.Markdown("No hay datos.")

    path = paths.get((host, tema))
    if not path or not os.path.exists(path):
        return pn.pane.Markdown("No hay CSV para esa selección.")

    df = read_checks_only(path)
    passed, failed, total, pct = calc_summary_from_checks(df)

    df_show = pd.DataFrame({
        "Prueba": df.get("prueba_id", ""),
        "Descripción": df.get("descripcion", ""),
        "Resultado": df.get("resultado_norm", "").apply(icon_from_result),
    })

    # Tabla bonita
    table = pn.widgets.Tabulator(
        df_show,
        disabled=True,
        pagination="local",
        page_size=12,
        height=420,
        sizing_mode="stretch_width",
        theme="simple",
    )

    top = header_card(host, tema)

    stats_row = pn.Row(
        pn.Column(score_card(passed, total, pct), sizing_mode="stretch_width"),
        pn.Column(
            pn.Row(
                small_stat_card("Aciertos", str(passed), "✅"),
                small_stat_card("Fallos", str(failed), "❌"),
                small_stat_card("Total", str(total), "📌"),
                sizing_mode="stretch_width"
            ),
            sizing_mode="stretch_width",
        ),
        sizing_mode="stretch_width",
    )

    data_card = pn.Card(
        pn.pane.Markdown("### Resultados por prueba"),
        table,
        title="Checklist",
        collapsed=False,
        styles={
            "border-radius": "16px",
            "box-shadow": "0 6px 16px rgba(2,6,23,.08)",
            "border": "1px solid rgba(15,23,42,.08)",
            "background": "#ffffff",
        },
        sizing_mode="stretch_width",
    )

    return pn.Column(
        top,
        pn.Spacer(height=10),
        stats_row,
        pn.Spacer(height=10),
        data_card,
        sizing_mode="stretch_width"
    )

# Layout final (dos columnas)
app = pn.template.FastListTemplate(
    title="Dashboard de auditorías",
    sidebar=[controls],
    main=[view],
    accent_base_color="#0f172a",
    header_background="#0f172a",
)

app.servable()

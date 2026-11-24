import os
import json
import glob
import html as html_lib

# 1. 2호기 사이트 기본 설정
SITE_NAME = "AWGWireCalc"
DOMAIN_URL = "https://awgwirecalc.com"
AMAZON_TAG = "awgwirecalc-20"
ADSENSE_PUB_ID = "ca-pub-8285144464443420"
CONTACT_EMAIL = "contact@awgwirecalc.com"

OUTPUT_DIR = "wire_calc_site"
os.makedirs(OUTPUT_DIR, exist_ok=True)

ADSENSE_SCRIPT = f"""<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ADSENSE_PUB_ID}"
     crossorigin="anonymous"></script>"""

# 2. 모든 scenarios*.json 불러오기 및 중복 제거
SCENARIOS = []
seen_slugs = set()

for json_file in sorted(glob.glob("scenarios*.json")):
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        for item in data:
            slug_key = item["slug"].strip().lower()
            if slug_key not in seen_slugs:
                seen_slugs.add(slug_key)
                SCENARIOS.append(item)

# 3. 공통 스타일시트 (북미 엔지니어링 프로 툴 UI)
CSS_STYLE = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
  :root {
    --bg: #f1f5f9;
    --surface: #ffffff;
    --navy: #0f172a;
    --primary: #2563eb;
    --accent: #f59e0b;
    --text-main: #0f172a;
    --text-sub: #475569;
    --text-muted: #64748b;
    --border: #e2e8f0;
  }
  * { box-sizing: border-box; }
  body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    line-height: 1.65;
    color: var(--text-main);
    margin: 0;
    background: var(--bg);
    -webkit-font-smoothing: antialiased;
  }
  .navbar {
    background: var(--navy);
    border-bottom: 1px solid rgba(255,255,255,0.08);
    position: sticky;
    top: 0;
    z-index: 100;
  }
  .nav-inner {
    max-width: 1060px;
    margin: 0 auto;
    padding: 0.9rem 1.25rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
  .brand {
    color: #fff;
    text-decoration: none;
    font-size: 1.25rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    display: flex;
    align-items: center;
    gap: 0.55rem;
  }
  .brand-icon {
    background: var(--accent);
    color: #0f172a;
    width: 30px;
    height: 30px;
    border-radius: 7px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 1rem;
    font-weight: 800;
  }
  .nav-links a {
    color: #cbd5e1;
    text-decoration: none;
    font-size: 0.9rem;
    font-weight: 500;
    margin-left: 1.25rem;
  }
  .nav-links a:hover { color: #fff; }

  .hero {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 60%, #1e3a8a 100%);
    color: #fff;
    padding: 2.6rem 1.25rem 3rem;
    text-align: center;
  }
  .hero-inner { max-width: 820px; margin: 0 auto; }
  .hero-tag {
    display: inline-block;
    background: rgba(245, 158, 11, 0.2);
    border: 1px solid rgba(251, 191, 36, 0.4);
    color: #fde68a;
    font-size: 0.8rem;
    font-weight: 700;
    padding: 0.3rem 0.85rem;
    border-radius: 999px;
    margin-bottom: 0.85rem;
  }
  .hero h1 {
    font-size: 2.15rem;
    font-weight: 800;
    letter-spacing: -0.025em;
    margin: 0 0 0.7rem;
    line-height: 1.25;
  }
  .hero p { color: #cbd5e1; font-size: 1.02rem; margin: 0; }

  .container { max-width: 1060px; margin: 2rem auto; padding: 0 1.25rem; }
  .article-container { max-width: 880px; margin: 2rem auto; padding: 0 1.25rem; }

  /* 실시간 인터랙티브 AWG 계산기 카드 */
  .calc-box {
    background: var(--surface);
    border: 2px solid #cbd5e1;
    border-radius: 16px;
    padding: 1.75rem;
    box-shadow: 0 10px 28px rgba(15, 23, 42, 0.08);
    margin-bottom: 2rem;
  }
  .calc-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-bottom: 0.95rem;
    padding-bottom: 0.85rem;
    border-bottom: 1px solid var(--border);
  }
  .calc-header h2 { margin: 0; font-size: 1.22rem; font-weight: 800; }
  .nec-badge {
    background: #eff6ff;
    color: #1d4ed8;
    border: 1px solid #bfdbfe;
    font-size: 0.76rem;
    font-weight: 700;
    padding: 0.25rem 0.65rem;
    border-radius: 6px;
  }

  /* 원클릭 프리셋 바 */
  .preset-bar {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 0.45rem;
    margin-bottom: 1.15rem;
    background: #f8fafc;
    padding: 0.6rem 0.8rem;
    border-radius: 10px;
    border: 1px solid var(--border);
  }
  .preset-label {
    font-size: 0.75rem;
    font-weight: 800;
    color: var(--text-muted);
    text-transform: uppercase;
    margin-right: 0.25rem;
  }
  .preset-chip {
    background: #fff;
    border: 1px solid #cbd5e1;
    color: var(--text-main);
    font-size: 0.78rem;
    font-weight: 600;
    padding: 0.32rem 0.7rem;
    border-radius: 999px;
    cursor: pointer;
    transition: all 0.15s;
  }
  .preset-chip:hover {
    border-color: var(--primary);
    color: var(--primary);
    background: #eff6ff;
  }

  .calc-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0.9rem;
    margin-bottom: 0.95rem;
  }
  .field label {
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 0.76rem;
    font-weight: 700;
    color: var(--text-sub);
    margin-bottom: 0.35rem;
    text-transform: uppercase;
    letter-spacing: 0.03em;
  }
  .unit-toggle {
    display: inline-flex;
    background: #e2e8f0;
    border-radius: 5px;
    padding: 1px;
  }
  .unit-btn {
    border: none;
    background: transparent;
    font-size: 0.68rem;
    font-weight: 800;
    color: var(--text-sub);
    padding: 0.12rem 0.42rem;
    border-radius: 4px;
    cursor: pointer;
  }
  .unit-btn.active {
    background: var(--primary);
    color: #fff;
  }
  .field select, .field input {
    width: 100%;
    height: 44px;
    padding: 0 0.8rem;
    border: 1.5px solid #cbd5e1;
    border-radius: 10px;
    font-size: 0.94rem;
    font-weight: 700;
    color: var(--text-main);
    background: #f8fafc;
    outline: none;
  }
  .field select:focus, .field input:focus {
    border-color: var(--primary);
    background: #fff;
  }
  .toggle-row {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    margin: 0.2rem 0 1.2rem;
    font-size: 0.88rem;
    font-weight: 600;
    color: var(--text-sub);
    cursor: pointer;
  }
  .toggle-row input { width: 17px; height: 17px; accent-color: var(--primary); cursor: pointer; }

  .results-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0.85rem;
    background: #0f172a;
    color: #fff;
    padding: 1.2rem;
    border-radius: 12px;
  }
  .res-item {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 10px;
    padding: 0.85rem 0.7rem;
    text-align: center;
  }
  .res-item.primary-res {
    background: rgba(37, 99, 235, 0.34);
    border-color: #60a5fa;
  }
  .res-label {
    font-size: 0.71rem;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    color: #94a3b8;
    font-weight: 700;
    margin-bottom: 0.25rem;
  }
  .res-val { font-size: 1.22rem; font-weight: 800; color: #fff; }
  .res-val.gold { color: #fbbf24; }
  .res-val.status-pass { color: #34d399; }
  .res-val.status-warn { color: #fbbf24; }
  .res-val.status-fail { color: #f87171; }
  .res-sub { font-size: 0.73rem; color: #cbd5e1; margin-top: 0.22rem; line-height: 1.3; }
  .res-reason {
    display: inline-block;
    margin-top: 0.28rem;
    padding: 0.12rem 0.48rem;
    border-radius: 4px;
    font-size: 0.68rem;
    font-weight: 700;
    background: rgba(251, 191, 36, 0.18);
    color: #fde68a;
  }

  /* 실시간 연동 아마존 직행 바 */
  .live-shop-bar {
    margin-top: 0.9rem;
    background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
    border: 1.5px solid #f59e0b;
    border-radius: 12px;
    padding: 0.85rem 1.1rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 0.75rem;
  }
  .live-shop-info {
    font-size: 0.88rem;
    font-weight: 700;
    color: #78350f;
  }
  .live-shop-info span {
    color: #b45309;
    font-weight: 800;
  }
  .live-shop-btns {
    display: flex;
    gap: 0.55rem;
    flex-wrap: wrap;
  }
  .live-amz-btn {
    background: #f59e0b;
    color: #111827;
    text-decoration: none;
    font-size: 0.83rem;
    font-weight: 800;
    padding: 0.55rem 0.95rem;
    border-radius: 8px;
    transition: background 0.15s;
    white-space: nowrap;
  }
  .live-amz-btn.secondary {
    background: #0f172a;
    color: #fff;
  }
  .live-amz-btn:hover { background: #d97706; color: #fff; }
  .live-amz-btn.secondary:hover { background: #1e293b; }

  /* 아마존 3종 자재 세트 카드 (상세 페이지) */
  .kit-section { margin-top: 1.8rem; }
  .kit-title { font-size: 1.15rem; font-weight: 800; margin: 0 0 0.85rem; }
  .kit-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.9rem; }
  .kit-card {
    background: linear-gradient(135deg, #ffffff 0%, #fffbeb 100%);
    border: 1.5px solid #fbbf24;
    border-radius: 12px;
    padding: 1.15rem;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }
  .kit-step { font-size: 0.72rem; font-weight: 800; color: #b45309; text-transform: uppercase; margin-bottom: 0.3rem; }
  .kit-name { font-size: 0.98rem; font-weight: 700; color: var(--text-main); margin-bottom: 0.9rem; line-height: 1.35; }
  .amz-btn {
    display: block;
    text-align: center;
    background: #f59e0b;
    color: #111827;
    font-weight: 800;
    font-size: 0.88rem;
    text-decoration: none;
    padding: 0.7rem 0.9rem;
    border-radius: 8px;
    transition: background 0.15s;
  }
  .amz-btn:hover { background: #d97706; color: #fff; }

  /* 시나리오 카드 목록 */
  .toolbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 0.8rem;
    margin: 2rem 0 1.2rem;
  }
  .filters { display: flex; gap: 0.5rem; flex-wrap: wrap; }
  .filter-btn {
    background: #fff;
    border: 1px solid var(--border);
    padding: 0.5rem 1rem;
    border-radius: 999px;
    cursor: pointer;
    font-weight: 600;
    font-size: 0.88rem;
    color: var(--text-sub);
  }
  .filter-btn.active { background: var(--primary); border-color: var(--primary); color: #fff; }
  .search-input {
    padding: 0.55rem 1rem;
    border: 1px solid #cbd5e1;
    border-radius: 999px;
    font-size: 0.9rem;
    min-width: 260px;
    outline: none;
  }

  .scenario-grid {
    list-style: none;
    padding: 0;
    margin: 0;
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
  }
  .scenario-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    transition: transform 0.15s, border-color 0.15s, box-shadow 0.15s;
  }
  .scenario-card:hover {
    transform: translateY(-2px);
    border-color: #93c5fd;
    box-shadow: 0 8px 20px rgba(15, 23, 42, 0.06);
  }
  .scenario-card a {
    display: block;
    padding: 1.25rem;
    text-decoration: none;
    color: inherit;
  }
  .card-top { display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem; }
  .cat-pill {
    font-size: 0.74rem;
    font-weight: 700;
    padding: 0.2rem 0.6rem;
    border-radius: 999px;
    background: #eff6ff;
    color: #1d4ed8;
  }
  .spec-pill {
    font-family: ui-monospace, monospace;
    font-size: 0.8rem;
    font-weight: 700;
    color: #047857;
    background: #ecfdf5;
    padding: 0.2rem 0.55rem;
    border-radius: 6px;
  }
  .card-title { font-size: 1.04rem; font-weight: 700; margin-bottom: 0.4rem; }
  .card-sum { font-size: 0.87rem; color: var(--text-muted); }

  /* 전체 AWG NEC 허용전류 레퍼런스 표 */
  .chart-section {
    margin-top: 3rem;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.8rem;
    box-shadow: 0 4px 16px rgba(15, 23, 42, 0.04);
  }
  .chart-section h2 {
    margin: 0 0 0.4rem;
    font-size: 1.35rem;
    font-weight: 800;
  }
  .chart-sub {
    color: var(--text-muted);
    font-size: 0.9rem;
    margin: 0 0 1.2rem;
  }
  .table-wrap { overflow-x: auto; }
  .awg-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.88rem;
    min-width: 640px;
  }
  .awg-table th {
    background: #0f172a;
    color: #fff;
    text-align: left;
    padding: 0.75rem 0.9rem;
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 0.03em;
  }
  .awg-table td {
    padding: 0.7rem 0.9rem;
    border-bottom: 1px solid var(--border);
    color: var(--text-sub);
  }
  .awg-table tr:nth-child(even) td { background: #f8fafc; }
  .awg-table td strong { color: var(--text-main); font-weight: 800; }

  /* 상세 페이지 */
  .breadcrumb { font-size: 0.86rem; color: var(--text-muted); margin-bottom: 1rem; }
  .breadcrumb a { color: var(--primary); text-decoration: none; font-weight: 500; }
  .article-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 2rem 2.2rem;
  }
  .article-card h1 { font-size: 1.78rem; font-weight: 800; margin: 0.5rem 0 0.8rem; line-height: 1.3; }
  .summary-box {
    background: #f8fafc;
    border-left: 4px solid var(--primary);
    padding: 0.95rem 1.15rem;
    border-radius: 0 8px 8px 0;
    color: var(--text-sub);
    margin-bottom: 1.4rem;
  }
  .safety-banner {
    background: #fffbeb;
    border: 1px solid #fde68a;
    color: #92400e;
    padding: 0.9rem 1.1rem;
    border-radius: 10px;
    font-size: 0.88rem;
    margin-bottom: 1.6rem;
  }
  .notes-box {
    background: #f8fafc;
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.25rem 1.4rem;
    margin-top: 1.6rem;
  }
  .notes-box h2 { margin: 0 0 0.7rem; font-size: 1.1rem; font-weight: 800; }
  .notes-box ul { margin: 0; padding-left: 1.2rem; color: var(--text-sub); }
  .notes-box li { margin-bottom: 0.45rem; }

  .faq-section { margin-top: 2rem; padding-top: 1.6rem; border-top: 1px solid var(--border); }
  .faq-section h2 { font-size: 1.2rem; font-weight: 800; margin: 0 0 0.9rem; }
  .faq-item { border: 1px solid var(--border); border-radius: 10px; margin-bottom: 0.6rem; background: #f8fafc; }
  .faq-item summary { padding: 0.9rem 1.1rem; font-weight: 700; cursor: pointer; }
  .faq-answer { padding: 0.8rem 1.1rem 1rem; background: #fff; border-top: 1px solid var(--border); color: var(--text-sub); font-size: 0.92rem; }

  footer {
    background: var(--navy);
    color: #94a3b8;
    padding: 2.5rem 1.25rem;
    margin-top: 3.5rem;
    font-size: 0.85rem;
    text-align: center;
  }
  .footer-links { margin-bottom: 0.8rem; }
  .footer-links a { color: #e2e8f0; text-decoration: none; margin: 0 0.75rem; }

  @media (max-width: 820px) {
    .calc-grid, .results-grid { grid-template-columns: repeat(2, 1fr); }
    .kit-grid, .scenario-grid { grid-template-columns: 1fr; }
    .hero h1 { font-size: 1.6rem; }
    .article-card { padding: 1.35rem 1.15rem; }
    .live-shop-bar { flex-direction: column; align-items: stretch; }
    .live-shop-btns { width: 100%; }
    .live-amz-btn { flex: 1; text-align: center; }
  }
</style>
"""

# 4. 실시간 자바스크립트 공학 계산 엔진 (NEC 60°C/75°C + 1P/3P + ft/m + Live Amazon CTA)
CALC_JS = f"""
<script>
  const AMAZON_TAG = "{AMAZON_TAG}";
  const AWG_TABLE = [
    {{ awg: "14 AWG", cmil: 4110,  cu60: 15,  cu75: 20,  al60: 0,   al75: 0,   necMaxCu: 15, necMaxAl: 0 }},
    {{ awg: "12 AWG", cmil: 6530,  cu60: 20,  cu75: 25,  al60: 15,  al75: 20,  necMaxCu: 20, necMaxAl: 15 }},
    {{ awg: "10 AWG", cmil: 10380, cu60: 30,  cu75: 35,  al60: 25,  al75: 30,  necMaxCu: 30, necMaxAl: 25 }},
    {{ awg: "8 AWG",  cmil: 16510, cu60: 40,  cu75: 50,  al60: 35,  al75: 40,  necMaxCu: 999, necMaxAl: 999 }},
    {{ awg: "6 AWG",  cmil: 26240, cu60: 55,  cu75: 65,  al60: 40,  al75: 50,  necMaxCu: 999, necMaxAl: 999 }},
    {{ awg: "4 AWG",  cmil: 41740, cu60: 70,  cu75: 85,  al60: 55,  al75: 65,  necMaxCu: 999, necMaxAl: 999 }},
    {{ awg: "3 AWG",  cmil: 52620, cu60: 85,  cu75: 100, al60: 65,  al75: 75,  necMaxCu: 999, necMaxAl: 999 }},
    {{ awg: "2 AWG",  cmil: 66360, cu60: 95,  cu75: 115, al60: 75,  al75: 90,  necMaxCu: 999, necMaxAl: 999 }},
    {{ awg: "1 AWG",  cmil: 83690, cu60: 110, cu75: 130, al60: 85,  al75: 100, necMaxCu: 999, necMaxAl: 999 }},
    {{ awg: "1/0 AWG",cmil: 105600,cu60: 125, cu75: 150, al60: 100, al75: 120, necMaxCu: 999, necMaxAl: 999 }},
    {{ awg: "2/0 AWG",cmil: 133100,cu60: 145, cu75: 175, al60: 115, al75: 135, necMaxCu: 999, necMaxAl: 999 }},
    {{ awg: "3/0 AWG",cmil: 167800,cu60: 165, cu75: 200, al60: 130, al75: 155, necMaxCu: 999, necMaxAl: 999 }},
    {{ awg: "4/0 AWG",cmil: 211600,cu60: 195, cu75: 230, al60: 150, al75: 180, necMaxCu: 999, necMaxAl: 999 }},
    {{ awg: "250 kcmil",cmil: 250000,cu60: 215,cu75: 255,al60: 170, al75: 205, necMaxCu: 999, necMaxAl: 999 }}
  ];
  const BREAKERS = [15, 20, 25, 30, 35, 40, 45, 50, 60, 70, 80, 90, 100, 110, 125, 150, 175, 200, 225, 250];
  let distUnit = 'ft';

  function setDistUnit(u) {{
    if (distUnit === u) return;
    const distEl = document.getElementById('calcDist');
    let val = parseFloat(distEl.value) || 50;
    distEl.value = (u === 'm') ? Math.round(val * 0.3048 * 10) / 10 : Math.round(val / 0.3048);
    distUnit = u;
    document.getElementById('unitFtBtn').classList.toggle('active', u === 'ft');
    document.getElementById('unitMBtn').classList.toggle('active', u === 'm');
    runWireCalc();
  }}

  function applyPreset(volts, amps, distFt, insul, isCont) {{
    document.getElementById('calcVolts').value = String(volts);
    document.getElementById('calcAmps').value = amps;
    document.getElementById('calcPhase').value = '1';
    document.getElementById('calcMat').value = 'copper';
    document.getElementById('calcInsul').value = String(insul);
    document.getElementById('calcMaxDrop').value = '3';
    document.getElementById('calcCont').checked = isCont;
    if (distUnit === 'm') {{
      document.getElementById('calcDist').value = Math.round(distFt * 0.3048 * 10) / 10;
    }} else {{
      document.getElementById('calcDist').value = distFt;
    }}
    runWireCalc();
  }}

  function getRowAmpacity(row, mat, insul) {{
    let raw = 0;
    if (mat === 'copper') {{
      raw = (insul === 60) ? row.cu60 : row.cu75;
      return Math.min(raw, row.necMaxCu);
    }} else {{
      raw = (insul === 60) ? row.al60 : row.al75;
      return Math.min(raw, row.necMaxAl);
    }}
  }}

  function runWireCalc() {{
    const volts = parseFloat(document.getElementById('calcVolts').value) || 240;
    const amps = parseFloat(document.getElementById('calcAmps').value) || 48;
    const rawDist = parseFloat(document.getElementById('calcDist').value) || 50;
    const distFt = (distUnit === 'm') ? rawDist * 3.28084 : rawDist;
    const phase = parseInt(document.getElementById('calcPhase').value, 10) || 1;
    const mat = document.getElementById('calcMat').value;
    const insul = parseInt(document.getElementById('calcInsul').value, 10) || 75;
    const maxDropLimit = parseFloat(document.getElementById('calcMaxDrop').value) || 3.0;
    const isCont = document.getElementById('calcCont').checked;

    const reqAmpacity = isCont ? amps * 1.25 : amps;
    const K = (mat === 'copper') ? 12.9 : 21.2;
    const phaseFactor = (phase === 3) ? 1.732 : 2.0;

    let ampOnlyRow = null;
    let selected = AWG_TABLE[AWG_TABLE.length - 1];
    let vDropVolts = 0;
    let vDropPct = 0;
    let matched = false;

    for (let i = 0; i < AWG_TABLE.length; i++) {{
      const row = AWG_TABLE[i];
      const maxA = getRowAmpacity(row, mat, insul);
      if (maxA < reqAmpacity) continue;
      if (!ampOnlyRow) ampOnlyRow = row;

      const vd = (phaseFactor * K * amps * distFt) / row.cmil;
      const pct = (vd / volts) * 100;
      if (pct <= maxDropLimit) {{
        selected = row;
        vDropVolts = vd;
        vDropPct = pct;
        matched = true;
        break;
      }}
    }}

    if (!matched) {{
      vDropVolts = (phaseFactor * K * amps * distFt) / selected.cmil;
      vDropPct = (vDropVolts / volts) * 100;
    }}

    let recBreaker = BREAKERS[BREAKERS.length - 1];
    for (let b of BREAKERS) {{
      if (b >= reqAmpacity) {{ recBreaker = b; break; }}
    }}

    const endVolts = Math.max(0, volts - vDropVolts);
    const totalKw = (phase === 3)
      ? ((1.732 * volts * amps) / 1000)
      : ((volts * amps) / 1000);

    const upsizedForDrop = ampOnlyRow && (ampOnlyRow.cmil < selected.cmil);

    document.getElementById('resAwg').textContent = selected.awg;
    const matLabel = (mat === 'copper') ? 'Copper' : 'Aluminum';
    const insulLabel = (insul === 60) ? '60°C NM-B' : '75°C THHN';
    document.getElementById('resMatSub').textContent = matLabel + ' (' + insulLabel + ')';
    document.getElementById('resReason').textContent = upsizedForDrop
      ? 'Upsized for Voltage Drop'
      : 'Sized by NEC Ampacity';

    document.getElementById('resBreaker').textContent = recBreaker + ' Amp';
    document.getElementById('resBreakerSub').textContent = isCont
      ? '125% Continuous (' + reqAmpacity.toFixed(0) + 'A min)'
      : 'Standard Non-Continuous';

    const dropEl = document.getElementById('resDrop');
    dropEl.textContent = vDropPct.toFixed(2) + '% (' + vDropVolts.toFixed(1) + 'V)';
    dropEl.className = 'res-val ' + (
      vDropPct <= maxDropLimit ? 'status-pass' : (vDropPct <= 5.0 ? 'status-warn' : 'status-fail')
    );
    document.getElementById('resDropSub').textContent =
      endVolts.toFixed(1) + 'V at load (' + (vDropPct <= maxDropLimit ? 'PASS <=' + maxDropLimit + '%' : 'Exceeds ' + maxDropLimit + '%') + ')';

    document.getElementById('resWatts').textContent = totalKw.toFixed(2) + ' kW';
    document.getElementById('resWattsSub').textContent = (phase === 3 ? '3-Phase ' : '1-Phase ') + volts + 'V Circuit';

    // 실시간 아마존 링크 업데이트
    const wireTypeStr = (insul === 60) ? 'nm-b+romex+wire' : 'thhn+wire';
    const wireQuery = encodeURIComponent(selected.awg + ' ' + matLabel.toLowerCase()) + '+' + wireTypeStr;
    const brkQuery = encodeURIComponent(recBreaker + ' amp circuit breaker');

    document.getElementById('liveSpecLabel').textContent = selected.awg + ' ' + matLabel + ' + ' + recBreaker + 'A Breaker';
    const wireBtn = document.getElementById('liveWireBtn');
    wireBtn.textContent = 'Shop ' + selected.awg + ' ' + matLabel + ' Wire ->';
    wireBtn.href = 'https://www.amazon.com/s?k=' + wireQuery + '&tag=' + AMAZON_TAG;

    const brkBtn = document.getElementById('liveBreakerBtn');
    brkBtn.textContent = 'Shop ' + recBreaker + 'A Breaker ->';
    brkBtn.href = 'https://www.amazon.com/s?k=' + brkQuery + '&tag=' + AMAZON_TAG;
  }}

  window.addEventListener('DOMContentLoaded', runWireCalc);
</script>
"""

def render_calc_widget(default_v=240, default_a=48, default_d=50, default_cont=True):
    volt_labels = {
        12: "12V DC (Solar / Auto / RV)",
        24: "24V DC (Solar / Battery Bank)",
        48: "48V DC (Off-Grid Inverter)",
        120: "120V AC (Standard US Outlet)",
        208: "208V AC (Commercial / 3-Phase)",
        240: "240V AC (EV / Dryer / Subpanel)",
        480: "480V AC (Industrial 3-Phase)"
    }
    v_opts = "".join(
        f'<option value="{v}" {"selected" if v == default_v else ""}>{lbl}</option>'
        for v, lbl in volt_labels.items()
    )
    checked_attr = "checked" if default_cont else ""
    return f"""
    <div class="calc-box">
      <div class="calc-header">
        <h2>&#9889; Interactive NEC Wire Size &amp; Voltage Drop Calculator</h2>
        <span class="nec-badge">NEC 310.16 &bull; US / Canada AWG</span>
      </div>

      <div class="preset-bar">
        <span class="preset-label">Quick Presets:</span>
        <button type="button" class="preset-chip" onclick="applyPreset(240, 48, 50, 75, true)">&#9889; 48A EV Charger</button>
        <button type="button" class="preset-chip" onclick="applyPreset(240, 50, 75, 75, false)">&#128656; 50A RV Hookup</button>
        <button type="button" class="preset-chip" onclick="applyPreset(240, 100, 100, 75, false)">&#127968; 100A Subpanel</button>
        <button type="button" class="preset-chip" onclick="applyPreset(240, 30, 40, 60, true)">&#129530; 30A Dryer (NM-B)</button>
        <button type="button" class="preset-chip" onclick="applyPreset(12, 30, 20, 75, true)">&#9728;&#65039; 12V 30A Solar</button>
      </div>

      <div class="calc-grid">
        <div class="field">
          <label for="calcVolts">System Voltage</label>
          <select id="calcVolts" onchange="runWireCalc()">{v_opts}</select>
        </div>
        <div class="field">
          <label for="calcAmps">Load Current (Amps)</label>
          <input type="number" id="calcAmps" value="{default_a}" min="1" max="250" oninput="runWireCalc()">
        </div>
        <div class="field">
          <label for="calcDist">
            <span>One-Way Distance</span>
            <span class="unit-toggle">
              <button type="button" id="unitFtBtn" class="unit-btn active" onclick="setDistUnit('ft')">FT</button>
              <button type="button" id="unitMBtn" class="unit-btn" onclick="setDistUnit('m')">M</button>
            </span>
          </label>
          <input type="number" id="calcDist" value="{default_d}" min="1" max="2000" oninput="runWireCalc()">
        </div>
        <div class="field">
          <label for="calcMat">Conductor Material</label>
          <select id="calcMat" onchange="runWireCalc()">
            <option value="copper" selected>Copper (Cu)</option>
            <option value="aluminum">Aluminum (Al)</option>
          </select>
        </div>
      </div>

      <div class="calc-grid">
        <div class="field">
          <label for="calcInsul">Wire / Insulation Rating</label>
          <select id="calcInsul" onchange="runWireCalc()">
            <option value="75" selected>75&deg;C THHN / THWN / MC (Conduit)</option>
            <option value="60">60&deg;C NM-B Romex / UF-B (Indoor)</option>
          </select>
        </div>
        <div class="field">
          <label for="calcPhase">System Phase</label>
          <select id="calcPhase" onchange="runWireCalc()">
            <option value="1" selected>Single-Phase / DC</option>
            <option value="3">Three-Phase (3&Phi; AC)</option>
          </select>
        </div>
        <div class="field">
          <label for="calcMaxDrop">Max Voltage Drop</label>
          <select id="calcMaxDrop" onchange="runWireCalc()">
            <option value="3" selected>3% (NEC Branch Standard)</option>
            <option value="2">2% (Sensitive / Solar DC)</option>
            <option value="5">5% (Feeder + Branch Max)</option>
          </select>
        </div>
        <div class="field">
          <label>NEC Table Reference</label>
          <input type="text" value="NEC 310.16 + 240.4(D)" readonly style="color:#475569; font-weight:600; cursor:default;">
        </div>
      </div>

      <label class="toggle-row">
        <input type="checkbox" id="calcCont" {checked_attr} onchange="runWireCalc()">
        <span>Continuous Load (Runs 3+ hours: EV Charger, Solar, Heater &mdash; applies NEC 125% rule)</span>
      </label>

      <div class="results-grid">
        <div class="res-item primary-res">
          <div class="res-label">Minimum Wire Size</div>
          <div class="res-val gold" id="resAwg">6 AWG</div>
          <div class="res-sub" id="resMatSub">Copper (75&deg;C THHN)</div>
          <div class="res-reason" id="resReason">Sized by NEC Ampacity</div>
        </div>
        <div class="res-item">
          <div class="res-label">Breaker / OCPD Size</div>
          <div class="res-val" id="resBreaker">60 Amp</div>
          <div class="res-sub" id="resBreakerSub">125% Continuous (60A min)</div>
        </div>
        <div class="res-item">
          <div class="res-label">Voltage Drop</div>
          <div class="res-val status-pass" id="resDrop">1.29% (3.1V)</div>
          <div class="res-sub" id="resDropSub">236.9V at load (PASS &lt;=3%)</div>
        </div>
        <div class="res-item">
          <div class="res-label">Circuit Capacity</div>
          <div class="res-val" id="resWatts">11.52 kW</div>
          <div class="res-sub" id="resWattsSub">1-Phase 240V Circuit</div>
        </div>
      </div>

      <div class="live-shop-bar">
        <div class="live-shop-info">
          &#128722; Matched Hardware for Your Calculation: <span id="liveSpecLabel">6 AWG Copper + 60A Breaker</span>
        </div>
        <div class="live-shop-btns">
          <a id="liveWireBtn" class="live-amz-btn" href="https://www.amazon.com/s?k=6+AWG+copper+thhn+wire&tag={AMAZON_TAG}" target="_blank" rel="nofollow sponsored">Shop 6 AWG Copper Wire &rarr;</a>
          <a id="liveBreakerBtn" class="live-amz-btn secondary" href="https://www.amazon.com/s?k=60+amp+circuit+breaker&tag={AMAZON_TAG}" target="_blank" rel="nofollow sponsored">Shop 60A Breaker &rarr;</a>
        </div>
      </div>
    </div>
    """

AWG_REFERENCE_CHART_HTML = """
  <section class="chart-section" id="awg-chart">
    <h2>NEC AWG Wire Size &amp; Ampacity Reference Chart (Table 310.16)</h2>
    <p class="chart-sub">Standard North American allowable ampacities for insulated Copper (Cu) and Aluminum (Al) conductors rated at 60&deg;C (NM-B Romex / UF-B) and 75&deg;C (THHN / THWN-2 / XHHW), including NEC 240.4(D) small conductor breaker limits.</p>
    <div class="table-wrap">
      <table class="awg-table">
        <thead>
          <tr>
            <th>Wire Gauge</th>
            <th>Copper 60&deg;C (NM-B)</th>
            <th>Copper 75&deg;C (THHN)</th>
            <th>Aluminum 75&deg;C</th>
            <th>Max Breaker (Cu)</th>
            <th>Typical North American Application</th>
          </tr>
        </thead>
        <tbody>
          <tr><td><strong>14 AWG</strong></td><td>15 A</td><td>20 A*</td><td>&mdash;</td><td>15 Amp</td><td>Lighting circuits, bedroom outlets</td></tr>
          <tr><td><strong>12 AWG</strong></td><td>20 A</td><td>25 A*</td><td>20 A*</td><td>20 Amp</td><td>Kitchen, bathroom, garage 20A receptacles</td></tr>
          <tr><td><strong>10 AWG</strong></td><td>30 A</td><td>35 A*</td><td>30 A*</td><td>30 Amp</td><td>Electric clothes dryers, 30A RV, water heaters</td></tr>
          <tr><td><strong>8 AWG</strong></td><td>40 A</td><td>50 A</td><td>40 A</td><td>40&ndash;50 Amp</td><td>32A&ndash;40A Level 2 EV chargers, electric ranges</td></tr>
          <tr><td><strong>6 AWG</strong></td><td>55 A</td><td>65 A</td><td>50 A</td><td>50&ndash;60 Amp</td><td>48A EV chargers (THHN), 50A RV pedestals, hot tubs</td></tr>
          <tr><td><strong>4 AWG</strong></td><td>70 A</td><td>85 A</td><td>65 A</td><td>70&ndash;80 Amp</td><td>60A&ndash;80A subpanels, long-run 48A EV chargers</td></tr>
          <tr><td><strong>3 AWG</strong></td><td>85 A</td><td>100 A</td><td>75 A</td><td>100 Amp</td><td>100A residential garage subpanel (Copper)</td></tr>
          <tr><td><strong>2 AWG</strong></td><td>95 A</td><td>115 A</td><td>90 A</td><td>90&ndash;115 Amp</td><td>90A&ndash;100A feeder subpanels (Al MHF / SER)</td></tr>
          <tr><td><strong>1 AWG</strong></td><td>110 A</td><td>130 A</td><td>100 A</td><td>125 Amp</td><td>100A Aluminum feeder / 125A Copper subpanel</td></tr>
          <tr><td><strong>1/0 AWG</strong></td><td>125 A</td><td>150 A</td><td>120 A</td><td>150 Amp</td><td>125A&ndash;150A service entrance &amp; heavy feeders</td></tr>
          <tr><td><strong>2/0 AWG</strong></td><td>145 A</td><td>175 A</td><td>135 A</td><td>175&ndash;200 Amp</td><td>200A residential service entrance (Copper NEC 310.12)</td></tr>
          <tr><td><strong>3/0 AWG</strong></td><td>165 A</td><td>200 A</td><td>155 A</td><td>200 Amp</td><td>200A commercial continuous main feeder (Copper)</td></tr>
          <tr><td><strong>4/0 AWG</strong></td><td>195 A</td><td>230 A</td><td>180 A</td><td>200&ndash;225 Amp</td><td>200A residential service entrance (Aluminum)</td></tr>
        </tbody>
      </table>
    </div>
    <p style="font-size:0.78rem; color:#64748b; margin:0.85rem 0 0;">*Per NEC 240.4(D), overcurrent protection shall not exceed 15A for 14 AWG, 20A for 12 AWG, and 30A for 10 AWG copper conductors in standard branch circuits.</p>
  </section>
"""

NAVBAR_HTML = f"""
  <nav class="navbar">
    <div class="nav-inner">
      <a class="brand" href="index.html">
        <span class="brand-icon">&#9889;</span>
        <span>{SITE_NAME}</span>
      </a>
      <div class="nav-links">
        <a href="index.html">Calculator</a>
        <a href="index.html#awg-chart">AWG Chart</a>
        <a href="about.html">About</a>
        <a href="contact.html">Contact</a>
      </div>
    </div>
  </nav>
"""

FOOTER_HTML = f"""
  <footer>
    <div class="footer-inner">
      <div class="footer-links">
        <a href="index.html">Home</a>
        <a href="index.html#awg-chart">NEC AWG Chart</a>
        <a href="about.html">About Us</a>
        <a href="privacy.html">Privacy Policy</a>
        <a href="contact.html">Contact</a>
      </div>
      <div>&copy; 2026 {SITE_NAME}. North American AWG Wire Gauge &amp; NEC Ampacity Reference Tool.</div>
      <div style="margin-top:0.35rem; font-size:0.78rem; color:#64748b;">Engineering Reference Disclaimer: Calculations follow standard NEC Table 310.16 ampacity and voltage drop formulas for educational estimation only. Always verify local electrical codes and consult a licensed electrician. As an Amazon Associate, we earn from qualifying purchases.</div>
    </div>
  </footer>
"""

sitemap_urls = [
    f"{DOMAIN_URL}/",
    f"{DOMAIN_URL}/about.html",
    f"{DOMAIN_URL}/privacy.html",
    f"{DOMAIN_URL}/contact.html"
]

# 5. 개별 시나리오 상세 페이지 생성
for item in SCENARIOS:
    filename = f"{item['slug']}.html"
    filepath = os.path.join(OUTPUT_DIR, filename)
    sitemap_urls.append(f"{DOMAIN_URL}/{filename}")

    title_esc = html_lib.escape(item["title"])
    cat_esc = html_lib.escape(item["category"])
    sum_esc = html_lib.escape(item["summary"])
    awg_esc = html_lib.escape(item["rec_awg_cu"])
    brk_esc = html_lib.escape(item["rec_breaker"])
    notes_html = "".join(f"<li>{html_lib.escape(n)}</li>" for n in item["notes"])

    wire_url = f"https://www.amazon.com/s?k={item['wire_query']}&tag={AMAZON_TAG}"
    brk_url = f"https://www.amazon.com/s?k={item['breaker_query']}&tag={AMAZON_TAG}"
    gear_url = f"https://www.amazon.com/s?k={item['gear_query']}&tag={AMAZON_TAG}"

    faqs = [
        (
            f"What wire gauge do I need for {item['title'].lower()}?",
            f"For a {item['amps']}A load at {item['voltage']}V over {item['distance']} feet, the recommended conductor is {item['rec_awg_cu']} paired with a {item['rec_breaker']} to meet NEC ampacity and keep voltage drop below 3%."
        ),
        (
            f"Can I use NM-B Romex or Aluminum wire for {item['amps']} Amps?",
            f"Indoor NM-B Romex is restricted to the 60°C NEC ampacity column, whereas THHN in conduit uses the 75°C column. Use our Wire / Insulation Rating selector above to compare exact 60°C vs 75°C Copper and Aluminum sizes."
        ),
        (
            f"Why does distance affect wire size for {item['equipment']}?",
            f"Longer wire runs increase electrical resistance, causing voltage drop. Under NEC guidelines, keeping voltage drop under 3% prevents overheating, nuisance breaker trips, and reduced charging or motor efficiency."
        )
    ]

    faq_html = "".join(
        f'<details class="faq-item" {"open" if i == 0 else ""}><summary>{html_lib.escape(q)}</summary><div class="faq-answer">{html_lib.escape(a)}</div></details>'
        for i, (q, a) in enumerate(faqs)
    )
    faq_schema_json = json.dumps({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]
    }, ensure_ascii=False)

    calc_widget = render_calc_widget(
        default_v=item["voltage"],
        default_a=item["amps"],
        default_d=item["distance"],
        default_cont=item["continuous"]
    )

    page_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title_esc} (NEC Chart &amp; Calculator) | {SITE_NAME}</title>
  <meta name="description" content="{sum_esc}">
  {ADSENSE_SCRIPT}
  {CSS_STYLE}
  <script type="application/ld+json">{faq_schema_json}</script>
</head>
<body>
  {NAVBAR_HTML}
  <div class="article-container">
    <div class="breadcrumb">
      <a href="index.html">Home Calculator</a> &rsaquo; <span>{cat_esc}</span>
    </div>

    <article class="article-card">
      <span class="cat-pill">&#9889; {cat_esc} &bull; {item['voltage']}V / {item['amps']}A / {item['distance']} ft</span>
      <h1>{title_esc}</h1>
      <p class="summary-box"><strong>Quick Answer:</strong> Use <strong>{awg_esc}</strong> with a <strong>{brk_esc}</strong>. {sum_esc}</p>

      <div class="safety-banner">
        <strong>&#9888;&#65039; Electrical Safety Notice:</strong> Always turn off the main service breaker and verify zero voltage with a non-contact tester before working inside any electrical panel.
      </div>

      {calc_widget}

      <div class="kit-section">
        <h2 class="kit-title">&#128722; Complete Installation Materials Checklist</h2>
        <div class="kit-grid">
          <div class="kit-card">
            <div>
              <div class="kit-step">1. Recommended Wire</div>
              <div class="kit-name">{html_lib.escape(item['wire_item'])}</div>
            </div>
            <a class="amz-btn" href="{wire_url}" target="_blank" rel="nofollow sponsored">Check Wire Price &rarr;</a>
          </div>
          <div class="kit-card">
            <div>
              <div class="kit-step">2. Breaker / Disconnect</div>
              <div class="kit-name">{html_lib.escape(item['breaker_item'])}</div>
            </div>
            <a class="amz-btn" href="{brk_url}" target="_blank" rel="nofollow sponsored">Check Breaker Price &rarr;</a>
          </div>
          <div class="kit-card">
            <div>
              <div class="kit-step">3. Compatible Equipment</div>
              <div class="kit-name">{html_lib.escape(item['gear_item'])}</div>
            </div>
            <a class="amz-btn" href="{gear_url}" target="_blank" rel="nofollow sponsored">View on Amazon &rarr;</a>
          </div>
        </div>
      </div>

      <div class="notes-box">
        <h2>&#128203; NEC Code &amp; Installation Notes</h2>
        <ul>{notes_html}</ul>
      </div>

      <section class="faq-section">
        <h2>Frequently Asked Questions</h2>
        {faq_html}
      </section>
    </article>
  </div>
  {FOOTER_HTML}
  {CALC_JS}
</body>
</html>"""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(page_html)

# 6. 메인 홈 페이지(index.html) 생성
cards_html = ""
for item in SCENARIOS:
    search_blob = html_lib.escape(f"{item['title']} {item['category']} {item['rec_awg_cu']} {item['summary']}".lower())
    cards_html += f"""
    <li class="scenario-card" data-cat="{html_lib.escape(item['category'])}" data-search="{search_blob}">
      <a href="{item['slug']}.html">
        <div class="card-top">
          <span class="cat-pill">{html_lib.escape(item['category'])}</span>
          <span class="spec-pill">{html_lib.escape(item['rec_awg_cu'].split('(')[0].strip())}</span>
        </div>
        <div class="card-title">{html_lib.escape(item['title'])}</div>
        <div class="card-sum">{html_lib.escape(item['summary'])}</div>
      </a>
    </li>"""

index_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{SITE_NAME} - NEC AWG Wire Size, Voltage Drop &amp; Breaker Calculator</title>
  <meta name="description" content="Free North American NEC 310.16 AWG wire gauge, 60C NM-B vs 75C THHN ampacity, voltage drop, and circuit breaker calculator for EV chargers, solar, RVs, and subpanels.">
  {ADSENSE_SCRIPT}
  {CSS_STYLE}
</head>
<body>
  {NAVBAR_HTML}
  <section class="hero">
    <div class="hero-inner">
      <span class="hero-tag">&#9889; NEC 310.16 Compliant &bull; 60&deg;C NM-B &amp; 75&deg;C THHN &bull; 1&Phi; / 3&Phi;</span>
      <h1>AWG Wire Size &amp; Breaker Calculator</h1>
      <p>Calculate exact NEC wire gauge, real-time voltage drop, and breaker sizing for EV chargers, solar arrays, RVs, and home subpanels.</p>
    </div>
  </section>

  <div class="container">
    {render_calc_widget(240, 48, 50, True)}

    <div class="toolbar">
      <div class="filters">
        <button class="filter-btn active" onclick="filterCat('all', this)">All Guides ({len(SCENARIOS)})</button>
        <button class="filter-btn" onclick="filterCat('EV Charger', this)">EV Chargers</button>
        <button class="filter-btn" onclick="filterCat('Solar & Off-Grid', this)">Solar &amp; Off-Grid</button>
        <button class="filter-btn" onclick="filterCat('RV & Marine', this)">RV &amp; Marine</button>
        <button class="filter-btn" onclick="filterCat('Home & Garage', this)">Home &amp; Garage</button>
      </div>
      <input type="text" id="searchBox" class="search-input" placeholder="Search (e.g., 48 amp, Tesla, 2000w, RV)...">
    </div>

    <ul class="scenario-grid" id="scenarioList">
      {cards_html}
    </ul>

    {AWG_REFERENCE_CHART_HTML}
  </div>
  {FOOTER_HTML}
  {CALC_JS}
  <script>
    let activeCat = 'all';
    const sBox = document.getElementById('searchBox');
    const sCards = document.querySelectorAll('.scenario-card');

    function updateCards() {{
      const q = sBox.value.toLowerCase().trim();
      sCards.forEach(c => {{
        const okText = !q || c.dataset.search.includes(q);
        const okCat = activeCat === 'all' || c.dataset.cat === activeCat;
        c.style.display = (okText && okCat) ? '' : 'none';
      }});
    }}
    function filterCat(cat, btn) {{
      activeCat = cat;
      document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      updateCards();
    }}
    sBox.addEventListener('input', updateCards);
  </script>
</body>
</html>"""
with open(os.path.join(OUTPUT_DIR, "index.html"), "w", encoding="utf-8") as f:
    f.write(index_html)

# 7. 애드센스 필수 페이지 3종 생성
static_pages = {
    "about.html": (
        f"About Us | {SITE_NAME}",
        "About AWGWireCalc",
        f"<p><strong>{SITE_NAME}</strong> provides fast, NEC-aligned wire gauge (AWG), 60&deg;C NM-B vs 75&deg;C THHN ampacity, single/three-phase voltage drop, and overcurrent breaker sizing calculators for North American homeowners, EV drivers, solar DIYers, and RV owners.</p><p><em>Disclaimer: All calculations are engineering estimates based on standard NEC Table 310.16 ampacity tables and NEC 240.4(D) rules. Always consult local building codes and a licensed electrician before installation.</em></p>"
    ),
    "privacy.html": (
        f"Privacy Policy | {SITE_NAME}",
        "Privacy Policy",
        f"<p>At <strong>{SITE_NAME}</strong> ({DOMAIN_URL}), we respect visitor privacy. We use standard analytics and Google AdSense cookies to serve relevant advertisements.</p><h2>Amazon Associate Disclosure</h2><p>{SITE_NAME} is a participant in the Amazon Services LLC Associates Program, an affiliate advertising program designed to provide a means for sites to earn advertising fees by linking to Amazon.com.</p>"
    ),
    "contact.html": (
        f"Contact Us | {SITE_NAME}",
        "Contact Us",
        f"<p>Have a suggestion for a new EV charger, solar inverter, or subpanel scenario? Contact our technical team at <strong>{CONTACT_EMAIL}</strong>.</p>"
    )
}

for filename, (page_title, h1_title, body_html) in static_pages.items():
    p_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{page_title}</title>
  {ADSENSE_SCRIPT}
  {CSS_STYLE}
</head>
<body>
  {NAVBAR_HTML}
  <div class="article-container">
    <article class="article-card">
      <h1>{h1_title}</h1>
      {body_html}
    </article>
  </div>
  {FOOTER_HTML}
</body>
</html>"""
    with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
        f.write(p_html)

# 8. sitemap.xml, robots.txt, ads.txt 생성
sitemap_xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for url in sitemap_urls:
    sitemap_xml += f"  <url><loc>{url}</loc></url>\n"
sitemap_xml += "</urlset>"
with open(os.path.join(OUTPUT_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
    f.write(sitemap_xml)

with open(os.path.join(OUTPUT_DIR, "robots.txt"), "w", encoding="utf-8") as f:
    f.write(f"User-agent: *\nAllow: /\nSitemap: {DOMAIN_URL}/sitemap.xml\n")

with open(os.path.join(OUTPUT_DIR, "ads.txt"), "w", encoding="utf-8") as f:
    f.write(f"google.com, {ADSENSE_PUB_ID.replace('ca-', '')}, DIRECT, f08c47fec0942fa0\n")

print(f"완료! 총 {len(SCENARIOS)}개 계산기 페이지 생성됨 ({OUTPUT_DIR} 폴더)")

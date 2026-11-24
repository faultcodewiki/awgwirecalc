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

# 3. 공통 스타일시트 (북미 엔지니어링 툴 UI)
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
    padding: 2.8rem 1.25rem 3.2rem;
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
    padding: 1.8rem;
    box-shadow: 0 10px 28px rgba(15, 23, 42, 0.08);
    margin-bottom: 2rem;
  }
  .calc-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-bottom: 1.25rem;
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
  .calc-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0.95rem;
    margin-bottom: 1.2rem;
  }
  .field label {
    display: block;
    font-size: 0.78rem;
    font-weight: 700;
    color: var(--text-sub);
    margin-bottom: 0.35rem;
    text-transform: uppercase;
    letter-spacing: 0.03em;
  }
  .field select, .field input {
    width: 100%;
    padding: 0.72rem 0.85rem;
    border: 1.5px solid #cbd5e1;
    border-radius: 10px;
    font-size: 0.98rem;
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
    margin-bottom: 1.35rem;
    font-size: 0.9rem;
    font-weight: 600;
    color: var(--text-sub);
  }
  .toggle-row input { width: 17px; height: 17px; accent-color: var(--primary); cursor: pointer; }

  .results-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0.85rem;
    background: #0f172a;
    color: #fff;
    padding: 1.25rem;
    border-radius: 12px;
  }
  .res-item {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 10px;
    padding: 0.85rem;
    text-align: center;
  }
  .res-item.primary-res {
    background: rgba(37, 99, 235, 0.32);
    border-color: #60a5fa;
  }
  .res-label {
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    color: #94a3b8;
    font-weight: 700;
    margin-bottom: 0.25rem;
  }
  .res-val { font-size: 1.18rem; font-weight: 800; color: #fff; }
  .res-val.gold { color: #fbbf24; }
  .res-sub { font-size: 0.74rem; color: #cbd5e1; margin-top: 0.2rem; }

  /* 아마존 3종 자재 세트 카드 */
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

  @media (max-width: 760px) {
    .calc-grid, .results-grid { grid-template-columns: repeat(2, 1fr); }
    .kit-grid, .scenario-grid { grid-template-columns: 1fr; }
    .hero h1 { font-size: 1.6rem; }
    .article-card { padding: 1.35rem 1.15rem; }
  }
</style>
"""

# 4. 실시간 자바스크립트 공학 계산 엔진 (NEC 75°C Ampacity + Voltage Drop <= 3%)
CALC_JS = """
<script>
  const AWG_TABLE = [
    { awg: "14 AWG", cmil: 4110, cuAmp: 15, alAmp: 0 },
    { awg: "12 AWG", cmil: 6530, cuAmp: 20, alAmp: 0 },
    { awg: "10 AWG", cmil: 10380, cuAmp: 30, alAmp: 25 },
    { awg: "8 AWG", cmil: 16510, cuAmp: 50, alAmp: 40 },
    { awg: "6 AWG", cmil: 26240, cuAmp: 65, alAmp: 50 },
    { awg: "4 AWG", cmil: 41740, cuAmp: 85, alAmp: 65 },
    { awg: "3 AWG", cmil: 52620, cuAmp: 100, alAmp: 75 },
    { awg: "2 AWG", cmil: 66360, cuAmp: 115, alAmp: 90 },
    { awg: "1 AWG", cmil: 83690, cuAmp: 130, alAmp: 100 },
    { awg: "1/0 AWG", cmil: 105600, cuAmp: 150, alAmp: 120 },
    { awg: "2/0 AWG", cmil: 133100, cuAmp: 175, alAmp: 135 },
    { awg: "3/0 AWG", cmil: 167800, cuAmp: 200, alAmp: 155 },
    { awg: "4/0 AWG", cmil: 211600, cuAmp: 230, alAmp: 180 },
    { awg: "250 kcmil", cmil: 250000, cuAmp: 255, alAmp: 205 }
  ];
  const BREAKERS = [15, 20, 25, 30, 35, 40, 45, 50, 60, 70, 80, 90, 100, 110, 125, 150, 175, 200, 225, 250];

  function runWireCalc() {
    const volts = parseFloat(document.getElementById('calcVolts').value) || 240;
    const amps = parseFloat(document.getElementById('calcAmps').value) || 48;
    const dist = parseFloat(document.getElementById('calcDist').value) || 50;
    const mat = document.getElementById('calcMat').value;
    const isCont = document.getElementById('calcCont').checked;

    const reqAmpacity = isCont ? amps * 1.25 : amps;
    const K = (mat === 'copper') ? 12.9 : 21.2;

    let selected = AWG_TABLE[AWG_TABLE.length - 1];
    let vDropPct = 0;

    for (let i = 0; i < AWG_TABLE.length; i++) {
      const row = AWG_TABLE[i];
      const maxA = (mat === 'copper') ? row.cuAmp : row.alAmp;
      if (maxA < reqAmpacity) continue;
      const vd = (2 * K * amps * dist) / row.cmil;
      const pct = (vd / volts) * 100;
      if (pct <= 3.0) {
        selected = row;
        vDropPct = pct;
        break;
      }
    }

    if (vDropPct === 0) {
      const vd = (2 * K * amps * dist) / selected.cmil;
      vDropPct = (vd / volts) * 100;
    }

    let recBreaker = BREAKERS[BREAKERS.length - 1];
    for (let b of BREAKERS) {
      if (b >= reqAmpacity) { recBreaker = b; break; }
    }

    document.getElementById('resAwg').textContent = selected.awg;
    document.getElementById('resMatSub').textContent = (mat === 'copper') ? 'Copper (75°C NEC)' : 'Aluminum (75°C NEC)';
    document.getElementById('resBreaker').textContent = recBreaker + ' Amp';
    document.getElementById('resBreakerSub').textContent = isCont ? 'Includes 125% NEC factor' : 'Standard non-continuous';
    document.getElementById('resDrop').textContent = vDropPct.toFixed(2) + '%';
    document.getElementById('resDropSub').textContent = (vDropPct <= 3.0) ? 'PASS (Under 3% NEC limit)' : 'Exceeds 3% limit';
    document.getElementById('resWatts').textContent = ((volts * amps) / 1000).toFixed(2) + ' kW';
  }

  window.addEventListener('DOMContentLoaded', runWireCalc);
</script>
"""

def render_calc_widget(default_v=240, default_a=48, default_d=50, default_cont=True):
    v_opts = "".join(
        f'<option value="{v}" {"selected" if v == default_v else ""}>{v}V {"(EV / Dryer / Subpanel)" if v==240 else "(Standard Outlet)" if v==120 else "(Solar / RV Bank)"}</option>'
        for v in [12, 24, 48, 120, 240]
    )
    checked_attr = "checked" if default_cont else ""
    return f"""
    <div class="calc-box">
      <div class="calc-header">
        <h2>&#9889; Interactive NEC Wire Size &amp; Voltage Drop Calculator</h2>
        <span class="nec-badge">US / Canada AWG Standard</span>
      </div>
      <div class="calc-grid">
        <div class="field">
          <label for="calcVolts">System Voltage (V)</label>
          <select id="calcVolts" onchange="runWireCalc()">{v_opts}</select>
        </div>
        <div class="field">
          <label for="calcAmps">Load Current (Amps)</label>
          <input type="number" id="calcAmps" value="{default_a}" min="1" max="250" oninput="runWireCalc()">
        </div>
        <div class="field">
          <label for="calcDist">One-Way Distance (Feet)</label>
          <input type="number" id="calcDist" value="{default_d}" min="1" max="1000" oninput="runWireCalc()">
        </div>
        <div class="field">
          <label for="calcMat">Conductor Material</label>
          <select id="calcMat" onchange="runWireCalc()">
            <option value="copper" selected>Copper (Cu)</option>
            <option value="aluminum">Aluminum (Al)</option>
          </select>
        </div>
      </div>
      <label class="toggle-row">
        <input type="checkbox" id="calcCont" {checked_attr} onchange="runWireCalc()">
        <span>Continuous Load (Runs 3+ hours: EV Charger, Solar, Heater — applies NEC 125% safety rule)</span>
      </label>
      <div class="results-grid">
        <div class="res-item primary-res">
          <div class="res-label">Minimum Wire Size</div>
          <div class="res-val gold" id="resAwg">6 AWG</div>
          <div class="res-sub" id="resMatSub">Copper (75°C NEC)</div>
        </div>
        <div class="res-item">
          <div class="res-label">Breaker / Fuse Size</div>
          <div class="res-val" id="resBreaker">60 Amp</div>
          <div class="res-sub" id="resBreakerSub">Includes 125% NEC factor</div>
        </div>
        <div class="res-item">
          <div class="res-label">Voltage Drop</div>
          <div class="res-val" id="resDrop">1.29%</div>
          <div class="res-sub" id="resDropSub">PASS (Under 3% NEC limit)</div>
        </div>
        <div class="res-item">
          <div class="res-label">Total Power</div>
          <div class="res-val" id="resWatts">11.52 kW</div>
          <div class="res-sub">Max Circuit Load</div>
        </div>
      </div>
    </div>
    """

NAVBAR_HTML = f"""
  <nav class="navbar">
    <div class="nav-inner">
      <a class="brand" href="index.html">
        <span class="brand-icon">&#9889;</span>
        <span>{SITE_NAME}</span>
      </a>
      <div class="nav-links">
        <a href="index.html">Calculator &amp; Guides</a>
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
        <a href="about.html">About Us</a>
        <a href="privacy.html">Privacy Policy</a>
        <a href="contact.html">Contact</a>
      </div>
      <div>&copy; 2026 {SITE_NAME}. North American AWG Wire Gauge &amp; NEC Ampacity Reference Tool.</div>
      <div style="margin-top:0.35rem; font-size:0.78rem; color:#64748b;">Engineering Reference Disclaimer: Calculations follow standard NEC ampacity and 3% voltage drop formulas for educational estimation only. Always verify local electrical codes and consult a licensed electrician. As an Amazon Associate, we earn from qualifying purchases.</div>
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
            f"Can I use aluminum wire instead of copper for {item['amps']} Amps?",
            f"Yes, for feeder runs (such as subpanels or RV pedestals), aluminum THHN/XHHW or SER cable can be used if upsized by 1 to 2 AWG sizes (check the Aluminum option in our calculator above) and terminated with anti-oxidant compound on AL-rated lugs."
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
  <meta name="description" content="Free North American AWG wire gauge, voltage drop, and circuit breaker calculator for EV chargers, solar inverters, RVs, hot tubs, and garage subpanels.">
  {ADSENSE_SCRIPT}
  {CSS_STYLE}
</head>
<body>
  {NAVBAR_HTML}
  <section class="hero">
    <div class="hero-inner">
      <span class="hero-tag">&#9889; NEC Compliant &bull; Copper &amp; Aluminum AWG</span>
      <h1>AWG Wire Size &amp; Breaker Calculator</h1>
      <p>Calculate exact wire gauge, voltage drop, and breaker size for EV chargers, solar arrays, RVs, and home subpanels.</p>
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
        f"<p><strong>{SITE_NAME}</strong> provides fast, NEC-aligned wire gauge (AWG), voltage drop, and overcurrent breaker sizing calculators for North American homeowners, EV drivers, solar DIYers, and RV owners.</p><p><em>Disclaimer: All calculations are engineering estimates based on standard NEC 75°C ampacity tables and a 3% voltage drop threshold. Always consult local building codes and a licensed electrician before installation.</em></p>"
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

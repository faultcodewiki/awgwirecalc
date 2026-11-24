import os
import sys
import json
import glob
import time
import urllib.request
import urllib.error
import urllib.parse

# ==========================================
# 기본 설정 (손댈 필요 없음)
# ==========================================
DOMAIN_URL = "https://awgwirecalc.com"
ADSENSE_CLIENT = "ca-pub-8285144464443420"
APPROVED_FLAG_FILE = ".adsense_approved"
AUTO_JSON_FILE = "scenarios_auto.json"

MAX_SCENARIOS = 100   # 총 100개 도달 시 영구 자동 종료
BATCH_SIZE = 7        # 회당 7개씩 생성 (주 2회 = 주당 14개)

VALID_CATEGORIES = {
    "EV Charger",
    "Solar & Off-Grid",
    "RV & Marine",
    "Home & Garage",
}

# 중복 스팸(Doorway Page) 방지를 위해 엄선한 북미 고단가 실수요 장비 86종 큐
# 형식: (slug, category, equipment, voltage, amps, distance_ft, continuous)
TOPIC_POOL = [
    # EV Charger (14종)
    ("80-amp-ford-charge-station-pro-wire-size-60-feet", "EV Charger", "80A Ford Charge Station Pro / GM 19.2kW EV Charger", 240, 80, 60, True),
    ("24-amp-ev-charger-nema-14-30-wire-size-50-feet", "EV Charger", "24A Level 2 EV Charger on 30A NEMA 14-30 Circuit", 240, 24, 50, True),
    ("16-amp-level-2-ev-charger-nema-6-20-wire-size-60-feet", "EV Charger", "16A 240V Plug-In Level 2 EV Charger (NEMA 6-20)", 240, 16, 60, True),
    ("dual-ev-charger-60-amp-power-sharing-wire-size-80-feet", "EV Charger", "Dual Load-Sharing Level 2 EV Chargers on 60A Circuit", 240, 48, 80, True),
    ("40-amp-hardwired-ev-charger-wire-size-125-feet", "EV Charger", "40A Hardwired EV Charger (Detached Parking Pad Run)", 240, 40, 125, True),
    ("12-amp-level-1-ev-charger-120v-wire-size-75-feet", "EV Charger", "Dedicated 120V 20A Outdoor Level 1 EV Charging Outlet", 120, 12, 75, True),
    ("64-amp-commercial-208v-ev-charger-wire-size-100-feet", "EV Charger", "Commercial 64A 208V Pedestal Level 2 EV Charger", 208, 64, 100, True),
    ("nema-6-50-ev-charger-receptacle-wire-size-60-feet", "EV Charger", "40A EV Charger Using 3-Prong NEMA 6-50 Outlet", 240, 40, 60, True),
    ("48v-golf-cart-charger-outlet-wire-size-50-feet", "EV Charger", "Dedicated 48V Club Car / EZGO Golf Cart Charger Circuit", 120, 15, 50, True),
    ("480v-3-phase-forklift-battery-charger-wire-size-80-feet", "EV Charger", "Warehouse 480V Industrial Electric Forklift Charger", 480, 30, 80, True),
    ("48-amp-ev-charger-underground-driveway-run-150-feet", "EV Charger", "48A Outdoor EV Pedestal (150 ft Underground Trench)", 240, 48, 150, True),
    ("30-amp-ev-charger-100a-panel-home-wire-size-65-feet", "EV Charger", "30A Load-Managed Level 2 EVSE for 100A Service Homes", 240, 30, 65, True),
    ("commercial-ebike-battery-charging-cabinet-wire-size-70-feet", "EV Charger", "20A Commercial E-Bike & Scooter Battery Charging Locker", 120, 16, 70, True),
    ("electric-utv-tractor-barn-charger-wire-size-120-feet", "EV Charger", "32A Barn Level 2 Charger for Electric Tractor / UTV", 240, 32, 120, True),

    # Solar & Off-Grid (20종)
    ("5000w-48v-hybrid-solar-inverter-cable-size-10-feet", "Solar & Off-Grid", "5000W 48V Hybrid Off-Grid Inverter & Server Rack Battery", 48, 122, 10, True),
    ("1000w-12v-pure-sine-inverter-wire-size-8-feet", "Solar & Off-Grid", "1000W 12V Pure Sine Wave Camper Van Inverter", 12, 98, 8, True),
    ("1500w-12v-inverter-battery-cable-size-10-feet", "Solar & Off-Grid", "1500W 12V Off-Grid Cabin Power Inverter", 12, 147, 10, True),
    ("4000w-24v-inverter-charger-cable-size-10-feet", "Solar & Off-Grid", "4000W 24V Split-Phase Solar Inverter Charger", 24, 196, 10, True),
    ("6000w-48v-split-phase-solar-inverter-wire-size-12-feet", "Solar & Off-Grid", "6000W 48V Split-Phase Off-Grid Solar Inverter", 48, 147, 12, True),
    ("10kw-48v-whole-home-solar-inverter-cable-size-10-feet", "Solar & Off-Grid", "10kW 48V Whole-Home Hybrid Solar Inverter Bank", 48, 245, 10, True),
    ("800w-ground-mount-solar-array-wire-size-100-feet", "Solar & Off-Grid", "800W Ground-Mount Solar Array to MPPT Controller", 48, 20, 100, True),
    ("1200w-solar-combiner-box-to-mppt-wire-size-75-feet", "Solar & Off-Grid", "1200W Rooftop Solar Combiner Box Feeder Run", 48, 28, 75, True),
    ("60-amp-mppt-charge-controller-battery-wire-size-10-feet", "Solar & Off-Grid", "60A MPPT Solar Charge Controller to LiFePO4 Busbar", 24, 60, 10, True),
    ("100-amp-mppt-solar-controller-cable-size-8-feet", "Solar & Off-Grid", "100A MPPT Charge Controller Battery Output Cables", 48, 100, 8, True),
    ("50-amp-dc-to-dc-alternator-charger-wire-size-20-feet", "Solar & Off-Grid", "50A Sprinter Van DC-to-DC Alternator Battery Charger", 12, 50, 20, True),
    ("30-amp-dc-dc-truck-camper-charger-wire-size-25-feet", "Solar & Off-Grid", "30A Pickup Truck Bed Camper DC-DC Auxiliary Charger", 12, 30, 25, True),
    ("12v-diesel-parking-heater-camper-wire-size-15-feet", "Solar & Off-Grid", "12V 5kW Diesel Air Parking Heater Glow Plug Harness", 12, 15, 15, False),
    ("12v-compressor-camper-fridge-wire-size-20-feet", "Solar & Off-Grid", "12V DC Portable Overlanding Refrigerator Freezer", 12, 8, 20, True),
    ("24v-dc-solar-submersible-well-pump-wire-size-150-feet", "Solar & Off-Grid", "Off-Grid 24V DC Solar Direct Submersible Water Pump", 24, 12, 150, True),
    ("48v-lifepo4-server-rack-battery-busbar-cable-6-feet", "Solar & Off-Grid", "48V 100Ah LiFePO4 Server Rack Parallel Battery Bank", 48, 200, 6, True),
    ("enphase-microinverter-solar-ac-branch-wire-size-90-feet", "Solar & Off-Grid", "240V Rooftop Solar Microinverter AC Trunk & Home Run", 240, 20, 90, True),
    ("24v-1000w-wind-turbine-tower-wire-size-120-feet", "Solar & Off-Grid", "1000W 24V Off-Grid Wind Turbine Tower Feeder", 24, 42, 120, True),
    ("50-amp-generator-inlet-box-interlock-wire-size-40-feet", "Solar & Off-Grid", "50A CS6375 / SS2-50P Home Backup Generator Inlet Box", 240, 50, 40, False),
    ("30-amp-generator-transfer-switch-l14-30-wire-size-50-feet", "Solar & Off-Grid", "30A NEMA L14-30P Portable Generator Transfer Switch", 240, 30, 50, False),

    # RV & Marine (18종)
    ("24v-80lb-trolling-motor-boat-wire-size-20-feet", "RV & Marine", "24V 80lb Thrust Bow-Mount Marine Trolling Motor", 24, 56, 20, True),
    ("48v-electric-outboard-boat-motor-wire-size-20-feet", "RV & Marine", "48V 3kW-5kW Electric Outboard Pontoon Boat Motor", 48, 95, 20, True),
    ("12v-55lb-trolling-motor-kayak-jon-boat-wire-size-16-feet", "RV & Marine", "12V 55lb Thrust Fishing Boat / Kayak Trolling Motor", 12, 50, 16, True),
    ("12v-1000w-marine-anchor-windlass-wire-size-30-feet", "RV & Marine", "12V 1000W Boat Bow Anchor Windlass Winch", 12, 85, 30, False),
    ("12v-boat-bow-thruster-battery-cable-size-18-feet", "RV & Marine", "12V Marine Bow Thruster High-Current Battery Run", 12, 220, 18, False),
    ("garmin-livescope-marine-fish-finder-wire-size-18-feet", "RV & Marine", "Dedicated Sonar / Garmin LiveScope Clean Power Harness", 12, 10, 18, True),
    ("12v-2000-gph-marine-bilge-pump-wire-size-20-feet", "RV & Marine", "12V 2000 GPH Heavy-Duty Submersible Boat Bilge Pump", 12, 14, 20, True),
    ("30-amp-marine-shore-power-dock-wire-size-100-feet", "RV & Marine", "30A 120V Boat Dock Shore Power Pedestal (ELCI)", 120, 30, 100, True),
    ("50-amp-240v-marine-dock-pedestal-wire-size-150-feet", "RV & Marine", "50A 125/250V Marina Boat Slip Power Pedestal", 240, 50, 150, True),
    ("55-amp-rv-converter-lifepo4-charger-wire-size-10-feet", "RV & Marine", "55A RV 12V Lithium Battery Converter Charger Upgrade", 12, 55, 10, True),
    ("12000-lb-12v-truck-winch-cable-size-12-feet", "RV & Marine", "12,000 lb Off-Road Truck & Trailer Electric Winch", 12, 240, 12, False),
    ("rv-hydraulic-leveling-jack-pump-wire-size-15-feet", "RV & Marine", "Fifth-Wheel RV 12V Hydraulic Leveling & Slide Pump", 12, 80, 15, False),
    ("1500w-rms-car-audio-amplifier-power-wire-size-17-feet", "RV & Marine", "1500W RMS Car / Marine Subwoofer Amplifier Power Kit", 12, 130, 17, False),
    ("12v-heavy-duty-onboard-air-compressor-wire-size-18-feet", "RV & Marine", "12V Dual Onboard Truck Air Suspension / Tire Compressor", 12, 40, 18, False),
    ("50-amp-rv-pad-pedestal-200-feet-long-run", "RV & Marine", "50A Homestead RV Pad Pedestal (200 ft Trench Run)", 240, 50, 200, False),
    ("marine-helm-12-circuit-fuse-block-feeder-15-feet", "RV & Marine", "Boat Helm Blue Sea 12V Electronics Fuse Block Feeder", 12, 25, 15, True),
    ("12v-electric-fishing-downrigger-wire-size-16-feet", "RV & Marine", "Dual 12V Electric Marine Fishing Downriggers", 12, 25, 16, False),
    ("dump-trailer-12v-hydraulic-pump-charge-wire-25-feet", "RV & Marine", "Tow Vehicle to Dump Trailer 12V Hydraulic Battery Line", 12, 150, 25, False),

    # Home & Garage (34종)
    ("1hp-240v-submersible-well-pump-wire-size-200-feet", "Home & Garage", "1 HP 240V Deep Submersible Residential Well Pump", 240, 10, 200, False),
    ("1-5hp-240v-deep-well-pump-wire-size-300-feet", "Home & Garage", "1.5 HP 240V Deep Well Submersible Water Pump", 240, 13, 300, False),
    ("27kw-electric-tankless-water-heater-wire-size-40-feet", "Home & Garage", "27kW Whole-House Electric Tankless Water Heater (3x40A)", 240, 38, 40, False),
    ("18kw-electric-tankless-water-heater-wire-size-35-feet", "Home & Garage", "18kW Electric Tankless Water Heater (Dual 40A Circuits)", 240, 38, 35, False),
    ("50-gallon-electric-water-heater-4500w-wire-size-50-feet", "Home & Garage", "4500W-5500W 240V Standard Tank Electric Water Heater", 240, 23, 50, True),
    ("40-amp-induction-range-cooktop-wire-size-45-feet", "Home & Garage", "240V Slide-In Induction Range & Electric Cooktop", 240, 40, 45, False),
    ("50-amp-double-wall-oven-240v-wire-size-50-feet", "Home & Garage", "50A Built-In Electric Double Wall Oven Circuit", 240, 50, 50, False),
    ("30-amp-electric-dryer-nema-14-30-wire-size-45-feet", "Home & Garage", "240V 30A 4-Prong Electric Clothes Dryer (NEMA 14-30)", 240, 24, 45, True),
    ("9kw-240v-home-sauna-heater-wire-size-50-feet", "Home & Garage", "9kW 240V Traditional Finnish Electric Sauna Stove", 240, 38, 50, True),
    ("6kw-240v-barrel-sauna-heater-wire-size-40-feet", "Home & Garage", "6kW 240V Outdoor Barrel / Home Sauna Heater", 240, 25, 40, True),
    ("5hp-240v-garage-air-compressor-wire-size-50-feet", "Home & Garage", "True 5 HP 240V 80-Gallon Single-Phase Shop Air Compressor", 240, 26, 50, False),
    ("7-5hp-240v-shop-air-compressor-wire-size-60-feet", "Home & Garage", "7.5 HP 240V Commercial Garage Air Compressor", 240, 40, 60, False),
    ("50-amp-swimming-pool-heat-pump-wire-size-75-feet", "Home & Garage", "240V Electric Swimming Pool Heat Pump Heater", 240, 40, 75, True),
    ("240v-variable-speed-pool-pump-wire-size-65-feet", "Home & Garage", "240V Inground Variable-Speed Swimming Pool Pump", 240, 12, 65, True),
    ("48-amp-pottery-ceramic-kiln-240v-wire-size-40-feet", "Home & Garage", "240V 48A Electric Ceramic & Pottery Studio Kiln", 240, 48, 40, True),
    ("125-amp-detached-workshop-subpanel-wire-size-150-feet", "Home & Garage", "125A Detached Workshop / Garage Subpanel Feeder", 240, 125, 150, False),
    ("200-amp-residential-service-entrance-wire-size-100-feet", "Home & Garage", "200A Main Residential Underground Service Feeder", 240, 200, 100, False),
    ("20-amp-backyard-office-shed-trench-wire-size-100-feet", "Home & Garage", "120V 20A Backyard Shed / Office Underground Circuit", 120, 16, 100, False),
    ("100-amp-pole-barn-feeder-wire-size-250-feet", "Home & Garage", "100A Detached Pole Barn Feeder (250 ft Long Run)", 240, 100, 250, False),
    ("3-ton-central-ac-condenser-240v-wire-size-50-feet", "Home & Garage", "3-Ton 240V Central Air Conditioner Outdoor Condenser", 240, 22, 50, True),
    ("5-ton-central-heat-pump-condenser-wire-size-60-feet", "Home & Garage", "5-Ton 240V Split-System Heat Pump Condenser", 240, 35, 60, True),
    ("10kw-electric-furnace-heat-strip-wire-size-45-feet", "Home & Garage", "10kW 240V Electric Air Handler Auxiliary Heat Strip", 240, 42, 45, True),
    ("40-amp-240v-plasma-cutter-shop-outlet-wire-size-40-feet", "Home & Garage", "240V CNC / Handheld Shop Air Plasma Cutter Circuit", 240, 32, 40, False),
    ("3hp-240v-woodshop-cyclone-dust-collector-wire-50-feet", "Home & Garage", "3 HP 240V Woodshop Cyclone Dust Collector Motor", 240, 16, 50, True),
    ("3hp-240v-cabinet-table-saw-wire-size-35-feet", "Home & Garage", "3 HP 240V Industrial Cabinet Table Saw Circuit", 240, 14, 35, False),
    ("2hp-240v-sewage-grinder-ejector-pump-wire-size-80-feet", "Home & Garage", "2 HP 240V Residential Sewage Grinder / Septic Pump", 240, 15, 80, False),
    ("dedicated-120v-basement-sump-pump-wire-size-50-feet", "Home & Garage", "3/4 HP 120V Primary Basement Sump Pump Circuit", 120, 12, 50, False),
    ("300w-12v-landscape-lighting-transformer-wire-150-feet", "Home & Garage", "300W Low-Voltage Outdoor Landscape Lighting Run", 12, 22, 150, True),
    ("roof-gutter-ice-dam-heat-cable-circuit-wire-60-feet", "Home & Garage", "120V Self-Regulating Roof & Gutter De-Icing Heat Trace", 120, 16, 60, True),
    ("240v-heated-bathroom-tile-floor-mat-wire-size-35-feet", "Home & Garage", "240V Electric Radiant Floor Heating Mat & Thermostat", 240, 12, 35, True),
    ("1500w-barn-livestock-tank-deicer-wire-size-125-feet", "Home & Garage", "1500W 120V Livestock Water Tank Heater (125 ft Barn Run)", 120, 13, 125, True),
    ("240v-waterfront-boat-lift-motor-wire-size-150-feet", "Home & Garage", "1 HP 240V Lakefront Boat Lift Canopy Motor Circuit", 240, 8, 150, False),
    ("residential-home-elevator-240v-30a-wire-size-50-feet", "Home & Garage", "240V Residential Home Elevator / Lift Disconnect Circuit", 240, 24, 50, False),
    ("240v-30a-l6-30r-home-server-miner-pdu-wire-40-feet", "Home & Garage", "240V 30A NEMA L6-30R Home Lab Server / ASIC PDU Circuit", 240, 24, 40, True),
]

AWG_TABLE = [
    ("14 AWG", 4110, 15),
    ("12 AWG", 6530, 20),
    ("10 AWG", 10380, 30),
    ("8 AWG", 16510, 50),
    ("6 AWG", 26240, 65),
    ("4 AWG", 41740, 85),
    ("3 AWG", 52620, 100),
    ("2 AWG", 66360, 115),
    ("1 AWG", 83690, 130),
    ("1/0 AWG", 105600, 150),
    ("2/0 AWG", 133100, 175),
    ("3/0 AWG", 167800, 200),
    ("4/0 AWG", 211600, 230),
    ("250 kcmil", 250000, 255),
]
BREAKERS = [15, 20, 25, 30, 35, 40, 45, 50, 60, 70, 80, 90, 100, 110, 125, 150, 175, 200, 225, 250]


def calc_nec_spec(volts, amps, dist_ft, continuous):
    """build.py 계산기와 100% 동일한 NEC 75C 구리선 + 3% 전압강하 정밀 계산"""
    req_amp = amps * 1.25 if continuous else amps
    phase_factor = 1.732 if volts == 480 else 2.0
    selected_awg, selected_cmil = AWG_TABLE[-1][0], AWG_TABLE[-1][1]

    for awg_name, cmil, cu75_max in AWG_TABLE:
        if cu75_max < req_amp:
            continue
        vd_pct = ((phase_factor * 12.9 * amps * dist_ft) / cmil / volts) * 100.0
        if vd_pct <= 3.0:
            selected_awg, selected_cmil = awg_name, cmil
            break

    vdrop_pct = ((phase_factor * 12.9 * amps * dist_ft) / selected_cmil / volts) * 100.0
    rec_brk = BREAKERS[-1]
    for b in BREAKERS:
        if b >= req_amp:
            rec_brk = b
            break
    return selected_awg, rec_brk, round(vdrop_pct, 2)


def is_adsense_approved():
    """구글 광고 서버의 공식 도메인 승인 응답(200 OK vs 403 미승인)을 주 2회 단 1회만 가볍게 확인"""
    if os.environ.get("FORCE_GENERATE", "false").lower() == "true":
        print("[수동 실행 모드] 애드센스 대기 없이 즉시 생성을 진행합니다.")
        return True

    if os.path.exists(APPROVED_FLAG_FILE):
        print("[승인 확인됨] 이전 실행에서 애드센스 승인이 이미 확인되었습니다.")
        return True

    encoded_url = urllib.parse.quote(f"{DOMAIN_URL}/", safe="")
    check_url = (
        f"https://googleads.g.doubleclick.net/pagead/ads"
        f"?client={ADSENSE_CLIENT}&output=html&h=280&slotname=auto"
        f"&adk=1812271804&adf=3025194257&w=336&format=336x280"
        f"&url={encoded_url}&ea=0&wgl=1"
    )
    req = urllib.request.Request(
        check_url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "Referer": f"{DOMAIN_URL}/",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=12) as resp:
            if resp.status == 200:
                with open(APPROVED_FLAG_FILE, "w", encoding="utf-8") as f:
                    f.write(f"approved_at={time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}\n")
                print("[축하합니다!] Google AdSense 사이트 승인(200 OK)이 감지되었습니다! 자동 업데이트를 시작합니다.")
                return True
    except urllib.error.HTTPError as e:
        print(f"[심사 대기 중] 현재 Google AdSense 심사 중(응답 코드 {e.code})입니다. 안전한 승인을 위해 새 글을 생성하지 않고 대기합니다.")
        return False
    except Exception as e:
        print(f"[네트워크 대기] 승인 상태 확인 보류({e}). 안전을 위해 다음 스케줄까지 대기합니다.")
        return False
    return False


def get_active_flash_models(api_key):
    """계정에서 현재 사용 가능한 최신 Gemini Flash 모델 목록을 자동으로 조회 (404 에러 원천 차단)"""
    list_url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    candidates = []
    try:
        with urllib.request.urlopen(list_url, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            for m in data.get("models", []):
                methods = m.get("supportedGenerationMethods", [])
                name = m.get("name", "").replace("models/", "")
                low = name.lower()
                if "generateContent" not in methods:
                    continue
                if "gemini" in low and "flash" in low:
                    if any(bad in low for bad in ["tts", "image", "audio", "vision", "embedding"]):
                        continue
                    candidates.append(name)
    except Exception as e:
        print(f"[참고] 모델 목록 자동 조회 실패, 기본 후보 사용: {e}")

    # 최신 안정형 모델을 우선 배치
    preferred = [m for m in candidates if "preview" not in m and "lite" not in m]
    others = [m for m in candidates if m not in preferred]
    ordered = sorted(preferred, reverse=True) + sorted(others, reverse=True)
    for fallback in ["gemini-flash-latest", "gemini-3.5-flash", "gemini-2.5-flash"]:
        if fallback not in ordered:
            ordered.append(fallback)
    return ordered


def call_gemini_json(api_key, models, prompt):
    payload = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.4,
            "responseMimeType": "application/json",
        },
    }).encode("utf-8")

    for model_name in models:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
        req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"}, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=90) as resp:
                body = json.loads(resp.read().decode("utf-8"))
                text = body["candidates"][0]["content"]["parts"][0]["text"].strip()
                if text.startswith("```"):
                    text = text.strip("`").lstrip("json").strip()
                return json.loads(text)
        except urllib.error.HTTPError as e:
            err_msg = e.read().decode("utf-8", errors="ignore")[:180]
            print(f"[모델 자동 전환] {model_name} 응답 {e.code} -> 다음 모델 시도 ({err_msg})")
            time.sleep(2)
        except Exception as e:
            print(f"[재시도] {model_name} 호출 오류: {e}")
            time.sleep(2)
    raise RuntimeError("사용 가능한 모든 Gemini 모델 호출에 실패했습니다.")


def clean_query(q_str):
    raw = str(q_str).replace("+", " ").replace("%2F", "/").strip()
    return urllib.parse.quote_plus(raw)


def main():
    # 1. 현재 총 시나리오 개수 파악
    seen_slugs = set()
    for jf in sorted(glob.glob("scenarios*.json")):
        try:
            with open(jf, "r", encoding="utf-8") as f:
                for item in json.load(f):
                    seen_slugs.add(item["slug"].strip().lower())
        except Exception as e:
            print(f"[경고] {jf} 읽기 오류: {e}")

    total_count = len(seen_slugs)
    print(f"[현재 상태] 등록된 전체 가이드 수: {total_count} / 목표 {MAX_SCENARIOS}개")

    if total_count >= MAX_SCENARIOS:
        print(f"[영구 완료] 목표 수량({MAX_SCENARIOS}개)이 모두 채워졌습니다! API 호출 없이 종료합니다.")
        sys.exit(0)

    # 2. 구글 애드센스 승인 상태 확인
    if not is_adsense_approved():
        sys.exit(0)

    # 3. 아직 생성하지 않은 고유 장비 토픽 추출
    remaining_slots = MAX_SCENARIOS - total_count
    target_n = min(BATCH_SIZE, remaining_slots)
    pending_topics = [t for t in TOPIC_POOL if t[0].lower() not in seen_slugs][:target_n]

    if not pending_topics:
        print("[영구 완료] 준비된 고유 시나리오 큐가 모두 생성 완료되었습니다.")
        sys.exit(0)

    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not api_key:
        print("[오류] GEMINI_API_KEY 시크릿이 설정되어 있지 않습니다.")
        sys.exit(1)

    models = get_active_flash_models(api_key)
    print(f"[모델 준비 완료] 우선 사용 모델: {models[0]} (이번 회차 생성 목표: {len(pending_topics)}개)")

    specs_input = []
    for slug, cat, equip, volts, amps, dist, cont in pending_topics:
        awg_cu, brk_amp, vdrop = calc_nec_spec(volts, amps, dist, cont)
        specs_input.append({
            "slug": slug,
            "category": cat,
            "equipment": equip,
            "voltage": volts,
            "amps": amps,
            "distance": dist,
            "continuous": cont,
            "verified_awg_copper_75c": f"{awg_cu} Copper",
            "verified_breaker_amps": f"{brk_amp} Amp",
            "verified_vdrop_pct": vdrop,
        })

    prompt = f"""You are a licensed North American Master Electrician writing concise, accurate NEC wire sizing guides for AWGWireCalc.com.
Generate a JSON array of {len(specs_input)} objects matching the EXACT input scenarios below.
Do NOT change slug, category, equipment, voltage, amps, distance, or continuous values.
Use the verified_awg_copper_75c and verified_breaker_amps so the text matches our NEC 310.16 calculator 100%.

Input scenarios:
{json.dumps(specs_input, indent=2)}

Each output object in the JSON array MUST contain these exact keys:
- "slug": exact string from input
- "category": exact string from input
- "title": natural SEO title including equipment/amps, Wire Size, and distance in feet (under 68 chars)
- "equipment": exact string from input
- "voltage": exact number from input
- "amps": exact number from input
- "distance": exact number from input
- "continuous": exact boolean from input
- "rec_awg_cu": start with exact verified_awg_copper_75c followed by cable/insulation type in parentheses, e.g. "6 AWG Copper (THHN in Conduit)" or "2/0 AWG Pure Copper (Welding/Battery Cable)"
- "rec_breaker": start with exact verified_breaker_amps followed by specific breaker/fuse type (e.g. "60 Amp 2-Pole GFCI Breaker" or "150 Amp Class T DC Fuse")
- "summary": 1-2 authoritative sentences stating exact wire size, breaker/fuse, continuous factor or voltage drop percentage ({specs_input[0]['verified_vdrop_pct']}% style), and practical reason.
- "notes": array of exactly 3 specific, non-generic bullet strings referencing relevant NEC articles (e.g. NEC 310.16, 240.4, 430, 422, 625, 680, 690, or ABYC for marine), conduit/burial/lug rating, and common DIY mistakes.
- "wire_item": specific Amazon buyer product title for the recommended copper wire/cable
- "wire_query": concise Amazon search keywords for that wire
- "breaker_item": specific Amazon buyer product title for the breaker, disconnect, or fuse block
- "breaker_query": concise Amazon search keywords for that breaker/fuse
- "gear_item": specific Amazon buyer product title for the main equipment or installation kit
- "gear_query": concise Amazon search keywords for that equipment
Return ONLY a valid JSON array."""

    generated_list = call_gemini_json(api_key, models, prompt)

    auto_existing = []
    if os.path.exists(AUTO_JSON_FILE):
        with open(AUTO_JSON_FILE, "r", encoding="utf-8") as f:
            auto_existing = json.load(f)

    input_map = {x["slug"]: x for x in specs_input}
    added = 0
    for obj in generated_list:
        slug = str(obj.get("slug", "")).strip()
        if slug not in input_map or slug.lower() in seen_slugs:
            continue
        ref = input_map[slug]
        clean_obj = {
            "slug": ref["slug"],
            "category": ref["category"] if ref["category"] in VALID_CATEGORIES else "Home & Garage",
            "title": str(obj.get("title", f"{ref['equipment']} Wire Size ({ref['distance']} Feet)")).strip(),
            "equipment": ref["equipment"],
            "voltage": ref["voltage"],
            "amps": ref["amps"],
            "distance": ref["distance"],
            "continuous": ref["continuous"],
            "rec_awg_cu": str(obj.get("rec_awg_cu", ref["verified_awg_copper_75c"])).strip(),
            "rec_breaker": str(obj.get("rec_breaker", f"{ref['verified_breaker_amps']} Breaker")).strip(),
            "summary": str(obj.get("summary", "")).strip(),
            "notes": [str(n).strip() for n in obj.get("notes", [])[:3]] or ["Verify terminal temperature ratings per NEC 110.14(C)."],
            "wire_item": str(obj.get("wire_item", f"{ref['verified_awg_copper_75c']} Wire")).strip(),
            "wire_query": clean_query(obj.get("wire_query", f"{ref['verified_awg_copper_75c']} wire")),
            "breaker_item": str(obj.get("breaker_item", f"{ref['verified_breaker_amps']} Circuit Breaker")).strip(),
            "breaker_query": clean_query(obj.get("breaker_query", f"{ref['verified_breaker_amps']} breaker")),
            "gear_item": str(obj.get("gear_item", ref["equipment"])).strip(),
            "gear_query": clean_query(obj.get("gear_query", ref["equipment"])),
        }
        auto_existing.append(clean_obj)
        seen_slugs.add(slug.lower())
        added += 1

    if added > 0:
        with open(AUTO_JSON_FILE, "w", encoding="utf-8") as f:
            json.dump(auto_existing, f, indent=2, ensure_ascii=False)
        print(f"[성공] 신규 가이드 {added}개 추가 완료! (누적 총 {len(seen_slugs)} / {MAX_SCENARIOS}개)")
    else:
        print("[알림] 추가된 항목이 없습니다.")


if __name__ == "__main__":
    main()

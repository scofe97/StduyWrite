# 타입 스펙: type-architecture
# 02-02.big-picture — OpenJDK 소스에서 배포판·내 이미지 JDK까지의 분화 구조
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 628

d = D(
    W,
    H,
    "CONTAINER · 02-02",
    "OpenJDK 소스에서 배포판까지의 분화",
    "업스트림 OpenJDK 소스가 배포처를 거쳐 이미지에 도달할 때 판 번호를 따라 같이 오는 요소와 배포처마다 달라지는 요소의 구분",
    lead="판 번호를 따라 같이 오는 보안 기본값과 배포처에서 달라지는 요소",
)


def zone(x, y, w, h, label, accent=False):
    if accent:
        d.tone(x, y, w, h, ACC, 8, "0A", 1.2)
        d.t(x + 12, y + 20, label, 13, ACC, KR, "start", 600)
    else:
        d.o.append(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" '
            f'fill="{PAPER2}" stroke="{RULE}" stroke-width="0.9" stroke-dasharray="5 4"/>'
        )
        d.t(x + 12, y + 20, label, 13, SOFT, KR, "start", 600)


# ── 3개 존 배치 (왼쪽 → 오른쪽, 4의 배수 좌표) ────────────────────────────
ZY = 88
ZH = 476
Z1_X, Z1_W = 20, 248
Z2_X, Z2_W = 308, 420
Z3_X, Z3_W = 768, 212

zone(Z1_X, ZY, Z1_W, ZH, "1. 업스트림")
zone(Z2_X, ZY, Z2_W, ZH, "2. 배포처")
zone(Z3_X, ZY, Z3_W, ZH, "3. 내 이미지가 받는 JDK", accent=True)

# ── 행 A: 소스 조건 & TCK 계약 경계 & 이미지 기준 ──────────────────────────
RA_Y, RA_H = 120, 76

# Zone 1: OpenJDK 프로젝트
d.box(Z1_X + 12, RA_Y, Z1_W - 24, RA_H, PAPER, RULE, 0.9, 6)
d.t(Z1_X + Z1_W // 2, RA_Y + 22, "OpenJDK 프로젝트", 13, INK, KR, "middle", 600)
d.t(Z1_X + Z1_W // 2, RA_Y + 44, "GPLv2 + Classpath Exception", 11, MUTED, MONO, "middle")
d.t(Z1_X + Z1_W // 2, RA_Y + 64, "jdk17u · jdk21u", 12, INFO, MONO, "middle", 600)

# Zone 2: TCK (OCTLA) 맞추는 것 vs 정의에 없는 것
d.box(Z2_X + 12, RA_Y, Z2_W - 24, RA_H, PAPER, RULE, 0.9, 6)
TCK_W = 188
d.tone(Z2_X + 18, RA_Y + 6, TCK_W, RA_H - 12, OK, 4, "10", 1.0)
d.t(Z2_X + 18 + TCK_W // 2, RA_Y + 24, "TCK 가 맞추는 것", 13, OK, KR, "middle", 600)
d.t(Z2_X + 18 + TCK_W // 2, RA_Y + 42, "사양 구현 · TCK 통과", 13, INK, KR, "middle")
d.t(Z2_X + 18 + TCK_W // 2, RA_Y + 58, "네임스페이스 비확장", 13, INK, KR, "middle")

d.tone(Z2_X + 214, RA_Y + 6, TCK_W, RA_H - 12, WARN, 4, "10", 1.0)
d.t(Z2_X + 214 + TCK_W // 2, RA_Y + 24, "TCK 정의에 없는 것", 13, WARN, KR, "middle", 600)
d.t(Z2_X + 214 + TCK_W // 2, RA_Y + 42, "인증서 묶음 · 벤더 패치", 13, INK, KR, "middle")
d.t(Z2_X + 214 + TCK_W // 2, RA_Y + 58, "지원 기간 · 라이선스", 13, INK, KR, "middle")

# Zone 3: Focal — 이미지 JDK 판별 기준
d.tone(Z3_X + 12, RA_Y, Z3_W - 24, RA_H, ACC, 6, "12", 1.4)
d.t(Z3_X + Z3_W // 2, RA_Y + 28, "이미지의 JDK 기준", 13, ACC, KR, "middle", 600)
d.t(Z3_X + Z3_W // 2, RA_Y + 52, "판 번호 · 배포처 · 포장", 13, INK, KR, "middle")

# ── 행 B/C: 움직이는 객체 (java.security / cacerts) & 배포처 카드 ──────────
JS_Y, JS_H = 232, 48
CA1_Y, CA1_H = 290, 48

# Zone 1 객체 1: java.security (jdk-17.0.18-ga)
d.tone(Z1_X + 12, JS_Y, Z1_W - 24, JS_H, INFO, 4, "14", 1.2)
d.t(Z1_X + 22, JS_Y + 20, "java.security", 12, INFO, MONO, "start", 600)
d.t(Z1_X + Z1_W - 22, JS_Y + 20, "jdk-17.0.18-ga", 11, MUTED, MONO, "end")
d.t(Z1_X + 22, JS_Y + 38, "TLS_RSA_* 끔", 13, INK, KR, "start", 600)

# Zone 1 객체 2: cacerts (OpenJDK 소스 목록)
d.tone(Z1_X + 12, CA1_Y, Z1_W - 24, CA1_H, WARN, 4, "10", 1.1)
d.t(Z1_X + 22, CA1_Y + 20, "cacerts", 12, WARN, MONO, "start", 600)
d.t(Z1_X + Z1_W - 22, CA1_Y + 20, "JEP 319", 11, MUTED, MONO, "end")
d.t(Z1_X + 22, CA1_Y + 38, "OpenJDK 소스 목록", 13, INK, KR, "start")

# Zone 2 — Corretto 카드 (y=204..346)
COR_Y, COR_H = 204, 142
d.box(Z2_X + 12, COR_Y, Z2_W - 24, COR_H, PAPER, RULE, 0.9, 6)
d.t(Z2_X + 24, COR_Y + 20, "Corretto · Amazon", 13, INK, MONO, "start", 600)

# Corretto 내 java.security (동일 객체 반복)
d.tone(Z2_X + 22, JS_Y, Z2_W - 44, JS_H, INFO, 4, "14", 1.2)
d.t(Z2_X + 34, JS_Y + 20, "java.security", 12, INFO, MONO, "start", 600)
d.t(Z2_X + 34, JS_Y + 38, "17.0.18.8.1", 12, INK, MONO, "start")
d.t(Z2_X + Z2_W - 34, JS_Y + 20, "TLS_RSA_* 끔", 13, INK, KR, "end", 600)
d.t(Z2_X + Z2_W - 34, JS_Y + 38, "16쌍·6속성 동일", 13, INFO, KR, "end", 600)

# Corretto 내 cacerts (모양 변화: 병합)
d.tone(Z2_X + 22, CA1_Y, Z2_W - 44, CA1_H, WARN, 4, "14", 1.2)
d.t(Z2_X + 34, CA1_Y + 20, "cacerts", 12, WARN, MONO, "start", 600)
d.t(Z2_X + 34, CA1_Y + 38, "OpenJDK 기본", 13, MUTED, KR, "start")
d.t(Z2_X + Z2_W - 34, CA1_Y + 28, "+ amazon-cacerts", 12, WARN, MONO, "end", 600)

# Zone 2 — Temurin 카드 (y=354..432)
TEM_Y, TEM_H = 354, 78
CA2_Y, CA2_H = 382, 42
d.box(Z2_X + 12, TEM_Y, Z2_W - 24, TEM_H, PAPER, RULE, 0.9, 6)
d.t(Z2_X + 24, TEM_Y + 20, "Temurin · Adoptium", 13, INK, MONO, "start", 600)

# Temurin 내 cacerts (모양 변화: Mozilla CA)
d.tone(Z2_X + 22, CA2_Y, Z2_W - 44, CA2_H, WARN, 4, "14", 1.2)
d.t(Z2_X + 34, CA2_Y + 25, "cacerts", 12, WARN, MONO, "start", 600)
d.t(Z2_X + Z2_W - 34, CA2_Y + 25, "Mozilla CA (기본값)", 13, WARN, KR, "end", 600)

# Zone 2 — 나머지 3종 배포판 (y=452..502, 상단 버스용 20px 여유 확보)
V3_Y, V3_H = 452, 50
VW = 128
VENDORS = [
    ("Red Hat 의", "OpenJDK"),
    ("Zulu", "Azul"),
    ("Microsoft Build", "of OpenJDK"),
]
for i, (v1, v2) in enumerate(VENDORS):
    vx = Z2_X + 12 + i * (VW + 6)
    d.box(vx, V3_Y, VW, V3_H, PAPER, RULE, 0.9, 6)
    d.t(
        vx + VW // 2,
        V3_Y + 21,
        v1,
        13 if any("가" <= c <= "힣" for c in v1) else 12,
        INK,
        KR if any("가" <= c <= "힣" for c in v1) else MONO,
        "middle",
        600,
    )
    d.t(vx + VW // 2, V3_Y + 39, v2, 11, MUTED, MONO, "middle")

# Zone 2 — Oracle JDK (y=510..554)
ORA_Y, ORA_H = 510, 44
d.box(Z2_X + 12, ORA_Y, Z2_W - 24, ORA_H, PAPER, RULE, 0.9, 6)
d.t(Z2_X + 24, ORA_Y + 26, "Oracle JDK", 12, INK, MONO, "start", 600)
d.t(Z2_X + Z2_W - 24, ORA_Y + 26, "라이선스: BCL → OTN, NFTC", 13, WARN, KR, "end", 600)

# Zone 3 — 도착 객체 1: java.security
d.tone(Z3_X + 12, JS_Y, Z3_W - 24, JS_H, INFO, 4, "14", 1.2)
d.t(Z3_X + Z3_W // 2, JS_Y + 20, "java.security", 12, INFO, MONO, "middle", 600)
d.t(Z3_X + Z3_W // 2, JS_Y + 38, "TLS_RSA_* 끔", 13, INK, KR, "middle")

# Zone 3 — 도착 객체 2: cacerts (y=332..388)
CA3_Y, CA3_H = 332, 56
d.tone(Z3_X + 12, CA3_Y, Z3_W - 24, CA3_H, WARN, 4, "14", 1.2)
d.t(Z3_X + Z3_W // 2, CA3_Y + 22, "cacerts", 12, WARN, MONO, "middle", 600)
d.t(Z3_X + Z3_W // 2, CA3_Y + 42, "배포처별 인증서 묶음", 13, INK, KR, "middle")

# Zone 3 — 도착 항목 3: 배포처별 나머지 차이 (y=460..540)
VD_Y, VD_H = 460, 80
d.box(Z3_X + 12, VD_Y, Z3_W - 24, VD_H, PAPER, WARN, 1.0, 6)
d.t(Z3_X + Z3_W // 2, VD_Y + 24, "배포처별 차이", 13, WARN, KR, "middle", 600)
d.t(Z3_X + Z3_W // 2, VD_Y + 46, "벤더 패치 · 지원 기간", 13, INK, KR, "middle")
d.t(Z3_X + Z3_W // 2, VD_Y + 64, "라이선스", 13, INK, KR, "middle")

# ── 화살표 (직교 경로만 사용, 4의 배수 좌표) ─────────────────────────────
JS_MID = JS_Y + JS_H // 2  # 256
CA1_MID = CA1_Y + CA1_H // 2  # 314
CA2_MID = CA2_Y + CA2_H // 2  # 403 -> 404
CA3_MID = CA3_Y + CA3_H // 2  # 360

# 0) OpenJDK 프로젝트 -> 배포처 6종 각각 (가는 선 SOFT 1.0px, 단일 라벨)
TRUNK_X = 284
SRC_X = 248
SRC_Y = RA_Y + RA_H  # 196
BUS_Y = 214
ROW_D_BUS_Y = 442

# 소스에서 인출선 -> 수직 간선 (객체 화살표와 교차하는 y=256, y=314 에 반원 hop)
d.path(f"M {SRC_X} {SRC_Y} L {SRC_X} {BUS_Y} L {TRUNK_X} {BUS_Y}", SOFT, 1.0)
d.t(SRC_X - 8, BUS_Y + 4, "같은 소스로 빌드", 13, MUTED, KR, "end", 600)

# 수직 간선: 214 -> 250 (hop over 256) -> 308 (hop over 314) -> 532
d.path(
    f"M {TRUNK_X} {BUS_Y} L {TRUNK_X} {JS_MID - 6} "
    f"a 6,6 0 0,0 0,12 L {TRUNK_X} {CA1_MID - 6} "
    f"a 6,6 0 0,0 0,12 L {TRUNK_X} {ORA_Y + 22}",
    SOFT,
    1.0,
)

# 6개 배포처 각각으로 가는 분기 화살표 (모두 SOFT 1.0px)
d.arrow([(TRUNK_X, BUS_Y), (Z2_X + 10, BUS_Y)], SOFT, "soft", 1.0)  # Corretto
d.arrow([(TRUNK_X, TEM_Y + 18), (Z2_X + 10, TEM_Y + 18)], SOFT, "soft", 1.0)  # Temurin
for i in range(3):
    cx = Z2_X + 12 + i * (VW + 6) + VW // 2
    d.arrow([(TRUNK_X, ROW_D_BUS_Y), (cx, ROW_D_BUS_Y), (cx, V3_Y - 2)], SOFT, "soft", 1.0)  # Red Hat / Zulu / MS
d.arrow([(TRUNK_X, ORA_Y + 22), (Z2_X + 10, ORA_Y + 22)], SOFT, "soft", 1.0)  # Oracle JDK

# 1) java.security: Zone 1 -> Corretto -> Zone 3 (수평 직선, 1.5px INFO)
d.arrow([(Z1_X + Z1_W - 12, JS_MID), (Z2_X + 20, JS_MID)], INFO, "info", 1.5)
d.arrow([(Z2_X + Z2_W - 22, JS_MID), (Z3_X + 10, JS_MID)], INFO, "info", 1.5)

# 2) cacerts: Zone 1 -> Corretto -> (Temurin 합류) -> Zone 3 (1.5px WARN)
d.arrow([(Z1_X + Z1_W - 12, CA1_MID), (Z2_X + 20, CA1_MID)], WARN, "warn", 1.5)
MERGE_X = Z2_X + Z2_W + 20  # 748
d.path(f"M {Z2_X + Z2_W - 22} {CA1_MID} L {MERGE_X} {CA1_MID} L {MERGE_X} {CA3_MID}", WARN, 1.5)
d.path(f"M {Z2_X + Z2_W - 22} {CA2_MID} L {MERGE_X} {CA2_MID} L {MERGE_X} {CA3_MID}", WARN, 1.5)
d.arrow([(MERGE_X, CA3_MID), (Z3_X + 10, CA3_MID)], WARN, "warn", 1.5)

# 3) 나머지 배포처(Row D/E) -> Zone 3 배포처별 차이
V3_MID = V3_Y + V3_H // 2  # 477
ORA_MID = ORA_Y + ORA_H // 2  # 532
VD_MID = VD_Y + VD_H // 2  # 500
d.path(f"M {Z2_X + Z2_W - 12} {V3_MID} L {MERGE_X} {V3_MID} L {MERGE_X} {VD_MID}", MUTED, 1.4)
d.path(f"M {Z2_X + Z2_W - 12} {ORA_MID} L {MERGE_X} {ORA_MID} L {MERGE_X} {VD_MID}", MUTED, 1.4)
d.arrow([(MERGE_X, VD_MID), (Z3_X + 10, VD_MID)], MUTED, "ar", 1.4)

# ── 범례 ──────────────────────────────────────────────────────────────────
LEG_Y = 580
d.legend(
    LEG_Y,
    [
        ("판 번호 따라 동일", INFO),
        ("TCK 가 맞추는 것", OK),
        ("배포처별 변경 요소", WARN),
        ("최종 이미지 기준", ACC),
    ],
)

out_path = (
    sys.argv[1]
    if len(sys.argv) > 1
    else str(pathlib.Path(__file__).resolve().parent.parent / "02-02.big-picture.svg")
)
d.save(out_path)
print("ok gen-02-02.big-picture")

# 타입 스펙: type-timeline
# 02-02.timeline — OpenJDK 공개·주기와 Oracle JDK 라이선스 연표
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 516

d = D(
    W, H,
    "CONTAINER · 02-02",
    "OpenJDK 공개·주기와 Oracle JDK 라이선스 연표",
    "2006년 OpenJDK 비공식 운영부터 2028년 9월(계획)까지 소스 공개·릴리스 주기와 Oracle JDK 라이선스 변화를 두 레인에 배치한 연표",
    lead="6개월 주기 전환 이후 Oracle JDK 라이선스 이름이 BCL · OTN · NFTC 로 바뀐 흐름",
)

AXIS_Y = 264

# ── 좌측 레인 머리 ───────────────────────────────────────────────────
d.box(16, 128, 108, 60, PAPER2, INFO, 1.0, 6)
d.t(70, 152, "소스 공개 ·", 13, INFO, KR, "middle", 600)
d.t(70, 174, "릴리스 주기", 13, INFO, KR, "middle", 600)

d.box(16, 332, 108, 60, PAPER2, WARN, 1.0, 6)
d.t(70, 356, "Oracle JDK", 13, WARN, MONO, "middle", 600)
d.t(70, 378, "라이선스", 13, WARN, KR, "middle", 600)

# ── 시간축 기준선 (2007 ~ 2017 축 단절 // · 2027~2028 계획 점선) ────────
d.line(132, AXIS_Y, 256, AXIS_Y, MUTED, 1.6)
# 축 단절 (//)
d.line(262, AXIS_Y + 8, 268, AXIS_Y - 8, MUTED, 1.4)
d.line(270, AXIS_Y + 8, 276, AXIS_Y - 8, MUTED, 1.4)
# 2017 ~ 2024 실선, 2024 ~ 2028 계획 점선
d.line(284, AXIS_Y, 840, AXIS_Y, MUTED, 1.6)
d.line(840, AXIS_Y, 976, AXIS_Y, MUTED, 1.4, "4 4")

# ── 사건 정의 ────────────────────────────────────────────────────────
# 상단 레인: 소스 공개와 릴리스 주기
UPPER = [
    # (dot_x, card_x, card_y, card_w, color, is_focal, date_txt, label_txt, leader_pts)
    (160, 136, 92, 156, INFO, False, "2006년", "OpenJDK 비공식 지침", [(160, 148), (160, AXIS_Y - 5)]),
    (224, 180, 172, 144, INFO, False, "2007년 5월 8일", "OpenJDK 헌장 채택", [(224, 228), (224, AXIS_Y - 5)]),
    (340, 312, 92, 196, ACC, True, "2017년 9월 6일", "글 게시 · 6개월 주기·LTS", [(340, 148), (340, AXIS_Y - 7)]),
    (356, 524, 92, 184, INFO, False, "2017년 9월", "Oracle OpenJDK 무료", [(616, 148), (616, 160), (356, 160), (356, AXIS_Y - 5)]),
    (408, 392, 172, 196, INFO, False, "2018년 9월 11일", "글 게시 · Java 11 빌드 동등", [(408, 228), (408, AXIS_Y - 5)]),
]

# 하단 레인: Oracle JDK 라이선스
LOWER = [
    # (dot_x, card_x, card_y, card_w, color, is_planned, date_txt, label_txt, leader_pts)
    (440, 364, 296, 168, WARN, False, "2019년 4월 16일", "앞선 판만 BCL 적용", [(440, AXIS_Y + 5), (440, 296)]),
    (568, 480, 376, 152, OK, False, "2021년 9월", "NFTC 사용 시작", [(568, AXIS_Y + 5), (568, 376)]),
    (732, 648, 376, 164, WARN, False, "2024년 9월", "17.0.13 이후 OTN 제공", [(732, AXIS_Y + 5), (732, 376)]),
    (892, 776, 296, 154, MUTED, True, "2027년 9월(계획)", "다음 LTS Java 29", [(892, AXIS_Y + 5), (892, 296)]),
    (948, 828, 376, 156, MUTED, True, "2028년 9월(계획)", "JDK 25 NFTC 기한", [(948, AXIS_Y + 5), (948, 376)]),
]

CARD_H = 56

# ── 상단·하단 레인 지시선 먼저(z-order) ─────────────────────────────────
for dot_x, cx, cy, cw, c, is_focal, _, _, pts in UPPER:
    d.path(" ".join(("M" if i == 0 else "L") + f" {x} {y}" for i, (x, y) in enumerate(pts)), c, 1.1)

for dot_x, cx, cy, cw, c, is_planned, _, _, pts in LOWER:
    dash = "3 3" if is_planned else None
    d.path(" ".join(("M" if i == 0 else "L") + f" {x} {y}" for i, (x, y) in enumerate(pts)), c, 1.1, dash=dash)

# ── 카드 및 축 점 ───────────────────────────────────────────────────
for dot_x, cx, cy, cw, c, is_focal, dt, lb, _ in UPPER:
    if is_focal:
        d.tone(cx, cy, cw, CARD_H, ACC, 6, "14", 1.4)
        d.o.append(f'<circle cx="{dot_x}" cy="{AXIS_Y}" r="6" fill="{ACC}" stroke="{PAPER}" stroke-width="1.5"/>')
    else:
        d.box(cx, cy, cw, CARD_H, PAPER2, c, 1.0, 6)
        d.o.append(f'<circle cx="{dot_x}" cy="{AXIS_Y}" r="4.5" fill="{c}" stroke="{PAPER}" stroke-width="1.2"/>')
    d.t(cx + cw // 2, cy + 22, dt, 13, c, KR, "middle", 600)
    d.t(cx + cw // 2, cy + 44, lb, 13, INK, KR, "middle")

for dot_x, cx, cy, cw, c, is_planned, dt, lb, _ in LOWER:
    if is_planned:
        d.o.append(f'<rect x="{cx}" y="{cy}" width="{cw}" height="{CARD_H}" rx="6" fill="{PAPER2}" stroke="{c}" stroke-width="1.1" stroke-dasharray="4 3"/>')
        d.o.append(f'<circle cx="{dot_x}" cy="{AXIS_Y}" r="4.5" fill="{PAPER}" stroke="{c}" stroke-width="1.5"/>')
    else:
        d.tone(cx, cy, cw, CARD_H, c, 6, "10", 1.1)
        d.o.append(f'<circle cx="{dot_x}" cy="{AXIS_Y}" r="4.5" fill="{c}" stroke="{PAPER}" stroke-width="1.2"/>')
    d.t(cx + cw // 2, cy + 22, dt, 13, c, KR, "middle", 600)
    d.t(cx + cw // 2, cy + 44, lb, 13, INK, KR, "middle")

# ── 범례 ────────────────────────────────────────────────────────────
LEG_Y = 468
d.legend(LEG_Y, [
    ("소스·주기", INFO),
    ("주기 제안", ACC),
    ("BCL·OTN", WARN),
    ("NFTC", OK),
    ("계획(점선)", MUTED),
])

out_path = sys.argv[1] if len(sys.argv) > 1 else str(pathlib.Path(__file__).resolve().parent.parent / "02-02.timeline.svg")
d.save(out_path)
print("ok gen-02-02.timeline")

# 타입 스펙: type-flowchart — 판정을 물어 가며 좁히는 결정 흐름. 마름모가 물음이고 사각이 결과다.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §6.4.3 — 필터링·포워딩의 세 경우와
#   Figure 6.22 · Figure 6.23 의 스위치 표 값 그대로
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, OK, BAD, KR, MONO

W, H = 1000, 514
d = D(W, H, "SECTION 6.4.3 · FILTERING AND FORWARDING",
      "표를 한 번 찾고 셋 중 하나를 합니다",
      "인터페이스 x 로 들어온 프레임의 목적지 MAC 을 스위치 표에서 찾는다. 없으면 뿌리고, x 자신이면 버리고, 다른 인터페이스면 그리로 보낸다.",
      "표의 값은 원문 Figure 6.23 그대로입니다")

d.box(40, 116, 300, 56, PAPER2, RULE, 0.9)
d.t(190, 140, "인터페이스 x 로 프레임 도착", 11, INK, KR, "middle", 600)
d.t(190, 159, "목적지 MAC = DD-DD-DD-DD-DD-DD", 10, MUTED, MONO)
d.arrow([(190, 176), (190, 190)], MUTED, "ar", 1.3)

CXD, CYD, HWD, HHD = 190, 236, 150, 44
d.o.append(f'<path d="M {CXD - HWD} {CYD} L {CXD} {CYD - HHD} L {CXD + HWD} {CYD} L {CXD} {CYD + HHD} Z" '
           f'fill="{ACC}14" stroke="{ACC}" stroke-width="1.5"/>')
d.t(CXD, CYD - 4, "표에 그 MAC 이 있는가", 11, ACC, KR, "middle", 600)
d.t(CXD, CYD + 14, "있다면 어느 인터페이스인가", 11, ACC, KR, "middle", 600)

BRANCH = [
    (40, "항목이 없습니다", "x 를 뺀 모든 인터페이스로 복사본을 보냅니다", "브로드캐스트", INFO, "info"),
    (368, "항목이 x 를 가리킵니다", "목적지가 이미 그 세그먼트에 있습니다", "버립니다 · 필터링", BAD, "bad"),
    (696, "항목이 y 를 가리킵니다", "y 앞의 출력 버퍼에 프레임을 넣습니다", "보냅니다 · 포워딩", OK, "ok"),
]
for x, cond, body, verdict, c, mk in BRANCH:
    d.path(f"M {CXD} {CYD + HHD} L {CXD} 308 L {x + 132} 308 L {x + 132} 322", c, 1.3, m=mk)
    d.tone(x, 322, 264, 92, c, 6, "14", 1.2)
    d.t(x + 132, 346, cond, 11, c, KR, "middle", 600)
    d.t(x + 132, 368, body, 10, MUTED, KR)
    d.t(x + 132, 396, verdict, 12, c, KR, "middle", 600)

d.box(500, 116, 460, 160, PAPER2, RULE, 1.0)
d.t(516, 140, "스위치 표 — 주소 · 인터페이스 · 기록 시각", 11, INK, KR, "start", 600)
d.line(516, 150, 944, 150, RULE, 0.8)
for i, (mac, itf, t) in enumerate([("01-12-23-34-45-56", "2", "9:39"),
                                   ("62-FE-F7-11-89-A3", "1", "9:32"),
                                   ("7C-BA-B2-B4-91-10", "3", "9:36")]):
    y = 174 + i * 24
    d.t(516, y, mac, 11, INK, MONO, "start")
    d.t(800, y, itf, 11, MUTED, MONO)
    d.t(944, y, t, 11, MUTED, MONO, "end")
d.t(516, 254, "62-FE-F7-11-89-A3 은 1 에서 오면 버리고 2 에서 오면 1 로 보냅니다.", 11, MUTED, KR, "start")

d.line(24, 434, W - 48, 434, RULE, 0.8)
d.t(24, 456, "표가 완전하고 정확한 동안 스위치는 브로드캐스트 없이 목적지 쪽으로만 프레임을 보냅니다. "
             "이 점에서 스위치는 허브보다 똑똑합니다.", 11, MUTED, KR, "start")

d.legend(474, [("표를 찾는 물음", ACC), ("모르면 뿌립니다", INFO), ("걸러 냅니다", BAD), ("골라 보냅니다", OK)])

out = pathlib.Path(__file__).resolve().parent.parent / "06-04.switch-decision.svg"
d.save(out)
print("→", out)

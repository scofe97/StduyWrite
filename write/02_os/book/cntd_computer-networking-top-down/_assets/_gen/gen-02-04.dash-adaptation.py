# 02-04 §2 — DASH 가 하는 일. 쓸 수 있는 대역폭이 출렁일 때 클라이언트가 청크마다 판을 고른다.
# 세 판의 비트율(300 kbps · 1 Mbps · 3 Mbps)은 원문 2.5.1 의 예 그대로다.
# 대역폭 곡선과 선택 이력은 *질적* 그림이다 — 원문에 이 시계열의 수치가 없으므로 값이 아니라 모양만 옮긴다.
# 타입 스펙: type-line — 연속 지표 위의 추세. 꺾은선으로 그리고 초점 계열에만 꼭짓점을 찍는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 640
PX0, PX1, PY0, PY1 = 148, 900, 140, 400
YMAX = 4.0          # Mbps
LEVELS = [(0.3, "300 kbps"), (1.0, "1 Mbps"), (3.0, "3 Mbps")]

d = D(W, H, "COMPUTER NETWORKING TOP-DOWN · 02-04 §2",
      "받을 수 있는 만큼만 요청합니다",
      "쓸 수 있는 대역폭이 시간에 따라 변할 때 클라이언트가 어느 판의 청크를 고르는지. 세 판의 비트율은 원문의 예이고 시계열은 모양만 옮긴 질적 그림이다.",
      "선택하는 쪽이 서버가 아니라 클라이언트입니다 — 청크마다 다시 정합니다")

def ypx(v): return PY1 - (v / YMAX) * (PY1 - PY0)

# 세 판을 수평 기준선으로
for v, lab in LEVELS:
    y = ypx(v)
    d.line(PX0, y, PX1, y, RULE, 0.8, "4 4")
    d.t(PX0 - 12, y + 4, lab, 11, MUTED, MONO, "end")
d.line(PX0, PY0, PX0, PY1, RULE, 1.0)
d.line(PX0, PY1, PX1, PY1, MUTED, 1.0)
d.t(PX0 - 12, PY0 - 16, "비트율", 11, SOFT, KR, "end")
d.t((PX0 + PX1) / 2, PY1 + 26, "시간 — 청크 하나가 몇 초입니다", 11, SOFT, KR)

# 쓸 수 있는 대역폭 (질적)
BW = [3.6, 3.4, 3.5, 2.6, 1.4, 0.9, 0.7, 1.2, 2.2, 3.3, 3.5, 3.4]
N = len(BW)
def xc(i): return PX0 + (i + 0.5) * (PX1 - PX0) / N
pts = " ".join(f"{xc(i):.1f},{ypx(v):.1f}" for i, v in enumerate(BW))
d.o.append(f'<polyline points="{pts}" fill="none" stroke="{INFO}" stroke-width="1.6" stroke-linejoin="round"/>')

# 클라이언트가 고른 판 — 대역폭 아래의 가장 높은 판
def pick(v):
    return max([lv for lv, _ in LEVELS if lv <= v], default=0.3)
CH_H = 20
for i, v in enumerate(BW):
    p = pick(v)
    x = PX0 + i * (PX1 - PX0) / N + 3
    w = (PX1 - PX0) / N - 6
    d.tone(x, ypx(p) - CH_H / 2, w, CH_H, ACC, 3, "1c", 1.2)

d.t(PX0, PY1 + 68, "대역폭이 3 Mbps 아래로 떨어지자 다음 청크부터 1 Mbps 판으로, 더 떨어지자 300 kbps 판으로 내려갑니다.",
     11, MUTED, KR, "start")
d.t(PX0, PY1 + 90, "회복되면 다시 올라갑니다. 판을 갈아타는 판단이 청크마다 새로 이뤄집니다.",
     11, MUTED, KR, "start")

d.t(20, 528, "서버가 준비하는 것은 판마다의 파일과 매니페스트뿐입니다. 무엇을 언제 가져갈지는 클라이언트가 측정한 대역폭과 버퍼 잔량으로 정합니다.",
     11, MUTED, KR, "start")

d.legend(H - 56, [("클라이언트가 고른 청크", ACC), ("쓸 수 있는 대역폭", INFO)])
d.save("02-04.dash-adaptation.svg")

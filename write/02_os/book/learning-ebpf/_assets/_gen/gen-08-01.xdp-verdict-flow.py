# 타입 스펙: type-flowchart — 시작 타원 하나, 검사 상자 하나, 마름모 넷(각각 출구 둘), 끝 타원 다섯. 마름모는 오른쪽으로 이어지고 끝 타원은 아래로 떨어진다. 코랄은 XDP_DROP 하나.
# 사실 출처: linux v7.2 include/uapi/linux/bpf.h 6571~6582행(enum xdp_action 0~4, 알 수 없는 반환값은 드랍과 경고),
#   추출본 ebpf8.txt 95~118행(반환 코드 다섯과 뜻)·130~150행(xdp_md, data·data_end 경계), 예제 저장소 chapter8/packet.h 28~29행(경계 검사 실패면 0 반환), lb-from-scratch xdp_lb_kern.c 19~20·26~27행(경계 검사 실패면 XDP_ABORTED).
# Layout conventions: 마름모 104×80(cy=176), 끝 타원 112×52, 가로 간격 48, 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 1000, 436
d = D(W, H, "LEARNING EBPF · 08-01 §1", "XDP 프로그램은 검사 끝에 반환 코드 하나로 패킷의 운명을 정한다",
      "XDP 프로그램이 data 와 data_end 사이의 경계를 검사한다. 경계 밖이면 XDP_ABORTED 0, 버릴 패킷이면 XDP_DROP 1, 스택에 맡기면 XDP_PASS 2, 같은 장치로 되돌리면 XDP_TX 3, 다른 장치로 보내면 XDP_REDIRECT 4 를 돌려준다.",
      "반환 코드가 곧 판정입니다")

def oval(x, y, w, h, c, op="12", sw=1.2):
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h // 2}" fill="{c}{op}" stroke="{c}" stroke-width="{sw}"/>')

def diamond(cx, cy, hw, hh, c, label):
    d.o.append(f'<polygon points="{cx},{cy - hh} {cx + hw},{cy} {cx},{cy + hh} {cx - hw},{cy}" fill="{PAPER2}" stroke="{c}" stroke-width="1.2"/>')
    d.t(cx, cy + 4, label, 12, INK, KR, "middle", 600)

YC = 176
# 시작 · 검사
oval(24, YC - 22, 96, 44, INFO)
d.t(72, YC + 4, "XDP 프로그램", 12, INFO, KR, "middle", 600)
d.arrow([(122, YC), (164, YC)], MUTED, "ar", 1.5)
d.tone(168, YC - 24, 96, 48, INFO, 6, "12", 1.2)
d.t(216, YC - 4, "경계 검사", 12, INFO, KR, "middle", 600)
d.t(216, YC + 14, "data_end", 11, MUTED, MONO)
d.arrow([(266, YC), (308, YC)], MUTED, "ar", 1.5)

DX = [364, 516, 668, 852]
HW, HH = 52, 40
LABELS = ["경계 안?", "버릴 패킷?", "스택에 맡김?", "같은 장치?"]
for cx, lab in zip(DX, LABELS):
    diamond(cx, YC, HW, HH, MUTED, lab)

# 마름모 사이 "아니오"/"예" 이음
d.arrow([(DX[0] + HW + 2, YC), (DX[1] - HW - 4, YC)], OK, "ok", 1.5)
d.chip(DX[0] + HW + 24, YC - 16, "예", OK, 11)
d.arrow([(DX[1] + HW + 2, YC), (DX[2] - HW - 4, YC)], MUTED, "ar", 1.5)
d.chip(DX[1] + HW + 24, YC - 16, "아니오", MUTED, 11)
d.arrow([(DX[2] + HW + 2, YC), (DX[3] - HW - 4, YC)], MUTED, "ar", 1.5)
d.chip(DX[2] + HW + 40, YC - 16, "아니오", MUTED, 11)

# 끝 타원 (아래로)
TY, TH_ = 268, 52
ENDS = [
    (DX[0], "XDP_ABORTED", "0 · 오류로 버림", WARN, "아니오"),
    (DX[1], "XDP_DROP", "1 · 버림", ACC, "예"),
    (DX[2], "XDP_PASS", "2 · 스택으로", OK, "예"),
]
for cx, code, sub, c, edge in ENDS:
    d.arrow([(cx, YC + HH + 2), (cx, TY - 4)], c if c != WARN else MUTED, "ok" if c == OK else ("acc" if c == ACC else "ar"), 1.5)
    d.chip(cx, YC + HH + 26, edge, MUTED, 11)
    oval(cx - 56, TY, 112, TH_, c, "1F" if c == ACC else "12", 1.4 if c == ACC else 1.2)
    d.t(cx, TY + 22, code, 12, c, MONO, "middle", 600)
    d.t(cx, TY + 40, sub, 11, MUTED, KR)

# 마지막 마름모: 예·아니오 둘 다 아래로 갈라진다
bx = DX[3]
BUS = YC + HH + 24
d.path(f"M {bx} {YC + HH + 2} L {bx} {BUS}", INFO, 1.5)
for tx, code, sub, edge in ((792, "XDP_TX", "3 · 들어온 장치로", "예"), (912, "XDP_REDIRECT", "4 · 다른 장치로", "아니오")):
    d.path(f"M {bx} {BUS} L {tx} {BUS} L {tx} {TY - 4}", INFO, 1.5, m="info")
    d.chip((bx + tx) / 2, BUS, edge, MUTED, 11)
    oval(tx - 56, TY, 112, TH_, INFO)
    d.t(tx, TY + 22, code, 12, INFO, MONO, "middle", 600)
    d.t(tx, TY + 40, sub, 11, MUTED, KR)

d.legend(H - 56, [("검사·시작", INFO), ("버림", ACC), ("오류로 버림", WARN), ("스택으로", OK), ("되돌림·넘김", INFO)])
d.save("08-01.xdp-verdict-flow.svg")

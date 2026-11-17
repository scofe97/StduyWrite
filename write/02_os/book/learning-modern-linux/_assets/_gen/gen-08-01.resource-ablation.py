# 08-01 §1 — 느린 앱의 원인을 좁히는 절차. 한 번에 한 자원만 바꾼다.
# 원문("Observability Strategy"): "One widely established strategy in the observability context is the
#       OODA loop (observe-orient-decide-act)." · "let's say an application is slow. Let's further assume
#       there are multiple possible reasons for this (not enough memory, too few CPU cycles, network I/O
#       insufficient, etc.). First, you want to be able to measure each resource consumption. Then you
#       would change each resource allocation individually (keeping the others unchanged) and measure the
#       outcome." · "Does the performance improve after you provided more RAM to the app? If so, you may
#       have found the reason. If not, you continue with a different resource, always measuring the
#       consumption and trying to relate to the observed impact on the situation."
# 타입 스펙: type-flowchart — 판단 논리. 고리를 시도 1·2·3 으로 펼쳐, 시도마다 세 자원 칸 중 바꾼 칸
#           하나만 켜진 모습을 보인다. 마름모(좋아졌나?)에서 예는 오른쪽, 아니오는 아래 시도로 간다.
#           맨 위 한 줄은 본문 첫 문장의 반례(셋을 한꺼번에 늘림)다.
# 근거: 본문 §1 — 자원 셋(메모리·CPU·네트워크 I/O), "RAM 을 더 줘서 좋아졌다면", 좋아져도 상관이지
#       인과의 증명이 아니라 원인 후보, 좋아지지 않으면 다음 자원으로 넘어가되 소비량을 계속 잰다.
# 축약: 시도 순서(RAM → CPU → 네트워크 I/O)는 본문의 RAM 예에서 시작한 예시다. 본문에 수치는 없다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, WARN, BAD, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 788
d = D(W, H, "LEARNING MODERN LINUX · 08-01 §1",
      "한 번에 하나만 바꿔야 무엇이 들었는지 알 수 있다",
      "느린 앱의 의심 자원 셋(메모리·CPU·네트워크 I/O)을 셋 다 늘리면 좋아져도 어느 덕인지 모른다. "
      "기준선을 잰 뒤 시도마다 한 칸만 바꾸고 나머지는 그대로 둔 채 다시 잰다. 좋아지면 그 자원이 "
      "원인 후보가 되고, 아니면 다음 자원으로 넘어간다.",
      "둘을 같이 바꾸면 좋아져도 어느 쪽 덕인지 모릅니다")

LX = 24                         # 행 이름
GX, CWD, CGP = 104, 96, 8       # 자원 칸 시작 x · 칸 폭 · 칸 사이
GW = 3 * CWD + 2 * CGP          # 자원 칸 셋의 폭 = 304
RH = 48                         # 칸 높이
DX = GX + GW + 40               # 마름모 왼쪽 x
DW = 120                        # 마름모 폭
OX = DX + DW + 40               # 결과 상자 x
OW = W - 24 - OX                # 결과 상자 폭
RES = ["메모리", "CPU", "네트워크 I/O"]

# 열 머리
for k, nm in enumerate(RES):
    d.t(GX + k * (CWD + CGP) + CWD / 2, 108, nm, 12, SOFT, KR, "middle", 600)
d.t(DX + DW / 2, 108, "다시 잰 뒤", 12, SOFT, KR, "middle", 600)
d.t(OX + OW / 2, 108, "판정", 12, SOFT, KR, "middle", 600)


def cells(y, states):
    """states: 칸마다 (글자, 색, 채움여부). 색이 None 이면 그대로 둔 칸."""
    for k, (txt, c) in enumerate(states):
        x = GX + k * (CWD + CGP)
        if c is None:
            d.o.append(f'<rect x="{x}" y="{y}" width="{CWD}" height="{RH}" rx="4" fill="none" '
                       f'stroke="{SOFT}" stroke-width="0.8" stroke-dasharray="3 3"/>')
            d.t(x + CWD / 2, y + RH / 2 + 4, txt, 12, SOFT, KR)
        else:
            d.tone(x, y, CWD, RH, c, 4, "1F", 1.4 if c is ACC else 1.1)
            d.t(x + CWD / 2, y + RH / 2 + 4, txt, 12.5, c if c is not MUTED else INK,
                MONO if txt.isascii() else KR, "middle", 600)


def diamond(y, txt, c):
    cx, cy = DX + DW / 2, y + RH / 2
    d.o.append(f'<polygon points="{DX},{cy} {cx},{cy - 30} {DX + DW},{cy} {cx},{cy + 30}" '
               f'fill="{PAPER}" stroke="{c}" stroke-width="1.3"/>')
    d.t(cx, cy + 4, txt, 12.5, c, KR, "middle", 600)


def outcome(y, name, sub, c, dash=False):
    if dash:
        d.o.append(f'<rect x="{OX}" y="{y}" width="{OW}" height="{RH}" rx="6" fill="none" '
                   f'stroke="{c}" stroke-width="1.2" stroke-dasharray="4 3"/>')
    else:
        d.tone(OX, y, OW, RH, c, 6, "14", 1.2)
    d.t(OX + 14, y + 20, name, 13, c, KR, "start", 600)
    d.t(OX + 14, y + 38, sub, 11.5, MUTED, KR, "start")


# 반례 — 셋을 한꺼번에 늘림
Y_BAD = 124
d.t(LX, Y_BAD + RH / 2 + 4, "한꺼번에", 13, BAD, KR, "start", 600)
cells(Y_BAD, [("RAM 늘림", BAD), ("CPU 늘림", BAD), ("I/O 늘림", BAD)])
d.arrow([(GX + GW + 4, Y_BAD + RH / 2), (OX - 4, Y_BAD + RH / 2)], BAD, "bad", 1.3)
d.chip(DX + DW / 2, Y_BAD + RH / 2, "좋아짐", BAD, 12)
outcome(Y_BAD, "어느 덕인지 모름", "다음 장애 때 무엇부터 볼지 모름", BAD)

SEP = Y_BAD + RH + 24
d.line(LX, SEP, W - 24, SEP, RULE, 1, "4 4")

# 기준선
Y0 = SEP + 24
d.t(LX, Y0 + RH / 2 + 4, "기준선", 13, INK, KR, "start", 600)
cells(Y0, [("소비량 잼", MUTED), ("소비량 잼", MUTED), ("소비량 잼", MUTED)])

# 시도 1·2·3 — 한 칸만 바꾼다
STRIDE = 112
TRY = [("시도 1", 0, "RAM"), ("시도 2", 1, "CPU"), ("시도 3", 2, "네트워크 I/O")]
ys = [Y0 + RH + 40 + i * STRIDE for i in range(3)]
d.arrow([(GX + GW / 2, Y0 + RH + 2), (GX + GW / 2, ys[0] - 4)], MUTED, "ar", 1.3)
for i, (nm, k, res) in enumerate(TRY):
    y = ys[i]
    d.t(LX, y + RH / 2 + 4, nm, 13, INK, KR, "start", 600)
    st = [("그대로", None)] * 3
    st[k] = (("RAM 늘림", "CPU 늘림", "I/O 늘림")[k], ACC if i == 0 else INFO)
    cells(y, st)
    d.arrow([(GX + GW + 4, y + RH / 2), (DX - 4, y + RH / 2)], MUTED, "ar", 1.3)
    diamond(y, "좋아졌나?", WARN)
    # 예 → 오른쪽
    d.arrow([(DX + DW + 2, y + RH / 2), (OX - 4, y + RH / 2)], OK, "ok", 1.3)
    d.t(DX + DW + 20, y + RH / 2 - 8, "예", 12, OK, KR, "middle", 600)
    outcome(y, f"원인 후보 · {res}", "상관일 뿐 · 인과 증명 아님", OK)
    # 아니오 → 아래
    cy = y + RH / 2 + 30
    if i < 2:
        ny = ys[i + 1]
        mid = cy + (ny - cy) / 2
        d.path(f"M {DX + DW / 2} {cy} L {DX + DW / 2} {mid} L {GX + GW / 2} {mid} "
               f"L {GX + GW / 2} {ny - 4}", WARN, 1.3, m="warn", dash="5 4")
        d.t(DX + DW / 2 + 8, mid - 8, "아니오 → 다음 자원", 12, WARN, KR, "start", 600)
    else:
        ny = cy + 34
        d.path(f"M {DX + DW / 2} {cy} L {DX + DW / 2} {ny + RH / 2} L {OX - 4} {ny + RH / 2}",
               WARN, 1.3, m="warn", dash="5 4")
        d.t(DX + DW / 2 + 8, cy + 18, "아니오", 12, WARN, KR, "start", 600)
        outcome(ny, "다른 자원으로", "소비량을 계속 재며 영향과 견줌", WARN, dash=True)

NY = ys[2] + RH + 30 + 34 + RH + 28
d.t(LX, NY, "OODA 고리: 관찰 → 방향 잡기 → 결정 → 행동 · 시도 순서는 본문의 RAM 예에서 시작한 예시",
    11.5, SOFT, KR, "start")

d.legend(NY + 22, [("셋을 한꺼번에", BAD), ("이 시도에서 바꾼 칸", INFO), ("본문의 RAM 예", ACC),
                   ("판정", WARN), ("원인 후보", OK)])
d.save("08-01.resource-ablation.svg")
print("ok 08-01.resource-ablation")

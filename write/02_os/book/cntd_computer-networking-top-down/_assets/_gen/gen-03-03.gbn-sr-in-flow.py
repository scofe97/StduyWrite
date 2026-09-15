# 03-03 §6 — GBN 쪽 성질과 SR 쪽 성질이 한 연결 안에서 번갈아 나오는 흐름. 1~5 를 보내는데 2 가 사라진 경우다.
# 본문 근거(§6 「한 흐름에서 둘을 같이 봅니다」): 순서 밖 3·4·5 는 버퍼에 둔다(SR 쪽) · 그러나 따로 확인하지 않고
#   ACK 1 을 되풀이한다(GBN 쪽) · 중복 셋이면 2 하나만 재전송한다(SR 쪽) · 구멍이 메워지면 ACK 5 하나로 3·4·5 까지
#   확인한다(GBN 쪽). ACK n 은 이 절의 표기대로 「n 까지 받았다」는 뜻이다.
#   3·4·5 와 중복 ACK 셋은 묶어 한 화살표로 그리고, 받는 쪽 버퍼는 오른쪽 칸에 두 시점으로 그린다.
# 타입 스펙: type-sequence — 참여자 레인 + 시간축 왕복. 레인 오른쪽에 상태 칸(버퍼)을 붙인다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, INFO, BAD, PAPER2, RULE, KR, MONO

def _kr(t): return KR if any("가" <= c <= "힣" for c in str(t)) else MONO

W, H = 1000, 780
AX, BX = 140, 560               # 레인 x
PX, PW = 660, 316               # 버퍼 칸
Y0, ST = 228, 62
def ry(i): return Y0 + ST * i

d = D(W, H, "COMPUTER NETWORKING TOP-DOWN · 03-03 §6",
      "버퍼는 SR 처럼, 확인은 GBN 처럼",
      "1~5 를 보내는데 2 가 사라진 흐름. 순서 밖 3·4·5 는 버퍼에 두지만 따로 확인하지 않고, 중복 ACK 셋에 2 하나만 다시 보낸 뒤 ACK 5 하나로 셋을 함께 확인한다.",
      "ACK n 은 이 절의 표기대로 n 까지 받았다는 뜻입니다. 오른쪽 칸이 받는 쪽의 수신 버퍼입니다")

for x, nm, sub in ((AX, "보내는 쪽", "송신 버퍼 · 확인 전까지 들고 있음"), (BX, "받는 쪽", "수신 버퍼 · 순서 밖도 보관")):
    d.box(x - 105, 104, 210, 44, PAPER2, RULE, 1.0)
    d.t(x, 124, nm, 12, INK, KR, "middle", 600)
    d.t(x, 141, sub, 11, MUTED, KR)
    d.line(x, 154, x, 640, RULE, 1.0, "3 6")

def msg(a2b, label, y, c=MUTED, mk="ar", dash=None, sub=None, subc=None, bundle=False):
    x1, x2 = (AX, BX) if a2b else (BX, AX)
    dd = 1 if a2b else -1
    if bundle:
        for off in (-5, 5):
            d.line(x1 + 10 * dd, y + off, x2 - 12 * dd, y + off, c, 1.0)
    d.path(f"M {x1 + 10 * dd} {y} L {x2 - 12 * dd} {y}", c, 1.5, m=mk, dash=dash)
    mx = (AX + BX) / 2
    d.t(mx, y - 13 if bundle else y - 9, label, 11, c, _kr(label), "middle", 600)
    if sub: d.t(mx, y + 21 if bundle else y + 17, sub, 11, subc or MUTED, KR)

def lost(label, y):
    mx = (AX + BX) / 2
    d.line(AX + 10, y, mx - 16, y, BAD, 1.5, "5 4")
    d.t(mx, y + 4, "✕", 13, BAD, MONO, "middle", 700)
    d.t((AX + mx) / 2, y - 9, label, 11, BAD, _kr(label), "middle", 600)
    d.t(mx + 24, y + 4, "유실", 11, BAD, KR, "start")

def buffer(y, title, slots, caption, cc):
    # slots: (번호, 상태) — 상태 hole / kept / ready
    d.box(PX, y, PW, 118, PAPER2, RULE, 0.9, 8)
    d.t(PX + 14, y + 22, title, 11, INK, KR, "start", 600)
    sw = 58; gap = 10; x0 = PX + 14
    for k, (num, st) in enumerate(slots):
        x = x0 + k * (sw + gap)
        if st == "hole":
            d.o.append(f'<rect x="{x}" y="{y+36}" width="{sw}" height="36" rx="5" fill="none" stroke="{BAD}" stroke-width="1.2" stroke-dasharray="4 3"/>')
            d.t(x + sw / 2, y + 59, num, 12, BAD, MONO, "middle", 600)
        else:
            c = OK if st == "kept" else ACC
            d.o.append(f'<rect x="{x}" y="{y+36}" width="{sw}" height="36" rx="5" fill="{c}22" stroke="{c}" stroke-width="1.2"/>')
            d.t(x + sw / 2, y + 59, num, 12, c, MONO, "middle", 600)
    d.t(PX + 14, y + 98, caption, 11, cc, KR, "start")

def link(y_from, y_box):
    # 받는 쪽 레인에서 버퍼 칸으로 가는 연결선
    d.path(f"M {BX + 12} {y_from} L {PX - 14} {y_from} L {PX - 14} {y_box} L {PX - 2} {y_box}", SOFT, 1.0, m="soft", dash="3 4")

msg(True, "seq 1", ry(0))
msg(False, "ACK 1", ry(1), INFO, "info", sub="1 까지 받았음")
lost("seq 2", ry(2))
msg(True, "seq 3 · 4 · 5", ry(3), MUTED, sub="셋 다 순서 밖 · 버리지 않고 버퍼에 둠", subc=OK, bundle=True)
msg(False, "ACK 1 × 3 (중복)", ry(4), INFO, "info", sub="3·4·5 를 따로 확인하지 않고 1 을 되풀이함", bundle=True)
msg(True, "seq 2 (재전송)", ry(5), ACC, "acc", sub="중복 셋을 보고 송신 버퍼의 2 하나만 다시 보냄 · 3·4·5 는 안 보냄", subc=ACC)
msg(False, "ACK 5", ry(6), INFO, "info", sub="구멍이 메워져 버퍼의 3·4·5 까지 한 번에 확인함")

buffer(ry(3) - 30, "수신 버퍼 · 3·4·5 가 온 뒤", [("2", "hole"), ("3", "kept"), ("4", "kept"), ("5", "kept")],
       "2 자리만 비어 있고 셋은 들고 있습니다 (SR 쪽)", OK)
link(ry(3), ry(3) + 29)
buffer(ry(5) - 30, "수신 버퍼 · 2 가 온 뒤", [("2", "ready"), ("3", "ready"), ("4", "ready"), ("5", "ready")],
       "구멍이 메워져 2~5 를 한 번에 위층으로", ACC)
link(ry(5), ry(5) + 29)

d.t(20, 672, "순수 GBN 이라면 받는 쪽이 3·4·5 를 버리고, 보내는 쪽은 2 의 타임아웃 뒤 2·3·4·5 를 전부 다시 보냄",
     11, MUTED, KR, "start")
d.t(20, 694, "순수 SR 이라면 받는 쪽이 3·4·5 를 각각 확인함 · TCP 는 버퍼는 SR 처럼, 확인은 GBN 처럼 함",
     11, MUTED, KR, "start")

d.legend(H - 44, [("GBN 쪽 — 누적·중복 ACK", INFO), ("SR 쪽 — 순서 밖 버퍼링", OK), ("재전송", ACC), ("유실·구멍", BAD)])
d.save("03-03.gbn-sr-in-flow.svg")
print("ok gbn-sr-in-flow")

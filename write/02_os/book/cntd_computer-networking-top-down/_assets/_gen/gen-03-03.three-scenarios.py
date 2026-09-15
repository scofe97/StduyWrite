# 03-03 §5 — 원문 Figure 3.33·3.34·3.35 의 세 시나리오를 나란히 놓는다. 값(seq 92·8바이트, seq 100·20바이트,
#   ACK 100·120)은 원문 그대로다. 본문 근거: "ACK 100 이 유실 → 같은 세그먼트 재전송", "ACK 100·120 이 둘 다 늦음
#   → seq 92 만 재전송, ACK 120 이 새 타임아웃 전에 오면 seq 100 은 재전송되지 않음", "ACK 100 만 유실되고 ACK 120 이
#   타임아웃 직전에 도착 → 누적 확인이므로 둘 다 재전송하지 않음".
# 타입 스펙: type-sequence — 참여자 레인 + 시간축 왕복을 세 판으로 나란히. 유실은 끊긴 점선과 ✕, 타임아웃은 레인 옆 괄호.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, WARN, BAD, INFO, PAPER2, RULE, KR, MONO

def _kr(t): return KR if any("가" <= c <= "힣" for c in str(t)) else MONO

W, H = 1000, 640
PX, PW = [24, 352, 680], 296
AX, BX = 60, 236          # 판 안에서 A·B 레인의 x 오프셋
Y0, ST = 232, 46
def ry(i): return Y0 + ST * i

d = D(W, H, "COMPUTER NETWORKING TOP-DOWN · 03-03 §5",
      "ACK 가 어떻게 오느냐로 갈립니다",
      "원문 Figure 3.33·3.34·3.35. ACK 가 사라지면 다시 보내고, 둘 다 늦으면 92 만 다시 보내고, 100 만 사라져도 120 이 제때 오면 아무것도 다시 보내지 않는다.",
      "첫 판은 seq 92 하나를, 뒤의 두 판은 seq 92 와 seq 100 을 연달아 보낸 뒤입니다")

def panel(i, title, sub):
    px = PX[i]
    d.tone(px, 104, PW, 460, RULE, 8, "08", 0.9)
    d.t(px + PW / 2, 128, title, 12, INK, KR, "middle", 600)
    d.t(px + PW / 2, 147, sub, 11, SOFT, KR)
    for x, nm in ((px + AX, "A 보내는 쪽"), (px + BX, "B 받는 쪽")):
        d.box(x - 44, 166, 88, 26, PAPER2, RULE, 0.9, 5)
        d.t(x, 183, nm, 11, INK, KR, "middle", 600)
        d.line(x, 198, x, 540, RULE, 1.0, "3 6")
    return px

def msg(px, a2b, label, y, c=MUTED, mk="ar", dash=None, sub=None, subc=None):
    x1, x2 = (px + AX, px + BX) if a2b else (px + BX, px + AX)
    dd = 1 if a2b else -1
    d.path(f"M {x1 + 8 * dd} {y} L {x2 - 10 * dd} {y}", c, 1.5, m=mk, dash=dash)
    mx = px + (AX + BX) / 2
    d.t(mx, y - 8, label, 11, c, _kr(label), "middle", 600)
    if sub: d.t(mx, y + 16, sub, 11, subc or MUTED, KR)

def lost(px, a2b, label, y):
    x1, x2 = (px + AX, px + BX) if a2b else (px + BX, px + AX)
    dd = 1 if a2b else -1
    mx = px + (AX + BX) / 2
    d.line(x1 + 8 * dd, y, mx - 12 * dd, y, BAD, 1.5, "5 4")
    d.t(mx, y + 4, "✕", 13, BAD, MONO, "middle", 700)
    d.t(mx, y - 8, label, 11, BAD, _kr(label), "middle", 600)
    d.t(mx + 20 * dd, y + 4, "유실", 11, BAD, KR, "start" if dd > 0 else "end")

def bracket(px, y1, y2, label, c=WARN):
    x = px + AX - 30
    d.line(x, y1, x, y2, c, 1.2)
    d.line(x, y1, x + 6, y1, c, 1.2)
    d.line(x, y2, x + 6, y2, c, 1.2)
    d.t(x, y2 + 14, label, 11, c, KR, "middle")

def note(px, y, lines, c=MUTED):
    for k, l in enumerate(lines):
        d.t(px + 12, y + k * 17, l, 11, c, KR, "start")

# ── 판 1 · Figure 3.33 ──
px = panel(0, "ACK 가 사라지면", "그 세그먼트를 다시 보냄")
msg(px, True, "seq 92 (8바이트)", ry(0))
lost(px, False, "ACK 100", ry(1))
bracket(px, ry(0), ry(2) - 12, "타임아웃")
msg(px, True, "seq 92 (재전송)", ry(2), ACC, "acc")
msg(px, False, "ACK 100", ry(3), INFO, "info")
note(px, 466, ["B 는 번호를 보고 이미 받은", "데이터임을 알아 버림"])

# ── 판 2 · Figure 3.34 ──
px = panel(1, "ACK 둘이 늦으면", "92 만 다시 보냄")
msg(px, True, "seq 92 (8바이트)", ry(0))
msg(px, True, "seq 100 (20바이트)", ry(1))
bracket(px, ry(0), ry(2) - 12, "타임아웃")
msg(px, True, "seq 92 (재전송)", ry(2), ACC, "acc")
msg(px, False, "ACK 100", ry(3), INFO, "info", "5 4", "늦게 도착")
msg(px, False, "ACK 120", ry(4), INFO, "info", "5 4", "새 타임아웃 전에 도착")
note(px, 466, ["ACK 120 이 제때 왔으니", "seq 100 은 다시 보내지 않음"])

# ── 판 3 · Figure 3.35 ──
px = panel(2, "ACK 100 만 사라지면", "아무것도 다시 보내지 않음")
msg(px, True, "seq 92 (8바이트)", ry(0))
msg(px, True, "seq 100 (20바이트)", ry(1))
lost(px, False, "ACK 100", ry(2))
msg(px, False, "ACK 120", ry(3), OK, "ok", None, "타임아웃 직전에 도착", OK)
note(px, 466, ["119 까지 다 받았다는 뜻이라", "누적 확인이 앞의 유실을 덮음"], OK)

d.legend(H - 44, [("재전송", ACC), ("확인 응답", INFO), ("누적 확인이 덮는 자리", OK), ("유실", BAD), ("타임아웃", WARN)])
d.save("03-03.three-scenarios.svg")
print("ok three-scenarios")

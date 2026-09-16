# 02-02.subchain-return — 종결은 어디까지인가: ACCEPT 는 테이블 순회를 끝내고, RETURN 만 부모로 돌아간다
# 본문 요구 (§2 "종결은 어디까지인가", 2026-09-16 정정본):
#            "ACCEPT는 서브체인에서 걸려도 부모 체인의 남은 규칙까지 건너뛰고 그 테이블을 빠져나갑니다.
#             같은 훅의 다음 테이블과 뒤 훅은 이 패킷을 여전히 평가합니다."
#            "RETURN은 지금 체인만 멈추고 부모 체인의 다음 규칙으로 돌아갑니다. 빌트인 체인에서 쓰면 그 체인의 policy가 판정합니다."
#            "incoming-ssh 서브체인에서 ACCEPT된 SSH 패킷은 부모 INPUT 체인의 뒤쪽 규칙을 만나지 않습니다."
#            → 2026-09-16 이전 판은 ACCEPT 뒤에 부모로 '복귀'하는 화살표를 요점으로 그렸다. iptables(8)·netfilter
#              Packet Filtering HOWTO 기준으로 틀린 동작이라 본문과 함께 다시 그렸다.
# 타입 스펙: type-sequence.md — 참여자 셋(부모 체인 · 서브체인 · 테이블 밖)의 레인과 시간축.
#           위 구간이 ACCEPT, 아래 구간이 RETURN 이다. focal 은 '테이블 순회 끝' 화살표 한 곳.
#           아래 RETURN 구간은 예제(Example 2-6)에 없는 규칙이라 '가정'으로 표시한다.
# 좌표: Layout conventions 타입이라 공식이 없다 — 메시지 stride 60, 전부 4의 배수.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 944
d = D(W, H, "SUBCHAIN · WHERE A VERDICT STOPS",
      "서브체인의 ACCEPT 는 테이블 순회를 끝내고, RETURN 만 부모 체인으로 돌아간다",
      "왼쪽 레인이 부모 INPUT 체인, 가운데가 서브체인 incoming-ssh, 오른쪽이 filter 테이블 밖이다. "
      "위 구간에서 ACCEPT 된 패킷은 부모의 남은 규칙을 건너뛰고 테이블을 빠져나간다. "
      "아래 구간에서 RETURN 을 만난 패킷만 부모 체인의 다음 규칙으로 돌아간다.",
      lead="아래로 갈수록 시간 · 위 = ACCEPT · 아래 = RETURN(가정)")

LX = {"parent": 196, "sub": 520, "out": 844}
LANE_W, LANE_Y = 264, 108
RAIL_TOP, RAIL_BOT = LANE_Y + 44 + 6, 632
STRIDE = 60


def lane(key, name, sub, mono=True):
    x = LX[key]
    d.box(x - LANE_W // 2, LANE_Y, LANE_W, 44, PAPER2, RULE, 1.0)
    d.t(x, LANE_Y + 20, name, 13, INK, MONO if mono else KR, "middle", 600)
    d.t(x, LANE_Y + 37, sub, 12, MUTED, KR)


def msg(a, b, label, y, sub, c=MUTED, mk="ar"):
    x1, x2 = LX[a], LX[b]
    sign = 1 if x2 > x1 else -1
    d.path(f"M {x1 + 12 * sign} {y} L {x2 - 14 * sign} {y}", c, 1.6, m=mk)
    mx = (x1 + x2) // 2
    d.t(mx, y - 10, label, 12, c, MONO if all(ord(ch) < 128 for ch in label) else KR, "middle", 600)
    d.t(mx, y + 18, sub, 12, MUTED, KR)


def selfmsg(key, label, y, sub, c=MUTED, side=1):
    x = LX[key]
    a, b = x + 12 * side, x + 56 * side
    d.path(f"M {a} {y - 14} L {b} {y - 14} L {b} {y + 14} L {x + 14 * side} {y + 14}", c, 1.5, m="ar")
    tx, anchor = x + 68 * side, ("start" if side > 0 else "end")
    d.t(tx, y - 6, label, 12, c, MONO if all(ord(ch) < 128 or ch == '·' for ch in label) else KR, anchor, 600)
    d.t(tx, y + 14, sub, 12, MUTED, KR, anchor)


lane("parent", "INPUT", "부모 · 빌트인 체인")
lane("sub", "incoming-ssh", "서브 · 사용자 정의 체인")
lane("out", "filter 테이블 밖", "다음 테이블 · 뒤 훅은 여전히 평가", mono=False)
for x in LX.values():
    d.line(x, RAIL_TOP, x, RAIL_BOT, RULE, 1.0, "3 6")

# ── 위 구간 — ACCEPT ──────────────────────────────────────────────
Y1 = 212
ddx.bracket(d, 20, Y1 - 24, Y1 + STRIDE * 2 + 28, "ACCEPT", OK)
msg("parent", "sub", "-j incoming-ssh", Y1, "22 번 포트 · 서브체인으로 점프")
selfmsg("sub", "-s 10.0.0.1 -j ACCEPT", Y1 + STRIDE, "이 테이블의 판정", OK, side=1)
msg("sub", "out", "테이블 순회 끝", Y1 + STRIDE * 2, "부모의 남은 규칙 건너뜀", ACC, mk="acc")
# 부모 레일 위의 건너뛴 규칙 — 이 패킷에는 실행되지 않는다
GX, GW, GY = LX["parent"] - 100, 200, Y1 + STRIDE * 2 - 20
d.o.append(f'<rect x="{GX}" y="{GY}" width="{GW}" height="44" rx="6" fill="{PAPER}" '
           f'stroke="{SOFT}" stroke-width="1.0" stroke-dasharray="5 4"/>')
d.t(LX["parent"], GY + 18, "점프 뒤 LOG · DROP", 12, SOFT, MONO, "middle")
d.t(LX["parent"], GY + 36, "만나지 않음", 12, SOFT, KR)

# ── 아래 구간 — RETURN (가정) ─────────────────────────────────────
Y2 = 448
ddx.bracket(d, 20, Y2 - 24, Y2 + STRIDE * 3 + 24, "RETURN · 가정", INFO)
msg("parent", "sub", "-j incoming-ssh", Y2, "22 번 포트 · 서브체인으로 점프")
selfmsg("sub", "-j RETURN", Y2 + STRIDE, "이 체인에서는 할 말 없음", INFO, side=1)
msg("sub", "parent", "복귀", Y2 + STRIDE * 2, "부모의 다음 규칙부터", INFO, mk="info")
selfmsg("parent", "다음 규칙 계속", Y2 + STRIDE * 3, "끝까지 안 걸리면 policy 판정", MUTED, side=1)

# ── 대조 — 타깃마다 '멈춘다'가 가리키는 범위 ─────────────────────────
BY, RH, RG, BW1, BW2 = 708, 48, 8, 280, 616                    # RETURN 괄호 끝(652)과 머리글 사이 여유
d.t(36, BY - 14, "타깃", 12, SOFT, KR, "start", 600)
d.t(348, BY - 14, "멈추는 범위", 12, SOFT, KR, "start", 600)
for i, (verdict, what, c) in enumerate((
        ("DROP · REJECT", "패킷의 운명 결정 · 뒤 평가 없음", BAD),
        ("ACCEPT", "그 테이블 순회 끝 · 부모 남은 규칙 건너뜀 · 다음 테이블은 평가", ACC),
        ("RETURN · 체인 끝", "부모 체인의 다음 규칙으로 복귀 · 빌트인이면 policy", INFO))):
    y = BY + i * (RH + RG)
    d.box(36, y, BW1, RH, PAPER2, c, 1.1 if c is not ACC else 1.4, 6)
    d.t(36 + BW1 // 2, y + 30, verdict, 13, c, MONO if all(ord(ch) < 128 or ch == '·' for ch in verdict) else KR, "middle", 600)
    d.box(348, y, BW2, RH, PAPER2, RULE, 1.1, 6)
    d.t(368, y + 30, ddx.fit(what, 12, BW2 - 40, what), 12, INK if c is ACC else MUTED, KR, "start")

d.legend(888, [("테이블 순회 끝 — ACCEPT", ACC), ("부모로 복귀 — RETURN", INFO), ("운명 결정 — DROP", BAD)])
d.save("02-02.subchain-return.svg")
print("ok subchain-return")

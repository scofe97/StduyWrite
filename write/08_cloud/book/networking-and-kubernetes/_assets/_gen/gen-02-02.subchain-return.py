# 02-02.subchain-return — 서브체인의 ACCEPT 는 그 체인의 판정일 뿐이다
# 본문 요구: "ACCEPT 와 RETURN 은 지금 있는 체인의 평가만 멈춥니다. 그 체인이 서브체인이었다면
#            부모 체인으로 돌아가 다음 규칙부터 이어서 평가합니다."
#            + "정작 패킷을 막은 것은 부모 INPUT 체인에 남아 있던 뒤쪽 규칙이었습니다."
#            → 시간 순서(점프 → 판정 → 복귀 → 재개 → 폐기)가 요점이라 시퀀스다.
# 타입 스펙: type-sequence.md — 참여자 둘의 레인과 시간축. 되돌아오는 화살표가 이 도식의 주장이라
#           복귀 화살표 하나에만 focal 을 건다. 아래 대조 띠는 "그 화살표가 없는 경우"를 짝지운다.
# 좌표: Layout conventions 타입이라 공식이 없다 — 메시지 간격 stride 76, 전부 4의 배수.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 760
d = D(W, H, "SUBCHAIN ACCEPT · AN OPINION, NOT A VERDICT",
      "서브체인의 ACCEPT 는 그 체인의 판정일 뿐 — 부모 체인이 이어서 평가한다",
      "왼쪽 레인이 부모 체인, 오른쪽이 서브체인이다. 아래로 갈수록 시간이 흐른다. "
      "주황 화살표가 이 도식의 요점이고, 그 화살표가 있기 때문에 뒤의 DROP 이 성립한다.",
      lead="아래로 갈수록 시간 · 주황 화살표(복귀)가 있어서 서브체인의 ACCEPT 가 최종이 아니다")

LX = {"parent": 268, "sub": 732}
LANE_W, LANE_Y = 300, 112
RAIL_TOP, RAIL_BOT = LANE_Y + 44 + 6, 512
STRIDE = 68


def lane(key, name, sub):
    x = LX[key]
    d.box(x - LANE_W // 2, LANE_Y, LANE_W, 44, PAPER2, RULE, 1.0)
    d.t(x, LANE_Y + 20, name, 12, INK, MONO, "middle", 600)
    d.t(x, LANE_Y + 37, sub, 11, MUTED, KR)


def msg(a, b, label, y, sub, c=MUTED, mk="ar"):
    x1, x2 = LX[a], LX[b]
    sign = 1 if x2 > x1 else -1
    d.path(f"M {x1 + 12 * sign} {y} L {x2 - 14 * sign} {y}", c, 1.6, m=mk)
    mx = (x1 + x2) // 2
    d.t(mx, y - 10, label, 12, c, MONO, "middle", 600)
    d.t(mx, y + 18, sub, 11, MUTED, KR)


def selfmsg(key, label, y, sub, c=MUTED, side=1):
    """side=1 이면 레인 오른쪽으로, -1 이면 왼쪽으로 고리를 낸다.
    오른쪽 레인에서 오른쪽으로 내면 라벨이 캔버스를 넘는다."""
    x = LX[key]
    a, b = x + 12 * side, x + 64 * side
    d.path(f"M {a} {y - 14} L {b} {y - 14} L {b} {y + 14} L {x + 14 * side} {y + 14}", c, 1.5, m="ar")
    tx, anchor = x + 76 * side, ("start" if side > 0 else "end")
    d.t(tx, y - 8, label, 12, c, MONO, anchor, 600)
    d.t(tx, y + 12, sub, 11, MUTED, KR, anchor)


lane("parent", "INPUT", "부모 · 빌트인 체인")
lane("sub", "incoming-ssh", "서브 · 사용자 정의 체인")
for x in LX.values():
    d.line(x, RAIL_TOP, x, RAIL_BOT, RULE, 1.0, "3 6")

Y = 216
msg("parent", "sub", "-j incoming-ssh", Y, "22 번 포트 조건에 맞아 서브체인으로 점프")
selfmsg("sub", "-s 10.0.0.1 -j ACCEPT", Y + STRIDE, "이 체인의 판정이 나왔다", OK, side=-1)

# 복귀 — 이 도식의 주장이라 focal 하나를 여기 건다
msg("sub", "parent", "복귀", Y + STRIDE * 2, "패킷의 운명은 아직 정해지지 않았다", ACC, mk="acc")

selfmsg("parent", "다음 규칙 계속", Y + STRIDE * 3, "ACCEPT 뒤에도 부모의 평가는 이어진다", MUTED)
selfmsg("parent", "-j DROP", Y + STRIDE * 4, "여기서 패킷이 끝난다", BAD)

# ── 대조 — 서브체인이 낸 판정에 따라 복귀 화살표가 있고 없고가 갈린다 ──────
BY, RH, BW1, BW2 = 568, 56, 300, 596
d.t(36, BY - 14, "서브체인이 낸 판정", 11, SOFT, KR, "start", 600)
d.t(352, BY - 14, "그 다음에 벌어지는 일", 11, SOFT, KR, "start", 600)
for i, (verdict, what, c) in enumerate((("ACCEPT · RETURN", "부모 체인으로 복귀 — 뒤 규칙이 그 패킷을 DROP 할 수 있다", ACC),
                                        ("DROP · REJECT", "복귀가 없다 — 패킷이 그 자리에서 사라진다", BAD))):
    y = BY + i * (RH + 12)
    d.box(36, y, BW1, RH, PAPER2, c, 1.1, 6)
    d.t(36 + BW1 // 2, y + 34, verdict, 13, c, MONO, "middle", 600)
    d.box(352, y, BW2, RH, PAPER2, RULE, 1.1, 6)
    d.t(372, y + 34, ddx.fit(what, 12, BW2 - 40, what), 12, MUTED, KR, "start")

d.legend(716, [("복귀 — 아직 안 끝났다", ACC), ("체인의 의견", OK), ("패킷의 끝", BAD)])
d.save("02-02.subchain-return.svg")
print("ok subchain-return")

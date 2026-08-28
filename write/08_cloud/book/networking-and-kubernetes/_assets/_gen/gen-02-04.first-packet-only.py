# 02-04.first-packet-only — 규칙은 연결의 첫 패킷에만 발화한다
# 본문 요구: §5 "ping 을 두 번 쳤는데 규칙에 걸린 것은 하나입니다(pkts 1, 84 bytes)."
#           둘째 패킷이 nat 규칙을 아예 안 거친다는 것이 논지이고, 그 '안 거침'은
#           표로는 안 보인다 — 레인 하나가 비는 것으로만 드러난다.
# 타입 스펙: type-sequence.md — 시간축이 논지다. 참여자 3(≤5), 메시지 7(≤12), 프래그먼트 0.
#           응답은 점선 + 채운 마커. coral 은 논점 하나 — 둘째 패킷의 조회 응답.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 692
d = D(W, H, "NAT RULE · FIRST PACKET ONLY",
      "둘째 패킷은 nat 규칙을 아예 거치지 않는다",
      "연결의 첫 패킷만 nat 규칙을 훑고, 그때 만들어진 conntrack 엔트리가 이후 패킷을 대신 변환합니다. "
      "그래서 ping 두 번에 규칙 카운터는 1 만 올라갑니다.",
      lead="첫 패킷이 규칙을 훑고, 이후는 저장된 튜플이 대신한다")

LX = ddx.lanes(d, [("커널", "packet path"),
                   ("nat 규칙", "POSTROUTING"),
                   ("conntrack", "flow table")], y0=104, lane_w=212)
Y = [196, 248, 300, 352, 404, 496, 548]
RAIL_BOT = 580
for x in LX.values():
    d.line(x, d.lane_top + 6, x, RAIL_BOT, RULE, 1.0, "3 6")

def msg(a, b, label, sub, y, c=MUTED, dash=None):
    x1, x2 = LX[a], LX[b]; dr = 1 if x2 > x1 else -1
    d.path(f"M {x1+10*dr} {y} L {x2-12*dr} {y}", c, 1.5, m="acc" if c is ACC else "ar", dash=dash)
    mx = (x1 + x2) // 2
    d.t(mx, y - 10, label, 12, c if c is ACC else (MUTED if dash else INK), MONO, "middle", 600)
    d.t(mx, y + 18, sub, 12, c if c is ACC else MUTED, KR)

# 첫 패킷 — 규칙을 훑는다
d.t(36, 176, "첫 패킷", 12, SOFT, KR, "start", 600)
msg("커널", "conntrack", "lookup", "아는 연결인가", Y[0])
msg("conntrack", "커널", "miss", "모른다", Y[1], dash="5 4")
msg("커널", "nat 규칙", "traverse", "규칙을 훑는다 — 카운터 +1", Y[2])
msg("nat 규칙", "커널", "MASQUERADE", "출발지를 바꾸라", Y[3], dash="5 4")
msg("커널", "conntrack", "create", "튜플 두 줄을 적는다", Y[4], INFO)

d.line(36, 448, W - 48, 448, RULE, 1.0, "4 5")
d.t(36, 476, "둘째 패킷", 12, SOFT, KR, "start", 600)
msg("커널", "conntrack", "lookup", "아는 연결인가", Y[5])
msg("conntrack", "커널", "hit", "이 튜플로 변환하라", Y[6], ACC, dash="5 4")

# 논점은 '아무것도 지나지 않는다'가 아니라 'nat 규칙에 닿는 화살표가 없다'는 것이다.
# 상자로 감싸면 지나가는 메시지를 가둔 것처럼 읽혀 반대 뜻이 된다 — 레인 자체를 강조한다.
# 가운데 레인은 메시지 라벨의 중앙 x 와 같아 그 옆에 주석을 둘 수 없다 —
# 브래킷을 세우면 'hit' 과 '이 튜플로 변환하라'를 관통한다. 레일 아래로 뺀다.
NX = LX["nat 규칙"]
d.line(NX, 470, NX, RAIL_BOT, ACC, 2.0, "3 6")
d.t(NX, 604, "이 레인에 닿는 화살표가 없다", 12, ACC, KR, "end")

d.t(36, 626, "규칙 카운터가 ping 두 번에 1 만 오른 이유가 이 빈칸입니다. "
             "kube-proxy 의 확률 사다리도 첫 패킷에서만 백엔드를 고릅니다.", 12, MUTED, KR, "start")
d.legend(642, [("엔트리 생성", INFO), ("저장된 튜플이 규칙을 대신한다", ACC)])
d.save("02-04.first-packet-only.svg")
print("ok first-packet-only")

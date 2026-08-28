# 02-04.three-requirements — 네임스페이스를 밖으로 내보내는 데 필요한 셋
# 본문 요구: §3 "나갈 길, 중계 허가, 돌아올 길" 세 가지가 각각 다른 곳에 있다.
#           그리고 TTL 64 → 63 이 라우터를 한 번 지났다는 증거라는 것.
# 타입 스펙: type-swimlane.md — 주체 셋을 가로지르며 패킷이 넘겨지는 절차이고,
#           각 주체가 무엇을 갖춰야 하는지가 레인 머리에 붙는다. deployment 를 먼저
#           검토했으나 그 타입은 버전·복제수 같은 배치 결정을 요구해 맞지 않았다.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 632
d = D(W, H, "THREE REQUIREMENTS · ONE PATH",
      "네임스페이스를 밖으로 내보내려면 세 곳에 하나씩 필요하다",
      "나갈 길은 네임스페이스에, 중계 허가는 중계 호스트에, 돌아올 길은 상대 호스트에 있습니다. "
      "셋 중 하나만 빠져도 통하지 않으며 빠진 것에 따라 실패 문구가 달라집니다.",
      lead="나갈 길·중계 허가·돌아올 길이 서로 다른 곳에 있다")

LANE_X, LANE_W, BODY_X = 40, 232, 292
LANES = [("ns1", "필요: default 경로", "route add default via 10.10.1.1", 200, INFO),
         ("ubuntu", "필요: 중계 허가", "net.ipv4.ip_forward = 1", 336, ACC),
         ("ubuntu2", "필요: 돌아올 경로", "route add 10.10.1.0/24 via .208", 472, INFO)]
NW, NH = 212, 76

for name, need, cmd, cy, c in LANES:
    d.o.append(f'<rect x="{LANE_X}" y="{cy-58}" width="{W-80}" height="116" rx="8" '
               f'fill="{PAPER2}" stroke="{RULE}" stroke-width="0.9"/>')
    d.line(BODY_X - 16, cy - 58, BODY_X - 16, cy + 58, RULE, 0.9)
    d.t(LANE_X + 20, cy - 22, name, 14, INK, MONO, "start", 600)
    d.t(LANE_X + 20, cy + 2, need, 12, c, KR, "start", 600)
    d.t(LANE_X + 20, cy + 26, ddx.fit(cmd, 10, LANE_W - 24, cmd), 10, SOFT, MONO, "start")

def step(cx, cy, title, sub, focal=False):
    x, y = cx - NW // 2, cy - NH // 2
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{NW}" height="{NH}" rx="6" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>'); tc = ACC
    else:
        d.box(x, y, NW, NH, PAPER, RULE, 1.1, 6); tc = INK
    d.t(cx, cy - 8, ddx.fit(title, 13, NW - 16, title), 13, tc, KR, "middle", 600)
    d.t(cx, cy + 16, ddx.fit(sub, 11, NW - 14, sub), 11, MUTED, KR)

C1, C2, C3 = 396, 632, 864
step(C1, 200, "default 에 걸림", "10.10.1.0/24 밖이다")
step(C1, 336, "br0 로 받음", "홉이 아니라 TTL 그대로")
step(C2, 336, "FORWARD 통과", "ip_forward 검사 · TTL 1 감소", focal=True)
step(C3, 472, "받는다", "출발지는 10.10.1.11")

d.path(f"M {C1} {200+NH//2} L {C1} {336-NH//2-8}", MUTED, 1.5, m="ar")
d.path(f"M {C1+NW//2} 336 L {C2-NW//2-8} 336", MUTED, 1.5, m="ar")
# 꺾이는 y 는 위 상자 아래끝(374)과 아래 상자 위끝(434) 사이여야 한다.
# 440 으로 두면 아래 상자보다 낮아 화살표가 밑에서 위로 꽂힌다.
MID = 404
d.path(f"M {C2} {336+NH//2} L {C2} {MID} L {C3} {MID} L {C3} {472-NH//2-8}", MUTED, 1.5, m="ar")

d.t(40, 556, "TTL 이 64 에서 63 으로 준 것이 중계를 지났다는 증거입니다. "
             "같은 호스트 안 ns1 에서 ns2 로 갈 때는 64 그대로였습니다.", 12, MUTED, KR, "start")
# 구분선을 566 에 두면 556 의 산문을 관통한다 — 아래로 내린다
d.legend(580, [("갖춰야 할 것", INFO), ("중계 허가가 없으면 여기서 버려진다", ACC)])
d.save("02-04.three-requirements.svg")
print("ok three-requirements")

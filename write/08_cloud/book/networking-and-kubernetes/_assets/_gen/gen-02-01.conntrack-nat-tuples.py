# 02-01.conntrack-nat-tuples — NAT 가 걸리면 응답 튜플이 뒤집기가 아니다
# 본문 요구: "flow 항목에는 기대 응답 패킷의 튜플이 함께 실리는데, 보통은 출발·목적지가 뒤집힌
#            형태지만 NAT 뒤에서는 다를 수 있습니다." + "NAT 는 아예 Conntrack 위에서 동작한다"
#            §5 본문 절반이 NAT 인데 이 절의 도식에 NAT 가 한 글자도 없었다.
# 장면: netfilter-hooks-flow 와 같은 장면(클러스터 밖 → NodePort 30080)을 쓴다. 한 절 건너
#      두 도식이 다른 장면이면 독자가 값을 이어 읽지 못한다. 그래서 DNAT 만이 아니라
#      MASQUERADE 까지 그린다 — 그래야 응답 튜플의 두 필드가 왜 둘 다 어긋나는지 설명된다.
# 타입 스펙: type-sequence.md — 논지가 '적용되는 순서'라 시간축이 필요하다. 참여자 3(≤5),
#           메시지 8(≤12), 조합 프래그먼트 0. 응답은 점선 + 채운 마커.
#           coral 은 스펙 기본값(주 성공 응답) 대신 스타일 계약을 따라 '본문이 짚는 단 하나의
#           논점'인 실제 응답 방향 튜플 줄에 건다 — focal 은 도식당 1곳이다.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 896
d = D(W, H, "CONNTRACK × NAT · ENTRY SHAPE",
      "conntrack 엔트리 한 줄에 튜플이 둘 — NAT 뒤에서는 응답 줄이 뒤집기가 아니다",
      "요청이 DNAT·MASQUERADE 를 거치는 순간 conntrack 은 원본 방향과 응답 방향 튜플을 함께 적는다. "
      "응답 패킷은 두 번째 튜플로 조회돼 두 변환이 한 번에 되돌려진다. "
      "DNAT 는 응답의 출발지를, MASQUERADE 는 응답의 목적지를 정한다.",
      lead="응답 방향 튜플은 원본을 뒤집은 값이 아니라 변환된 주소를 담는다")

LX = ddx.lanes(d, [("클라이언트", "203.0.113.9:51000"),
                   ("노드 커널", "conntrack + nat"),
                   ("Pod", "10.244.1.66:8080")], y0=104, lane_w=212)
Y = [180, 232, 284, 336, 388, 440, 492, 544]
RAIL_BOT = 568
for x in LX.values():
    d.line(x, d.lane_top + 6, x, RAIL_BOT, RULE, 1.0, "3 6")
d.o.append(f'<rect x="{LX["노드 커널"]-4}" y="{Y[0]}" width="8" height="{Y[-1]-Y[0]}" '
           f'fill="{MUTED}18" stroke="{SOFT}" stroke-width="0.8"/>')

def msg(a, b, label, sub, y, dash=None):
    x1, x2 = LX[a], LX[b]; dr = 1 if x2 > x1 else -1
    d.path(f"M {x1+10*dr} {y} L {x2-12*dr} {y}", MUTED, 1.5, m="ar", dash=dash)
    mx = (x1 + x2) // 2
    d.t(mx, y - 10, label, 12, MUTED if dash else INK, MONO, "middle", 600)
    d.t(mx, y + 18, sub, 12, MUTED, KR)

def selfmsg(a, label, sub, y, c=MUTED):
    x = LX[a]
    d.path(f"M {x+10} {y-12} L {x+64} {y-12} L {x+64} {y+12} L {x+13} {y+12}", c, 1.4, m="ar")
    d.t(x + 76, y - 4, label, 12, c, KR, "start", 600)
    d.t(x + 76, y + 16, sub, 12, SOFT, KR, "start")

msg("클라이언트", "노드 커널", "SYN", "dst = 노드 IP:30080", Y[0])
selfmsg("노드 커널", "PRE_ROUTING 에서 DNAT", "목적지를 Pod IP 로 바꾼다", Y[1])
selfmsg("노드 커널", "POST_ROUTING 에서 MASQUERADE", "출발지를 노드 IP 로 바꾼다", Y[2])
selfmsg("노드 커널", "conntrack 엔트리 생성", "튜플 두 줄이 여기서 정해진다", Y[3], INFO)
msg("노드 커널", "Pod", "SYN", "src = 노드 IP · dst = Pod IP", Y[4])
msg("Pod", "노드 커널", "SYN-ACK", "src = Pod IP · dst = 노드 IP", Y[5], dash="5 4")
selfmsg("노드 커널", "응답 방향 튜플로 조회", "두 변환을 한 번에 되돌린다", Y[6])
msg("노드 커널", "클라이언트", "SYN-ACK", "src = 노드 IP:30080", Y[7], dash="5 4")

# ── 엔트리의 실제 모양 — 뒤집기라면 어땠을지를 가운데 줄로 끼워 대조한다 ──
PX0, PX1, PY0, PY1 = 40, 960, 600, 784
d.box(PX0, PY0, PX1 - PX0, PY1 - PY0, PAPER2, RULE, 1.0, 8)
d.t(PX0 + 24, PY0 + 22, "conntrack 엔트리 하나 — 위 '엔트리 생성' 단계에서 채워지는 항목", 12, SOFT, KR, "start")
ROWS = [(632, "원본 방향", "src=203.0.113.9:51000", "dst=노드 IP:30080", INFO, False),
        (672, "뒤집기라면", "src=노드 IP:30080", "dst=203.0.113.9:51000", SOFT, True),
        (712, "실제 응답 방향", "src=10.244.1.66:8080", "dst=노드 IP:51000", ACC, False)]
for y0, lab, src, dst, c, ghost in ROWS:
    d.o.append(f'<rect x="{PX0+16}" y="{y0}" width="{PX1-PX0-32}" height="32" rx="5" '
               f'fill="{"none" if ghost else c+"12"}" stroke="{c}" stroke-width="{1.4 if c is ACC else 1.0}"'
               f'{" stroke-dasharray=\"6 5\"" if ghost else ""}/>')
    tc = SOFT if ghost else (INK if c is ACC else MUTED)
    d.t(PX0 + 40, y0 + 21, lab, 12, c, KR, "start", 600)
    d.t(PX0 + 168, y0 + 21, ddx.fit(src, 12, 300, src), 12, tc, MONO, "start")
    d.t(PX0 + 488, y0 + 21, ddx.fit(dst, 12, 300, dst), 12, tc, MONO, "start")
d.t(PX0 + 168, 766, "두 필드가 모두 어긋난다 — DNAT 가 응답의 src 를, MASQUERADE 가 응답의 dst 를 정했다",
    12, ACC, KR, "start")

# 한 줄로 두면 1018px 로 viewBox 를 넘는다 — 문장 경계에서 끊는다
d.t(36, 808, "NAT 가 없을 때만 아래 줄이 위 줄을 그대로 뒤집은 값이 된다.", 12, MUTED, KR, "start")
d.t(36, 828, "로드밸런서가 연결을 한 백엔드에 고정하는 것도 이 두 번째 줄 덕분이다 — 규칙을 다시 고르지 않는다.",
    12, MUTED, KR, "start")
d.legend(844, [("원본 방향", INFO), ("실제 응답 방향 — 뒤집기가 아니다", ACC)])
d.save("02-01.conntrack-nat-tuples.svg")
print("ok conntrack-nat-tuples")

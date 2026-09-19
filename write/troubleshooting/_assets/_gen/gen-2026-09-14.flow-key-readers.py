# 개념 노트 「흐름을 가르는 다섯 값」 · 쓰는 쪽마다 처리가 갈립니다 — Packet Too Big 한 통을 셋이 읽는다.
# 논지는 "흐름을 가르는 포트가 패킷의 어느 깊이에 있고, 누가 거기까지 읽는가"다.
# 문항 2026-09-14 A 의 사건 순서는 ptb-misdelivery 가 맡으므로 여기에는 서버도 번호도 없다.
# 타입 스펙: type-nested — 바깥 헤더 안에 ICMPv6 헤더, 그 안에 인용된 원본, 그 안에 포트.
#           포함의 깊이가 곧 "바깥 헤더만 보면 안 보이는 정도"라서 겹 상자로 그린다.
#           읽는 쪽 셋은 오른쪽에 두고, 화살표가 끝나는 겹이 그 쪽이 읽는 깊이다.
#           dp-security-matrix(읽는 쪽 × 칸)를 검토했으나 포트가 인용 안쪽에 들어 있다는 포함이 사라져 기각.
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dd import D, ACC, OK, BAD, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 920, 504
d = D(W, H, "TROUBLESHOOTING CONCEPT · FLOW KEY",
      "누가 어디까지 읽는가",
      "경로 중간 라우터가 만든 Packet Too Big 한 통은 바깥 IPv6 헤더, ICMPv6 헤더, 인용된 원본 패킷이 겹으로 들어 있고 "
      "TCP 포트 둘은 가장 안쪽에 있다. 받는 호스트의 커널과 conntrack 은 인용까지 읽어 원래 흐름을 찾고, "
      "바깥 헤더만 해시하는 ECMP 라우터는 주소 둘만 보고 흐름과 다른 다음 홉을 고른다.",
      lead="Packet Too Big 한 통에서 흐름을 가르는 포트는 인용된 원본 안쪽에만 있습니다")

# 겹 — 가로 안쪽 여백 28, 위 60(글자 두 줄), 아래 20 을 모든 겹에 같게 준다
RINGS = [(24, 104, 520, 320), (52, 164, 464, 240), (80, 224, 408, 160), (108, 284, 352, 80)]
STROKE = ["rgba(245,245,245,0.28)", "rgba(245,245,245,0.40)", "rgba(245,245,245,0.55)"]
FILL = ["rgba(245,245,245,0.015)", "rgba(245,245,245,0.025)", "rgba(245,245,245,0.035)"]

# 화살표를 먼저 — 겹과 상자가 위에 앉게 한다
d.arrow([(616, 136), (546, 136)], BAD, "bad", 1.6)
d.arrow([(616, 300), (462, 300)], OK, "ok", 1.6)
d.arrow([(616, 384), (588, 384), (588, 344), (462, 344)], OK, "ok", 1.6)

for i, (x, y, w, h) in enumerate(RINGS[:3]):
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{FILL[i]}" '
               f'stroke="{STROKE[i]}" stroke-width="1.0"/>')
x, y, w, h = RINGS[3]
d.tone(x, y, w, h, ACC, 8)

d.t(40, 128, "Packet Too Big 한 통", 13, INK, KR, "start", 600)
d.t(40, 150, "바깥 IPv6 헤더 · 출발지 중간 라우터 · 목적지 서비스 주소", 12, MUTED, KR, "start")
d.t(68, 188, "ICMPv6 헤더 · 타입 2 · MTU 값", 12, INK, KR, "start", 600)
d.t(68, 208, "포트 칸 없음", 12, BAD, KR, "start")
d.t(96, 248, "인용된 원본 · 서버가 보냈던 패킷", 12, INK, KR, "start", 600)
d.t(96, 268, "출발지 서비스 주소 · 목적지 사용자", 12, MUTED, KR, "start")
d.t(124, 316, "TCP 포트 둘", 13, ACC, KR, "start", 600)
d.t(124, 340, "443 · 51514", 13, INK, MONO, "start")

def reader(y, title, sub, c):
    d.box(616, y, 284, 64, PAPER2, RULE, 1.0, 6)
    d.t(632, y + 26, title, 13, INK, KR, "start", 600)
    d.t(632, y + 48, sub, 12, c, KR, "start")

reader(108, "ECMP 라우터 · 바깥 헤더만", "주소 둘 해시 · 흐름과 다른 서버로", BAD)
reader(268, "받는 호스트의 커널", "인용의 네 값 · 소켓 조회", OK)
reader(352, "conntrack", "기존 연결에 묶음 · RELATED", OK)

d.legend(448, [("바깥 헤더만 읽음", BAD), ("인용까지 읽음", OK), ("흐름을 가르는 값", ACC)])

d.save(os.path.join(os.path.dirname(__file__), "..", "2026-09-14.flow-key-readers.svg"))
print("ok")

# 05-01 §6 — 리스가 5초 남은 키를 물으면 응답 TTL 은 하한 30초가 되어, 키가 지워진 뒤에도 클라이언트 캐시가 25초 남는다.
# 소스 근거: plugin/etcd/etcd.go 의 TTL 함수 — 리스 남은 시간을 min-lease-ttl(기본 30)·max-lease-ttl 로 가두고,
#            메시지 ttl 이 없으면 그 값을 쓰며, 있으면 둘 중 작은 값을 쓴다. 리스 만료 시 키 삭제는 etcd 리스의 정의.
# 타입 스펙: type-gantt — 키·응답·캐시 세 막대의 시작과 끝이 어긋나는 구간이 논지다. 가로축은 초.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, OK, BAD, KR, MONO

W, H = 880, 470
d = D(W, H, "LEARNING COREDNS · 05-01 §6",
      "키는 5초 뒤 지워져도 응답은 30초를 산다",
      "0초에 리스가 5초 남은 키를 물으면 리스 유래 TTL 5 가 하한 30 으로 올라간다. 메시지에 ttl 이 없으면 응답 TTL 은 30 이고, "
      "키가 5초에 지워진 뒤에도 그 응답을 캐시한 클라이언트는 30초까지 옛 주소를 쓴다.",
      "주황 괄호가 키는 없는데 캐시는 살아 있는 구간입니다")


def X(t):
    return 220 + t * 17


for t in range(0, 36, 5):
    d.t(X(t), 120, f"{t}s", 12, SOFT, MONO)
    d.line(X(t), 128, X(t), 336, RULE, 0.6, "2 6")
d.line(X(0), 128, X(35), 128, RULE, 1.0)

lanes = [(170, "etcd 키", "리스 5초 남음"), (240, "CoreDNS 응답", "0초에 받은 답"), (310, "클라이언트 캐시", "그 답을 저장")]
for cy, name, sub in lanes:
    d.t(20, cy - 2, name, 14, INK, KR, "start", 600)
    d.t(20, cy + 18, sub, 12, MUTED, KR, "start")

d.tone(X(0), 156, X(5) - X(0), 28, OK, 4, "22", 1.1)
d.t(X(5) + 10, 175, "리스 만료 · 키 삭제", 12, BAD, KR, "start")

d.box(X(0), 226, X(30) - X(0), 28, PAPER2, MUTED, 1.0, 4)
# 5초 점선이 글자를 가르지 않게 라벨은 점선 오른쪽에서 시작한다
d.t(X(5) + 12, 245, "응답 TTL 30 · 리스 5초를 하한 30 으로", 12, MUTED, KR, "start")

d.tone(X(0), 296, X(5) - X(0), 28, OK, 4, "22", 1.1)
d.tone(X(5), 296, X(30) - X(5), 28, BAD, 4, "22", 1.1)
d.t(X(5) + 12, 315, "죽은 주소를 계속 쓴다", 12, BAD, KR, "start")
d.t(X(30) + 8, 315, "재질의", 12, MUTED, KR, "start")

d.line(X(5), 140, X(5), 336, BAD, 1.2, "4 4")

d.path(f"M {X(5)} 346 L {X(5)} 354 L {X(30)} 354 L {X(30)} 346", ACC, 1.4)
d.t((X(5) + X(30)) / 2, 374, "25초 · 키는 없는데 캐시는 살아 있다", 13, ACC, KR, "middle", 600)

d.t(20, 404, "메시지 ttl 을 10 으로 적으면 · 응답 TTL 10 · 이 구간이 5초로 준다", 13, MUTED, KR, "start")

d.legend(420, [("키가 살아 있는 동안", OK), ("죽은 주소를 쓰는 동안", BAD), ("어긋나는 구간", ACC)])
d.save("05-01.lease-cache-gap.svg")

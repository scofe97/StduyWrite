# 타입 스펙: type-architecture — 소켓 fd 셋이 epoll 인스턴스에 등록되고, 준비된 fd 7·9 의 명령이 주 스레드의 이벤트 루프에서 한 번에 하나씩 실행되는 경로(위)와 io-threads 가 읽기·쓰기를 맡는 경로(아래). 존 둘.
# 사실 출처: Redis 8.10.2 src/ae.c L30-L44(다중화 계층을 evport > epoll > kqueue > select 순으로 고름), src/ae_epoll.c L28(epoll_create)·L93(epoll_wait),
#   redis.conf 8.10.2 L1390-L1416(대부분 단일 스레드이고 io-threads 를 켜면 클라이언트 소켓 읽기·쓰기와 프로토콜 파싱을 I/O 스레드가 맡음, 기본은 꺼짐),
#   redis.io benchmarks 문서(명령 실행 기준으로는 대체로 단일 스레드 서버), 추출본 v1.txt 1846~1850행과 PDF 쪽 77 그림(소켓 → IO 다중화 → 이벤트 루프 → 작업 큐 → 실행).
#   fd 7·8·9, GET user:42 → Kim, SET user:42=Lee → OK 는 이 편이 정한 예시 값이다.
# Layout conventions: 존 둘(주 스레드 하나 · io-threads), 상자 폭 168~224·높이 88(위)·64(아래), 흐름은 왼쪽에서 오른쪽, 연결선은 직각만. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 960, 496
d = D(W, H, "BYTEBYTEGO · 02-01 §4",
      "소켓 여럿은 epoll 이 기다리고 명령은 하나씩 실행된다",
      "fd 7·9 가 준비되면 GET 다음 SET 이 차례로 돌고, io-threads 를 켜도 실행은 주 스레드가 맡습니다",
      "Redis 8.10.2 소스와 문서 기준")


def zone(x, y, w, h, label):
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="rgba(245,245,245,0.02)" stroke="{RULE}" stroke-width="0.9" stroke-dasharray="5 4"/>')
    d.t(x + 16, y + 24, label, 12, SOFT, KR, "start", 600)


def node(x, y, w, h, l1, l2, c, focal=False, fam1=KR):
    if focal:
        d.tone(x, y, w, h, ACC, 6, "14", 1.4)
        c = ACC
    elif c == MUTED:
        d.box(x, y, w, h, PAPER2, RULE, 0.9, 6)
    else:
        d.tone(x, y, w, h, c, 6, "10", 0.9)
    d.t(x + w / 2, y + h / 2 - 4, l1, 13, c if c != MUTED else INK, fam1, "middle", 600)
    d.t(x + w / 2, y + h / 2 + 16, l2, 12, MUTED, KR if any("가" <= ch <= "힣" for ch in l2) else MONO)


# 존 A — 주 스레드 하나가 기다리고 실행한다
zone(240, 100, 696, 176, "주 스레드 하나")
socks = [("fd 7", "GET user:42", 124, True), ("fd 8", "대기", 172, False), ("fd 9", "SET user:42=Lee", 220, True)]
for nm, cmd, y, ready in socks:
    d.box(24, y, 180, 36, PAPER2, RULE if ready else "rgba(191,192,192,0.14)", 0.9, 4)
    d.t(36, y + 23, nm, 12, INK if ready else SOFT, MONO, "start", 600)
    d.t(196, y + 23, cmd, 12, MUTED if ready else SOFT, KR if any("가" <= ch <= "힣" for ch in cmd) else MONO, "end")
d.arrow([(206, 142), (224, 142), (224, 190), (262, 190)], MUTED, "ar", 1.4)
d.path("M 206 238 L 224 238 L 224 190", MUTED, 1.4)
node(264, 146, 168, 88, "epoll_wait", "준비된 fd 7 · 9", INFO, fam1=MONO)
d.arrow([(434, 190), (478, 190)], MUTED, "ar", 1.4)
node(480, 146, 168, 88, "이벤트 루프", "다음 fd 를 꺼냄", MUTED)
d.arrow([(650, 190), (694, 190)], MUTED, "ar", 1.4)
d.box(696, 146, 224, 88, PAPER2, RULE, 0.9, 6)
d.t(808, 174, "명령 하나씩 실행", 13, INK, KR, "middle", 600)
d.t(808, 198, "GET user:42 → Kim", 12, MUTED, MONO)
d.t(808, 218, "SET user:42=Lee → OK", 12, MUTED, MONO)

# 존 B — io-threads 가 소켓 읽기·쓰기를 나눠 맡는다
zone(240, 304, 696, 120, "io-threads 사용")
d.box(24, 358, 180, 36, PAPER2, RULE, 0.9, 4)
d.t(36, 381, "fd 7", 12, INK, MONO, "start", 600)
d.t(196, 381, "GET user:42", 12, MUTED, MONO, "end")
d.arrow([(206, 376), (262, 376)], MUTED, "ar", 1.4)
node(264, 344, 180, 64, "I/O 스레드", "읽기 · 파싱", INFO)
d.arrow([(446, 376), (490, 376)], MUTED, "ar", 1.4)
node(492, 344, 180, 64, "주 스레드", "GET → Kim 실행", INFO, focal=True)
d.arrow([(674, 376), (718, 376)], MUTED, "ar", 1.4)
node(720, 344, 180, 64, "I/O 스레드", "Kim 쓰기", INFO)

d.legend(H - 44, [("소켓", MUTED), ("I/O 스레드·epoll", INFO), ("명령 실행은 주 스레드", ACC)])
d.save("02-01.event-loop.svg")

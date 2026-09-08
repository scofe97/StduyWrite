# 07-03 §1 — 왕복 대기를 줄이려는 시도 넷을 세대순으로 나란히. 층이 다르고, 남는 병목이 다르다.
# 노트의 읽기: 2026-09-08 복습 세션에서 학습자가 직접 요청한 도식. 원문 §1 은 HTTP 1.1·2·3 을 RFC 번호로만
#       나열한다(RFC 2616 · RFC 7540 · 초안). 세대가 무엇을 바꿨는지는 원문에 없다.
#   RFC 793 (September 1981) — 슬라이딩 윈도우. ACK 를 기다리지 않고 창만큼 보낸다.
#   RFC 2616 (June 1999) §8.1.2.2 — "A client that supports persistent connections MAY "pipeline" its requests
#       ... A server MUST send its responses to those requests in the same order that the requests were received."
#   RFC 7540 (May 2015) §1 — "HTTP/1.1 added request pipelining, but this only partially addressed request
#       concurrency and still suffers from head-of-line blocking.  Therefore, HTTP/1.0 and HTTP/1.1 clients that
#       need to make many requests use multiple connections" · §5.1.1 스트림 식별자.
#   RFC 9000 (May 2021) §2.2 — "One of the benefits of QUIC is avoidance of head-of-line blocking across multiple
#       streams.  When a packet loss occurs, only streams with data in that packet are blocked" · RFC 9114 (June 2022).
#   인과 방향(학습자 지적): 순서가 없어서 ID 가 나온 것이 아니라, 프레임에 스트림 ID 를 붙였기 때문에 순서가 자유로워졌다.
# 타입 스펙: type-timeline — 사건이 시간 위에 놓이고 세대가 바꾼 것을 적는다. 간격은 연도 비례(1980~2022 선형).
#       라벨은 위아래로 번갈아 두고, 아래쪽 둘은 서로 반대편으로 뻗게 앵커를 갈라 충돌을 피한다.
#       주요 이정표(HTTP/2 스트림 ID) 하나만 강조색 r=6.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, PAPER, RULE, KR, MONO

W, H = 1000, 600
Y0, Y1, X0, X1 = 1980, 2022, 76, 936
def X(y): return round(X0 + (y - Y0) * (X1 - X0) / (Y0 and (Y1 - Y0)))
BASE = 320

d = D(W, H, "LEARNING MODERN LINUX · 07-03 §1",
      "왕복 대기를 줄이려는 시도 넷",
      "TCP 윈도우, HTTP/1.1 파이프라이닝, HTTP/2 멀티플렉싱, HTTP/3 이 각각 무엇을 겹치게 했고 무엇이 남았는지. "
      "층이 다르고 남는 병목이 다르다.",
      "세대마다 겹치게 한 것과 남은 병목이 다릅니다")

# 축·눈금(10년 단위)
d.line(X0, BASE, X1 + 24, BASE, "rgba(245,245,245,0.30)", 1.0)
for yr in (1980, 1990, 2000, 2010, 2020):
    d.line(X(yr), BASE - 4, X(yr), BASE + 4, "rgba(245,245,245,0.30)", 1.0)
    d.t(X(yr), BASE + 22, str(yr), 12, SOFT, MONO)

EVENTS = [  # (연도, 층, 제목, 줄1, 줄2, 색, 위/아래, 앵커, focal)
    (1981, "L4", "TCP 윈도우 · RFC 793", "ACK 를 안 기다리고 창만큼 밀어 넣는다",
     "남는 것: 세그먼트는 한 줄 — 하나 빠지면 뒤가 선다", INFO, "up", "start", False),
    (1999, "L7", "HTTP/1.1 파이프라이닝 · RFC 2616", "요청은 겹치되 응답은 받은 순서대로",
     "앞 응답이 늦으면 뒤가 막힌다 — 대신 연결을 여럿 연다", MUTED, "down", "end", False),
    (2015, "L7", "HTTP/2 멀티플렉싱 · RFC 7540", "프레임마다 스트림 ID 를 붙였다",
     "그래서 응답 순서가 자유롭다 — TCP 한 줄은 그대로", ACC, "up", "end", True),
    (2022, "L4", "HTTP/3 · QUIC 위로 · RFC 9114", "UDP 위에 스트림을 독립으로 둔다",
     "한 스트림의 손실이 다른 스트림을 막지 않는다", INFO, "down", "end", False),
]
for yr, layer, title, l1, l2, c, side, anchor, focal in EVENTS:
    x = X(yr)
    r = 6 if focal else 4
    d.o.append(f'<circle cx="{x}" cy="{BASE}" r="{r}" fill="{c}" stroke="{PAPER}" stroke-width="1.5"/>')
    if side == "up":
        ty = 196; d.line(x, ty + 56, x, BASE - r - 2, RULE, 1.0)
    else:
        ty = 392; d.line(x, BASE + r + 2, x, ty - 22, RULE, 1.0)
    tx = x + (10 if anchor == "start" else -10)
    d.t(tx, ty - 22, f"{yr} · {layer}", 12, c, MONO, anchor, 600)
    d.t(tx, ty, title, 13, c if focal else INK, KR, anchor, 600)
    d.t(tx, ty + 22, l1, 12, MUTED, KR, anchor)
    d.t(tx, ty + 42, l2, 12, MUTED, KR, anchor)

d.t(24, 500, "인과 방향이 중요합니다. 순서가 없어서 ID 가 나온 것이 아니라, 프레임에 스트림 ID 를 붙였기 때문에 순서가 자유로워졌습니다.",
    12, MUTED, KR, "start")
d.t(24, 524, "왼쪽 셋은 같은 TCP 한 줄 위라 세그먼트 하나가 빠지면 스트림 전부가 함께 섭니다. 그 줄을 UDP 위의 독립 스트림으로 바꾼 것이 QUIC 입니다.",
    12, MUTED, KR, "start")

d.legend(H - 44, [("L4 전송 계층", INFO), ("L7 애플리케이션 계층", MUTED), ("순서를 푼 열쇠", ACC)])
d.save("07-03.roundtrip-generations.svg")
print("ok 07-03.roundtrip-generations")

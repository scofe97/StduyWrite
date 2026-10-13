# 타입 스펙: type-process — 편 전체 지도. 절 번호·이름·대표 값이 칸마다 같은 자리에 반복되고 화살표는 읽는 순서를 나른다(semantic-patterns 의 Stage framework with semantic slots, 주체 없는 단계 지도라서 selection 표의 알려진 공백 대체).
# 사실 출처: 추출본 v1.txt 1601~1620행(Redis vs Memcached 자료 구조 쓰임) · 1683~1721행(캐시 관통) · 1747~1788행(읽기·쓰기 전략 다섯) · 1840~1858행(Redis 속도), PDF 쪽 65·69·73·77 그림.
#   120ns·50~150µs 는 같은 그림(쪽 77)의 지연 값이고 설계 가정이다. user:42·Kim·user:404 는 이 편이 정한 예시 값이다.
# Layout conventions: 카드 폭 204·높이 212, 가로 stride 220(x=40+220k), 카드 y=112, 화살표는 카드 중앙 y=218. 4 카드라서 01-01(5 카드, stride 180) 보다 stride 를 넓혔다. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 960, 392
d = D(W, H, "BYTEBYTEGO · 02-01",
      "캐시는 요청 경로의 어디에 서는가",
      "읽기·쓰기 경로, 없는 키 방어, 저장소 고르기, 속도의 이유가 키 하나의 값으로 이어집니다.",
      "네 절이 값 하나씩을 들고 이어집니다")

CW, CH, STRIDE, X0, Y0 = 204, 212, 220, 40, 112
cards = [
    ("§1", "읽기·쓰기 전략 다섯", "GET user:42", "miss → SELECT → SET", "캐시가 서는 자리", ACC),
    ("§2", "캐시 관통 방어", "GET user:404", "miss → 0 rows", "DB 앞의 방어선", INFO),
    ("§3", "Redis 와 Memcached", "hash · zset · bitmap", "값은 바이트 또는 구조", "값의 모양", INFO),
    ("§4", "Redis 가 빠른 이유", "120ns · 50~150µs", "epoll → 명령 하나씩", "메모리 · 루프 · 구조", INFO),
]
for k, (tag, title, v1, v2, sub, c) in enumerate(cards):
    x = X0 + k * STRIDE
    cx = x + CW / 2
    if c == ACC:
        d.tone(x, Y0, CW, CH, ACC, 6, "14", 1.4)
    else:
        d.box(x, Y0, CW, CH, PAPER2, RULE, 0.9, 6)
    d.t(x + 12, Y0 + 24, tag, 12, SOFT, MONO, "start")
    d.t(cx, Y0 + 52, title, 13, c if c == ACC else INK, KR, "middle", 600)
    d.line(x + 12, Y0 + 68, x + CW - 12, Y0 + 68, RULE, 0.6)
    d.t(cx, Y0 + 104, v1, 12, c, MONO, "middle", 600)
    d.t(cx, Y0 + 132, v2, 12, INK, KR if any("가" <= ch <= "힣" for ch in v2) else MONO, "middle")
    d.t(cx, Y0 + 176, sub, 12, MUTED, KR, "middle")
    if k < len(cards) - 1:
        d.arrow([(x + CW + 2, Y0 + CH / 2), (x + STRIDE - 4, Y0 + CH / 2)], MUTED, "ar", 1.4)

d.legend(H - 44, [("이 편의 초점", ACC), ("절별 대표 값", INFO)])
d.save("02-01.chapter-overview.svg")

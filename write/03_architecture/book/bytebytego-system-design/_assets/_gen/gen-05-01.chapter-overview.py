# 타입 스펙: type-process — 편 전체 지도. 절 번호·이름·실제 값이 칸마다 같은 자리에 반복되고 화살표는 읽는 순서를 나른다(semantic-patterns 의 Stage framework with semantic slots, 주체 없는 단계 지도라서 selection 표의 알려진 공백 대체).
# 사실 출처: Kafka 4.3 설계 문서 https://kafka.apache.org/43/design/design/ (순차 600MB/sec 대 무작위 100kB/sec, 복사 4회 대 sendfile, 전달 보장, pull, fetch.max.wait.ms 500 은 consumer-configs). 시스템 콜 2회 대 1회는 설계 문서·sendfile(2).
# Layout conventions: 카드 폭 164·높이 212, 가로 stride 180(x=40+180k), 카드 y=112, 화살표는 카드 중앙 y=218. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 960, 392
d = D(W, H, "BYTEBYTEGO · 05-01",
      "Kafka 의 속도와 전달 보장을 다루는 다섯 절",
      "로그에 덧붙이고 복사를 줄이며, 커밋 시점이 보장을 가르고, 소비자가 당기며, 서비스는 조율자를 두거나 두지 않습니다",
      "절마다 값 하나씩을 들고 이어집니다")

CW, CH, STRIDE, X0, Y0 = 164, 212, 180, 40, 112
cards = [
    ("§1", "순차 IO · 페이지 캐시", "600MB/s : 100kB/s", "순차 쓰기 : 무작위 쓰기", "덧붙이기만 하는 로그", INFO),
    ("§2", "제로 카피", "복사 4회 → 2회", "시스템 콜 2회 → 1회", "사용자 버퍼를 건너뜀", INFO),
    ("§3", "전달 보장 셋", "commit 13", "유실 · 중복 · 1벌", "커밋 시점이 결과를 가름", ACC),
    ("§4", "당기기와 밀기", "fetch.max.wait.ms", "500 ms", "소비자가 속도를 정함", INFO),
    ("§5", "서비스 협업", "조율자 있음 : 없음", "전부 경유 : 직접", "조율자를 두는가", INFO),
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
    d.t(cx, Y0 + 104, v1, 12, c, KR if any("가" <= ch <= "힣" for ch in v1) else MONO, "middle", 600)
    d.t(cx, Y0 + 132, v2, 12, INK, KR if any("가" <= ch <= "힣" for ch in v2) else MONO, "middle")
    d.t(cx, Y0 + 176, sub, 12, MUTED, KR, "middle")
    if k < len(cards) - 1:
        d.arrow([(x + CW + 2, Y0 + CH / 2), (x + STRIDE - 4, Y0 + CH / 2)], MUTED, "ar", 1.4)

d.legend(H - 44, [("이 편의 초점", ACC), ("절별 대표 값", INFO)])
d.save("05-01.chapter-overview.svg")

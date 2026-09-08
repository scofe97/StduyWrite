# 10-01 전체 지도 — 이 편이 다루는 다섯 갈래와, 각 갈래가 성능에서 맡는 몫.
# 타입 스펙: type-layers — 아래로 갈수록 구체(모델 → 경로/크기 → 지연 → 버퍼 → 공유 자원)인
#           계층이 아니라 "관심의 층"이라 layers 의 밴드 문법을 쓴다.
#           축약: 프로토콜 계층이 아니므로 인덱스 태그에 L3 같은 층 번호 대신 절 번호를 넣는다
#           (type-layers §Layout conventions 의 "index tag" 슬롯을 절 번호로 채운 것).
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import ACC, MUTED, SOFT, INK, INFO, PAPER, PAPER2, RULE, KR, MONO



W, H = 928, 560
BX, BW, BH, Y0, STRIDE = 96, 736, 64, 108, 72

d = DK(W, H, "SYSTEMS PERFORMANCE · 10-01",
      "네트워크 성능을 보는 다섯 갈래",
      "이 편이 다루는 다섯 절과 각 절이 성능에서 맡는 몫. 위 두 절이 무대를 세우고, 아래 세 절이 느려지는 자리를 짚는다.",
      "아래로 갈수록 '무엇이 있는가' 에서 '무엇이 느려지는가' 로 옮겨 갑니다")

BANDS = [
    ("§1", "용어와 모델", "인터페이스 · 컨트롤러 · 프로토콜 스택", "무대를 세운다", None),
    ("§2", "라우팅 · 캡슐화 · 패킷 크기", "MTU 1,500 과 점보 프레임", "경로와 크기를 정한다", None),
    ("§3", "지연 여섯 가지", "이름 해석 · ping · 연결 · TTFB · RTT · 수명", "어디가 느린지 좁힌다", ACC),
    ("§4", "버퍼링 · 백로그", "처리량을 떠받치고 부하를 흡수한다", "과하면 되레 느려진다", None),
    ("§5", "혼잡 회피 · 협상 · 사용률", "공유 자원을 나눠 쓰는 법", "한 방향이 100% 면 병목", None),
]

for i, (tag, name, sub, role, c) in enumerate(BANDS):
    y = Y0 + i * STRIDE
    if c: d.tone(BX, y, BW, BH, c, 8)
    else: d.box(BX, y, BW, BH, PAPER2, RULE, 1.0, 8)
    d.t(BX - 24, y + 38, tag, 12, c if c else SOFT, MONO, "end", 600)
    d.t(BX + 20, y + 28, name, 14, c if c else INK, KR, "start", 600)
    d.t(BX + 20, y + 48, sub, 13, MUTED, KR, "start")
    d.t(BX + BW - 20, y + 38, role, 12, c if c else SOFT, KR, "end")

d.t(BX - 60, Y0 + 4, "무대", 13, SOFT, KR, "middle")
d.arrow([(BX - 60, Y0 + 16), (BX - 60, Y0 + 4 * STRIDE + BH - 8)], SOFT, "soft", 1.2, "4 6")
d.t(BX - 60, Y0 + 4 * STRIDE + BH + 16, "병목", 13, SOFT, KR, "middle")

d.t(BX, Y0 + 5 * STRIDE + 18, "네트워크는 '모르면 일단 의심받는' 자원이라, 분석은 무슨 일이 일어나는지 밝혀 네트워크를 면죄하는 데서 출발합니다",
    13, MUTED, KR, "start")

d.legend(Y0 + 5 * STRIDE + 44, [("이 편의 중심 — 지연을 나눠 재는 절", ACC), ("나머지 절", MUTED)])
d.save("10-01.chapter-overview.svg")

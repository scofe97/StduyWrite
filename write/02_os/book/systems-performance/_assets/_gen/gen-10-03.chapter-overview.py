# 10-03 전체 지도 — 관찰에서 실험으로, 실험에서 튜닝으로.
# 타입 스펙: type-layers — 다섯 절이 관찰 → 실험 → 튜닝 순으로 행동 강도가 세지는 지도다.
#           축약: OSI 층이 아니므로 인덱스 태그를 절 번호로 채운다.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 928, 560
BX, BW, BH, Y0, STRIDE = 96, 736, 64, 108, 72

d = DK(W, H, "SYSTEMS PERFORMANCE · 10-03",
       "행동으로 옮기는 다섯 갈래",
       "10-03 이 다루는 다섯 절. 무엇부터 볼지 정하고, 원천을 좁히고, 정밀 도구를 꺼내고, 능동으로 재고, 마지막에 손잡이를 돌린다.",
       "10-01·10-02 가 개념과 구조였다면 이 편은 행동입니다")

BANDS = [
    ("§1", "방법론 10종", "USE · 워크로드 특성화 · 정적 튜닝", "무엇부터 볼지 정한다", None),
    ("§2", "지연 분석 · TCP 분석", "버퍼 · 백로그 · 혼잡 윈도 · TIME_WAIT", "원천을 좁힌다", None),
    ("§3", "패킷 스니핑", "커널 BPF 필터로 오버헤드를 줄인다", "마지막 수단의 정밀 도구", None),
    ("§4", "실험", "ping · traceroute · iperf · tc", "능동으로 재 네트워크를 가린다", ACC),
    ("§5", "튜닝", "sysctl · setsockopt · 설정", "마지막에 손잡이를 돌린다", None),
]

for i, (tag, name, sub, role, c) in enumerate(BANDS):
    y = Y0 + i * STRIDE
    if c: d.tone(BX, y, BW, BH, c, 8)
    else: d.box(BX, y, BW, BH, PAPER2, RULE, 1.0, 8)
    d.t(BX - 24, y + 38, tag, 13, c if c else SOFT, MONO, "end", 600)
    d.t(BX + 20, y + 28, name, 14, c if c else INK, KR, "start", 600)
    d.t(BX + 20, y + 48, sub, 13, MUTED, KR, "start")
    d.t(BX + BW - 20, y + 38, role, 13, c if c else SOFT, KR, "end")

d.t(BX - 60, Y0 + 4, "관찰", 13, SOFT, KR, "middle")
d.arrow([(BX - 60, Y0 + 16), (BX - 60, Y0 + 4 * STRIDE + BH - 8)], SOFT, "soft", 1.2, "4 6")
d.t(BX - 60, Y0 + 4 * STRIDE + BH + 16, "변경", 13, SOFT, KR, "middle")

d.t(BX, Y0 + 5 * STRIDE + 18, "권장 시작 순서는 성능 모니터링 → USE → 정적 성능 튜닝 → 워크로드 특성화입니다", 13, MUTED, KR, "start")

d.legend(Y0 + 5 * STRIDE + 44, [("네트워크를 가리는 절", ACC), ("나머지 절", MUTED)])
d.save("10-03.chapter-overview.svg")

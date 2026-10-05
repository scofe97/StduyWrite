# 01-01 전체 지도 — 여섯 절이 "성능을 다루는 지형"에서 "잴 수 있는 지표"로 옮겨 가는 순서.
# 타입 스펙: type-layers — 여섯 절이 범위 → 사람 → 시점 → 방향 → 어려움 → 지표로 구체화되는 관심의 층 지도다.
#           축약: 프로토콜 계층이 아니므로 인덱스 태그 슬롯에 절 번호를 넣는다(10-01 개요와 같은 관례).
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 928, 636
BX, BW, BH, Y0, STRIDE = 96, 736, 64, 108, 72

d = DK(W, H, "SYSTEMS PERFORMANCE · 01-01",
       "성능을 다루는 지형에서 재는 지표까지",
       "이 편의 여섯 절. 위 네 절이 무엇을·누가·언제·어느 방향에서 보는지를 세우고, §5 가 성능이 어려운 이유를, §6 이 그 어려움을 숫자로 바꾸는 지연시간을 다룬다.",
       "아래로 갈수록 '어디를 보나' 에서 '얼마나 큰가' 로 옮겨 갑니다")

BANDS = [
    ("§1", "시스템 성능 · 풀 스택", "애플리케이션부터 metal · 데이터 경로 전체", "무엇을 보나", None),
    ("§2", "역할", "SRE · 개발자 · DBA · 성능 엔지니어", "누가 보나", None),
    ("§3", "활동", "11단계 · canary · blue-green · 용량 계획", "언제 보나", None),
    ("§4", "관점", "자원 분석 · 워크로드 분석", "어느 방향에서", None),
    ("§5", "성능은 왜 어려운가", "주관성 · 복잡성 · 다중 원인 · 다중 이슈", "길을 잃는 이유", None),
    ("§6", "지연시간", "최대 speedup · 한정어 · BPF 분포", "크기를 숫자로", ACC),
]

for i, (tag, name, sub, role, c) in enumerate(BANDS):
    y = Y0 + i * STRIDE
    if c: d.tone(BX, y, BW, BH, c, 8)
    else: d.box(BX, y, BW, BH, PAPER2, RULE, 1.0, 8)
    d.t(BX - 24, y + 38, tag, 12, c if c else SOFT, MONO, "end", 600)
    d.t(BX + 20, y + 28, name, 14, c if c else INK, KR, "start", 600)
    d.t(BX + 20, y + 48, sub, 13, MUTED, KR, "start")
    d.t(BX + BW - 20, y + 38, role, 13, c if c else SOFT, KR, "end")

d.t(BX - 60, Y0 + 4, "지형", 13, SOFT, KR, "middle")
d.arrow([(BX - 60, Y0 + 16), (BX - 60, Y0 + 5 * STRIDE + BH - 8)], SOFT, "soft", 1.2, "4 6")
d.t(BX - 60, Y0 + 5 * STRIDE + BH + 16, "지표", 13, SOFT, KR, "middle")

d.legend(Y0 + 6 * STRIDE + 40, [("이 편의 결론 — 모호함을 재는 지표", ACC), ("나머지 절", MUTED)])
d.save("01-01.chapter-overview.svg")

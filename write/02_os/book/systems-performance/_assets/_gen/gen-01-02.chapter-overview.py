# 01-02 전체 지도 — 여덟 절을 여섯 갈래로 묶어 "어떤 손을 드나"에서 "손이 맞물리는 사례"로 옮겨 간다.
# 타입 스펙: type-layers — 도구의 갈래 → 환경 → 순서 → 사례로 구체화되는 관심의 층 지도다.
#           축약: 인덱스 태그 슬롯에 절 번호를 넣고(10-01 개요 관례), §2~§4 관측 세 절은 한 층으로 묶는다.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 928, 636
BX, BW, BH, Y0, STRIDE = 112, 720, 64, 108, 72

d = DK(W, H, "SYSTEMS PERFORMANCE · 01-02",
       "두 손에서 맞물리는 사례까지",
       "이 편의 여덟 절. §1 이 도구를 관측과 실험 두 손으로 나누고, §2~§4 가 관측의 세 갈래, §5 가 실험, §6 이 클라우드라는 환경, §7 이 도구를 고르는 순서, §8 이 그 모두가 맞물린 두 사례를 다룬다.",
       "아래로 갈수록 '무엇을 드나' 에서 '어떻게 맞물리나' 로 옮겨 갑니다")

BANDS = [
    ("§1", "관측 vs 실험", "건드리지 않고 관찰 · 합성 워크로드", "두 손", None),
    ("§2~4", "관측의 세 갈래", "카운터 · 프로파일링 · 트레이싱 · BPF", "보는 손", None),
    ("§5", "실험 · 벤치마킹", "매크로 · 마이크로 · iperf 두 모드", "거는 손", None),
    ("§6", "클라우드 컴퓨팅", "비용 절감 가능 · 성능 격리", "환경", None),
    ("§7", "방법론 · 60초 체크리스트", "uptime 부터 top 까지 열 개", "고르는 순서", None),
    ("§8", "케이스 스터디", "느린 디스크 · 소프트웨어 변경", "두 손이 맞물림", ACC),
]
for i, (tag, name, sub, role, c) in enumerate(BANDS):
    y = Y0 + i * STRIDE
    if c: d.tone(BX, y, BW, BH, c, 8)
    else: d.box(BX, y, BW, BH, PAPER2, RULE, 1.0, 8)
    d.t(BX - 20, y + 38, tag, 12, c if c else SOFT, MONO, "end", 600)
    d.t(BX + 20, y + 28, name, 14, c if c else INK, KR, "start", 600)
    d.t(BX + 20, y + 48, sub, 13, MUTED, KR, "start")
    d.t(BX + BW - 20, y + 38, role, 13, c if c else SOFT, KR, "end")

d.t(36, Y0 + 4, "도구", 13, SOFT, KR, "middle")
d.arrow([(36, Y0 + 16), (36, Y0 + 5 * STRIDE + BH - 8)], SOFT, "soft", 1.2, "4 6")
d.t(36, Y0 + 5 * STRIDE + BH + 16, "사례", 13, SOFT, KR, "middle")

d.legend(Y0 + 6 * STRIDE + 40, [("도구가 맞물리는 자리", ACC), ("나머지 절", MUTED)])
d.save("01-02.chapter-overview.svg")

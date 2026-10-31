# 09-04 §5 — 9장 분산 시스템 불신뢰 3요소(네트워크·프로세스·시계) 결함 현실과 분산 설계 대응 원칙 종합.
# 사실 출처: 09-04 본문 §5(L74~L99), 원서 Ch.9 "Summary", "Reliability and Fault Tolerance".
# 타입 스펙: type-layers
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, OK, WARN, BAD, KR, MONO

W = 880
LEG = 484
H = LEG + 56

d = D(W, H, "09-04 §5 · CHAPTER 9 SUMMARY", "9장 분산 시스템 불신뢰 3요소와 설계 대응 원칙",
      "비동기 네트워크 패킷 지연, 프로세스 일시 중단, 클럭 스큐와 점프라는 세 가지 불신뢰 현실과 이에 대응하는 동적 타임아웃, 쿼럼과 펜싱 토큰, 단조·논리 시계 및 결합 검증 체계를 조망한다.",
      "불신뢰 3요소(네트워크·프로세스·시계) 결함 현실과 분산 설계 대응 원칙")

layers = [
    ("비신뢰 네트워크 (Network)",
     "비동기 패킷망 전송 지연 · 큐잉 버퍼 가득 참",
     "요청 성공 여부 불명 · 무한 지연 가능성",
     "장애 탐지: 동적 타임아웃 조율",
     "타임아웃 기반 장애 탐지 · 오탐과 지연 균형",
     "지연 관측 분포에 따른 타임아웃 동적 조정",
     INFO, False),
    ("비신뢰 프로세스 (Process)",
     "GC 일시 정지 · VM 중단 · OS 스케줄링 지연",
     "노드가 자신이 얼마나 멈췄는지 자각 불가",
     "결정 방식: 과반수 쿼럼 투표 & 펜싱 토큰",
     "단일 노드 맹신 배제 · 쿼럼 투표로 결정",
     "단조 증가 펜싱 토큰으로 좀비 노드 쓰기 차단",
     ACC, True),
    ("불신뢰 시계 (Clocks)",
     "쿼츠 드리프트 · NTP 강제 조정 및 윤초 급변",
     "이벤트 순서 판단 오류 · 경과 시간 측정 오류",
     "시간 다루기: 단조 시계 & 논리 시계 사용",
     "경과 시간 측정: 벽시계 배제, 단조 시계 사용",
     "이벤트 발생 순서 결정: 논리 시계 사용",
     WARN, False),
]

for idx, (l_title, l_f1, l_f2, r_title, r_m1, r_m2, col_c, is_focal) in enumerate(layers):
    y = 96 + idx * 96

    # 좌측 패널: 현실 결함과 원인
    d.box(28, y, 380, 80, PAPER2, RULE, 1.0)
    d.t(40, y + 20, l_title, 12, INK, KR, "start", 600)
    d.box(36, y + 28, 364, 44, PAPER, RULE, 0.6, r=4)
    d.t(44, y + 44, l_f1, 11, MUTED, KR, "start")
    d.t(44, y + 62, l_f2, 11, MUTED, KR, "start")

    # 중앙 대응 화살표
    d.arrow([(412, y + 40), (440, y + 40)], col_c if is_focal else MUTED, "acc" if is_focal else "ar", 1.4)

    # 우측 패널: 설계 대응 원칙
    if is_focal:
        d.tone(444, y, 408, 80, col_c, 6, "16", 1.4)
    else:
        d.box(444, y, 408, 80, PAPER2, col_c, 1.0)
    d.t(456, y + 20, r_title, 12, col_c, KR, "start", 600)
    d.box(452, y + 28, 392, 44, PAPER, RULE, 0.6, r=4)
    d.t(460, y + 44, r_m1, 11, INK, KR, "start")
    d.t(460, y + 62, r_m2, 11, col_c, KR, "start")

# 바닥 기반 박스: 다층 검증 체계 및 현실 운영 지침
BY = 384
BH = 76
d.box(28, BY, 824, BH, PAPER2, RULE, 1.0)
d.t(40, BY + 18, "분산 시스템 올바름 검증 체계와 현실적 운영 지침", 12, INK, KR, "start", 600)

d.box(36, BY + 26, 396, 42, PAPER, OK, 0.8, r=4)
d.t(44, BY + 42, "결합 검증: 모델 체커(명세) + 결함 주입 + DST(재현)", 11, OK, KR, "start")
d.t(44, BY + 58, "시스템 모델을 명시하고 실제 장애 시나리오 테스트", 11, MUTED, KR, "start")

d.box(444, BY + 26, 400, 42, PAPER, RULE, 0.8, r=4)
d.t(452, BY + 42, "단일 노드 우선: 가능한 한 단일 노드로 해결", 11, INK, KR, "start")
d.t(452, BY + 58, "내결함성·지리분산·무중단 서비스 요구 시 분산 전환", 11, MUTED, KR, "start")

# 범례
d.legend(LEG, [
    ("네트워크 장애 탐지", INFO),
    ("프로세스 쿼럼·펜싱 (focal)", ACC),
    ("시계·시간 원칙", WARN),
    ("결합 검증 체계", OK),
])

d.save("09-04.chapter-summary.svg")

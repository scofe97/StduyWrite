# 13-01 §4 — 분산 환경에서 전순서(Total Order)가 깨지는 네 가지 구조적 요인과 합의 병목.
# 사실 출처: 13-01 §4(L70~L84), DDIA 2판 Ch.13 The limits of total ordering(장 PDF p.5) — shard the log, separate leader in each datacenter, microservices with no shared durable state, client-side state/offline, total order broadcast ≡ consensus.
# 2026-10-31 검증(cc-ddia-dverify13): 본문·원서에 없는 라벨(지역 자율성 우선·도메인 격리 비용·상태 갱신 충돌·파티션 단위 순서·"인과성 포착이 필수")을 걷어 내고 배너·결론 바를 중립 상자로 바꿨다.
# 타입 스펙: type-architecture
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, BAD, KR, MONO

W = 880
BANNER_Y = 96
BANNER_H = 34
PY = 146
PH = 244
BOTTOM_Y = PY + PH + 16
LEG = BOTTOM_Y + 40
H = LEG + 52

d = D(W, H, "13-01 · §4 THE LIMITS OF TOTAL ORDERING", "분산 환경에서 전순서가 깨지는 네 가지 구조적 요인",
      "단일 리더 전순서 로그가 샤딩·지리 분산·마이크로서비스·오프라인 클라이언트에서 깨지는 이유와, 전순서 결정이 합의와 같다는 점.",
      "샤딩 로그 · 지리 분산 · 마이크로서비스 · 오프라인 클라이언트 · 합의 알고리즘 한계")

# 상단 형식적 동치 배너
d.box(24, BANNER_Y, W - 48, BANNER_H, PAPER2, RULE, 0.9, 4)
d.t(W / 2, BANNER_Y + 22, "단일 리더 복제 = 리더가 정한 전순서 로그 · 규모 확장 시 한계 넷", 12, INK, KR, "middle", 600)

X0 = 25
CW = 200
GAP = 10

cards = [
    ("샤딩", "샤딩된 로그", "처리량 확장",
     [("처리량 > 단일 머신", "단일 리더로 감당 못 함"),
      ("로그를 샤드로 분할", "여러 머신에 나눔"),
      ("샤드 간 순서 모호", "두 샤드 간 순서 미정의")],
     BAD, False),
    ("지리", "지리적 분산", "데이터센터 장애 대비",
     [("지역 간 네트워크 지연", "동기 코디네이션 비효율"),
      ("DC별 독립 리더", "데이터센터마다 리더"),
      ("DC 간 순서 불분명", "다른 DC 발생 이벤트")],
     WARN, False),
    ("서비스", "마이크로서비스", "독립 단위 배포",
     [("서비스 + 영속 상태", "한 단위로 배포"),
      ("공유 영속 상태 없음", "서비스끼리 분리"),
      ("서비스 간 순서 없음", "다른 서비스 발생 이벤트")],
     INFO, False),
    ("단말", "오프라인 클라이언트", "클라이언트 쪽 상태",
     [("로컬 상태 즉시 갱신", "서버 확인 기다리지 않음"),
      ("오프라인에서도 동작", "서버와 끊긴 채 입력"),
      ("관찰 순서가 다름", "클라이언트 ≠ 서버 순서")],
     ACC, True),
]

for idx, (chip_txt, title, role, items, card_c, is_focal) in enumerate(cards):
    x = X0 + idx * (CW + GAP)
    y = PY

    if is_focal:
        d.box(x, y, CW, PH, PAPER2, ACC, 1.4)
    else:
        d.box(x, y, CW, PH, PAPER2, RULE, 0.9)

    # 카드 헤더
    d.chip(x + 24, y + 20, chip_txt, card_c, 11, pad=3)
    d.t(x + CW / 2 + 14, y + 24, title, 12, INK, KR, "middle", 600)
    d.t(x + CW / 2, y + 46, role, 11, SOFT, KR, "middle")

    d.line(x + 10, y + 56, x + CW - 10, y + 56, RULE, 0.8)

    # 3개 항목 박스
    iy0 = y + 74
    for i_idx, (head, sub) in enumerate(items):
        iy = iy0 + i_idx * 54
        if is_focal and i_idx == 0:
            d.tone(x + 8, iy - 8, CW - 16, 46, ACC, 4, "22", 1.2)
            d.t(x + CW / 2, iy + 10, head, 12, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 27, sub, 11, ACC, KR, "middle")
        else:
            d.box(x + 8, iy - 8, CW - 16, 46, PAPER, RULE, 0.6)
            d.t(x + CW / 2, iy + 10, head, 12, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 27, sub, 11, MUTED, KR, "middle")

# Bottom Summary Panel
d.box(24, BOTTOM_Y, W - 48, 30, PAPER2, RULE, 0.9, 4)
d.t(W / 2, BOTTOM_Y + 19, "전순서 결정 = 전순서 브로드캐스트 ≡ 합의 · 합의 알고리즘은 순서 결정 작업을 여러 노드에 나누지 않음", 11, INK, KR, "middle", 600)

d.legend(LEG, [
    ("오프라인 클라이언트 (focal)", ACC),
    ("샤딩된 로그", BAD),
    ("지리적 분산", WARN),
    ("마이크로서비스", INFO),
])

d.save("13-01.data-integration-total-ordering.svg")

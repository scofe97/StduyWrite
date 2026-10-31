# 11-01 §1 — 기존 11-01.batch-processing-overview.svg 재생성 및 §1 이동. 온라인·배치·스트림 세 데이터 처리 패러다임 비교.
# 사실 출처: 11-01 본문 §1(L29~L35), DDIA 2판 Ch 11 p.1~3 ("Batch Processing"). 칸 라벨은 본문 및 원서 대목.
# 온라인 결함 내성 칸은 원서 p.2 "rolling back the code will do nothing to fix that data", 스트림 "잡이 끝나지 않음"은 p.3 NOTE 로 상호작용 칸의 지속 관측에 해당하고 결함 내성은 원서·본문이 12장으로 넘긴다.
# 타입 스펙: type-dp-security-matrix
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

W = 880
BANNER_Y = 104
BANNER_H = 36
PY = 156
PH = 288
LEG = PY + PH + 28
H = LEG + 52

d = D(W, H, "11-01 · §1 PROCESSING PARADIGMS", "온라인 · 배치 · 스트림 처리 시스템 비교",
      "데이터 처리 시스템의 세 패러다임을 상호작용 방식, 핵심 지표, 입출력 특성, 결함 내성 기준으로 대조한다. 배치의 불변 입력과 재실행 가능성이 핵심 논점이다.",
      "대화형 vs 일괄 계산 vs 무한 스트림 · 응답 시간 vs 처리량 vs 지연 · 불변 입력과 인간 결함 내성")

# 상단 공통 전제 배너
d.tone(28, BANNER_Y, W - 56, BANNER_H, INFO, 4, "14", 1.0)
d.t(W / 2, BANNER_Y + 23, "처리 방식의 구분 기준: 결과를 기다리는 주체, 핵심 성능 지표, 입력 데이터의 불변성과 부작용 유무", 12, INK, KR, "middle", 600)

PW = 264
GAP = 16
X0 = 28

columns = [
    ("온라인 시스템", "대화형 상호작용", INFO, False, [
        ("상호작용", "사람 · 서비스 요청 대기", "최대한 빨리 응답 반환"),
        ("핵심 지표", "응답 시간 (response time)", "지연 시간 최소화 목표"),
        ("입출력", "가변 읽기 · 쓰기 트랜잭션", "DB · 웹 서버 · REST API"),
        ("결함 내성", "버그 발생 시 데이터 오염 위험", "코드 롤백해도 데이터는 그대로"),
    ]),
    ("배치 처리 잡", "오프라인 일괄 계산", ACC, True, [
        ("상호작용", "사람이 대기하지 않음", "오프라인 일괄 배치 실행"),
        ("핵심 지표", "처리량 (throughput)", "단위 시간당 데이터 양"),
        ("입출력", "불변 입력 · 새 출력 생성", "부작용 없음 · 읽기 전용"),
        ("결함 내성", "인간 결함 내성 확보", "코드 롤백 후 안전한 재실행"),
    ]),
    ("스트림 처리", "무한 이벤트 처리", OK, False, [
        ("상호작용", "지속 관측 · 이벤트 수신", "배치와 온라인의 경계"),
        ("핵심 지표", "짧은 지연 (low latency)", "빠른 이벤트 처리"),
        ("입출력", "끝없는 이벤트 스트림", "지속 유입 데이터 소비"),
        ("결함 내성", "12장에서 다룸", "Ch.12 Stream Processing"),
    ]),
]

for i, (title, sub, c, is_focal, rows) in enumerate(columns):
    x = X0 + i * (PW + GAP)

    # 외곽 상자 (focal은 강조 선)
    if is_focal:
        d.box(x, PY, PW, PH, PAPER2, ACC, 1.4)
    else:
        d.box(x, PY, PW, PH, PAPER2, RULE, 0.9)

    # 헤더
    d.t(x + PW / 2, PY + 24, title, 14, c if is_focal else INK, KR, "middle", 600)
    d.t(x + PW / 2, PY + 44, sub, 11, MUTED, KR, "middle")
    d.line(x + 10, PY + 54, x + PW - 10, PY + 54, RULE, 0.8)

    # 4개 행
    for j, (cat, val1, val2) in enumerate(rows):
        ry = PY + 64 + j * 54
        if is_focal:
            d.tone(x + 8, ry, PW - 16, 46, ACC, 4, "10", 0.9)
        else:
            d.box(x + 8, ry, PW - 16, 46, PAPER, RULE, 0.8)

        # 좌측 카테고리 태그
        d.chip(x + 40, ry + 23, cat, c, 11, 4)
        # 우측 값 2줄
        d.t(x + 80, ry + 19, val1, 11.5, INK if is_focal else MUTED, KR, "start", 600 if is_focal else 400)
        d.t(x + 80, ry + 35, val2, 11, MUTED, KR, "start")

d.legend(LEG, [
    ("온라인 시스템", INFO),
    ("배치 처리 잡 (focal)", ACC),
    ("스트림 처리", OK),
])

d.save("11-01.batch-processing-overview.svg")

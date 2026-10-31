# 11-01 개요 — 온라인·배치·스트림 구분에서 단일 머신 Unix 파이프라인, 정렬 vs 인메모리 집계, 분산 운영체제 유추로 이어지는 전체 지도.
# 사실 출처: 11-01 본문 도입(L14~L18), §1(L26~L35), §2(L43~L61), §3(L69~L90), §4(L94~L103), §5(L113~L124). 칸 라벨은 본문 낱말.
# 타입 스펙: type-architecture
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

W = 880
BANNER_Y = 104
BANNER_H = 36
PY = 156
PH = 248
LEG = PY + PH + 28
H = LEG + 52

d = D(W, H, "11-01 · CHAPTER OVERVIEW", "배치 처리 개요와 Unix 도구 전체 지도",
      "처리 방식의 세 갈래(§1)에서 출발해 Unix 파이프라인 원리(§2), 파이프라인과 프로그램 비교(§3), 정렬과 인메모리 집계(§4), 분산 운영체제 유추(§5)로 이어지는 흐름을 조망한다.",
      "처리 패러다임 구분 · 단일 책임 파이프라인 · 집계 구조와 워킹셋 · 외장 정렬 스필 · 분산 운영체제 유추")

# 상단 공통 전제 배너
d.tone(28, BANNER_Y, W - 56, BANNER_H, INFO, 4, "14", 1.0)
d.t(W / 2, BANNER_Y + 23, "배치 처리의 본질: 불변 입력을 읽어 새 출력을 생성하며, 단일 머신 파이프라인 원리를 분산 환경으로 확장", 12, INK, KR, "middle", 600)

CW = 152
GAP = 16
X0 = 28

cards = [
    ("§1", "처리 모델", "온라인 · 배치 · 스트림",
     [("온라인 시스템", "응답 시간 지표"),
      ("배치 처리 잡", "처리량 · 불변 입력"),
      ("인간 결함 내성", "롤백 후 재실행")],
     INFO),
    ("§2", "Unix 도구", "단일 책임 파이프",
     [("표준 인터페이스", "stdin · stdout"),
      ("단일 책임 명령", "cat awk sort uniq"),
      ("조합 가능성", "파이프라인 연결")],
     OK),
    ("§3", "프로그램", "집계 구조와 메모리",
     [("Python 커스텀", "인메모리 해시 집계"),
      ("워킹셋 정의", "고유 키 수 × 크기"),
      ("메모리 초과", "초과 시 OOM 발생")],
     WARN),
    ("§4", "정렬 vs 해시", "외장 정렬과 스필",
     [("인메모리 해시", "워킹셋 적합 시 O(1)"),
      ("외장 병합 정렬", "디스크 스필 처리"),
      ("I/O 병목", "파일 순차 읽기 속도")],
     WARN),
    ("§5", "분산 OS 유추", "단일 머신에서 분산",
     [("분산 파일시스템", "HDFS · S3 저장소"),
      ("잡 오케스트레이터", "Airflow · 커널 역할"),
      ("처리 프레임워크", "Spark · Flink 엔진")],
     ACC),
]

for i, (sec, title, sub, items, c) in enumerate(cards):
    x = X0 + i * (CW + GAP)
    d.box(x, PY, CW, PH, PAPER2, c, 1.2)
    d.chip(x + 22, PY + 20, sec, c, 11)
    d.t(x + CW / 2 + 12, PY + 24, title, 13, INK, KR, "middle", 600)
    d.t(x + CW / 2, PY + 44, sub, 11, MUTED, KR, "middle")
    d.line(x + 8, PY + 54, x + CW - 8, PY + 54, RULE, 0.8)

    for j, (h_txt, d_txt) in enumerate(items):
        iy = PY + 64 + j * 58
        d.tone(x + 8, iy, CW - 16, 50, c, 4, "10", 0.8)
        d.t(x + CW / 2, iy + 20, h_txt, 12, INK, KR, "middle", 600)
        d.t(x + CW / 2, iy + 38, d_txt, 11.5, MUTED, KR, "middle")

    if i < len(cards) - 1:
        arr_x = x + CW + 1
        arr_y = PY + PH / 2
        d.arrow([(arr_x, arr_y), (arr_x + GAP - 2, arr_y)], MUTED, "ar", 1.4)

d.legend(LEG, [
    ("기본 패러다임", INFO),
    ("Unix 파이프라인", OK),
    ("집계와 정렬 구조", WARN),
    ("분산 시스템 유추", ACC),
])

d.save("11-01.chapter-overview.svg")

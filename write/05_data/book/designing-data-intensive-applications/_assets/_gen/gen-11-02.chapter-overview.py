# 11-02 개요 — DFS 구조(§1), 복제와 이레이저 코딩(§2), 오브젝트 스토어(§3), 저장소 비교(§4), VFS 인터페이스(§5) 전체 지도.
# 사실 출처: 11-02 본문 서두(L14~L18), §1(L24~L36), §2(L39~L49), §3(L52~L64), §4(L67~L83), §5(L86~L94).
# 타입 스펙: type-architecture
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

W = 900
BANNER_Y = 104
BANNER_H = 36
PY = 156
PH = 228
LEG = PY + PH + 24
H = LEG + 52

d = D(W, H, "11-02 · CHAPTER OVERVIEW", "분산 파일시스템과 오브젝트 스토어 전체 지도",
      "분산 배치 처리가 전제하는 저장 계층의 핵심 축과 절별 구성 체계",
      "DFS 계층 구조 · 복제와 이레이저 코딩 · 불변 객체 모델 · 계산-저장 분리 · S3 API 표준화")

# 상단 공통 전제 배너
d.tone(24, BANNER_Y, W - 48, BANNER_H, INFO, 4, "14", 1.0)
d.t(W / 2, BANNER_Y + 23, "분산 배치 저장 계층: POSIX 계층을 클러스터로 확장한 DFS 대 불변 객체 기반 오브젝트 스토어", 12, INK, KR, "middle", 600)

X0 = 24
CW = 162
GAP = 10

cards = [
    ("§1", "DFS 구조", "계층의 분산화",
     [("블록 분할", "128MB 대형 블록 크기"),
      ("메타데이터", "NameNode 메모리 관리"),
      ("데이터 노드", "로컬 디스크 및 캐시")],
     INFO, False),
    ("§2", "내결함성", "복제 vs 이레이저",
     [("단순 복제", "3배 복사본 · 로컬리티"),
      ("이레이저 코딩", "RS(6,3) 1.5배 용량"),
      ("트레이드오프", "저장 효율 대 복구 연산")],
     OK, False),
    ("§3", "오브젝트 스토어", "불변 객체 모델",
     [("URL 주소 체계", "s3://bucket/key"),
      ("불변 객체", "수정 시 전체 재작성"),
      ("네임스페이스", "디렉토리 부재 · 비원자")],
     WARN, False),
    ("§4", "스토리지 비교", "계산-저장 배치",
     [("연산-저장", "co-location 대 분리"),
      ("확장 방식", "동시 증설 대 독립 확장"),
      ("호환 생태계", "Hadoop 대 S3 API")],
     ACC, True),
    ("§5", "VFS 인터페이스", "플러그어블 계층",
     [("표준 프로토콜", "S3 API 사실상 표준"),
      ("POSIX 호환", "FUSE 마운트 · EFS"),
      ("클러스터 구조", "비공유 대 공유 디스크")],
     INFO, False),
]

for idx, (sec, title, role, items, card_c, is_focal) in enumerate(cards):
    x = X0 + idx * (CW + GAP)
    y = PY

    if is_focal:
        d.box(x, y, CW, PH, PAPER2, ACC, 1.4)
    else:
        d.box(x, y, CW, PH, PAPER2, RULE, 0.9)

    # 카드 상단 헤더: 절 칩 + 제목 + 부제목
    d.chip(x + 28, y + 20, sec, card_c, 12)
    d.t(x + 52, y + 24, title, 13, INK, KR, "start", 600)
    d.t(x + 14, y + 46, role, 12, SOFT, KR, "start")

    d.line(x + 10, y + 56, x + CW - 10, y + 56, RULE, 0.8)

    # 3개 항목
    iy0 = y + 74
    for i_idx, (head, sub) in enumerate(items):
        iy = iy0 + i_idx * 49
        d.box(x + 8, iy - 12, CW - 16, 43, PAPER, RULE, 0.6)
        d.t(x + 14, iy + 5, head, 12, INK, KR, "start", 600)
        d.t(x + 14, iy + 23, sub, 12, MUTED, KR, "start")

d.legend(LEG, [
    ("핵심 비교 (focal)", ACC),
    ("DFS 구조·인터페이스", INFO),
    ("내결함성 보장", OK),
    ("오브젝트 스토어", WARN),
])

d.save("11-02.chapter-overview.svg")

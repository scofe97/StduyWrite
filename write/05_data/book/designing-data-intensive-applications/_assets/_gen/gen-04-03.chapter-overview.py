# 04-03 개요 — B-tree와 LSM 두 저장 엔진 학파의 갈림과 네 절의 핵심 대상 및 비교 축.
# 사실 출처: 04-03 서두(L21~L26), §1(L30~L38), §2(L43~L50), §3(L54~L60), §4(L64~L72).
# 타입 스펙: type-architecture
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

W = 880
PY, PH = 104, 268
LEG = PY + PH + 32
H = LEG + 56

d = D(W, H, "04-03 · CHAPTER OVERVIEW", "B-tree와 LSM 저장 엔진 비교 지도",
      "고정 크기 페이지 제자리 갱신과 불변 파일 순차 쓰기의 설계 갈림을 네 절의 핵심 축으로 조망한다.",
      "페이지 구조 · 선행 로그 신뢰성 · 읽기·쓰기 특성 · 증폭과 디스크 공간")

CW = 196
GAP = 16
X0 = 24

cards = [
    ("§1", "B-tree 구조", "고정 페이지 트리",
     [("4~16 KiB 페이지", "고정 크기 블록 분할"),
      ("제자리 덮어쓰기", "in-place 갱신 방식"),
      ("O(log n) 깊이", "4레벨 · 최대 250 TB")],
     INFO),
    ("§2", "WAL 신뢰성", "선행 로그와 복구",
     [("다중 페이지 분할", "크래시 손상 위험"),
      ("append-only WAL", "트리 수정 전 디스크 기록"),
      ("크래시 복구", "일관 상태 복원 보장")],
     OK),
    ("§3", "읽기·쓰기 비교", "두 학파의 성능 갈림",
     [("B-tree 읽기 유리", "레벨당 1페이지 예측성"),
      ("LSM 쓰기 유리", "순차 쓰기 높은 처리량"),
      ("SSD 수명·GC", "랜덤 vs 순차 마모 차이")],
     ACC),
    ("§4", "증폭과 공간", "비용과 저장 효율",
     [("Write Amplification", "디스크 쓰기 배수 비교"),
      ("B-tree 단편화", "vacuum 프로세스 필요"),
      ("LSM 압축·스냅샷", "compaction 파일 절감")],
     WARN),
]

FOCAL = 2

for i, (sec, title, role, items, card_c) in enumerate(cards):
    x = X0 + i * (CW + GAP)
    is_focal = (i == FOCAL)

    # 카드 외곽
    if is_focal:
        d.box(x, PY, CW, PH, PAPER2, ACC, 1.4)
    else:
        d.box(x, PY, CW, PH, PAPER2, RULE, 0.9)

    # 절 헤더: 칩(sec) + 제목
    d.chip(x + 28, PY + 22, sec, card_c, 11)
    d.t(x + CW / 2 + 14, PY + 26, title, 13, INK, KR, "middle", 600)
    d.t(x + CW / 2, PY + 46, role, 12, SOFT, KR, "middle")
    d.line(x + 12, PY + 56, x + CW - 12, PY + 56, RULE, 0.8)

    # 내부 항목 3개
    for j, (top_txt, bot_txt) in enumerate(items):
        iy = PY + 68 + j * 64

        if is_focal and j == 1:
            d.tone(x + 12, iy, CW - 24, 52, ACC, 6, "22", 1.4)
            d.t(x + CW / 2, iy + 22, top_txt, 12, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 40, bot_txt, 12, ACC, KR, "middle")
        elif is_focal:
            d.tone(x + 12, iy, CW - 24, 52, ACC, 6, "12", 1.0)
            d.t(x + CW / 2, iy + 22, top_txt, 12, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 40, bot_txt, 12, MUTED, KR, "middle")
        elif i == 1 and j == 1:
            d.tone(x + 12, iy, CW - 24, 52, OK, 6, "1A", 1.2)
            d.t(x + CW / 2, iy + 22, top_txt, 12, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 40, bot_txt, 12, OK, KR, "middle")
        elif i == 3 and j == 0:
            d.tone(x + 12, iy, CW - 24, 52, WARN, 6, "1A", 1.2)
            d.t(x + CW / 2, iy + 22, top_txt, 12, INK, MONO, "middle", 600)
            d.t(x + CW / 2, iy + 40, bot_txt, 12, WARN, KR, "middle")
        else:
            d.box(x + 12, iy, CW - 24, 52, PAPER, RULE, 0.8)
            d.t(x + CW / 2, iy + 22, top_txt, 12, INK, MONO if any(c in top_txt for c in "0123456789~") else KR, "middle", 600)
            d.t(x + CW / 2, iy + 40, bot_txt, 12, MUTED, KR, "middle")

# 카드 간 수평 연결 화살표
for i in range(3):
    x1 = X0 + i * (CW + GAP) + CW
    x2 = x1 + GAP
    y = PY + PH / 2
    d.arrow([(x1 + 2, y), (x2 - 4, y)], SOFT, "soft", 1.3)

d.legend(LEG, [
    ("핵심 비교 축", ACC),
    ("페이지 기반 구조", INFO),
    ("내구성·복구 메커니즘", OK),
    ("저장 비용·증폭", WARN)
])

d.save("04-03.chapter-overview.svg")

# 07-01 §5 샤드 분할 — 임계 크기 초과에 따른 하위 범위 분할과 새 파일 재작성 및 노드 이전 프로세스.
# 사실 출처: 07-01 본문 §5(L76~L84)·면접 질문 3(L96), DDIA 2판 7장 "Rebalancing key-range sharded data" (PDF 9~10쪽).
# B-tree 상위 수준 비유는 본문 L76. 10 GB·처리량 임계치·작은 핫 샤드 분할·재작성 과부하 위험은 PDF 10쪽, 여러 노드 분산·병합·사전 분할은 PDF 9쪽.
# 타입 스펙: type-process
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, BAD, KR, MONO

W = 880
CARD_H = 66 + 2 * 56 + 8
H = 104 + CARD_H + 14 + 40 + 86
LEG = H - 46

d = D(W, H, "07-01 · §5 PROCESS", "키 범위 샤드 분할과 재배치 프로세스",
      "샤드가 설정 크기(HBase 기본 10 GB)나 쓰기 처리량 임계치를 넘으면 하위 범위로 나누고, 새 파일 재작성 비용을 치른 뒤 작은 샤드를 여러 노드로 분산한다.",
      "설정 크기·처리량 초과 · 하위 범위 분할 · 새 파일 재작성 · 여러 노드로 분산")

COL_W = 192
GAP = 14
X0 = 36
Y_CARDS = 104

steps = [
    ("01 · 임계치 도달", "크기 또는 처리량 초과", WARN, [
        ("설정 크기 초과", "HBase 기본 10 GB"),
        ("쓰기 처리량 임계치 초과", "작은 핫 샤드도 분할"),
    ]),
    ("02 · 하위 분할", "연속 하위 범위", INFO, [
        ("하위 범위 둘로 분할", "각자 연속 키 구간"),
        ("B-tree 상위 수준", "비슷한 분할 과정"),
    ]),
    ("03 · 파일 재작성", "고비용 작업", ACC, [
        ("모든 데이터 새 파일로", "컴팩션과 비슷한 재작성"),
        ("핫 샤드 분할", "과부하 악화 위험"),
    ]),
    ("04 · 노드 분산", "작은 샤드 재배치", OK, [
        ("작은 샤드들", "여러 노드로 분산"),
        ("분할 중 서빙", "기존 할당으로 읽기·쓰기"),
    ]),
]

FOCAL = 2

for i, (s_chip, s_sub, s_col, items) in enumerate(steps):
    x = X0 + i * (COL_W + GAP)
    is_focal = (i == FOCAL)

    # 외곽 상자
    if is_focal:
        d.box(x, Y_CARDS, COL_W, CARD_H, PAPER2, ACC, 1.4)
    else:
        d.box(x, Y_CARDS, COL_W, CARD_H, PAPER2, RULE, 0.9)

    # 헤더: 칩 + 서브라벨
    d.chip(x + COL_W / 2, Y_CARDS + 18, s_chip, s_col, 11)
    d.t(x + COL_W / 2, Y_CARDS + 44, s_sub, 12, INK if is_focal else s_col, KR, "middle", 600)
    d.line(x + 12, Y_CARDS + 54, x + COL_W - 12, Y_CARDS + 54, RULE, 0.8)

    # 3개 항목
    for j, (top_t, bot_t) in enumerate(items):
        iy = Y_CARDS + 66 + j * 56
        d.tone(x + 10, iy, COL_W - 20, 48, s_col, 4, "12", 0.9)
        d.t(x + COL_W / 2, iy + 20, top_t, 12, INK, KR, "middle", 600)
        d.t(x + COL_W / 2, iy + 36, bot_t, 11, MUTED, KR if any("가" <= c <= "힣" for c in bot_t) else MONO, "middle")

    # 단계 간 연결 화살표 (오른쪽 카드로)
    if i < len(steps) - 1:
        ax = x + COL_W
        ay = Y_CARDS + 18
        d.arrow([(ax + 2, ay), (ax + GAP - 2, ay)], MUTED, "ar", 1.3)

# 하단: 사전 분할(Pre-splitting) 안내 배너
Y_PRE = Y_CARDS + CARD_H + 14
d.tone(36, Y_PRE, W - 72, 40, INFO, 4, "12", 1.0)
d.t(48, Y_PRE + 17, "사전 분할 (Pre-splitting)", 11.5, INFO, KR, "start", 600)
d.t(48, Y_PRE + 31, "빈 데이터베이스 · 초기 샤드 미리 설정 · 예상 키 분포 필요", 11.5, INK, KR, "start")

# 하단 범례
d.legend(LEG, [
    ("임계치 도달", WARN),
    ("하위 범위 분할", INFO),
    ("파일 재작성", ACC),
    ("노드 분산", OK),
])

d.save("07-01.shard-split.svg")

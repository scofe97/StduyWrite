# 02-02 §7 — MySQL 쿼리 지연을 둘로 나눠 큰 쪽만 따라간 여섯 단계(지연의 이진 탐색).
# 타입 스펙: type-tree — 부모 하나가 자식 둘로 갈리고, 고른 자식만 다시 갈린다.
#           원서 2.5.13(p.42)·그림 2.14. 예시 답은 원서의 괄호 답. 셋째 질문은 원서가 둘로 나누지 않아 "그 밖의 대기"로 짝을 채웠다.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import ACC, MUTED, SOFT, INK, INFO, PAPER2, RULE, KR, MONO

W, H = 928, 600
LX, XL, XR, XM = 24, 360, 664, 512
BW, BH, Y0, STRIDE = 216, 40, 116, 72

d = DK(W, H, "SYSTEMS PERFORMANCE · 02-02 §7",
       "지연을 둘로 나눠 큰 쪽만 따라간다",
       "MySQL 쿼리 지연 예에서 매 질문이 지연을 둘로 나누고, 더 큰 쪽(색 칸)만 다시 나눈다. 흐린 칸은 버린 갈래다.",
       "원서 2.5.13 · 괄호 안이 원서의 예시 답")

ROWS = [  # (질문, 왼쪽, 오른쪽, 고른 쪽 0/1)
    ("Q2 어디서 시간을 쓰나", "on-CPU", "off-CPU 대기", 1),
    ("Q3 무엇을 기다리나", "파일시스템 I/O", "그 밖의 대기", 0),
    ("Q4 FS I/O 의 원인", "디스크 I/O", "락 경합", 0),
    ("Q5 디스크 시간의 몫", "큐잉", "서비스", 1),
    ("Q6 서비스 시간의 몫", "초기화", "데이터 전송", 1),
]

def node(cx, y, txt, state):
    if state == "pick": d.tone(cx - BW / 2, y, BW, BH, INFO, 6)
    elif state == "final": d.tone(cx - BW / 2, y, BW, BH, ACC, 6)
    else: d.box(cx - BW / 2, y, BW, BH, PAPER2, RULE, 1.0, 6)
    c = SOFT if state == "drop" else INK
    d.t(cx, y + 26, txt, 13, c, KR if any("가" <= ch <= "힣" for ch in txt) else MONO, "middle", 400 if state == "drop" else 600)

d.t(LX, Y0 + 26, "Q1 쿼리 지연 이슈?", 12, SOFT, KR, "start")
node(XM, Y0, "쿼리 지연 — 예", "pick")
px = XM
for i, (q, a, b, pick) in enumerate(ROWS):
    y = Y0 + (i + 1) * STRIDE
    ymid = y - (STRIDE - BH) / 2
    d.line(px, y - STRIDE + BH, px, ymid, MUTED, 1.2)
    d.line(XL, ymid, XR, ymid, MUTED, 1.2)
    for cx in (XL, XR):
        d.arrow([(cx, ymid), (cx, y - 4)], MUTED, "ar", 1.2)
    last = i == len(ROWS) - 1
    for k, (cx, txt) in enumerate(((XL, a), (XR, b))):
        st = ("final" if last else "pick") if k == pick else "drop"
        node(cx, y, txt, st)
    d.t(LX, y + 26, q, 12, SOFT, KR, "start")
    px = XR if pick else XL

d.legend(Y0 + 6 * STRIDE + 8, [("더 큰 쪽 — 다시 나눈다", INFO), ("근본 원인", ACC), ("버린 갈래", MUTED)])
d.save("02-02.latency-binary-search.svg")

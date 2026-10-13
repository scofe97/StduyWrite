# 타입 스펙: type-dp-security-matrix — 행 셋(CP 모두 확인 · CP 과반 확인 · AP)과 열 셋(쓰기 · n3 읽기 · 복구 뒤)의 격자에서 같은 n1·n2·n3 값이 어떻게 갈리는지 비교한다. focal 은 n3 읽기 열.
# 사실 출처: n1·n2·n3 와 n3 단절 · CP 는 쓰기 차단 · AP 는 낡은 데이터 읽기와 복구 뒤 동기화는 추출본 v2.txt 1563~1588행(PDF 91·92쪽 그림), 일관성 위해 최신을 확인 못 하는 쪽이 거절하는 것은 Brewer 2012 "Why 2 of 3 is misleading".
#   잔액 100 → 70 과 W·R 값은 설계 예시(은행 잔액 예는 v2.txt 1582~1585행).
# Layout conventions: 행 이름 열 x=24 폭 184, 셀 폭 232 · stride 240(x=216·456·696), 머리 y=100 높이 36, 행 stride 112(y=148·260·372) 높이 100, 노드 칩 폭 64 · 높이 28 · stride 72. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, MUTED, INK, PAPER, PAPER2, RULE, SOFT, INFO, KR, MONO

W, H = 960, 580
d = D(W, H, "SYSTEM DESIGN INTERVIEW · 06-01 §2",
      "n3 가 끊기면 CP 는 오류를 돌려주고 AP 는 낡은 값 100 을 돌려준다",
      "n3 가 n1·n2 와 끊긴 채 잔액 100 을 70 으로 바꾸는 요청이 n1 에 오면, 같은 세 노드의 값과 응답이 정책마다 갈린다.",
      "칩의 숫자는 노드가 가진 잔액")

XS = (216, 456, 696)
YS = (148, 260, 372)
CW, CH = 232, 100
HY = 100

HEAD = ("쓰기 70 → n1", "읽기 → n3", "복구 뒤")
ROWS = (("CP · 모두 확인", "W = 3 · R = 1"), ("CP · 과반 확인", "W = 2 · R = 2"), ("AP · 한 곳 확인", "W = 1 · R = 1"))
# (노드 값 셋, 응답 문구, 응답 색)
CELLS = (
    (((100, 100, 100), "쓰기 거절", BAD), ((100, 100, 100), "100 반환", OK), ((100, 100, 100), "쓰기 재개", OK)),
    (((70, 70, 100), "쓰기 수락", OK), ((70, 70, 100), "오류", BAD), ((70, 70, 70), "n3 따라잡음", OK)),
    (((70, 70, 100), "쓰기 수락", OK), ((70, 70, 100), "100 반환 · 낡음", WARN), ((70, 70, 70), "n3 따라잡음", OK)),
)

# 갈리는 열 — focal
fx = XS[1]
d.tone(fx - 4, HY - 8, CW + 8, 372 + CH - HY + 16, ACC, 8, "10", 1.4)

for j, h in enumerate(HEAD):
    d.t(XS[j] + CW / 2, HY + 24, h, 14, INK, KR, "middle", 600)
for i, (nm, sub) in enumerate(ROWS):
    y = YS[i]
    d.t(24, y + 40, nm, 14, INK, KR, "start", 600)
    d.t(24, y + 64, sub, 12, MUTED, MONO, "start")
    for j in range(3):
        vals, out, oc = CELLS[i][j]
        x = XS[j]
        d.box(x, y, CW, CH, PAPER2, RULE, 0.9, 6)
        for k, v in enumerate(vals):
            fresh = v == 70 or (v == 100 and 70 not in vals)
            c = OK if fresh else WARN
            cx = x + 12 + 72 * k
            d.tone(cx, y + 14, 64, 28, c, 4, "14", 1.1)
            d.t(cx + 32, y + 33, f"n{k + 1} {v}", 12, c, MONO, "middle", 600)
        d.t(x + CW / 2, y + 76, out, 14, oc, KR, "middle", 600)

d.legend(H - 56, [("최신 값", OK), ("낡은 값", WARN), ("오류 · 거절", BAD), ("갈리는 열", ACC)])
d.save("06-01.cap-partition.svg")

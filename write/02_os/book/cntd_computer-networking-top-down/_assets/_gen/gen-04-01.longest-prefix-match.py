# 04-01 §4 — 원문 4.2.1 의 접두 표를 트라이로 편 것. 최장 접두 일치는 가장 깊이 내려간 잎을 고르는 일이다.
# 접두와 인터페이스 배정은 원문 표 그대로이고, 세 예시 주소의 판정도 코드로 검산해 원문과 일치함을 확인했다.
# 앞 16비트(11001000 00010111)는 세 항목이 모두 공유하므로 뿌리에 접어 두고 그 뒤부터 그린다.
# 타입 스펙: type-tree — 분류 자체가 트리다. 부모의 성질이 자식에게 이어지고, 잎이 최종 판정이다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, WARN, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 616
NW, NH = 116, 44

d = D(W, H, "COMPUTER NETWORKING TOP-DOWN · 04-01 §4",
      "가장 깊이 내려간 곳이 답입니다",
      "원문의 접두 표를 트라이로 편 것. 한 주소가 여러 항목에 맞을 수 있어서 가장 긴 접두를 고른다.",
      "앞 16비트는 셋이 공유하므로 뿌리에 접어 두었습니다")

def node(cx, cy, label, sub, c=MUTED, focal=False, w=NW):
    if focal: d.tone(cx - w / 2, cy - NH / 2, w, NH, c, 6, "14", 1.4)
    else: d.box(cx - w / 2, cy - NH / 2, w, NH, PAPER2, RULE, 1.0, 6)
    d.t(cx, cy - 2, label, 12, c if focal else INK, MONO, "middle", 600)
    if sub: d.t(cx, cy + 16, sub, 12, SOFT, KR)

ROOT = (500, 154)
node(*ROOT, "11001000 00010111", "공통 16비트", INFO, True, 260)

L1 = [(300, 250, "…0001 0"), (700, 250, "…0001 1")]
for x, y, lab in L1:
    node(x, y, lab, "20비트", MUTED)
    d.path(f"M 500 {ROOT[1] + NH/2 + 2} L 500 204 L {x} 204 L {x} {y - NH/2 - 8}", MUTED, 1.2, m="ar")

node(220, 348, "…00010", "21비트", OK, True)
d.path(f"M 300 {250 + NH/2 + 2} L 300 300 L 220 300 L 220 {348 - NH/2 - 8}", MUTED, 1.2, m="ar")
node(600, 348, "…00011", "21비트", OK, True)
d.path(f"M 700 {250 + NH/2 + 2} L 700 300 L 600 300 L 600 {348 - NH/2 - 8}", MUTED, 1.2, m="ar")
node(824, 348, "…00011000", "24비트", ACC, True, 148)
d.path(f"M 700 {250 + NH/2 + 2} L 700 300 L 824 300 L 824 {348 - NH/2 - 8}", ACC, 1.4, m="acc")

LEAF = [(220, 446, "인터페이스 0", OK), (600, 446, "인터페이스 2", OK), (824, 446, "인터페이스 1", ACC)]
for x, y, lab, c in LEAF:
    d.box(x - NW / 2, y - 20, NW, 40, PAPER, c, 1.2, 6)
    d.t(x, y + 4, lab, 12, c, KR)
    d.path(f"M {x} {348 + NH/2 + 2} L {x} {y - 26}", c, 1.2, m="acc" if c is ACC else "ok")

d.box(24, 486, 420, 62, PAPER2, RULE, 0.9, 6)
d.t(40, 510, "…00011000 10101010 은 21비트와 24비트 둘 다에 맞습니다", 12, SOFT, KR, "start")
d.t(40, 532, "긴 쪽인 24비트가 이겨 인터페이스 1 로 갑니다", 12, ACC, KR, "start")

d.t(468, 510, "어느 항목에도 안 맞으면 길이 0 인 기본 항목이 이깁니다 — 인터페이스 3.", 12, MUTED, KR, "start")
d.t(468, 532, "TCAM 의 '신경 안 씀' 비트가 이 접두 표를 작게 유지하는 열쇠입니다.", 12, MUTED, KR, "start")

d.legend(H - 44, [("가장 긴 접두", ACC), ("더 짧은 접두", OK), ("공통 부분", INFO)])
d.save("04-01.longest-prefix-match.svg")

# 타입 스펙: type-tree — 뿌리 [8] ____btf_map_config, 가지 둘(key · value), 가지마다 type_id 사슬이 잎까지 이어지는 좌→우 트리. 아래에 같은 구조체의 바이트 자 0~15.
# 사실 출처: 추출본 src/ebpf5.txt 338~340행([1] u32 → [2] __u32 → [3] unsigned int size=4), 368~372행([4] user_msg_t size=12 · [5] char · [6] ARRAY nr_elems=12 · [7] __ARRAY_SIZE_TYPE__),
#   402~405행([8] ____btf_map_config size=16 · key bits_offset=0 · value bits_offset=32). user_msg_t 의 message 는 이 출력을 낸 실행의 12바이트(nr_elems=12).
# Layout conventions: 열 x=24·372·568·832, 상자 폭 200·148·148·148 높이 56, 키 줄 y=132 · 값 줄 y=276, 잎 둘은 값 줄 중앙 ±40. 바이트 자는 30px 한 칸. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 1000, 556
d = D(W, H, "LEARNING EBPF · 05-01 §3", "type_id 사슬이 config 맵의 키와 값 배치를 잇는다",
      "구조체 ____btf_map_config(16바이트)의 key 는 bits_offset=0 에서 u32 → __u32 → unsigned int 사슬로, value 는 bits_offset=32 에서 user_msg_t → char 12칸 배열로 이어진다.",
      "대괄호 안 숫자가 type_id 입니다")

NH = 56
C0, C1, C2, C3 = 24, 372, 568, 832
W0, WN = 200, 148
YK, YV = 132, 276
Y5, Y7 = YV - 40, YV + 40   # [5] 위 · [7] 아래
RY = (YK + NH // 2 + YV + NH // 2) // 2 - 32
SPX = 240


def node(x, y, w, title, sub, c, fill="12", sw=1.2):
    if c is None:
        d.box(x, y, w, NH, PAPER2, RULE, 0.9, 6)
        tc = INK
    else:
        d.tone(x, y, w, NH, c, 6, fill, sw)
        tc = c
    d.t(x + w / 2, y + 24, title, 13, tc, MONO, "middle", 600)
    d.t(x + w / 2, y + 44, sub, 13 if any("가" <= ch <= "힣" for ch in sub) else 12, MUTED, KR if any("가" <= ch <= "힣" for ch in sub) else MONO)


# 뿌리
node(C0, RY, W0, "[8] ____btf_map_config", "STRUCT · size=16", INFO)
# 키 사슬
node(C1, YK, WN, "[1] u32", "key · TYPEDEF", None)
node(C2, YK, WN, "[2] __u32", "TYPEDEF", None)
node(C3, YK, WN, "[3] unsigned int", "INT · size=4", OK)
# 값 사슬
node(C1, YV, WN, "[4] user_msg_t", "value · size=12", INFO)
node(C2, YV, WN, "[6] ARRAY", "nr_elems=12", None)
node(C3, Y5, WN, "[5] char", "원소 · size=1", OK)
node(C3, Y7, WN, "[7] INT", "__ARRAY_SIZE_TYPE__", OK)

# 뿌리 → 키·값 (척추 + 엘보 화살표 + 오프셋 칩)
rcy = RY + NH // 2
d.line(C0 + W0, rcy, SPX, rcy, MUTED, 1.2)
d.line(SPX, YK + NH // 2, SPX, YV + NH // 2, MUTED, 1.2)
d.arrow([(SPX, YK + NH // 2), (C1 - 6, YK + NH // 2)], MUTED, "ar", 1.5)
d.arrow([(SPX, YV + NH // 2), (C1 - 6, YV + NH // 2)], MUTED, "ar", 1.5)
d.chip((SPX + C1) // 2, YK + NH // 2 - 18, "bits_offset=0", MUTED, 11)
d.chip((SPX + C1) // 2, YV + NH // 2 - 18, "bits_offset=32", ACC, 11)

# 사슬 화살표
for (a, b, y) in ((C1, C2, YK), (C2, C3, YK), (C1, C2, YV)):
    d.arrow([(a + WN + 2, y + NH // 2), (b - 6, y + NH // 2)], MUTED, "ar", 1.5)
# [6] → [5] 원소, [6] → [7] 인덱스 (엘보)
mx = C2 + WN + 24
vcy = YV + NH // 2
d.line(C2 + WN + 2, vcy, mx, vcy, MUTED, 1.4)
d.arrow([(mx, vcy), (mx, Y5 + NH // 2), (C3 - 6, Y5 + NH // 2)], MUTED, "ar", 1.5)
d.arrow([(mx, vcy), (mx, Y7 + NH // 2), (C3 - 6, Y7 + NH // 2)], MUTED, "ar", 1.5)
d.chip(mx + 48, Y5 + NH // 2 - 18, "원소", MUTED, 13)
d.chip(mx + 48, Y7 + NH // 2 - 18, "인덱스", MUTED, 13)

# 바이트 자 — 같은 16바이트
RX0, CELL, RYY = 24, 30, 420
d.t(RX0, RYY - 12, "메모리 위치(바이트)", 13, SOFT, KR, "start", 600)
d.tone(RX0, RYY, 4 * CELL, 36, OK, 4, "12", 1.2)
d.tone(RX0 + 4 * CELL, RYY, 12 * CELL, 36, INFO, 4, "12", 1.2)
d.t(RX0 + 2 * CELL, RYY + 23, "key", 12, OK, MONO, "middle", 600)
d.t(RX0 + 4 * CELL + 6 * CELL, RYY + 23, "value · message[12]", 12, INFO, MONO, "middle", 600)
for off in (0, 4, 16):
    d.t(RX0 + off * CELL, RYY + 54, str(off), 11, MUTED, MONO)

d.legend(H - 56, [("STRUCT", INFO), ("INT", OK), ("value 시작 오프셋", ACC)])
d.save("05-01.btf-type-chain.svg")

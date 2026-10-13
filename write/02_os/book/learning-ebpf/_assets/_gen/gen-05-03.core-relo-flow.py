# 타입 스펙: type-data-flow — 레인 셋(오브젝트 · libbpf · vmlinux BTF) × 단계 넷(기록 · 후보 · 대응 · 패치). 값(type_id 24 · 0:0:0 · [205] · off 0 -> 0)이 칸마다 움직인다.
#   focal 은 libbpf 가 명령에 오프셋을 다시 쓰는 건넘 하나. 스펙의 데이터 종류 칩(WB·DB·TB·FL·LS)은 이 흐름의 값이 아니라 생략하고 값을 부제로 실었다.
# 사실 출처: 추출본 src/ebpf5.txt 1259~1265행(bpftool -d prog load 출력: CO-RE relocating [24] struct user_pt_regs · found target candidate [205] · relo #0 <byte_off> … (0:0:0 @ offset 0) ·
#   matching candidate #0 · patched insn #1 (LDX/ST/STX) off 0 -> 0). 필드 의미는 linux v7.2 include/uapi/linux/bpf.h 7633~7686행, 패치 로그 문자열은 libbpf v1.8.0 src/relo_core.c 1105행.
# Layout conventions(스펙 §2 를 본문 폭 960 에 맞춰 키움): label_col 144 · step_slot 192 · node 168×88 · lane_h 112 · header 56. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 960, 556
d = D(W, H, "LEARNING EBPF · 05-03 §2",
      "relo #0 이 insn #1 의 오프셋을 다시 쓰기까지",
      "오브젝트의 재배치 레코드 relo #0 이 type_id 24 와 접근 문자열 0:0:0 을 가리키고, libbpf 가 vmlinux BTF 의 [205] struct user_pt_regs 를 후보로 찾아 regs[0] 의 오프셋 0 을 확인한 뒤 insn #1 의 off 를 0 에서 0 으로 쓴다.",
      "같은 기계라서 값은 그대로, 기록 한 줄이 명령 한 줄을 고친다")

LABEL_W, SLOT, NW, NH, LH = 144, 192, 168, 88, 112
Y_HEAD, Y0 = 92, 148
LANES = [("오브젝트", ".bpf.o", INFO), ("libbpf", "적재 때", OK), ("vmlinux", "BTF", MUTED)]
STEPS = [("01", "기록"), ("02", "후보"), ("03", "대응"), ("04", "패치")]
FOCAL_STEP = 3


def cx(j):
    return LABEL_W + j * SLOT + SLOT // 2


def top(k):
    return Y0 + k * LH


def fam(t):
    return KR if any("가" <= c <= "힣" for c in str(t)) else MONO


# 레인 바탕과 구분선
for k, (a, b, c) in enumerate(LANES):
    if k % 2 == 0:
        d.o.append(f'<rect x="12" y="{top(k)}" width="{W - 24}" height="{LH}" fill="#F5F5F3" fill-opacity="0.025"/>')
    d.line(12, top(k), W - 12, top(k), RULE, 0.8)
    d.t(76, top(k) + LH / 2 - 2, a, 13, c, fam(a), "middle", 600)
    d.t(76, top(k) + LH / 2 + 16, b, 12, MUTED, fam(b))
d.line(12, top(3), W - 12, top(3), RULE, 0.8)
d.line(LABEL_W, Y0, LABEL_W, top(3), RULE, 0.8)

# 단계 머리
for j, (num, name) in enumerate(STEPS):
    foc = j == FOCAL_STEP
    d.tone(cx(j) - 18, Y_HEAD - 2, 36, 22, ACC if foc else INK, 11, "33" if foc else "1F", 1.0)
    d.t(cx(j), Y_HEAD + 13, num, 12, ACC if foc else INK, MONO, "middle", 600)
    d.t(cx(j), Y_HEAD + 38, name, 12, ACC if foc else MUTED, KR, "middle", 600)

# 화살표는 노드보다 먼저 — 가로 먼저 꺾어 세로로 들어간다
nx = lambda j: cx(j) - NW // 2
ny = lambda k: top(k) + 12
mid = lambda k: ny(k) + NH // 2
d.arrow([(nx(0) + NW + 2, mid(0)), (cx(1), mid(0)), (cx(1), ny(1) - 6)], MUTED, "ar", 1.4)
d.arrow([(cx(1), ny(1) + NH + 2), (cx(1), ny(2) - 6)], MUTED, "ar", 1.4)
d.arrow([(nx(1) + NW + 2, mid(2)), (cx(2), mid(2)), (cx(2), ny(1) + NH + 6)], MUTED, "ar", 1.4)
d.arrow([(nx(2) + NW + 2, mid(1)), (cx(3), mid(1)), (cx(3), ny(0) + NH + 6)], ACC, "acc", 1.8)
d.chip(cx(3), (mid(1) + ny(0) + NH) // 2, "다시 쓰기", ACC, 12)

NODES = [
    (0, 0, "relo #0", "insn #1 · type_id 24", "0:0:0 · byte_off", INFO, False),
    (1, 1, "후보 탐색", "[24] user_pt_regs", "target candidate", OK, False),
    (1, 2, "[205]", "struct user_pt_regs", "in [vmlinux]", MUTED, False),
    (2, 1, "후보 #0 대응", "regs[0] @ offset 0", "<byte_off>", OK, False),
    (3, 0, "insn #1", "off 0 -> 0", "LDX/ST/STX", ACC, True),
]
for j, k, title, sub, l3, c, foc in NODES:
    x, y = nx(j), ny(k)
    d.tone(x, y, NW, NH, ACC if foc else c, 6, "1F" if foc else "12", 1.4 if foc else 1.2)
    d.t(x + NW / 2, y + 28, title, 14, INK, fam(title), "middle", 600)
    d.t(x + NW / 2, y + 52, sub, 12, MUTED, fam(sub))
    d.t(x + NW / 2, y + 72, l3, 12, SOFT, fam(l3))

d.legend(H - 56, [("오브젝트에 기록된 값", INFO), ("libbpf 의 작업", OK), ("vmlinux BTF 의 타입", MUTED), ("패치 결과", ACC)])
d.save("05-03.core-relo-flow.svg")

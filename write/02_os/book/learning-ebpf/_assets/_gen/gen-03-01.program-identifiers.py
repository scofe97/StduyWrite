# 타입 스펙: type-tree — 커널에 적재된 BPF 프로그램 식별자 계층과 참조 객체 트리
# 사실 출처: 본문 §4 bpftool prog show id 540, v7.2 kernel/bpf/core.c L301~337 bpf_prog_calc_tag; 예제 태그는 SHA-1 시절 값
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 920, 520
d = D(W, H, "LEARNING EBPF · 03-01 §4",
      "적재된 eBPF 프로그램의 식별자와 참조 객체 구조",
      "bpftool 은 프로그램을 ID·이름·태그·고정 경로로 지정하며 맵과 BTF 를 참조합니다",
      "커널 내부 ID · 함수 이름 · 명령어 해시 태그 · 고정 경로 및 참조 맵")

# 뿌리 노드 (Root)
RX, RY, RW, RH = 360, 100, 200, 48
d.box(RX, RY, RW, RH, PAPER2, RULE, 1.2, 8)
d.t(RX + RW//2, RY + 20, "프로그램 hello", 14, INK, KR, "middle", 600)
d.t(RX + RW//2, RY + 36, "type xdp · bpf_prog", 11, MUTED, MONO, "middle")

# 중간 브랜치 2개 (식별자 묶음, 참조 객체 묶음)
BX1, BY, BW, BH = 140, 184, 260, 44
BX2 = 520
d.box(BX1, BY, BW, BH, PAPER2, RULE, 1.2, 6)
d.t(BX1 + BW//2, BY + 20, "네 가지 식별자", 13, INK, KR, "middle", 600)
d.t(BX1 + BW//2, BY + 34, "ID · 이름 · 태그 · 고정 경로", 11, MUTED, KR, "middle")

d.tone(BX2, BY, BW, BH, INFO, 6, "15", 1.2)
d.t(BX2 + BW//2, BY + 20, "참조 객체", 13, INFO, KR, "middle", 600)
d.t(BX2 + BW//2, BY + 34, "BPF 맵 및 BTF 타입 정보", 11, MUTED, KR, "middle")

# 뿌리에서 브랜치 연결선
d.line(RX + RW//2, RY + RH, RX + RW//2, 164, MUTED, 1.2)
d.line(BX1 + BW//2, 164, BX2 + BW//2, 164, MUTED, 1.2)
d.line(BX1 + BW//2, 164, BX1 + BW//2, BY, MUTED, 1.2)
d.line(BX2 + BW//2, 164, BX2 + BW//2, BY, MUTED, 1.2)

# 식별자 잎 노드들 (세로 목록)
ID_LEAVES = [
    ("ID: 540", "적재마다 새로 붙음", OK),
    ("name: hello", "함수 이름 · 겹칠 수 있음", WARN),
    ("tag: d35b94b4c0c10efb", "명령 해시 앞 8바이트 · 명령이 같으면 같음", ACC),
    ("pinned: /sys/fs/bpf/hello", "고정 경로 · 유일", OK),
]

LX = BX1
LY0 = 250
L_STRIDE = 48
d.line(LX + 20, BY + BH, LX + 20, LY0 + 3 * L_STRIDE + 20, RULE, 1.2)

for i, (title, sub, c) in enumerate(ID_LEAVES):
    ly = LY0 + i * L_STRIDE
    d.line(LX + 20, ly + 20, LX + 36, ly + 20, RULE, 1.2)
    d.box(LX + 36, ly, 300, 40, PAPER, RULE, 0.9, 4)
    d.t(LX + 48, ly + 18, title, 11, c, MONO, "start", 600)
    d.t(LX + 48, ly + 32, sub, 11, MUTED, KR, "start")

# 참조 객체 잎 노드들
REF_LEAVES = [
    ("map_ids: [165, 166]", "프로그램이 참조하는 맵 두 개", INFO),
    ("btf_id: 254", "-g 로 만든 BTF 블록", INFO),
]

RX2 = BX2
d.line(RX2 + 20, BY + BH, RX2 + 20, LY0 + 1 * L_STRIDE + 20, RULE, 1.2)

for i, (title, sub, c) in enumerate(REF_LEAVES):
    ly = LY0 + i * L_STRIDE
    d.line(RX2 + 20, ly + 20, RX2 + 36, ly + 20, RULE, 1.2)
    d.box(RX2 + 36, ly, 300, 40, PAPER, RULE, 0.9, 4)
    d.t(RX2 + 48, ly + 18, title, 11, c, MONO, "start", 600)
    d.t(RX2 + 48, ly + 32, sub, 11, MUTED, KR, "start")

d.legend(H - 46, [
    ("고유 식별자", OK),
    ("명령어 태그", ACC),
    ("외부 참조 객체", INFO),
    ("중복 가능 이름", WARN),
])

d.save("03-01.program-identifiers.svg")

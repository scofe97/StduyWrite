# 타입 스펙: type-tree — 뿌리 하나, 묶음 넷, 묶음 아래 세로 목록(잎). 깊이 3.
# 사실 출처: 커널 v7.2 include/uapi/linux/bpf.h 1001~1050행(enum bpf_map_type), Documentation/bpf/map_*.rst
#   (array·hash·lpm_trie·queue_stack·bloom_filter·sockmap·devmap·of_maps), 추출본 src/ebpf2.txt 277~303행.
# Layout conventions: 묶음 열 stride 224, 잎 높이 36·stride 44, 잎은 묶음 아래 세로 척추에 엘보로 잇는다(스펙의 깊이 4·폭 5 안).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 920, 560
d = D(W, H, "LEARNING EBPF · 02-01 §3", "맵 종류는 키가 무엇이고 무엇에 쓰이는지로 묶인다",
      "BPF 맵은 배열 계열, 해시 계열, 특수 목적, 객체 참조 네 묶음으로 나뉜다. 해시 계열에는 per-CPU 와 LRU 변형이 있고 배열에도 per-CPU 변형이 있다. 이 편의 예제는 HASH 를 쓴다.",
      "per-CPU 변형은 배열과 해시 양쪽에 있습니다")

COLS = [
    ("배열 계열", "키는 4바이트 인덱스", [("ARRAY", "인덱스 → 값", None), ("PERCPU_ARRAY", "CPU 별 값", INFO)]),
    ("해시 계열", "키는 임의 타입", [("HASH", "키 → 값", ACC), ("PERCPU_HASH", "CPU 별 값", INFO), ("LRU_HASH", "오래된 것 제거", None), ("LRU_PERCPU_HASH", "CPU 별 값", INFO)]),
    ("특수 목적", "연산에 맞춘 구조", [("QUEUE", "FIFO", None), ("STACK", "LIFO", None), ("LPM_TRIE", "최장 접두사", None), ("BLOOM_FILTER", "있는지 검사", None)]),
    ("객체 참조", "객체 정보를 보관", [("SOCKMAP", "소켓", None), ("DEVMAP", "네트워크 장치", None), ("PROG_ARRAY", "프로그램", None), ("ARRAY_OF_MAPS", "맵 속의 맵", None), ("HASH_OF_MAPS", "맵 속의 맵", None)]),
]
X0, STRIDE, GW = 20, 224, 200
RX, RY, RW, RH = 340, 100, 240, 52
GY = 196

# 연결선 먼저
d.line(RX + RW/2, RY + RH, RX + RW/2, 176, MUTED, 1.2)
cx = [X0 + i*STRIDE + GW/2 for i in range(4)]
d.line(cx[0], 176, cx[-1], 176, MUTED, 1.2)
for i, (g, gs, leaves) in enumerate(COLS):
    x = X0 + i*STRIDE
    d.line(cx[i], 176, cx[i], GY, MUTED, 1.2)
    sx = x + 12
    last = 272 + (len(leaves)-1)*44 + 18
    d.line(sx, GY + 52, sx, last, RULE, 1.2)
    for k in range(len(leaves)):
        ly = 272 + k*44 + 18
        d.line(sx, ly, sx + 12, ly, RULE, 1.2)

d.box(RX, RY, RW, RH, PAPER2, RULE, 1.0)
d.t(RX + RW/2, RY + 24, "BPF 맵", 15, INK, KR, "middle", 600)
d.t(RX + RW/2, RY + 42, "대부분 키-값 저장소", 11, MUTED, KR)
for i, (g, gs, leaves) in enumerate(COLS):
    x = X0 + i*STRIDE
    d.box(x, GY, GW, 52, PAPER2, RULE, 1.0)
    d.t(x + GW/2, GY + 24, g, 14, INK, KR, "middle", 600)
    d.t(x + GW/2, GY + 42, gs, 11, MUTED, KR)
    for k, (name, hint, c) in enumerate(leaves):
        lx, ly = x + 24, 272 + k*44
        if c: d.tone(lx, ly, 176, 36, c, 5, "14", 1.3)
        else: d.box(lx, ly, 176, 36, PAPER2, RULE, 0.9, 5)
        d.t(lx + 8, ly + 23, name, 11, c or INK, MONO, "start", 600)
        d.t(lx + 168, ly + 23, hint, 11, MUTED, KR, "end")

d.legend(H - 56, [("이 편의 해시 맵", ACC), ("per-CPU 변형", INFO)])
d.save("02-01.map-types.svg")

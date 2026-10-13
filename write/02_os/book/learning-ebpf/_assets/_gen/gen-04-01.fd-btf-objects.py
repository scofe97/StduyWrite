# 타입 스펙: type-architecture — 존 둘(프로세스 fd 표 · 커널 객체)과 fd→객체 화살표 넷, 맵과 프로그램에서 BTF 로 가는 화살표 둘(focal).
# 사실 출처: 추출본 src/ebpf4.txt 192~269행(BTF_LOAD=3, output PERF_EVENT_ARRAY key 4 value 4 max_entries 4 = fd 4, config HASH key 4 value 12 max_entries 10240 btf_fd=3 = fd 5)
#   302~304행(PROG_LOAD KPROBE insn_cnt=44 license GPL prog_btf_fd=3 = fd 6), BTF 매직은 linux v7.2 include/uapi/linux/btf.h 줄 8~9(0xeB9F, version 1).
# Layout conventions: 노드 높이 72·stride 92, fd 열 x=32~332, 객체 열 x=428~672, 되돌이 세로선 x=720·800. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 960, 620
d = D(W, H, "LEARNING EBPF · 04-01 §2",
      "fd 번호표와 커널 객체, BTF 를 가리키는 두 화살표",
      "프로세스의 fd 3·4·5·6 은 각각 BTF·output 맵·config 맵·hello 프로그램을 가리킨다. config 는 btf_fd=3, hello 는 prog_btf_fd=3 으로 같은 BTF 를 가리킨다.",
      "번호가 객체를 가리키고 객체 둘이 다시 BTF 를 가리킵니다")

# 존
UZ = (16, 100, 332, 412)
KZ = (380, 100, 564, 412)
for (x, y, w, h), name, fam in ((UZ, "프로세스 · fd 표", KR), (KZ, "KERNEL", MONO)):
    d.box(x, y, w, h, PAPER2, RULE, 0.9, 8)
    d.t(x + 12, y + 20, name, 12 if fam == KR else 9, SOFT, fam, "start")

NH, ST, Y0 = 72, 92, 140
UX, UW = 32, 300
KX, KW = 428, 244
FD = [("fd 3", "BPF_BTF_LOAD"), ("fd 4", "BPF_MAP_CREATE"), ("fd 5", "BPF_MAP_CREATE"), ("fd 6", "BPF_PROG_LOAD")]
OBJ = [("BTF", "BTF_MAGIC 0xeB9F", "version 1"),
       ("output", "PERF_EVENT_ARRAY", "key 4 · value 4 · 칸 4"),
       ("config", "HASH", "key 4 · value 12 · 칸 10240"),
       ("hello", "KPROBE", "insn_cnt 44 · GPL")]
COL = [INFO, OK, OK, WARN]
MK = ["info", "ok", "ok", "warn"]

# 화살표 먼저(상자가 위로 오도록)
for k in range(4):
    y = Y0 + k * ST
    cy = y + NH // 2
    d.arrow([(UX + UW + 2, cy), (KX - 6, cy)], COL[k], MK[k], 1.5)
y_btf, y_cfg, y_hel = Y0, Y0 + 2 * ST, Y0 + 3 * ST
# config → BTF (안쪽 되돌이), hello → BTF (바깥 되돌이)
d.arrow([(KX + KW + 2, y_cfg + NH // 2), (720, y_cfg + NH // 2), (720, y_btf + 52), (KX + KW + 6, y_btf + 52)], ACC, "acc", 1.8)
d.arrow([(KX + KW + 2, y_hel + NH // 2), (800, y_hel + NH // 2), (800, y_btf + 20), (KX + KW + 6, y_btf + 20)], ACC, "acc", 1.8)
d.chip(720, 236, "btf_fd=3", ACC, 13)
d.chip(800, 316, "prog_btf_fd=3", ACC, 13)

for k in range(4):
    y = Y0 + k * ST
    d.tone(UX, y, UW, NH, COL[k], 6, "12", 1.2)
    d.t(UX + UW/2, y + 32, FD[k][0], 14, COL[k], MONO, "middle", 600)
    d.t(UX + UW/2, y + 54, FD[k][1], 13, MUTED, MONO)
    d.tone(KX, y, KW, NH, COL[k], 6, "12", 1.2)
    d.t(KX + KW/2, y + 26, OBJ[k][0], 14, COL[k], MONO, "middle", 600)
    d.t(KX + KW/2, y + 46, OBJ[k][1], 13, MUTED, MONO)
    d.t(KX + KW/2, y + 64, OBJ[k][2], 13, MUTED, KR if any("가" <= c <= "힣" for c in OBJ[k][2]) else MONO)

d.legend(H - 56, [("BTF", INFO), ("맵", OK), ("프로그램", WARN), ("BTF 참조", ACC)])
d.save("04-01.fd-btf-objects.svg")

# 타입 스펙: type-architecture — CO-RE 다섯 요소(BTF · 커널 헤더 · 컴파일러 · 라이브러리 · 스켈레톤)를 빌드 기계와 대상 기계 두 존에 놓고, 가운데 "적재 때 오프셋 수정" 화살표를 focal 로 둔다.
# 사실 출처: 추출본 src/ebpf5.txt 97~146행(다섯 요소: BTF · 커널 헤더 vmlinux.h · clang -g / GCC 12 · libbpf / cilium/ebpf / Aya · bpftool gen skeleton),
#   GCC 12 BPF CO-RE 지원은 gcc.gnu.org/gcc-12/changes.html, 커널 BTF 경로 /sys/kernel/btf/vmlinux 는 linux v5.4 kernel/bpf/sysfs_btf.c,
#   오브젝트의 .BTF 는 추출본 ebpf5.txt 236~244행(bpftool btf list 의 anon BTF 149).
# Layout conventions: 존 둘 폭 376(좌 x=16 · 우 x=568), 노드 344×64, 줄 stride 96(y=132·228·324·420), 화살표 y 는 노드 중앙. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, MUTED, INK, PAPER, PAPER2, RULE, SOFT, INFO, KR, MONO

W, H = 960, 568
d = D(W, H, "LEARNING EBPF · 05-01",
      "CO-RE 다섯 요소가 빌드 기계와 대상 기계에 놓이는 자리",
      "빌드 기계에서는 vmlinux.h 와 clang -g 가 .BTF 를 품은 오브젝트를 만들고 bpftool gen skeleton 이 스켈레톤을 더한다. 대상 기계에서는 libbpf 가 /sys/kernel/btf/vmlinux 와 오브젝트의 BTF 를 맞대어 오프셋을 고친 뒤 싣는다.",
      "구조체 차이는 적재 때 라이브러리가 BTF 두 벌을 맞대어 고칩니다")

LZ = (16, 92, 376, 400)
RZ = (568, 92, 376, 400)
for (x, y, w, h), name in ((LZ, "빌드 기계"), (RZ, "대상 기계")):
    d.box(x, y, w, h, PAPER2, RULE, 0.9, 8)
    d.t(x + 12, y + 20, name, 13, SOFT, KR, "start", 600)

NW, NH = 344, 64
LX, RX = 32, 584
ROWS = (132, 228, 324, 420)


def node(x, y, title, sub, c, fill="12", sw=1.2):
    if c is None:
        d.box(x, y, NW, NH, PAPER, RULE, 0.9, 6)
        tc = INK
    else:
        d.tone(x, y, NW, NH, c, 6, fill, sw)
        tc = c
    d.t(x + NW / 2, y + 28, title, 14, tc, KR if any("가" <= ch <= "힣" for ch in title) else MONO, "middle", 600)
    d.t(x + NW / 2, y + 48, sub, 13, MUTED, KR if any("가" <= ch <= "힣" for ch in sub) else MONO)


# 빌드 기계 — 위에서 아래로
node(LX, ROWS[0], "커널 헤더", "vmlinux.h", INFO)
node(LX, ROWS[1], "컴파일러", "clang -g · GCC 12", OK)
node(LX, ROWS[2], "BPF 오브젝트", ".bpf.o · .BTF", INFO)
node(LX, ROWS[3], "스켈레톤 · 선택", "bpftool gen skeleton", None)
d.arrow([(LX + NW / 2, ROWS[0] + NH + 2), (LX + NW / 2, ROWS[1] - 6)], MUTED, "ar", 1.5)
d.arrow([(LX + NW / 2, ROWS[1] + NH + 2), (LX + NW / 2, ROWS[2] - 6)], MUTED, "ar", 1.5)
d.arrow([(LX + NW / 2, ROWS[2] + NH + 2), (LX + NW / 2, ROWS[3] - 6)], MUTED, "ar", 1.5, "4 4")

# 대상 기계
node(RX, ROWS[1], "커널 BTF", "/sys/kernel/btf/vmlinux", INFO)
node(RX, ROWS[2], "라이브러리", "libbpf · cilium/ebpf · Aya", OK)
d.arrow([(RX + NW / 2, ROWS[1] + NH + 2), (RX + NW / 2, ROWS[2] - 6)], INFO, "info", 1.5)

# focal — 오브젝트의 BTF 와 커널 BTF 의 차이만큼 오프셋을 고친다
d.arrow([(LX + NW + 2, ROWS[2] + 24), (RX - 6, ROWS[2] + 24)], ACC, "acc", 1.8)
d.chip(480, ROWS[2] + 4, "적재 때 오프셋 수정", ACC, 13)

# 스켈레톤이 라이브러리를 부른다(점선)
d.arrow([(LX + NW + 2, ROWS[3] + 32), (480, ROWS[3] + 32), (480, ROWS[2] + 48), (RX - 6, ROWS[2] + 48)], MUTED, "ar", 1.4, "4 4")

d.legend(H - 56, [("자료", INFO), ("도구", OK), ("적재 때 보정", ACC)])
d.save("05-01.chapter-overview.svg")

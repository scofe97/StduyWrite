# 타입 스펙: type-tree — 뿌리 BTF 하나, 가지 넷(CO-RE 재배치 · 맵 덤프 · 줄·함수 정보 · 스핀 락), 가지마다 실제 값 잎 하나. 좌에서 우로 편 깊이 3.
# 사실 출처: 추출본 src/ebpf5.txt 173~219행(BTF 쓰임: 재배치 · 구조체 pretty-print · 줄·함수 정보 · bpf_spin_lock), 609~617행(커널 /sys/kernel/btf/vmlinux · 오브젝트 .BTF 비교),
#   src/ebpf4.txt 395~420행(bpftool map dump name config 의 "key": 501 · "message": "Hi user 501!"), src/ebpf3.txt 331행·예제 03-01 §(xlated 덤프의 `; bpf_printk("Hello World %d", counter);`),
#   linux v7.2 include/uapi/linux/bpf.h 3951~3994행(bpf_spin_lock 헬퍼 주석: 맵 값 최상위 필드 · BTF 필수).
# Layout conventions: 뿌리 180×64, 가지 232×60·stride 84, 잎 420×40, 연결선은 뿌리 오른쪽 척추에서 엘보. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 960, 516
d = D(W, H, "LEARNING EBPF · 05-01 §2", "BTF 한 벌이 쓰이는 자리는 넷이다",
      "BTF 는 CO-RE 재배치에 오프셋을 대 주고, 맵 덤프를 필드 이름으로 풀어 찍게 하고, 소스 줄과 함수 이름을 덤프에 끼우게 하고, 스핀 락 필드의 위치를 알려 준다.",
      "타입 ID 로 적은 배치 하나가 네 가지 일에 씁니다")

RX, RY, RW, RH = 20, 236, 180, 64
BX, BW_, BH = 244, 232, 60
LX, LW, LH = 520, 420, 40
YS = [112, 196, 280, 364]
BR = [
    ("CO-RE 재배치", "구조체 오프셋 비교", "/sys/kernel/btf/vmlinux · .BTF", ACC),
    ("맵 덤프 출력", "필드 이름으로 풀어 찍기", '"key": 501 · "message": "Hi user 501!"', None),
    ("줄·함수 정보", "덤프에 소스 줄 끼우기", '; bpf_printk("Hello World %d", counter);', None),
    ("스핀 락", "값 구조체 안 lock 위치", "struct bpf_spin_lock lock;", None),
]

# 연결선 먼저
cy = [y + BH // 2 for y in YS]
d.line(RX + RW, RY + RH // 2, 224, RY + RH // 2, MUTED, 1.2)
d.line(224, cy[0], 224, cy[-1], MUTED, 1.2)
for y in cy:
    d.line(224, y, BX, y, MUTED, 1.2)
    d.line(BX + BW_, y, LX, y, RULE, 1.2)

d.tone(RX, RY, RW, RH, INFO, 6, "12", 1.2)
d.t(RX + RW / 2, RY + 28, "BTF", 16, INFO, MONO, "middle", 600)
d.t(RX + RW / 2, RY + 48, "타입 ID 로 적은 배치", 13, MUTED, KR)

for (title, sub, leaf, c), y in zip(BR, YS):
    if c:
        d.tone(BX, y, BW_, BH, c, 6, "1F", 1.4)
    else:
        d.box(BX, y, BW_, BH, PAPER2, RULE, 1.0)
    d.t(BX + BW_ / 2, y + 26, title, 14, c or INK, KR, "middle", 600)
    d.t(BX + BW_ / 2, y + 46, sub, 13, MUTED, KR)
    d.box(LX, y + 10, LW, LH, PAPER, RULE, 0.9, 5)
    d.t(LX + 14, y + 35, leaf, 12, INK, MONO, "start", 600)

d.legend(H - 56, [("뿌리 BTF", INFO), ("이 편의 중심 쓰임", ACC), ("그 밖의 쓰임", MUTED)])
d.save("05-01.btf-uses.svg")

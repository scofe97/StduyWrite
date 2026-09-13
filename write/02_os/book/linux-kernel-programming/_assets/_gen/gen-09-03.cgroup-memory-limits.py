# 09-03 §6 — cgroup 이 프로세스 그룹을 어떻게 가두고, 네 한계가 어디에 걸리는가.
# 본문이 요구한 형태: "CPU 시간은 무한하지만 메모리는 그렇지 않아 여러 한계를 둔다".
# 주의: 어느 것이 주 수단인가에서 자료가 갈린다 — 원서·systemd 는 high, 커널 cgroup v2 문서는 max 를 주 메커니즘이라 적는다.
#       라벨은 각 문서의 동작 서술만 담고 권장 여부는 본문에 남긴다(2026-09-13 축자 인용 확인).
# 타입 스펙: type-nested — 포함·범위로 드러나는 계층. 바깥이 안쪽을 가두고, 한계는 안쪽 상자의 경계다.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import ACC, MUTED, SOFT, INK, OK, WARN, BAD, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 680
OX, OY, OW, OH = 24, 140, 560, 372

d = DK(W, H, "LINUX KERNEL PROGRAMMING · 09-03 §6",
       "사후에 죽이는 대신 미리 가둡니다",
       "cgroup v2 의 메모리 컨트롤러는 그룹 안 프로세스들의 합산 메모리 사용을 제한한다. CPU 시간과 달리 메모리는 유한해 한계가 하나가 아니라 넷이다. high 는 조이기만 하고 OOM 을 부르지 않으며, max 에 닿고 줄일 수 없을 때 그 cgroup 안에서 OOM killer 가 불린다.",
       "OOM killer 에 대한 합리적 결론은 애초에 그 상황을 만들지 않는 것입니다")

d.box(OX, OY, OW, OH, PAPER2, RULE, 1.0, 10)
d.t(OX + 20, OY + 32, "시스템 전체 RAM", 14, MUTED, KR, "start", 600)

MX, MY, MW, MH = OX + 28, OY + 56, OW - 56, 288
d.box(MX, MY, MW, MH, PAPER, RULE, 1.0, 10)
d.t(MX + 20, MY + 32, "부모 cgroup", 14, MUTED, KR, "start", 600)
d.t(MX + MW - 20, MY + 32, "자식의 합을 다시 가둡니다", 13, MUTED, KR, "end")

IX, IY, IW, IH = MX + 28, MY + 56, MW - 56, 208
d.tone(IX, IY, IW, IH, ACC, 10, "10", 1.4)
d.t(IX + 20, IY + 32, "자식 cgroup — 내 워크로드", 14, ACC, KR, "start", 600)

# 안에서 도는 프로세스들
for k in range(4):
    px = IX + 20 + k * 108
    d.box(px, IY + 56, 92, 48, PAPER2, RULE, 0.9, 6)
    d.t(px + 46, IY + 85, f"프로세스 {k + 1}", 13, MUTED, KR)
d.t(IX + 20, IY + 138, "이 안의 합산 사용량이 아래 네 한계에 걸립니다", 13, MUTED, KR, "start")
d.t(IX + 20, IY + 168, "memory.oom.group 을 켜면 하나가 터질 때 이 상자째 죽습니다", 13, ACC, KR, "start")

# 네 한계
RX, RW = 624, 352
LIMITS = [
    ("memory.min", "이만큼은 보장받습니다", "회수 대상에서 제외", OK),
    ("memory.low", "가능하면 지켜 줍니다", "다른 데가 급하면 양보", OK),
    ("memory.high", "넘으면 조입니다", "throttle + 적극 회수 · OOM 은 안 부릅니다", WARN),
    ("memory.max", "닿으면 죽습니다", "줄일 수 없으면 cgroup 안에서 OOM", BAD),
]
for i, (name, what, how, c) in enumerate(LIMITS):
    y = 148 + i * 92
    d.tone(RX, y, RW, 76, c, 8, "14", 1.1)
    d.t(RX + 16, y + 26, name, 12, c, MONO, "start", 600)
    d.t(RX + RW - 16, y + 26, what, 13, c, KR, "end")
    d.t(RX + 16, y + 52, how, 13, MUTED, KR, "start")

d.t(24, 544, "systemd 로도 같은 것을 겁니다 — MemoryMin·MemoryLow·MemoryHigh·MemoryMax, swap 은 MemorySwapMax 입니다.", 13, MUTED, KR, "start")
d.t(24, 568, "5.9 커널부터 새 slab 메모리 컨트롤러가 memcg 마다 slab 을 복제하던 낭비를 없앴습니다. 절감은 35~50% 에 달합니다.", 13, SOFT, KR, "start")

d.legend(H - 56, [("보장되는 바닥", OK), ("조이는 천장", WARN), ("죽이는 천장", BAD), ("내 워크로드", ACC)])
d.save("09-03.cgroup-memory-limits.svg")
print("ok 09-03.cgroup-memory-limits")

# 08-02 §1 — slab 이 페이지 할당자 위에 어떻게 얹히는가, 그리고 왜 얹는가.
# 본문이 요구한 형태: "페이지 할당자 위에 layered 된다" + 두 존재 이유(객체 캐싱 · 작은 할당 낭비 완화).
# 타입 스펙: type-nested — 포함·범위로 드러나는 계층. 안쪽 상자가 바깥 상자에서 메모리를 받는다.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 976, 616
OX, OY, OW, OH = 32, 144, 560, 332

d = DK(W, H, "LINUX KERNEL PROGRAMMING · 08-02 §1",
       "페이지 안에 slab, slab 안에 객체",
       "slab 할당자는 페이지 할당자에서 물리 연속 청크를 받아 그것을 같은 크기의 객체로 잘라 둔다. 그래서 slab 을 쓰는 코드도 결국 페이지 할당자에서 메모리를 받는다. 이 계층이 존재하는 이유는 둘 — 자주 쓰는 커널 객체를 미리 캐시하는 것과, 페이지보다 작은 요청의 낭비를 줄이는 것이다.",
       "안쪽 상자는 바깥 상자에서 메모리를 받습니다 — 우회로가 없습니다")

d.box(OX, OY, OW, OH, PAPER2, RULE, 1.0, 10)
d.t(OX + 20, OY + 32, "페이지 할당자", 14, INFO, KR, "start", 600)
d.t(OX + OW - 20, OY + 32, "물리 연속 청크 · order 단위", 13, MUTED, KR, "end")

MX, MY, MW, MH = OX + 32, OY + 56, OW - 64, 244
d.tone(MX, MY, MW, MH, ACC, 8, "10", 1.4)
d.t(MX + 20, MY + 32, "slab 캐시 — kmalloc-64", 14, ACC, KR, "start", 600)
d.t(MX + MW - 20, MY + 32, "받은 청크를 같은 크기로 자릅니다", 13, MUTED, KR, "end")

# 잘린 객체들 — 상자 하나가 64바이트 객체 하나
IX, IY = MX + 20, MY + 56
for r in range(3):
    for cn in range(8):
        used = r * 8 + cn < 19
        x = IX + cn * 56
        y = IY + r * 52
        if used:
            d.tone(x, y, 48, 40, OK, 4, "18", 1.1)
            d.t(x + 24, y + 25, "사용", 13, OK, KR)
        else:
            d.box(x, y, 48, 40, PAPER, RULE, 0.9, 4)
            d.t(x + 24, y + 25, "자유", 13, SOFT, KR)

d.t(MX + 20, MY + MH + 24, "객체 하나 = 64바이트. 반납해도 캐시로 돌아갈 뿐 페이지가 풀리지는 않습니다.", 13, MUTED, KR, "start")

# 두 존재 이유
RX, RW = 624, 320
for i, (tag, title, body, c) in enumerate([
        ("1", "객체 캐싱", "task_struct · inode · dentry · sk_buff\n부팅 때 미리 할당해 거의 즉시 내줍니다", OK),
        ("2", "작은 할당 낭비 완화", "12바이트 요청에 kmalloc-16 이 16바이트를 줍니다\n페이지 할당자였다면 4KB 였을 자리입니다", INFO)]):
    y = 144 + i * 172
    d.tone(RX, y, RW, 148, c, 8, "12", 1.1)
    d.chip(RX + 32, y + 30, tag, c, 13)
    d.t(RX + 60, y + 35, title, 14, c, KR, "start", 600)
    for k, line in enumerate(body.split("\n")):
        d.t(RX + 20, y + 76 + k * 24, line, 13, MUTED, KR, "start")

d.t(24, 508, "Jeff Bonwick 이 SunOS 에서 낸 아이디어입니다. 특정 커널 객체가 자주 할당·해제되니 미리 캐시해 두자는 것이었습니다.", 13, MUTED, KR, "start")
d.t(24, 532, "전통적 heap 할당자는 잦은 할당·해제로 구멍을 만들지만, slab 객체는 캐시로 반납되므로 성능이 유지됩니다.", 13, SOFT, KR, "start")

d.legend(H - 56, [("slab 계층 — 이 절의 논점", ACC), ("페이지 할당자", INFO), ("캐시 안의 객체", OK)])
d.save("08-02.slab-nesting.svg")
print("ok 08-02.slab-nesting")

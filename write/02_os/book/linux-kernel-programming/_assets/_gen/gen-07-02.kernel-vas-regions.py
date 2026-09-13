# 07-02 §3 — 커널 VAS 가 어떤 영역으로 나뉘고 각 경계가 어느 매크로인가.
# 주소·크기는 kernel.org v6.1 x86_64 mm 문서의 4-level 메모리 맵 표에서 축자 확인한 값이다.
#   https://www.kernel.org/doc/html/v6.1/x86/x86_64/mm.html
# 타입 스펙: type-layers — 위가 높은 주소. 주소 내림차순으로 쌓아 procmap 의 세로 타일과 같은 순서로 읽힌다.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 700
LX, LW = 24, 176
C1, C1W = 208, 200
C2, C2W = 416, 336
C3, C3W = 760, 216
HY, RH, RS, Y0 = 116, 48, 52, 164

d = DK(W, H, "LINUX KERNEL PROGRAMMING · 07-02 §3",
       "커널 VAS 는 역할별 영역으로 나뉩니다",
       "x86_64 4-level 페이징의 커널 VAS 레이아웃. 위가 높은 주소이고, 각 영역의 경계는 커널 매크로로 표현되어 LKM 에서 그대로 읽을 수 있다. RAM 을 1:1 로 direct-map 하는 lowmem 이 이 중 핵심이다.",
       "주소·크기는 kernel.org v6.1 x86_64 메모리 맵 문서의 값입니다 — 위치는 arch 마다 다릅니다")

for x, w, lab in ((LX, LW, "영역"), (C1, C1W, "경계 매크로"), (C2, C2W, "무엇에 쓰나"), (C3, C3W, "시작 주소 · 크기")):
    d.box(x, HY, w, RH, PAPER2, RULE, 0.9)
    d.t(x + w / 2, HY + 29, lab, 13, SOFT, KR)

ROWS = [
    ("모듈 영역", "MODULES_VADDR", "적재한 LKM 의 static code/data", "ffffffffa0000000", "1520 MB", INFO),
    ("커널 이미지", "_text · _etext · _sdata", "비압축 커널의 code/data", "ffffffff80000000", "512 MB", INFO),
    ("KASAN shadow", "KASAN_SHADOW_START", "메모리 버그 검출용 그림자", "ffffec0000000000", "16 TB", INFO),
    ("vmemmap", "VMEMMAP_START", "sparsemem 의 struct page 배열", "ffffea0000000000", "1 TB", INFO),
    ("vmalloc · ioremap", "VMALLOC_START", "vmalloc() 이 주는 가상 연속 메모리", "ffffc90000000000", "32 TB", INFO),
    ("lowmem", "PAGE_OFFSET", "모든 RAM 을 1:1 로 direct-map 한다", "ffff888000000000", "64 TB", ACC),
]

for i, (name, macro, role, addr, size, c) in enumerate(ROWS):
    y = Y0 + i * RS
    focal = c is ACC
    if focal:
        d.tone(LX, y, LW, RH, ACC, 6, "12", 1.4)
    else:
        d.box(LX, y, LW, RH, PAPER2, RULE, 0.9)
    d.t(LX + LW / 2, y + 29, name, 13, ACC if focal else INK, KR, "middle", 600)
    d.box(C1, y, C1W, RH, PAPER2, RULE, 0.9)
    d.t(C1 + C1W / 2, y + 29, macro, 12, MUTED, MONO)
    d.tone(C2, y, C2W, RH, ACC if focal else c, 6, "12" if focal else "14", 1.4 if focal else 1.1)
    d.t(C2 + 16, y + 29, role, 13, ACC if focal else c, KR, "start")
    d.box(C3, y, C3W, RH, PAPER2, RULE, 0.9)
    d.t(C3 + 16, y + 22, addr, 12, MUTED, MONO, "start")
    d.t(C3 + C3W - 16, y + 40, size, 12, SOFT, MONO, "end")

HOLE = Y0 + len(ROWS) * RS
d.box(LX, HOLE, W - 48, 28, PAPER, RULE, 0.8, 4)
d.t(W / 2 - 12, HOLE + 19, "non-canonical hole — 쓸 수 없는 구간", 13, WARN, KR)

UY = HOLE + 36
d.tone(LX, UY, W - 48, RH, OK, 6, "14", 1.1)
d.t(LX + 16, UY + 29, "유저 VAS", 13, OK, KR, "start", 600)
d.t(LX + 200, UY + 29, "TASK_SIZE", 12, MUTED, MONO, "start")
d.t(LX + 424, UY + 29, "프로세스마다 따로 — VMA 로 관리되는 유일한 쪽", 13, OK, KR, "start")

BOT = UY + RH
d.t(LX, BOT + 32, "lowmem 주소는 물리 주소와 고정 오프셋이라 kernel logical address 라 부릅니다. virt_to_phys() 가 이 구간에서만 유효한 이유입니다.", 13, MUTED, KR, "start")
d.t(LX, BOT + 56, "AArch32 는 모듈 영역이 PAGE_OFFSET 바로 아래 16MB 에 놓입니다 — 그래서 LKM 출력 순서를 arch 별로 갈라야 합니다.", 13, SOFT, KR, "start")

d.legend(H - 56, [("커널 VAS 영역", INFO), ("RAM direct-map — 이 절의 핵심", ACC), ("유저 VAS", OK), ("쓸 수 없는 구간", WARN)])
d.save("07-02.kernel-vas-regions.svg")
print("ok 07-02.kernel-vas-regions")

# 07-03 §1 — 커널이 부팅 시 물리 RAM 을 나누는 3단계 계층.
# 본문이 요구한 형태: "노드(Level 1) → 존(Level 2) → 페이지 프레임(Level 3)" 트리.
# 타입 스펙: type-tree — 부모에서 자식으로 내려가는 포함 관계. 세 단계가 곧 세 depth 다.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 928, 560
ROOT_X, ROOT_W, ROOT_Y, ROOT_H = 376, 240, 116, 68
ZW, ZH, ZY = 240, 68, 248
ZX = [88, 376, 664]
FY = 360

d = DK(W, H, "LINUX KERNEL PROGRAMMING · 07-03 §1",
       "물리 RAM 은 3단계로 쪼개집니다",
       "커널은 부팅 시 물리 RAM 을 트리형 계층으로 조직한다. 노드가 물리 RAM 뱅크를 추상화하고, 그 안이 존으로 구획되며, 존은 페이지 프레임으로 이뤄진다. 페이지 프레임은 PFN 으로 추적한다.",
       "존 이름과 개수는 부팅 때 커널이 동적으로 정합니다 — 고정 목록이 아닙니다")

d.tone(ROOT_X, ROOT_Y, ROOT_W, ROOT_H, ACC, 8, "12", 1.4)
d.t(ROOT_X + ROOT_W / 2, ROOT_Y + 28, "노드", 14, ACC, KR, "middle", 600)
d.t(ROOT_X + ROOT_W / 2, ROOT_Y + 50, "pg_data_t · 물리 RAM 뱅크", 13, MUTED, KR)
d.t(24, ROOT_Y + 40, "Level 1", 12, SOFT, MONO, "start")

BUS = ROOT_Y + ROOT_H + 28
d.line(ROOT_X + ROOT_W / 2, ROOT_Y + ROOT_H, ROOT_X + ROOT_W / 2, BUS, MUTED, 1.4)
d.line(ZX[0] + ZW / 2, BUS, ZX[2] + ZW / 2, BUS, MUTED, 1.4)

ZONES = [("ZONE_DMA", "옛 ISA 장치가 닿는 저주소", INFO),
         ("ZONE_DMA32", "32비트 DMA 가 닿는 4GB 아래", INFO),
         ("ZONE_NORMAL", "나머지 일반 메모리", OK)]

for i, (name, role, c) in enumerate(ZONES):
    cx = ZX[i] + ZW / 2
    d.arrow([(cx, BUS), (cx, ZY - 6)], MUTED, "ar", 1.4)
    d.tone(ZX[i], ZY, ZW, ZH, c, 8, "14", 1.1)
    d.t(cx, ZY + 28, name, 13, c, MONO, "middle", 600)
    d.t(cx, ZY + 50, role, 13, MUTED, KR)
    # Level 3 — 존을 이루는 페이지 프레임들
    d.arrow([(cx, ZY + ZH), (cx, FY - 6)], MUTED, "ar", 1.2)
    for j in range(8):
        fx = ZX[i] + 8 + j * 29
        d.box(fx, FY, 24, 24, PAPER2, RULE, 0.9, 3)
    d.t(cx, FY + 46, "페이지 프레임 · PFN 으로 추적", 13, SOFT, KR)

d.t(24, ZY + 40, "Level 2", 12, SOFT, MONO, "start")
d.t(24, FY + 16, "Level 3", 12, SOFT, MONO, "start")

d.t(24, 452, "노드는 시스템 보드의 물리 RAM 모듈과 그 컨트롤러 칩셋을 추상화하고, CPU 코어와 연관됩니다.", 13, MUTED, KR, "start")
d.t(24, 476, "존마다 PFN 범위가 할당되고, 페이지 프레임 하나가 물리 RAM 페이지 하나입니다.", 13, SOFT, KR, "start")

d.legend(H - 56, [("Level 1 — 이 계층의 뿌리", ACC), ("하드웨어 제약이 만든 존", INFO), ("일반 메모리", OK)])
d.save("07-03.node-zone-frame.svg")
print("ok 07-03.node-zone-frame")

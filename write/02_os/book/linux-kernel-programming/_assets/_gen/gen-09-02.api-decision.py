# 09-02 §1 — 필요한 양과 타입으로 API 를 고르는 결정 트리. 본문 선택표를 흐름으로 옮겼다.
# 타입 스펙: type-flowchart — 조건에 따라 갈라지는 판단 논리. 위에서부터 물어 내려가면 답이 하나 남는다.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import ACC, MUTED, SOFT, INK, INFO, OK, WARN, BAD, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 704
MX, MW = 248, 296
RX, RW = 608, 368
CX = MX + MW / 2

d = DK(W, H, "LINUX KERNEL PROGRAMMING · 09-02 §1",
       "위에서부터 물으면 하나가 남습니다",
       "커널 할당 엔진은 결국 페이지 할당자 하나이고 그 위에 slab 이 얹힌다. 고르는 기준은 필요한 양과 타입 둘뿐이다. 위에서부터 차례로 물어 내려가면 쓸 API 가 하나로 좁혀지고, 아무 조건에도 안 걸리면 기본값인 kzalloc 이 답이다.",
       "1페이지 미만 일반 할당의 1차 선택은 언제나 slab 입니다")

def node(y, title, c):
    d.box(MX, y, MW, 52, PAPER2, RULE, 1.0, 8)
    d.t(CX, y + 31, title, 13, c, KR, "middle", 600)

def exit_box(y, api, why, c, focal=False):
    if focal:
        d.tone(RX, y, RW, 52, ACC, 8, "12", 1.4)
    else:
        d.tone(RX, y, RW, 52, c, 8, "14", 1.1)
    d.t(RX + 16, y + 22, api, 12, ACC if focal else c, MONO, "start", 600)
    d.t(RX + 16, y + 41, why, 13, MUTED, KR, "start")

Q = [
    (120, "DMA 에 쓸 메모리인가?", "dma_alloc_coherent()", "전용 엔진을 씁니다 — slab·page 직접 금지", WARN, False),
    (196, "자주 쓰는 전용 객체인가?", "kmem_cache_*()", "09-01 의 custom slab cache", INFO, False),
    (272, "크기가 불확실한가?", "kvmalloc()", "kmalloc 먼저, 실패하면 vmalloc", INFO, False),
    (348, "1페이지보다 큰가?", "vmalloc() · 페이지 할당자", "물리 연속이 필요하면 페이지 할당자", INFO, False),
    (424, "드라이버 probe · init 인가?", "devm_kzalloc()", "detach 때 자동으로 풀립니다", OK, False),
]

for i, (y, q, api, why, c, _) in enumerate(Q):
    node(y, q, WARN if i == 0 else INK)
    exit_box(y, api, why, c)
    mid = y + 26
    d.arrow([(MX + MW + 4, mid), (RX - 6, mid)], c, {"ok": OK}.get("", "ar") if c is not OK else "ok", 1.4)
    if i < len(Q) - 1:
        d.arrow([(CX, y + 52), (CX, Q[i + 1][0] - 6)], MUTED, "ar", 1.4)

for i, y in enumerate([q[0] for q in Q]):
    d.chip((MX + MW + RX) / 2, y + 4, "예", MUTED, 13)
    if i < len(Q) - 1:
        d.chip(CX - 84, y + 66, "아니오", SOFT, 13)

# 아무 조건에도 안 걸리면
FY = 500
d.arrow([(CX, Q[-1][0] + 52), (CX, FY - 6)], ACC, "acc", 1.4)
d.chip(CX - 84, Q[-1][0] + 66, "아니오", SOFT, 13)
d.tone(MX, FY, MW, 52, ACC, 8, "12", 1.4)
d.t(CX, FY + 31, "어디에도 안 걸리는 경우", 13, ACC, KR, "middle", 600)
exit_box(FY, "kmalloc() · kzalloc()", "1페이지 미만 일반 할당의 기본값", OK, True)
d.arrow([(MX + MW + 4, FY + 26), (RX - 6, FY + 26)], ACC, "acc", 1.4)

d.t(24, 588, "컨텍스트가 atomic 이면 어느 길로 가든 GFP_ATOMIC 입니다. spinlock 을 쥔 채 GFP_KERNEL 은 금지입니다.", 13, MUTED, KR, "start")
d.t(24, 612, "slab 으로 받았으면 ksize() 나 sysfs 의 slab_size 로 실제 크기를 확인합니다.", 13, SOFT, KR, "start")

d.legend(H - 56, [("전용 API 를 써야 함", WARN), ("조건에 맞는 계층", INFO), ("자동 해제", OK), ("기본값 — 이 절의 결론", ACC)])
d.save("09-02.api-decision.svg")
print("ok 09-02.api-decision")

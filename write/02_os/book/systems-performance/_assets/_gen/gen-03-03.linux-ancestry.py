# 03-03 §3 — Linux 가 아이디어를 가져온 선조와, 선조끼리의 파생 관계(원서 3.4 목록 · 3.3.2 · 3.3.3).
# 타입 스펙: type-dependency — Unix 가 BSD · Solaris · Linux 셋의 공통 의존(fan-in 3)이라 트리로 못 그린다.
#           rank 0 Linux → rank 1 Solaris · Plan 9 → rank 2 BSD → rank 3 Unix. rank 간격 128(스펙 120 을 4 의 배수로).
#           축약: 노드 폭을 160 대신 320 으로 넓혀 물려받은 기능을 노드 안에 둔다. 순환이 없어 accent 를 쓰지 않는다.
#           Plan 9 의 선조 관계는 원서가 적지 않아 간선을 긋지 않았다.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import MUTED, SOFT, INK, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 960, 700
NW, NH = 320, 72
R = [112, 240, 368, 496]           # rank y top

d = DK(W, H, "SYSTEMS PERFORMANCE · 03-03 §3",
       "Linux 가 선조에게서 물려받은 것",
       "Linux 는 Unix(와 Multics) · BSD · Solaris · Plan 9 에서 아이디어를 가져왔다. BSD 는 Unix 6판을 개선하며 시작했고 Solaris 는 Unix · BSD 에서 파생됐다. 화살표는 '아이디어를 가져온 쪽 → 준 쪽'이고, 노드 안이 물려받은 기능이다.",
       "Unix 에는 화살표가 셋 들어옵니다")

def node(cx, y, title, l1, l2, badge, tone=None):
    x = cx - NW / 2
    if tone: d.tone(x, y, NW, NH, tone, 6)
    else: d.box(x, y, NW, NH, PAPER2, RULE, 1.0, 6)
    d.t(x + 16, y + 24, title, 14, tone if tone else INK, KR, "start", 600)
    d.t(x + 16, y + 44, l1, 12, MUTED, KR, "start")
    if l2: d.t(x + 16, y + 62, l2, 12, MUTED, KR, "start")
    if badge:
        d.o.append(f'<rect x="{x + NW - 48}" y="{y + 8}" width="40" height="18" rx="2" fill="{PAPER}" stroke="{SOFT}" stroke-width="0.8"/>')
        d.t(x + NW - 28, y + 21, badge, 11, SOFT, MONO)

LX, RX = 280, 760
node(560, R[0], "Linux · 1991", "Torvalds · 386(486) AT 호환기용 자유 OS", None, None, INFO)
node(LX, R[1], "Solaris · 1982 SunOS", "VFS · NFS · page cache", "unified page cache · slab 할당자", "1 in")
node(RX, R[1], "Plan 9", "rfork — 프로세스 · 스레드 공유 수준", None, "1 in")
node(LX, R[2], "BSD · 1978", "paged VM · demand paging · FFS", "TCP/IP 스택 · 소켓", "2 in")
node(LX, R[3], "Unix (+ Multics) · 1969", "OS 계층 · syscall · 프로세스 · 우선순위 · 가상 메모리", "전역 FS · 권한 · 장치 노드 · 버퍼 캐시", "3 in")

B0 = R[0] + NH
mid1 = B0 + 28
# Linux → Solaris
d.arrow([(500, B0), (500, mid1), (LX, mid1), (LX, R[1] - 4)], MUTED, "ar", 1.4)
# Linux → Plan 9
d.arrow([(620, B0), (620, mid1), (RX, mid1), (RX, R[1] - 4)], MUTED, "ar", 1.4)
# Linux → BSD (rank 1 사이 빈틈으로)
d.arrow([(540, B0), (540, R[2] + NH / 2), (LX + NW / 2 + 4, R[2] + NH / 2)], MUTED, "ar", 1.4)
# Linux → Unix
d.arrow([(580, B0), (580, R[3] + NH / 2), (LX + NW / 2 + 4, R[3] + NH / 2)], MUTED, "ar", 1.4)
# Solaris → BSD
d.arrow([(LX, R[1] + NH), (LX, R[2] - 4)], SOFT, "soft", 1.4)
# BSD → Unix
d.arrow([(LX, R[2] + NH), (LX, R[3] - 4)], SOFT, "soft", 1.4)
# Solaris → Unix (왼쪽 바깥으로)
ox = LX - NW / 2 - 28
d.arrow([(LX - NW / 2, R[1] + 24), (ox, R[1] + 24), (ox, R[3] + 24), (LX - NW / 2 - 4, R[3] + 24)], SOFT, "soft", 1.4)

d.legend(R[3] + NH + 40, [("Linux", INFO), ("Linux 가 가져옴", MUTED), ("선조끼리의 파생", SOFT)])
d.save("03-03.linux-ancestry.svg")

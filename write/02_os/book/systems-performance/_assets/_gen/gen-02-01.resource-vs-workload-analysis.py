# 02-01 §11 — 같은 OS 스택을 위(워크로드)와 아래(자원)에서 보는 두 분석 관점.
# 타입 스펙: type-layers — 소프트웨어 스택의 추상 수준을 층으로 쌓고, 양옆에 두 분석의 방향을 둔다.
#           원서 그림 2.10(p.20)·2.4.1·2.4.2. 옛 손 SVG 를 대체하며 원문에 없던 라벨은 넣지 않는다.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import ACC, MUTED, SOFT, INK, INFO, OK, PAPER2, RULE, KR, MONO

W, H = 928, 512
BX, BW, BH, Y0, STRIDE = 248, 432, 56, 124, 64
LAYERS = ["애플리케이션", "시스템 라이브러리", "시스템 콜", "커널", "장치 · 하드웨어 자원"]

d = DK(W, H, "SYSTEMS PERFORMANCE · 02-01 §11",
       "같은 스택을 반대 방향에서 본다",
       "워크로드 분석은 애플리케이션에서 아래로, 자원 분석은 하드웨어 자원에서 위로 OS 소프트웨어 스택을 본다. 양옆은 각 관점의 대상과 지표다.",
       "원서 그림 2.10 · 2.4.1 · 2.4.2")

for i, name in enumerate(LAYERS):
    y = Y0 + i * STRIDE
    d.box(BX, y, BW, BH, PAPER2, RULE, 1.0, 6)
    d.t(BX + BW / 2, y + 33, name, 14, INK, KR, "middle", 600)

top, bot = Y0 + 4, Y0 + 4 * STRIDE + BH - 4
lx, rx = BX - 28, BX + BW + 28
d.arrow([(lx, top), (lx, bot)], ACC, "acc", 1.8)
d.arrow([(rx, bot), (rx, top)], INFO, "info", 1.8)

LEFT = [("워크로드 분석", ACC, 14, 600), ("top-down", ACC, 12, 400), ("앱 개발자 · 지원", MUTED, 12, 400),
        ("대상", SOFT, 12, 400), ("요청 · 지연 · 완료", INK, 13, 400),
        ("지표", SOFT, 12, 400), ("처리량 · 지연", INK, 13, 400)]
RIGHT = [("자원 분석", INFO, 14, 600), ("bottom-up", INFO, 12, 400), ("시스템 관리자", MUTED, 12, 400),
         ("대상", SOFT, 12, 400), ("CPU · 메모리 · 디스크", INK, 13, 400),
         ("지표", SOFT, 12, 400), ("IOPS · 사용률 · 포화", INK, 13, 400)]
for k, (txt, c, sz, wt) in enumerate(LEFT):
    d.t(lx - 16, Y0 + 20 + k * 36, txt, sz, c, KR, "end", wt)
for k, (txt, c, sz, wt) in enumerate(RIGHT):
    d.t(rx + 16, Y0 + 20 + k * 36, txt, sz, c, KR, "start", wt)

d.legend(Y0 + 5 * STRIDE + 20, [("워크로드 분석", ACC), ("자원 분석", INFO), ("OS 스택 층", MUTED)])
d.save("02-01.resource-vs-workload-analysis.svg")

# 11-02 §3 — I/O 오버헤드를 줄여 온 역사는 소프트웨어 단계를 하나씩 없앤 역사다.
# 타입 스펙: type-layers — 위에서 아래로 갈수록 게스트와 하드웨어 사이 단계가 줄어드는 지도다.
#           축약: OSI 층이 아니라 기술 세대라 인덱스 태그를 세대 번호로 채운다.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 952, 540
BX, BW, BH, Y0, STRIDE = 156, 676, 64, 116, 76

d = DK(W, H, "SYSTEMS PERFORMANCE · 11-02 §3",
       "I/O 단계를 하나씩 없애 온 역사",
       "게스트와 하드웨어 사이에 소프트웨어가 몇 겹 끼어 있느냐가 I/O 오버헤드를 정한다. 발전사는 그 겹을 하나씩 걷어낸 과정이다.",
       "10Gbit/s 급에서는 건당 작은 오버헤드도 전체 성능을 크게 떨어뜨립니다")

BANDS = [
    ("01", "전체 에뮬레이션", "하이퍼바이저가 모든 디바이스 I/O 를 변환", "가장 느림", None),
    ("02", "패러버추얼 드라이버", "I/O 를 합치고 인터럽트를 줄임", "오버헤드 감소", None),
    ("03", "PCI pass-through", "디바이스를 게스트에 직접 할당", "빠르지만 유연성 낮음", None),
    ("04", "SR-IOV", "하드웨어 가상화로 게스트가 직접 접근", "베어메탈에 근접", ACC),
]

for i, (n, name, sub, role, c) in enumerate(BANDS):
    y = Y0 + i * STRIDE
    if c: d.tone(BX, y, BW, BH, c, 8)
    else: d.box(BX, y, BW, BH, PAPER2, RULE, 1.0, 8)
    d.t(BX - 20, y + 38, n, 13, c if c else SOFT, MONO, "end", 600)
    d.t(BX + 20, y + 28, name, 14, c if c else INK, KR, "start", 600)
    d.t(BX + 20, y + 48, sub, 13, MUTED, KR, "start")
    d.t(BX + BW - 20, y + 38, role, 13, c if c else SOFT, KR, "end")

d.t(BX - 132, Y0 + 4, "단계 많음", 13, SOFT, KR, "start")
d.arrow([(BX - 76, Y0 + 16), (BX - 76, Y0 + 3 * STRIDE + BH - 28)], SOFT, "soft", 1.2, "4 6")
d.t(BX - 132, Y0 + 3 * STRIDE + BH - 4, "단계 없음", 13, SOFT, KR, "start")

YB = Y0 + 4 * STRIDE + 32
d.t(BX - 132, YB, "Nitro 는 이 방향의 끝으로, I/O 프록시(QEMU)를 아예 두지 않아 베어메탈급 성능을 냅니다", 13, MUTED, KR, "start")

d.legend(YB + 28, [("소프트웨어 단계가 사라진 자리", ACC), ("이전 세대", MUTED)])
d.save("11-02.io-path-evolution.svg")

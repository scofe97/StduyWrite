# 11-02 §3 — I/O 오버헤드 완화는 개입을 줄여 온 과정이고, 마지막 층에서는 성능과 유연성을 맞바꾼다.
# 타입 스펙: type-layers — 위 두 층은 하이퍼바이저 개입이 줄어드는 순서, 맨 아래 층은 같은 높이의 두 선택지다.
#           축약: OSI 층이 아니라 기술 층이라 인덱스 태그를 번호로 채운다. 03·04 는 빠르기 순서가 아니라 나란히 둔다
#           (원서 881: pass-through 가 최고 성능, SR-IOV 는 유연성 개선책).
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 952, 516
BX, BW, BH, Y0, STRIDE = 156, 676, 64, 116, 76

d = DK(W, H, "SYSTEMS PERFORMANCE · 11-02 §3",
       "I/O 경로 — 성능과 유연성의 교환",
       "게스트와 하드웨어 사이에 끼는 소프트웨어가 I/O 오버헤드를 정한다. 직접 접근까지 오면 남는 선택은 최고 성능이냐 공유냐다.",
       "10Gbit/s 급에서는 건당 작은 오버헤드도 전체 성능을 크게 떨어뜨립니다")

BANDS = [
    ("01", "전체 에뮬레이션", "모든 디바이스 I/O 를 하이퍼바이저가 변환", "오버헤드 최대"),
    ("02", "패러버추얼 드라이버", "I/O 병합 · 디바이스 인터럽트 감소", "게스트 OS 지원 필요"),
]
for i, (n, name, sub, role) in enumerate(BANDS):
    y = Y0 + i * STRIDE
    d.box(BX, y, BW, BH, PAPER2, RULE, 1.0, 8)
    d.t(BX - 20, y + 38, n, 13, SOFT, MONO, "end", 600)
    d.t(BX + 20, y + 28, name, 14, INK, KR, "start", 600)
    d.t(BX + 20, y + 48, sub, 13, MUTED, KR, "start")
    d.t(BX + BW - 20, y + 38, role, 13, SOFT, KR, "end")

# 03 · 04 — 같은 층의 두 선택지
Y3, H3, G3 = Y0 + 2 * STRIDE + 24, 104, 24
CW3 = (BW - G3) / 2
d.t(BX, Y3 - 10, "03 · 04 — 같은 층의 직접 접근, 빠르기가 아니라 공유 여부로 갈림", 13, SOFT, KR, "start")
PAIR = [
    ("03", "PCI pass-through", "디바이스를 게스트 하나에 직접 할당", ("원서 기준 최고 성능", OK), ("장치 독점 · 공유 불가", WARN), None),
    ("04", "SR-IOV / MR-IOV", "하드웨어 가상화로 여러 게스트가 직접 접근", ("공유 가능 · 유연성 회복", ACC), ("Nitro 의 기본", MUTED), ACC),
]
for k, (n, name, sub, a, b, c) in enumerate(PAIR):
    x = BX + k * (CW3 + G3)
    if c: d.tone(x, Y3, CW3, H3, c, 8)
    else: d.box(x, Y3, CW3, H3, PAPER2, RULE, 1.0, 8)
    d.t(x + CW3 - 16, Y3 + 26, n, 13, c if c else SOFT, MONO, "end", 600)
    d.t(x + 16, Y3 + 26, name, 14, c if c else INK, KR, "start", 600)
    d.t(x + 16, Y3 + 48, sub, 13, MUTED, KR, "start")
    d.t(x + 16, Y3 + 72, a[0], 13, a[1], KR, "start")
    d.t(x + 16, Y3 + 92, b[0], 13, b[1], KR, "start")

d.t(BX - 132, Y0 + 4, "개입 많음", 13, SOFT, KR, "start")
d.arrow([(BX - 76, Y0 + 16), (BX - 76, Y3 + H3 - 28)], SOFT, "soft", 1.2, "4 6")
d.t(BX - 132, Y3 + H3 - 4, "직접 접근", 13, SOFT, KR, "start")

YB = Y3 + H3 + 36
d.t(BX - 132, YB, "Nitro — I/O 프록시(QEMU) 없음 · 하드웨어 지원 기본 · 베어메탈급", 13, MUTED, KR, "start")

d.legend(YB + 28, [("공유를 되찾은 자리", ACC), ("성능", OK), ("공유 제약", WARN), ("이전 세대", MUTED)])
d.save("11-02.io-path-evolution.svg")

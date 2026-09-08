# 11-01 §5 — 수평 확장이 주는 것과 멀티테넌시가 가져오는 것.
# 타입 스펙: type-process — 칸마다 같은 의미 슬롯(무엇을 얻나 · 무엇이 따라오나)이 반복되는 대조 지도다.
#           축약: 주체(lane)가 없는 대조라 §1 lanes 와 §2 공식을 쓰지 않고 카드 stride 로 놓는다
#           (visual-diagram-selection §알려진 공백 "주체 없는 단계 지도" 관례).
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 928, 496
CW, CH, GAP, X0, Y = 424, 200, 32, 24, 116

d = DK(W, H, "SYSTEMS PERFORMANCE · 11-01 §5",
       "공유가 주는 것과 가져가는 것",
       "작은 인스턴스를 여럿 두면 자원을 잘게 맞출 수 있다. 그 인스턴스들이 한 물리 시스템을 나눠 쓰므로 이웃의 부하가 내 성능에 새어 든다.",
       "공유가 효율을 주지만 경합을 부릅니다")

CARDS = [
    ("얻는 것", "수평 확장", OK,
     ["작은 시스템 여럿에 부하를 나눕니다.", "512GB 호스트에 8GB 인스턴스처럼", "잘게 나누면 놀리는 자원이 줄어", "최적 가격·성능에 가까워집니다"],
     "거대 시스템에 미리 투자하지 않아도 됩니다"),
    ("따라오는 것", "멀티테넌시", ACC,
     ["전체 OS 인스턴스가 한 물리 시스템에", "공존합니다. 이웃이 피크 시간에", "DB 덤프를 돌리면 내 디스크·네트워크", "I/O 가 함께 느려집니다"],
     "noisy neighbor — 자원 제어로 격리합니다"),
]

for i, (tag, name, c, body, foot) in enumerate(CARDS):
    x = X0 + i * (CW + GAP)
    if c is ACC: d.tone(x, Y, CW, CH, c, 8)
    else: d.box(x, Y, CW, CH, PAPER2, RULE, 1.0, 8)
    d.t(x + 16, Y + 28, tag, 13, SOFT, KR, "start")
    d.t(x + 16, Y + 52, name, 15, c, KR, "start", 600)
    d.line(x + 16, Y + 66, x + CW - 16, Y + 66, RULE, 0.8)
    for j, line in enumerate(body):
        d.t(x + 16, Y + 92 + j * 20, line, 13, MUTED, KR, "start")
    d.t(x + 16, Y + CH - 20, foot, 13, c, KR, "start")

YB = Y + CH + 40
d.t(X0, YB, "게스트는 서로를 보지 못하므로, 이웃 탓인지 내 탓인지를 가리려면 자원 제어와 관측성이 함께 필요합니다",
    13, MUTED, KR, "start")
d.t(X0, YB + 24, "관측성은 가상화 유형에 따라 크게 달라집니다 — 11-02~11-04 가 그 차이를 다룹니다", 13, SOFT, KR, "start")

d.legend(YB + 48, [("공유가 부르는 문제", ACC), ("공유가 주는 이득", OK)])
d.save("11-01.cloud-scaling-multitenancy.svg")

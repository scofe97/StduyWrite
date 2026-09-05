# 08-01 §2 — 저자가 세운 용어 다섯이 신호 하나가 지나는 경로의 각 자리 이름이다.
# 원문("Terminology"): Source("Generates signals, potentially of different types. Sources can be the
#       Linux operating system or an application."), Destination("Where you consume, store, and further
#       process signals. We call a destination that exposes a user interface (GUI, TUI, or CLI) a
#       frontend. For example, a log viewer or a dashboard plotting time series is a frontend, whereas an
#       S3 bucket is not (but can still act as a destination for, say, logs)."),
#       Telemetry("The process of extracting signals from sources and transporting (or routing, shipping)
#       the signals to destinations, often employing agents that collect and/or preprocess signals (for
#       example, filter or downsample).").
# 타입 스펙: type-data-flow — 파이프라인 단계마다 누가 무엇을 하는지. 단계 사이를 건너가는 것이
#           신호이므로 process 가 아니라 data-flow 다. 축약: 신호 유형 셋은 §3 도식이 맡는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, PAPER2, RULE, KR, MONO

W, H = 880, 480
d = D(W, H, "LEARNING MODERN LINUX · 08-01 §2",
      "신호는 소스에서 나서 텔레메트리를 타고 목적지에 닿는다",
      "저자가 정의한 용어 다섯 중 셋이 경로의 자리 이름이고 하나가 그 사이를 나르는 과정의 이름이다. "
      "오른쪽 두 칸의 차이가 저자가 굳이 세운 구분이다.",
      "목적지라고 다 프론트엔드는 아닙니다")

CW, CH, Y0 = 232, 76, 128
COLX = [24, 324, 624]
STAGE = [("소스", "신호를 만든다"), ("텔레메트리", "뽑아서 나른다"), ("목적지", "받아서 쌓고 처리한다")]
for i, (nm, sub) in enumerate(STAGE):
    d.t(COLX[i] + CW / 2, 108, nm, 13, SOFT, KR, "middle", 600)
    d.t(COLX[i] + CW / 2, 124, sub, 11, SOFT, KR)

srcs = [("리눅스 운영체제", "커널이 내는 신호"), ("애플리케이션", "내 코드가 내는 신호")]
for k, (nm, sub) in enumerate(srcs):
    y = Y0 + 14 + k * (CH + 20)
    d.box(COLX[0], y, CW, CH, PAPER2, INFO, 1.2, 6)
    d.t(COLX[0] + 18, y + 30, nm, 14, INK, KR, "start", 600)
    d.t(COLX[0] + 18, y + 52, sub, 11.5, MUTED, KR, "start")

AY, AH = Y0 + 14, CH * 2 + 20
d.tone(COLX[1], AY, CW, AH, ACC, 6, "12", 1.4)
d.t(COLX[1] + CW / 2, AY + 32, "에이전트", 15, ACC, KR, "middle", 600)
for k, line in enumerate(["모아서(collect)", "미리 손질해서(filter · downsample)", "실어 보낸다(ship · route)"]):
    d.t(COLX[1] + CW / 2, AY + 58 + k * 24, line, 11.5, MUTED, KR)

dsts = [("프론트엔드", "로그 뷰어 · 대시보드", OK, "사용자 인터페이스가 있다"),
        ("프론트엔드가 아닌 목적지", "S3 버킷", MUTED, "받아 두지만 보여 주지는 않는다")]
for k, (nm, ex, col, sub) in enumerate(dsts):
    y = Y0 + 14 + k * (CH + 20)
    d.box(COLX[2], y, CW, CH, PAPER2, col, 1.2, 6)
    d.t(COLX[2] + 18, y + 26, nm, 13, col if col is OK else INK, KR, "start", 600)
    d.t(COLX[2] + 18, y + 46, ex, 11.5, MUTED, MONO, "start")
    d.t(COLX[2] + 18, y + 64, sub, 11, SOFT, KR, "start")

for k in range(2):
    y = Y0 + 14 + k * (CH + 20) + CH / 2
    d.arrow([(COLX[0] + CW, y), (COLX[1] - 4, y)], MUTED, "ar", 1.3)
    d.arrow([(COLX[1] + CW, y), (COLX[2] - 4, y)], MUTED, "ar", 1.3)

NY = Y0 + 14 + AH + 28
d.t(24, NY + 4, "관측 가능성 자체의 정의가 이 경로 위에 있습니다.", 12.5, INK, KR, "start", 600)
d.t(24, NY + 26, "바깥 정보를 재서 시스템의 안쪽 상태를 판정하고, 대개 그것을 근거로 조치하는 일입니다.",
    12, MUTED, KR, "start")
d.t(24, NY + 48, "저자의 예 — 반응이 굼뜨다고 느끼면 남은 주 메모리를 재고, 한 앱이 다 먹고 있음을 알아내",
    12, SOFT, KR, "start")
d.t(24, NY + 68, "그것을 끝내기로 정합니다. 재는 것은 바깥이고 알고 싶은 것은 안입니다.", 12, SOFT, KR, "start")

d.legend(440, [("신호를 나르는 과정", ACC), ("소스", INFO), ("프론트엔드", OK),
                  ("보여 주지 않는 목적지", MUTED)])
d.save("08-01.signal-path.svg")
print("ok 08-01.signal-path")

# 16-03.bytes-to-struct — 네트워크에서 읽은 16바이트를 unsafe.Pointer 로 Data 로 보면 칸이 필드에 겹치고, 리틀 엔디언 기계에서는 Value 만 뒤집는다
# 본문 요구(16-03 §2 「안전한 변환과 unsafe 변환」): [0 132 95 237 | 80 104 111 110 101 0 0 0 0 0 | 1 | 0] 이 Value(4) · Label(10) · Active(1) · 패딩(1)
#           에 겹친다. 리틀 엔디언 CPU 는 Value 를 거꾸로 읽으므로 bits.ReverseBytes32 로 뒤집어 8675309 를 얻는다.
# 타입 스펙: type-layers 변형 — 윗줄 바이트 칸 16개(칸 폭 48), 그 아래 필드 구간 막대, 맨 아래 해석 결과 칩. focal 은 Value 구간의 뒤집기.
# 사실 출처: Learning Go 2판 16장 「Using unsafe to Convert External Binary Data」, go1.27.1 실행(2026-09-29) — {Value:8675309, Label:Phone, Active: true}.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 984, 470
X0, CW, CH = 108, 48, 40
YB, YF, YR = 140, 216, 320
bytes_ = [0, 132, 95, 237, 80, 104, 111, 110, 101, 0, 0, 0, 0, 0, 1, 0]

d = D(W, H, "LAYOUT · 16-03 §2",
      "같은 16바이트를 Data 로 보고 Value 만 바이트 순서를 뒤집습니다",
      "네트워크에서 읽은 16바이트를 unsafe.Pointer 로 Data 구조체로 보면 앞 4바이트가 Value, 다음 10바이트가 Label, 그다음 1바이트가 Active, 마지막 1바이트가 패딩에 겹친다. "
      "네트워크 바이트 순서는 빅 엔디언이라 리틀 엔디언 CPU 는 Value 를 거꾸로 읽는다. bits.ReverseBytes32 로 뒤집으면 8675309 가 되고, Label 은 Phone, Active 는 true 다.",
      lead="윗줄은 받은 바이트, 가운데는 Data 의 필드 구간, 아랫줄은 해석한 값입니다.")

d.t(X0 - 14, YB + 25, "[16]byte", 12, INK, MONO, "end", 600)
for i, v in enumerate(bytes_):
    x = X0 + i * CW
    d.box(x + 2, YB, CW - 4, CH, PAPER, RULE, 0.9, 3)
    d.t(x + CW / 2, YB + 25, str(v), 12, INK, MONO, "middle")
    d.t(x + CW / 2, YB - 8, str(i), 10, MUTED, MONO, "middle")

spans = [("Value uint32", 0, 4, ACC), ("Label [10]byte", 4, 10, INFO), ("Active", 14, 1, OK), ("pad", 15, 1, SOFT)]
d.t(X0 - 14, YF + 21, "Data", 12, INK, MONO, "end", 600)
for lab, off, n, c in spans:
    x = X0 + off * CW
    d.tone(x + 2, YF, n * CW - 4, 32, c, 4, "18" if c == ACC else "12", 1.3 if c == ACC else 1.0)
    d.t(x + n * CW / 2, YF + 21, lab if n > 1 else lab[:3], 11, c if c != SOFT else MUTED, MONO, "middle", 600)
d.arrow([(X0 + 8 * CW, YB + CH + 4), (X0 + 8 * CW, YF - 4)], SOFT, "soft", 1.2)
d.t(X0 + 8 * CW + 10, YB + CH + 22, "*(*Data)(unsafe.Pointer(&b))", 11, MUTED, MONO, "start", 600)

vx = X0 + 2 * CW
d.arrow([(vx, YF + 32 + 4), (vx, YR - 4)], ACC, "acc", 1.3)
d.t(vx + 10, YF + 70, "리틀 엔디언이면 ReverseBytes32", 11, ACC, KR, "start", 600)
res = [("Value: 8675309", vx, ACC), ("Label: Phone", X0 + 9 * CW, INFO), ("Active: true", X0 + 14.5 * CW, OK)]
for txt, cx, c in res:
    w = len(txt) * 7.2 + 24
    d.tone(cx - w / 2, YR, w, 30, c, 4, "18", 1.1)
    d.t(cx, YR + 20, txt, 12, c, MONO, "middle", 600)

d.legend(414, [("바이트 순서를 뒤집는 필드", ACC), ("그대로 쓰는 바이트", INFO), ("불리언", OK)])
d.save("16-03.bytes-to-struct.svg")
print("ok 16-03 bytes-to-struct")

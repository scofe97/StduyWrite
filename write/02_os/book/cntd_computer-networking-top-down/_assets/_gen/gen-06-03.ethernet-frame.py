# 타입 스펙: type-treemap — 면적 = 바이트 수. 최소 크기 프레임 72 바이트를 여섯 필드로 분해한다.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §6.4.2 Figure 6.20 —
#   필드 순서와 바이트 수(프리앰블 8 · 목적지 6 · 출발지 6 · 타입 2 · 데이터 46~1500 · CRC 4) 그대로
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, OK, KR, MONO

W, H = 940, 502
d = D(W, H, "SECTION 6.4.2 · ETHERNET FRAME STRUCTURE",
      "최소 프레임 72 바이트를 쪼개 보면",
      "데이터 필드가 46 바이트로 최소일 때 프레임 전체가 72 바이트다. 면적이 곧 바이트 수이며, 칸은 크기순으로 놓았다.",
      "바이트 수는 원문 Figure 6.20 그대로입니다")

TX, TY, TW, TH = 24, 116, 560, 268
DATA_W = 356                                  # 560 x 46/72
d.tone(TX, TY, DATA_W - 4, TH, ACC, 6, "1E", 1.5)
d.t(TX + (DATA_W - 4) / 2, TY + TH / 2 - 14, "데이터", 14, ACC, KR, "middle", 600)
d.t(TX + (DATA_W - 4) / 2, TY + TH / 2 + 12, "46", 20, ACC, MONO, "middle", 600)
d.t(TX + (DATA_W - 4) / 2, TY + TH / 2 + 34, "최대 1500 까지 늘어납니다", 11, MUTED, KR)

RX, RW = TX + DATA_W, TW - DATA_W
y = TY
for name, size, h, c in [("프리앰블", 8, 88, INFO), ("목적지 MAC", 6, 64, OK),
                         ("출발지 MAC", 6, 64, OK), ("CRC", 4, 32, MUTED), ("타입", 2, 20, MUTED)]:
    d.tone(RX, y, RW, h - 4, c, 4, "14", 1.1)
    d.t(RX + 16, y + h / 2 + 2, name, 11, c, KR, "start", 600)
    d.t(RX + RW - 16, y + h / 2 + 2, str(size), 12, c, MONO, "end", 600)
    y += h

AX, AW = 620, 296
d.box(AX, 116, AW, 268, PAPER2, RULE, 1.0)
d.t(AX + 16, 140, "필드가 하는 일", 11, INK, KR, "start", 600)
d.line(AX + 16, 150, AX + AW - 16, 150, RULE, 0.8)
yy = 174
for head, body in [
    ("프리앰블 8 바이트", ["앞 7 바이트가 10101010 을 반복해", "수신 어댑터의 클록을 맞춥니다.",
                      "여덟째 바이트는 10101011 이라", "끝의 연속된 1 두 개가 시작을 알립니다."]),
    ("타입 2 바이트", ["어느 네트워크 계층으로 올릴지 고릅니다.", "ARP 는 0806 을 씁니다."]),
    ("CRC 4 바이트", ["수신 어댑터가 비트 오류를 잡습니다."]),
]:
    d.t(AX + 16, yy, head, 11, ACC, KR, "start", 600)
    for j, line in enumerate(body):
        d.t(AX + 16, yy + 18 + j * 17, line, 11, MUTED, KR, "start")
    yy += 18 + 17 * len(body) + 12

d.line(24, 404, W - 48, 404, RULE, 0.8)
d.t(24, 426, "데이터가 46 바이트에 못 미치면 채워 넣습니다. 네트워크 계층이 IP 헤더의 길이 필드로 그 채움을 걷어냅니다.",
     11, MUTED, KR, "start")
d.t(24, 444, "선로 위 순서는 크기순이 아니라 프리앰블 · 목적지 MAC · 출발지 MAC · 타입 · 데이터 · CRC 입니다. MTU 1500 은 데이터 필드의 상한입니다.",
     11, MUTED, KR, "start")

d.legend(462, [("데이터 — 실을 것", ACC), ("동기화", INFO), ("주소", OK), ("나머지 헤더", MUTED)])

out = pathlib.Path(__file__).resolve().parent.parent / "06-03.ethernet-frame.svg"
d.save(out)
print("→", out)

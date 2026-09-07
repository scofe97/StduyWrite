# 타입 스펙: type-layers — 위아래로 쌓인 추상 수준. 블루투스 스택에 없는 두 층이 이 도식의 논점이다.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §7.6.1 Figure 7.48 과 본문 —
#   네트워크 계층과 전통적 트랜스포트 계층이 없다는 서술, 79 채널 · 625 µs · 피코넷 8 대는 원문 그대로
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, OK, BAD, KR, MONO

W, H = 940, 600
d = D(W, H, "SECTION 7.6.1 · BLUETOOTH",
      "스택에 층이 둘 빠져 있습니다",
      "블루투스는 단일 홉 애드혹 망이라 라우팅이 필요 없다. 그래서 네트워크 계층과 전통적 트랜스포트 계층이 없다.",
      "빠진 층과 수치는 원문 §7.6.1 Figure 7.48 의 것입니다")

LX, LW = 24, 512
LY0, LH, STRIDE = 122, 56, 64
LAYERS = [
    ("응용", "이어폰 · 키보드 · 센서", OK, False),
    ("네트워크 계층", "없습니다 — 단일 홉이라 라우팅이 필요 없습니다", BAD, True),
    ("전통적 트랜스포트 계층", "없습니다 — 그 서비스는 아래 층이 대신합니다", BAD, True),
    ("L2CAP", "신뢰 전송 · 흐름 제어 · 분할 · 연결형과 비연결형 · 상위 API", ACC, False),
    ("베이스밴드와 무선", "TDM 과 FDM 을 겹쳐 쓰고 주파수를 도약합니다", INFO, False),
]
for i, (name, desc, c, missing) in enumerate(LAYERS):
    y = LY0 + i * STRIDE
    if missing:
        d.box(LX, y, LW, LH, PAPER, c, 1.2, 6)
        d.o[-1] = d.o[-1].replace('stroke-width="1.2"', 'stroke-width="1.2" stroke-dasharray="6 5"')
    else:
        d.tone(LX, y, LW, LH, c, 6, "12", 1.2)
    d.t(LX + 20, y + 26, name, 12, c, KR, "start", 600)
    d.t(LX + 20, y + 44, desc, 10, MUTED, KR, "start")

PX, PW = 572, 332
d.box(PX, LY0, PW, 5 * STRIDE - (STRIDE - LH), PAPER2, RULE, 1.0)
d.t(PX + 20, LY0 + 28, "숫자로 본 블루투스", 12, INK, KR, "start", 600)
d.line(PX + 20, LY0 + 40, PX + PW - 20, LY0 + 40, RULE, 0.8)
FACTS = [
    ("주파수 채널", "79 개"),
    ("슬롯 길이", "625 µs"),
    ("피코넷 활성 기기", "최대 8 대"),
    ("전송 속도", "2 에서 3 Mbps"),
    ("주변 기기 송신 출력", "100 · 2.5 · 1 mW"),
    ("탐색 질의", "채널마다 32 회 · 최대 128 번 반복"),
    ("응답 전 임의 대기", "0 에서 0.3 초"),
]
for j, (k, v) in enumerate(FACTS):
    y = LY0 + 66 + j * 26
    d.t(PX + 20, y, k, 11, MUTED, KR, "start")
    d.t(PX + PW - 20, y, v, 11, INK, MONO, "end")

NY = 456
d.box(24, NY, 880, 82, PAPER2, RULE, 1.0)
d.t(44, NY + 26, "중앙 제어기가 피코넷을 지배합니다", 12, INK, KR, "start", 600)
for i, ln in enumerate([
    "제어기의 시계가 슬롯 경계를 정하고, 도약 순서를 정하고, 누가 들어올지를 정합니다.",
    "주변 기기의 송신 출력까지 제어기가 정하고, 폴링으로 송신 권한을 줍니다. 주변끼리는 직접 통신하지 않습니다.",
]):
    d.t(44, NY + 50 + i * 20, ln, 11, MUTED, KR, "start")

d.legend(556, [("응용", OK), ("빠진 층", BAD), ("그 자리를 메우는 층", ACC), ("무선", INFO)])

out = pathlib.Path(__file__).resolve().parent.parent / "07-05.bluetooth-stack.svg"
d.save(out)
print("→", out)

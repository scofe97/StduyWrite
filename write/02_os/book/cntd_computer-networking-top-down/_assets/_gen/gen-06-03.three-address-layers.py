# 타입 스펙: type-layers — 위아래로 쌓인 추상 수준. 계층마다 자기 주소 체계를 하나씩 갖는다.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §6.4.1 —
#   "host names for the application layer, IP addresses for the network layer, and MAC addresses for the link layer"
#   와 곁상자 Principles in Practice: Keeping the Layers Independent 의 세 가지 이유
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, OK, KR, MONO

W, H = 940, 494
d = D(W, H, "SECTION 6.4.1 · THREE ADDRESS SPACES",
      "계층마다 자기 주소를 하나씩 갖습니다",
      "호스트 이름·IP 주소·MAC 주소는 서로 다른 계층에 붙는다. 계층이 독립적인 구성 요소로 남으려면 주소 체계도 갈라져 있어야 한다.",
      "세 주소의 성질은 원문 §6.4.1 의 서술 그대로입니다")

LX, LW, LH = 24, 470, 68
LAYERS = [
    ("애플리케이션", "호스트 이름", "www.example.com", INFO, "사람이 읽습니다"),
    ("네트워크", "IP 주소", "222.222.222.222", OK, "계층 구조 · 옮기면 바뀝니다"),
    ("링크", "MAC 주소", "49-BD-D2-C7-56-2A", ACC, "평면 구조 · 옮겨도 그대로입니다"),
]
for i, (layer, kind, sample, c, note) in enumerate(LAYERS):
    y = 116 + i * (LH + 12)
    d.tone(LX, y, LW, LH, c, 6, "14", 1.2)
    d.t(LX + 16, y + 24, layer, 11, c, KR, "start", 600)
    d.t(LX + 16, y + 46, kind, 13, INK, KR, "start", 600)
    d.t(LX + LW - 16, y + 26, sample, 11, MUTED, MONO, "end")
    d.t(LX + LW - 16, y + 48, note, 11, MUTED, KR, "end")

d.t(24, 364, "MAC 주소는 주민등록번호를 닮았고 IP 주소는 우편 주소를 닮았습니다. "
             "사람이 둘 다 갖는 것이 쓸모 있듯이 인터페이스도 둘 다 갖습니다.", 11, MUTED, KR, "start")

AX, AW = 524, 392
d.box(AX, 116, AW, 232, PAPER2, RULE, 1.0)
d.t(AX + 16, 140, "왜 MAC 주소가 따로 있어야 하나", 11, INK, KR, "start", 600)
d.line(AX + 16, 150, AX + AW - 16, 150, RULE, 0.8)
y = 176
for head, lines in [
    ("LAN 은 IP 전용이 아닙니다",
     ["어댑터에 IP 주소를 박으면 다른 네트워크 계층", "프로토콜을 받치기 어려워집니다"]),
    ("옮길 때마다 다시 설정해야 합니다",
     ["네트워크 계층 주소를 어댑터 RAM 에 저장해", "옮기거나 켤 때마다 고쳐 넣어야 합니다"]),
    ("주소를 아예 안 두면 더 비쌉니다",
     ["LAN 의 모든 프레임이 호스트를 인터럽트합니다"]),
]:
    d.t(AX + 16, y, "·", 11, ACC, KR, "start", 600)
    d.t(AX + 30, y, head, 11, INK, KR, "start", 600)
    for j, line in enumerate(lines):
        d.t(AX + 30, y + 18 + j * 18, line, 11, MUTED, KR, "start")
    y += 18 * (1 + len(lines)) + 12

d.line(24, 396, W - 48, 396, RULE, 0.8)
d.t(24, 418, "MAC 주소는 6 바이트라 2^48 개가 있고, IEEE 가 회사마다 앞 24 비트를 고정한 2^24 개 덩어리를 팔아 겹치지 않게 관리합니다.",
     11, MUTED, KR, "start")

d.legend(434, [("링크 계층 주소", ACC), ("네트워크 계층 주소", OK), ("애플리케이션 계층 이름", INFO)])

out = pathlib.Path(__file__).resolve().parent.parent / "06-03.three-address-layers.svg"
d.save(out)
print("→", out)

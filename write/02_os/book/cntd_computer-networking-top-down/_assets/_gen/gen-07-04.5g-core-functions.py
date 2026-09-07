# 타입 스펙: type-architecture — 시스템의 구성요소와 연결. 5G 코어의 네트워크 기능과 기준점.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §7.4.1 Figure 7.40 —
#   기능 이름과 N1·N2·N3 기준점, 그리고 UPF 가 유일한 데이터 평면 기능이라는 서술은 원문 그대로
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, OK, KR, MONO

W, H = 940, 592
d = D(W, H, "SECTION 7.4.1 · 5G CORE NETWORK FUNCTIONS",
      "제어는 여럿이 나눠 맡고 데이터는 하나가 다 나릅니다",
      "5G 코어는 기능 단위로 쪼개진 서비스 모음이다. 그중 사용자 데이터를 나르는 것은 UPF 하나뿐이다.",
      "기능 이름과 기준점 번호는 원문 Figure 7.40 의 것입니다")

EDGE = [(24, 148, "무선 기기", "user device", INFO), (24, 252, "기지국", "base station", INFO)]
for x, y, name, sub, c in EDGE:
    d.tone(x, y, 156, 64, c, 6, "12", 1.2)
    d.t(x + 78, y + 28, name, 12, c, KR, "middle", 600)
    d.t(x + 78, y + 48, sub, 10, MUTED, KR)

d.tone(232, 148, 188, 64, ACC, 6, "16", 1.4)
d.t(326, 176, "AMF", 13, ACC, MONO, "middle", 600)
d.t(326, 196, "제어 평면의 중심", 10, MUTED, KR)
d.tone(232, 252, 188, 64, OK, 6, "16", 1.4)
d.t(326, 280, "UPF", 13, OK, MONO, "middle", 600)
d.t(326, 300, "데이터 평면 유일", 10, MUTED, KR)
d.box(232, 352, 188, 52, PAPER2, RULE, 1.0)
d.t(326, 383, "바깥 인터넷", 12, MUTED, KR)

d.arrow([(102, 212), (102, 252)], MUTED, "ar", 1.3)
d.arrow([(180, 264), (206, 264), (206, 180), (232, 180)], MUTED, "ar", 1.3)
d.t(212, 236, "N2", 10, SOFT, MONO, "start")
d.arrow([(180, 296), (232, 296)], OK, "ok", 1.3)
d.t(206, 288, "N3", 10, SOFT, MONO)
d.arrow([(102, 148), (102, 120), (326, 120), (326, 148)], ACC, "acc", 1.3, "5 5")
d.t(214, 112, "N1 — AMF 만 기기와 직접 제어 메시지를 주고받습니다", 10, ACC, KR)
d.arrow([(326, 316), (326, 352)], OK, "ok", 1.3)

GX, GW, GH = 472, 136, 56
NFS = [
    ("SMF", "세션 · IP 주소 배정"), ("AUSF", "인증"), ("UDM", "가입자 정보"),
    ("UDR", "외부 저장소"), ("PCF", "정책 규칙"), ("NRF", "기능 등록 · 발견"),
    ("NSSF", "네트워크 슬라이싱"), ("NEF · AF", "앱에 기능 노출"), ("SEPP", "사업자 간 보안"),
]
for i, (nm, desc) in enumerate(NFS):
    x = GX + (i % 3) * (GW + 12)
    y = 148 + (i // 3) * (GH + 12)
    d.box(x, y, GW, GH, PAPER2, RULE, 0.9)
    d.t(x + GW / 2, y + 24, nm, 11, INK, MONO, "middle", 600)
    d.t(x + GW / 2, y + 42, desc, 10, MUTED, KR)
d.arrow([(420, 180), (GX - 8, 180)], ACC, "acc", 1.3)
d.t(GX + (GW * 3 + 24) / 2, 360, "서로를 요청·응답 또는 구독·통지로 부릅니다", 11, SOFT, KR)

PY = 424
d.box(24, PY, 880, 82, PAPER2, RULE, 1.0)
d.t(44, PY + 26, "왜 코어망이 셀룰러에만 있는가", 12, INK, KR, "start", 600)
for i, ln in enumerate([
    "1G·2G 는 전화망이었고 3G 도 주로 전화망이었습니다. 신원·이동성·로밍·과금이 처음부터 필요했습니다.",
    "그때 인터넷에는 그런 서비스가 없었고, 지금도 일반 ISP 에는 없습니다. 그 차이가 코어망으로 남았습니다.",
]):
    d.t(44, PY + 52 + i * 20, ln, 11, MUTED, KR, "start")

d.legend(526, [("가장자리 장치", INFO), ("제어 평면 중심", ACC), ("데이터 평면", OK)])

out = pathlib.Path(__file__).resolve().parent.parent / "07-04.5g-core-functions.svg"
d.save(out)
print("→", out)

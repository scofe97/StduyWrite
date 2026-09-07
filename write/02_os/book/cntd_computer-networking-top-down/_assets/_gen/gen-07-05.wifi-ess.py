# 타입 스펙: type-architecture — 시스템의 구성요소와 연결. 확장 서비스 집합 안에서 기기가 옮겨 다닌다.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §7.5.2 Figure 7.44 —
#   ESS 와 BSS 의 관계, 같은 SSID 와 같은 서브넷이라는 조건은 원문 그대로
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, OK, BAD, KR, MONO

W, H = 940, 560
d = D(W, H, "SECTION 7.5.2 · MOBILITY IN A WIFI NETWORK",
      "서브넷을 안 벗어나면 망 계층은 움직임을 모릅니다",
      "802.11 은 링크 계층 표준이라 이동성도 링크 계층에서만 다룬다. 그래서 이동 범위가 서브넷 안으로 묶인다.",
      "구성과 조건은 원문 Figure 7.44 의 것입니다")

d.tone(56, 148, 552, 228, ACC, 10, "08", 1.4)
d.t(76, 176, "확장 서비스 집합 (ESS)", 12, ACC, KR, "start", 600)
d.t(76, 196, "AP 들이 같은 SSID 를 쓰면 하나의 WLAN 으로 보입니다", 10, MUTED, KR, "start")

BSS = [(96, 220, "BSS 2", "AP2", INFO), (356, 220, "BSS 3", "AP3", INFO)]
for x, y, name, ap, c in BSS:
    d.tone(x, y, 220, 104, c, 8, "12", 1.2)
    d.t(x + 110, y + 30, name, 12, c, KR, "middle", 600)
    d.t(x + 110, y + 52, ap, 11, MUTED, MONO)
    d.t(x + 110, y + 76, "여기 붙은 기기들", 10, SOFT, KR)

d.arrow([(206, 350), (316, 350)], OK, "ok", 1.6)
d.t(261, 342, "기기가 옮겨 갑니다", 10, OK, KR)

d.box(660, 148, 244, 92, PAPER2, RULE, 1.0)
d.t(782, 180, "스위치 또는 라우터", 12, INK, KR, "middle", 600)
d.t(782, 204, "두 AP 가 같은 서브넷에 붙습니다", 10, MUTED, KR)
d.t(782, 224, "그래서 3 계층 주소가 안 바뀝니다", 10, MUTED, KR)
d.arrow([(608, 194), (656, 194)], MUTED, "ar", 1.3)

d.tone(660, 264, 244, 100, OK, 8, "12", 1.2)
d.t(782, 292, "망 계층이 보기에는", 12, OK, KR, "middle", 600)
d.t(782, 316, "이 기기는 움직이지 않았습니다", 11, OK, KR)
d.t(782, 340, "서브넷을 떠난 적이 없기 때문입니다", 10, MUTED, KR)

PY = 396
d.box(24, PY, 430, 90, PAPER2, RULE, 1.0)
d.t(44, PY + 26, "표준이 더해 준 것", 12, INK, KR, "start", 600)
for i, ln in enumerate([
    "빠른 BSS 전환이 802.1X 인증을 앞당깁니다.",
    "AP 가 옮겨 갈 만한 다른 AP 를 제안합니다.",
]):
    d.t(44, PY + 50 + i * 20, "·  " + ln, 11, MUTED, KR, "start")

d.box(474, PY, 430, 90, PAPER2, RULE, 1.0)
d.t(494, PY + 26, "서브넷을 벗어나면", 12, BAD, KR, "start", 600)
for i, ln in enumerate([
    "바깥에서 온 데이터그램은 여전히 옛 서브넷으로",
    "전달됩니다. 링크 계층만으로는 못 따라갑니다.",
]):
    d.t(494, PY + 50 + i * 20, "·  " + ln, 11, MUTED, KR, "start")

d.legend(504, [("확장 서비스 집합", ACC), ("각 BSS", INFO), ("움직여도 그대로인 것", OK), ("링크 계층의 한계", BAD)])

out = pathlib.Path(__file__).resolve().parent.parent / "07-05.wifi-ess.svg"
d.save(out)
print("→", out)

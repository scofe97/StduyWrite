# 타입 스펙: type-swimlane — 같은 절차를 두 환경에서 나란히 놓고, 어느 레인이 판정하는지를 가른다.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §8.8.1 Figure 8.30 · 8.31 · 8.32 (책 606~610쪽) —
#   SAE 네 단계, 802.1X·EAP-TTLS 의 통과 구조, EAPoL·RADIUS 캡슐화는 원문 그대로.
#   원문이 기업용 절에서 WPA3-Personal 이라 적은 것은 오기이며 본문에 정오로 병기했다.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, OK, WARN, KR, MONO

W, H = 1000, 668
d = D(W, H, "SECTION 8.8.1 · WIFI AUTHENTICATION",
      "확인하는 상대가 환경에 따라 다릅니다",
      "개인용은 AP 와 직접 인증하고, 기업용은 인증 서버와 인증하며 AP 는 통과 장치가 된다.",
      "두 환경의 구성과 SAE 네 단계는 원문 §8.8.1 의 것입니다")

LX, LW = 24, 200
CX0, CW = 240, 240
LANES = [
    (148, "개인용", "WPA3-Personal", ACC,
     ["기기가 AP 와 직접", "SAE 네 단계", "PMK 를 각자 유도"]),
    (272, "기업용", "WPA3-Enterprise", INFO,
     ["기기가 인증 서버와", "802.1X · EAP-TTLS", "서버가 AP 에 PMK 전달"]),
]
LH = 104
HEAD = ["누구와 인증하나", "쓰는 프로토콜", "끝나면"]
for i, h in enumerate(HEAD):
    d.t(CX0 + i * CW + CW / 2, 130, h, 11, SOFT, KR, "middle", 600)
d.line(CX0, 138, CX0 + 3 * CW, 138, RULE, 0.8)
for ly, name, en, c, cells in LANES:
    d.tone(LX, ly, LW, LH, c, 6, "16" if c is ACC else "12", 1.3)
    d.t(LX + LW / 2, ly + 44, name, 13, c, KR, "middle", 600)
    d.t(LX + LW / 2, ly + 68, en, 10, SOFT, MONO)
    for i, txt in enumerate(cells):
        x = CX0 + i * CW
        d.tone(x + 6, ly + 16, CW - 12, LH - 32, c, 4, "20", 1.2)
        d.t(x + CW / 2, ly + 58, txt, 11, c, KR)

SY = 408
d.box(24, SY, 470, 180, PAPER2, RULE, 1.0)
d.t(44, SY + 28, "SAE 네 단계 — Dragonfly 열쇠 교환", 12, INK, KR, "start", 600)
d.line(44, SY + 40, 474, SY + 40, RULE, 0.8)
for i, ln in enumerate(["1. 클라이언트 커밋 — element1 과 논스",
                        "2. AP 커밋 — element2 와 논스",
                        "3. 클라이언트 확인 — 앞선 값들의 해시",
                        "4. AP 확인 — 받은 해시 검사 후 자기 해시",
                        "공유 비밀을 망으로 보내지 않고 서로를 확인합니다."]):
    d.t(44, SY + 64 + i * 22, ln, 11, ACC if i == 4 else MUTED, KR, "start")

d.box(514, SY, 462, 180, PAPER2, RULE, 1.0)
d.t(534, SY + 28, "메시지가 실려 가는 길", 12, INK, KR, "start", 600)
d.line(534, SY + 40, 956, SY + 40, RULE, 0.8)
HOPS = [("EAP", "기기 ↔ 인증 서버 종단 간", OK), ("EAPoL", "무선 구간에서 EAP 를 감쌈", INFO),
        ("RADIUS", "AP ↔ 인증 서버, UDP/IP 위", INFO)]
for i, (k, v, c) in enumerate(HOPS):
    d.t(534, SY + 68 + i * 26, k, 11, c, MONO, "start", 600)
    d.t(624, SY + 68 + i * 26, v, 11, MUTED, KR, "start")
d.t(534, SY + 146, "카페 비밀번호는 모두가 공유합니다. 모르는 사람만 막힙니다.", 11, WARN, KR, "start")

d.legend(608, [("개인용", ACC), ("기업용", INFO), ("종단 간", OK), ("주의할 점", WARN)])
out = pathlib.Path(__file__).resolve().parent.parent / "08-04.wifi-auth.svg"
d.save(out); print("→", out.name)

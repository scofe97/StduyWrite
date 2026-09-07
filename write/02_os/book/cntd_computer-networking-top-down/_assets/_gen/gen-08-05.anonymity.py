# 타입 스펙: type-process — 요청이 왼쪽에서 오른쪽으로 흐르며 어느 구간에서 무엇이 드러나는가.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §8.9.1 곁상자 Figure 8.36 (책 620~621쪽) —
#   TLS 만으로는 앞의 둘이 실패한다는 것, 프록시 하나의 한계, TOR 가 셋을 무작위로 고른다는 것은 원문 그대로
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, OK, WARN, BAD, KR, MONO

W, H = 1000, 596
d = D(W, H, "SECTION 8.9.1 · ANONYMITY AND PRIVACY",
      "TLS 는 내용을 가리지 그 사실을 가리지 않습니다",
      "출발지 주소는 사이트에 그대로 제시되고 목적지 주소는 ISP 가 엿본다. 그래서 프록시를 겹친다.",
      "세 요구와 TOR 의 사슬 구조는 원문 곁상자의 것입니다")

WY = 144
WANT = [(24, "사이트에 내 IP 를 안 드러내기", BAD), (348, "ISP 가 방문을 모르게", BAD),
        (672, "ISP 가 데이터를 못 보게", OK)]
d.t(24, WY - 12, "TLS 만 썼을 때 — 셋 중 둘이 실패합니다", 12, INK, KR, "start", 600)
for x, want, c in WANT:
    d.tone(x, WY, 304, 60, c, 6, "16", 1.2)
    d.t(x + 152, WY + 28, want, 11, c, KR)
    d.t(x + 152, WY + 48, "실패" if c is BAD else "성공", 11, c, KR)

PY = 252
d.t(24, PY - 12, "프록시 하나 + TLS", 12, INFO, KR, "start", 600)
CHAIN = [(24, "나", "", INK), (216, "프록시", "TLS 로 감쌈", INFO),
         (408, "사이트", "프록시 IP 만 봅니다", OK)]
for x, name, sub, c in CHAIN:
    d.box(x, PY, 152, 64, PAPER2, RULE, 1.0, 7)
    d.t(x + 76, PY + (38 if not sub else 28), name, 12, c, KR, "middle", 600)
    if sub:
        d.t(x + 76, PY + 50, sub, 10, MUTED, KR)
for a in (176, 368):
    d.arrow([(a + 2, PY + 32), (a + 36, PY + 32)], MUTED, "ar", 1.3)
d.tone(608, PY, 368, 64, WARN, 7, "14", 1.3)
d.t(792, PY + 28, "프록시는 전부 압니다", 12, WARN, KR, "middle", 600)
d.t(792, PY + 50, "내 IP · 사이트 IP · 오가는 평문", 11, MUTED, KR)

TY = 368
d.t(24, TY - 12, "TOR — 담합하지 않는 프록시 셋을 무작위로", 12, ACC, KR, "start", 600)
NODES = [(24, "나", INK), (200, "프록시 1", ACC), (376, "프록시 2", ACC),
         (552, "프록시 3", ACC), (728, "사이트", OK)]
for x, name, c in NODES:
    if c is ACC:
        d.tone(x, TY, 136, 56, c, 6, "18", 1.3)
    else:
        d.box(x, TY, 136, 56, PAPER2, RULE, 1.0, 7)
    d.t(x + 68, TY + 34, name, 12, c, KR, "middle", 600)
for a in (160, 336, 512, 688):
    d.arrow([(a + 2, TY + 28), (a + 36, TY + 28)], ACC, "acc", 1.3)
d.t(24, TY + 84, "담합하지 않는다면 내 IP 와 목적지 사이에 통신이 있었다는 것을 아무도 모릅니다.", 11, MUTED, KR, "start")
d.t(24, TY + 106, "마지막 프록시와 서버 사이는 평문이지만, 그 프록시는 평문을 주고받는 IP 가 누구인지 모릅니다.",
    11, MUTED, KR, "start")

d.legend(516, [("실패하는 요구", BAD), ("되는 요구", OK), ("프록시 하나의 한계", WARN), ("사슬", ACC)])
out = pathlib.Path(__file__).resolve().parent.parent / "08-05.anonymity.svg"
d.save(out); print("→", out.name)

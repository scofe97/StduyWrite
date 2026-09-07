# 타입 스펙: type-process — 판마다 같은 의미 슬롯이 반복되고 왼쪽에서 오른쪽으로 흐른다.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §8.4 (책 583~586쪽) —
#   ap1.0·ap2.0·ap3.0·ap3.1·ap4.0 의 이름과 각 실패 시나리오는 원문 그대로. 원문은 ap5.0 을 본문에 두지 않는다.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, OK, WARN, BAD, KR, MONO

W, H = 1000, 560
d = D(W, H, "SECTION 8.4 · AUTHENTICATION PROTOCOL",
      "판마다 구체적인 공격 하나씩을 막습니다",
      "3장의 rdt 와 같은 방식으로 다섯 번 다시 짓는다. 마지막 판이 더한 것은 한 번만 쓰는 수 하나다.",
      "다섯 판과 실패 시나리오는 원문 §8.4 의 것입니다")

BW, BH, BY = 180, 224, 148
XS = [24, 216, 408, 600, 792]
STEPS = [
    ("ap1.0", "이름만 말합니다", "\"나는 앨리스다\"", "트루디도 똑같이\n보낼 수 있습니다", BAD),
    ("ap2.0", "출발지 IP 를 봅니다", "알려진 주소와 대조", "IP 스푸핑으로\n주소를 채웁니다", BAD),
    ("ap3.0", "비밀번호를 보냅니다", "공유 비밀", "엿들으면\n그대로 샙니다", BAD),
    ("ap3.1", "비밀번호를 암호화", "K_A-B 로 잠급니다", "녹음해서 다시 틀면\n통과합니다", WARN),
    ("ap4.0", "논스를 되돌립니다", "K_A-B(R)", "신원과 생존성을\n함께 증명합니다", ACC),
]
for x, (name, what, how, fail, c) in zip(XS, STEPS):
    if c is ACC:
        d.tone(x, BY, BW, BH, c, 7, "18", 1.4)
    else:
        d.box(x, BY, BW, BH, PAPER2, RULE, 1.0, 7)
    d.t(x + BW / 2, BY + 30, name, 13, c, MONO, "middle", 600)
    d.line(x + 16, BY + 44, x + BW - 16, BY + 44, RULE, 0.8)
    d.t(x + BW / 2, BY + 70, "하는 일", 10, SOFT, KR)
    d.t(x + BW / 2, BY + 92, what, 11, INK, KR)
    d.t(x + BW / 2, BY + 114, how, 10, MUTED, MONO)
    d.t(x + BW / 2, BY + 150, "남은 구멍" if c is not ACC else "얻는 것", 10, SOFT, KR)
    for i, ln in enumerate(fail.split("\n")):
        d.t(x + BW / 2, BY + 172 + i * 18, ln, 11, c, KR)
for a, b in zip(XS, XS[1:]):
    d.arrow([(a + BW + 2, BY + BH / 2), (b - 4, BY + BH / 2)], MUTED, "ar", 1.3)

PY = 404
d.box(24, PY, 952, 76, PAPER2, RULE, 1.0)
d.t(44, PY + 28, "TCP 3-way 핸드셰이크와 같은 얼개입니다", 12, INK, KR, "start", 600)
d.t(44, PY + 56, "서버가 오래 쓰지 않은 초기 순서 번호를 보내고 그 번호를 담은 ACK 를 기다린 것과 같습니다. 논스는 그 착상을 인증에 옮긴 것입니다.",
    11, MUTED, KR, "start")

d.legend(500, [("깨지는 판", BAD), ("재생에 약한 판", WARN), ("논스를 더한 판", ACC)])
out = pathlib.Path(__file__).resolve().parent.parent / "08-03.auth-protocol-evolution.svg"
d.save(out); print("→", out.name)

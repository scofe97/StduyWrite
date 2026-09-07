# 02-03 §3 — 원문 Figure 2.14. 메일이 지나는 세 구간과 각 구간의 프로토콜.
# 마지막 구간만 방향이 반대인 것이 이 절의 요점이라 그 구간에 강조색을 뒀다.
# 타입 스펙: type-data-flow — 단계마다 누가 무엇을 하는지. 화살표 라벨이 그 구간의 프로토콜이다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 496
# 상자를 좁히고 사이를 넓힌 것은 화살표 라벨이 들어갈 자리를 만들기 위해서다.
NW, NH, NY = 150, 76, 164
XS = [96, 344, 616, 902]

d = D(W, H, "COMPUTER NETWORKING TOP-DOWN · 02-03 §3",
      "메일은 밀려 가고 당겨서 옵니다",
      "원문 Figure 2.14 의 경로. 앞의 두 구간은 보내는 쪽이 밀고, 마지막 구간만 받는 쪽이 당긴다.",
      "SMTP 로는 편지함을 열어 볼 수 없습니다 — 방향이 반대이기 때문입니다")

NODES = [("Alice", "사용자 에이전트", False), ("Alice 의", "메일 서버", False),
         ("Bob 의", "메일 서버", False), ("Bob", "사용자 에이전트", True)]
for x, (l1, l2, focal) in zip(XS, NODES):
    if focal:
        d.tone(x - NW / 2, NY, NW, NH, ACC, 6, "14", 1.4)
    else:
        d.box(x - NW / 2, NY, NW, NH, PAPER2, RULE, 1.0, 6)
    d.t(x, NY + 32, l1, 12, ACC if focal else INK, KR, "middle", 600)
    d.t(x, NY + 54, l2, 11, SOFT, KR)

def hop(a, b, label, sub, c=MUTED, y=NY + NH / 2, dash=None):
    x1, x2 = XS[a] + NW / 2 + 8, XS[b] - NW / 2 - 12
    d.path(f"M {x1} {y} L {x2} {y}", c, 1.5, m={MUTED: "ar", ACC: "acc", OK: "ok"}[c], dash=dash)
    mx = (x1 + x2) / 2
    d.t(mx, y - 12, label, 11, c, MONO)
    d.t(mx, y + 20, sub, 11, SOFT, KR)

hop(0, 1, "SMTP or HTTP", "밀기")
hop(1, 2, "SMTP", "밀기 · TCP 25")
# 마지막 구간은 방향이 반대 — 오른쪽에서 왼쪽으로 요청이 가고 데이터가 온다
x1, x2 = XS[3] - NW / 2 - 8, XS[2] + NW / 2 + 12
d.path(f"M {x1} {NY + 26} L {x2} {NY + 26}", ACC, 1.5, m="acc")
d.t((x1 + x2) / 2, NY + 16, "요청", 11, ACC, KR)
d.path(f"M {x2} {NY + 58} L {x1} {NY + 58}", ACC, 1.5, m="acc", dash="5 4")
d.t((x1 + x2) / 2, NY + 78, "HTTP or IMAP", 11, ACC, MONO)
d.t((x1 + x2) / 2, NY + 98, "당기기", 11, ACC, KR)

# 밀기 구간의 실패 처리
d.box(XS[1] - NW / 2, NY + NH + 44, NW + 120, 70, PAPER2, RULE, 0.9, 6)
d.t(XS[1] + 60, NY + NH + 70, "Bob 의 서버가 죽어 있으면", 11, SOFT, KR)
d.t(XS[1] + 60, NY + NH + 92, "여기 남아 30분마다 다시 시도합니다", 11, SOFT, KR)

d.t(20, 384, "중간 메일 서버를 거치지 않습니다. Alice 의 서버가 홍콩에 있고 Bob 의 서버가 세인트루이스에 있어도 둘 사이의 TCP 연결이 직접 맺힙니다.",
     11, MUTED, KR, "start")
d.t(20, 406, "Alice 의 에이전트가 Bob 의 서버로 곧장 보내지 않는 이유는, 도달할 수 없을 때 에이전트에게 아무 대책이 없기 때문입니다.",
     11, MUTED, KR, "start")

d.legend(H - 56, [("방향이 반대인 구간", ACC), ("미는 구간", MUTED)])
d.save("02-03.mail-protocols.svg")

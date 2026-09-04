# 02-04.firewall-two-traces — 세 줄짜리 방화벽을 두 패킷이 다르게 지난다
# 본문 요구: §5 "이 세 줄이 안에서 나가는 것은 되고 밖에서 새로 들어오는 것은 안 되는 방화벽입니다."
#           같은 규칙 묶음인데 패킷에 따라 도착지가 갈린다는 것이 논지다.
# 타입 스펙: type-flowchart.md — 모양이 종류를 나른다(타원=시작·끝, 마름모=판단).
#           semantic-patterns 의 Paired policy-evaluation traces 가 이 형태를 지목한다.
#           coral 은 가장 결과가 무거운 종착지 하나.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 664
d = D(W, H, "FORWARD CHAIN · TWO TRACES",
      "같은 세 줄인데 패킷에 따라 도착지가 다르다",
      "정책을 DROP 으로 뒤집고 두 줄만 허용하면 방향성 있는 방화벽이 됩니다. "
      "기존 연결의 응답은 첫 줄에서 통과하고, 밖에서 온 새 연결은 어디에도 걸리지 않아 정책을 맞습니다.",
      lead="응답은 첫 줄에서, 나가는 새 연결은 둘째 줄에서, 나머지는 정책이 맞는다")

LCX, RCX = 340, 764
DW, DH = 360, 96

def oval(cx, cy, txt, c=MUTED, w=200, focal=False):
    if focal:
        d.o.append(f'<rect x="{cx-w//2}" y="{cy-22}" width="{w}" height="44" rx="20" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>'); c = ACC
    else:
        d.box(cx - w // 2, cy - 22, w, 44, PAPER2, c, 1.1, 20)
    d.t(cx, cy + 5, ddx.fit(txt, 12, w - 24, txt), 12, c, KR, "middle", 600)

def diamond(cx, cy, txt, sub):
    """마름모는 세로로 갈수록 좁아진다. 부제를 중앙 폭 기준으로 재면 경사변을 뚫는다 —
    그 y 에서의 실제 폭으로 가드를 건다."""
    hw, hh = DW // 2, DH // 2
    d.path(f"M {cx} {cy-hh} L {cx+hw} {cy} L {cx} {cy+hh} L {cx-hw} {cy} Z", RULE, 1.2)
    d.t(cx, cy - 10, ddx.fit(txt, 12, DW - 48, txt), 12, INK, KR, "middle", 600)
    avail = int(2 * hw * (1 - 16 / hh)) - 24
    d.t(cx, cy + 16, ddx.fit(sub, 11, avail, f"diamond sub @{cy}"), 11, SOFT, MONO)

def note(cx, cy, txt, c):
    ddx.tag(d, cx, cy, txt, c, ddx.textw(txt, 12) + 28)

oval(LCX, 168, "FORWARD 체인 도착")
d.path(f"M {LCX} 190 L {LCX} {268-DH//2-8}", MUTED, 1.5, m="ar")
diamond(LCX, 268, "기존 연결의 일부인가?", "--ctstate ESTABLISHED,RELATED")
d.path(f"M {LCX+DW//2} 268 L {RCX-100-8} 268", MUTED, 1.5, m="ar")
d.t((LCX + DW // 2 + RCX - 100) // 2, 256, "예", 11, SOFT, KR)
oval(RCX, 268, "ACCEPT", OK)
note(RCX, 324, "밖에서 온 응답", OK)

d.path(f"M {LCX} {268+DH//2} L {LCX} {420-DH//2-8}", MUTED, 1.5, m="ar")
d.t(LCX + 14, 356, "아니오", 11, SOFT, KR, )
diamond(LCX, 420, "출발지가 10.10.1.0/24 인가?", "-s 10.10.1.0/24")
d.path(f"M {LCX+DW//2} 420 L {RCX-100-8} 420", MUTED, 1.5, m="ar")
d.t((LCX + DW // 2 + RCX - 100) // 2, 408, "예", 11, SOFT, KR)
oval(RCX, 420, "ACCEPT", OK)
note(RCX, 476, "안에서 나가는 새 연결", OK)

d.path(f"M {LCX} {420+DH//2} L {LCX} {540-22-8}", ACC, 1.6, m="acc")
d.t(LCX + 14, 508, "아니오 — 어느 줄에도 안 걸림", 11, ACC, KR, "start")
oval(LCX, 540, "정책 DROP", focal=True)
note(RCX, 540, "밖에서 온 새 연결", ACC)

d.t(36, 604, "규칙을 다 훑고도 안 걸리면 체인의 기본 정책이 적용됩니다. "
             "정책이 ACCEPT 인 채로 두면 이 세 줄은 아무것도 막지 못합니다.", 12, MUTED, KR, "start")
d.legend(620, [("통과", OK), ("어디에도 안 걸려 정책을 맞는다", ACC)])
d.save("02-04.firewall-two-traces.svg")
print("ok firewall-two-traces")

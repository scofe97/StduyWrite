# 02-03 §1 — Wireshark 가 프로토콜을 정하는 기본 규칙과 그 규칙이 틀리는 지점, 그리고 Decode-As 로
# 사람이 덮어쓰는 경로.
# 타입 스펙: type-flowchart — 조건에 따라 갈라지는 판단 논리. 도형이 종류를 나른다
#           (사각형=단계, 마름모=판단). focal 은 규칙이 틀리는 판단 하나.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, WARN, PAPER2, RULE, KR, MONO

W, H = 880, 592
d = D(W, H, "PACKET ANALYSIS WITH WIRESHARK · 02-03 §1",
      "프로토콜은 포트로 정해집니다",
      "Wireshark 는 표준 포트를 근거로 디섹터를 고른다. 비표준 포트에서 도는 서비스는 그 판별에 걸리지 않아 TCP 로만 보이고, Decode-As 가 그 매핑을 사람이 덮어쓰는 경로다.",
      "복호화가 아니라 해석입니다 — 암호화된 내용은 그대로 남습니다")

CX = 300
def step(cx, y, w, h, title, sub, c=None):
    if c: d.tone(cx - w / 2, y, w, h, c, 6)
    else: d.box(cx - w / 2, y, w, h, PAPER2, RULE, 1.0, 6)
    d.t(cx, y + 24, title, 13, c if c else INK, KR, "middle", 600)
    d.t(cx, y + 44, sub, 11, MUTED, KR)

def diamond(cx, y, hw, hh, txt, focal=False):
    cy, c = y + hh, (ACC if focal else INK)
    d.o.append(f'<polygon points="{cx},{y} {cx + hw},{cy} {cx},{y + 2 * hh} {cx - hw},{cy}" '
               f'fill="{ACC + "12" if focal else PAPER2}" stroke="{c}" stroke-width="{1.4 if focal else 1.1}"/>')
    d.t(cx, cy + 5, txt, 13, c, KR, "middle", 600)

Y_S1, Y_D, Y_OK, Y_OVR, Y_END = 108, 200, 320, 320, 452

d.arrow([(CX, Y_S1 + 64), (CX, Y_D - 4)], MUTED, "ar", 1.4)
d.arrow([(CX, Y_D + 80), (CX, Y_OK - 4)], MUTED, "ar", 1.4)
d.arrow([(CX + 148, Y_D + 40), (588, Y_D + 40)], WARN, "warn", 1.4)
d.arrow([(700, Y_D + 80), (700, Y_OVR - 4)], WARN, "warn", 1.4)
d.arrow([(CX, Y_OK + 64), (CX, Y_END - 4)], MUTED, "ar", 1.4)
d.arrow([(700, Y_OVR + 64), (700, Y_END + 32), (CX + 152, Y_END + 32)], WARN, "warn", 1.4)

step(CX, Y_S1, 300, 64, "프레임이 들어옵니다", "TCP 목적지 포트를 읽습니다")
diamond(CX, Y_D, 148, 40, "표준 포트인가?", focal=True)
step(CX, Y_OK, 300, 64, "해당 디섹터로 해석", "443 이면 TLS 로 펼칩니다", c=OK)
step(700, Y_D, 296, 80, "TCP 로만 보입니다", "4433 의 TLS 는 판별에 안 걸립니다", c=WARN)
step(700, Y_OVR, 296, 64, "Analyze | Decode As", "포트에 디섹터를 손으로 지정", c=WARN)
step(CX, Y_END, 300, 64, "Packet Details 에 펼쳐집니다", "복호화가 아니라 해석입니다")

d.t(CX + 16, Y_D + 100, "예", 11, MUTED, KR, "start", 600)
d.t(474, Y_D + 26, "아니오", 11, WARN, KR, "middle", 600)

d.legend(540, [("규칙이 틀리는 판단", ACC), ("기본 판별이 맞은 경로", OK), ("사람이 덮어쓰는 경로", WARN)])
d.save("02-03.decode-as.svg")

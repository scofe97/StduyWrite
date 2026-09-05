# 02-01 §7 — 패킷이 안 보일 때 무엇부터 가르는가. 원문 Troubleshooting 절의 두 갈래를 판단 순서로 세운다.
# 타입 스펙: type-flowchart — 조건에 따라 갈라지는 판단 논리. 도형이 종류를 나른다
#           (타원=시작·끝, 사각형=조치, 마름모=판단). focal 은 가장 먼저 갈라야 할 판단 하나.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, BAD, PAPER2, RULE, KR, MONO

W, H = 880, 616
d = D(W, H, "PACKET ANALYSIS WITH WIRESHARK · 02-01 §7",
      "패킷이 안 보일 때",
      "인터페이스 목록이 비어 있는 경우와 목록은 있는데 패킷이 안 잡히는 경우는 원인이 다르다. 먼저 목록 유무로 가른 뒤 각각의 조치로 내려간다.",
      "목록이 비었으면 권한 문제, 목록이 있으면 인터페이스·모드 문제입니다")

CX = 300
def oval(cx, y, w, h, txt, c=INK):
    d.o.append(f'<rect x="{cx - w / 2}" y="{y}" width="{w}" height="{h}" rx="20" '
               f'fill="{PAPER2}" stroke="{c}" stroke-width="1.1"/>')
    d.t(cx, y + h / 2 + 5, txt, 13, c, KR, "middle", 600)

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

Y_S, Y_D, Y_L, Y_R2, Y_END = 96, 160, 268, 372, 500

d.arrow([(CX, Y_S + 40), (CX, Y_D - 4)], MUTED, "ar", 1.4)
d.arrow([(CX, Y_D + 76), (CX, Y_L - 4)], MUTED, "ar", 1.4)            # 목록 있음 → 아래
d.arrow([(CX + 140, Y_D + 38), (536, Y_D + 38)], MUTED, "ar", 1.4)            # 목록 없음 → 오른쪽
d.arrow([(CX, Y_L + 68), (CX, Y_R2 - 4)], MUTED, "ar", 1.4)
d.arrow([(700, Y_D + 76), (700, Y_R2 + 34), (CX + 180, Y_R2 + 34)], MUTED, "ar", 1.4)
d.arrow([(CX, Y_R2 + 68), (CX, Y_END - 4)], MUTED, "ar", 1.4)

oval(CX, Y_S, 200, 40, "패킷이 안 보인다")
diamond(CX, Y_D, 140, 38, "인터페이스 목록이 뜨는가?", focal=True)
step(CX, Y_L, 352, 68, "인터페이스와 트래픽을 확인합니다",
     "맞는 인터페이스인가 · 라이브 트래픽이 있는가")
step(CX, Y_R2, 352, 68, "promiscuous 를 껐다 켭니다",
     "자기 것 아닌 프레임을 버리고 있지 않은가")
step(700, Y_D, 320, 76, "캡처 권한을 확인합니다",
     "Wireshark 가 NIC 을 쓸 권한이 있는가", c=BAD)
oval(CX, Y_END, 200, 40, "다시 캡처", OK)

d.t(CX + 16, Y_D + 96, "뜬다", 11, MUTED, KR, "start", 600)
d.t(458, Y_D + 26, "안 뜬다", 11, MUTED, KR, "middle", 600)
d.t(CX + 200, Y_R2 + 22, "권한 해결 후 합류", 11, MUTED, KR, "start")

d.legend(556, [("먼저 갈라야 할 판단", ACC), ("권한 쪽 경로", BAD), ("복귀", OK)])
d.save("02-01.no-packets-triage.svg")

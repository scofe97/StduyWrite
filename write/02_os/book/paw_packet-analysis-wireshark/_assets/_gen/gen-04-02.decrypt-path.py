# 04-02 §2 — 잡아 둔 TLS 트래픽을 복호화할 수 있는지, 있다면 무엇이 필요한지 가르는 순서.
# 원문의 RSA 경로와 DHE/ECDHE 불가 판정, 그리고 원문 뒤에 바뀐 TLS 1.3 조건을 함께 놓는다.
# 타입 스펙: type-flowchart — 조건에 따라 갈라지는 판단 논리. 도형이 종류를 나르고,
#           focal 은 실패 갈림길이 아니라 실제로 자주 쓰이는 경로 하나(세션 키 로그).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, BAD, WARN, PAPER2, RULE, KR, MONO

W, H = 920, 700
d = D(W, H, "PACKET ANALYSIS WITH WIRESHARK · 04-02 §2",
      "복호화가 되는 경우와 안 되는 경우",
      "Server Hello 가 고른 cipher suite 의 이름 하나가 복호화 가능 여부를 정한다. 정적 RSA 면 서버 개인키로 열리고, DHE·ECDHE 면 개인키로는 열리지 않아 세션 키 로그가 필요하다.",
      "이름에 DHE 나 ECDHE 가 있으면 개인키를 갖고 있어도 열리지 않습니다")

CX = 300
def oval(cx, y, w, h, txt, c=INK):
    d.o.append(f'<rect x="{cx - w / 2}" y="{y}" width="{w}" height="{h}" rx="20" '
               f'fill="{PAPER2}" stroke="{c}" stroke-width="1.1"/>')
    d.t(cx, y + h / 2 + 5, txt, 13, c, KR, "middle", 600)

def step(cx, y, w, h, title, sub, c=None, focal=False):
    if focal:
        d.o.append(f'<rect x="{cx - w / 2}" y="{y}" width="{w}" height="{h}" rx="6" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    elif c: d.tone(cx - w / 2, y, w, h, c, 6)
    else: d.box(cx - w / 2, y, w, h, PAPER2, RULE, 1.0, 6)
    col = ACC if focal else (c if c else INK)
    d.t(cx, y + 24, title, 13, col, KR, "middle", 600)
    d.t(cx, y + 44, sub, 11, MUTED, KR)

def diamond(cx, y, hw, hh, txt):
    cy = y + hh
    d.o.append(f'<polygon points="{cx},{y} {cx + hw},{cy} {cx},{y + 2 * hh} {cx - hw},{cy}" '
               f'fill="{PAPER2}" stroke="{INK}" stroke-width="1.1"/>')
    d.t(cx, cy + 5, txt, 13, INK, KR, "middle", 600)

Y_S, Y_D1, Y_R1, Y_D2, Y_R2, Y_KEY, Y_END = 96, 160, 166, 300, 306, 452, 588

d.arrow([(CX, Y_S + 40), (CX, Y_D1 - 4)], MUTED, "ar", 1.4)
d.arrow([(CX + 152, Y_D1 + 40), (600, Y_R1 + 34)], OK, "ok", 1.4)
d.arrow([(CX, Y_D1 + 80), (CX, Y_D2 - 4)], MUTED, "ar", 1.4)
d.arrow([(CX + 152, Y_D2 + 40), (600, Y_R2 + 34)], BAD, "bad", 1.4)
d.arrow([(CX, Y_D2 + 80), (CX, Y_KEY - 4)], MUTED, "ar", 1.4)
d.arrow([(740, Y_R2 + 68), (740, Y_KEY + 34), (CX + 176, Y_KEY + 34)], BAD, "bad", 1.4)
d.arrow([(740, Y_R1 + 68), (740, Y_KEY - 40), (CX + 176, Y_KEY - 40), (CX, Y_KEY - 40), (CX, Y_KEY - 4)],
        OK, "ok", 1.4, dash="4,3")
d.arrow([(CX, Y_KEY + 68), (CX, Y_END - 4)], MUTED, "ar", 1.4)

oval(CX, Y_S, 320, 40, "잡아 둔 TLS 를 열고 싶다")
diamond(CX, Y_D1, 152, 40, "이름에 DHE·ECDHE 가 없나?")
step(740, Y_R1, 320, 68, "서버 개인키로 열립니다", "Preferences 에 server.key 등록", c=OK)
diamond(CX, Y_D2, 152, 40, "TLS 1.3 인가?")
step(740, Y_R2, 320, 68, "정적 RSA 자체가 없습니다", "RFC 8446 이 없앴습니다", c=BAD)
step(CX, Y_KEY, 352, 68, "(pre)-master-secret 로그가 필요합니다",
     "브라우저·클라이언트가 남긴 세션 키 파일", focal=True)
oval(CX, Y_END, 320, 40, "Wireshark 가 평문으로 펼칩니다", OK)

d.t(CX + 220, Y_D1 + 26, "없음", 11, OK, KR, "middle", 600)
d.t(CX + 16, Y_D1 + 100, "있음", 11, MUTED, KR, "start", 600)
d.t(CX + 220, Y_D2 + 26, "예", 11, BAD, KR, "middle", 600)
d.t(CX + 16, Y_D2 + 100, "아니오", 11, MUTED, KR, "start", 600)
d.t(CX + 200, Y_KEY - 52, "키를 내보내 공유할 때도 같은 파일", 11, OK, KR, "start")

d.legend(H - 60, [("실무에서 실제로 쓰는 경로", ACC), ("열리는 경우", OK), ("열리지 않는 경우", BAD)])
d.save("04-02.decrypt-path.svg")

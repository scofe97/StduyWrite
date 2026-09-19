# 04-02 §2 — 잡아 둔 TLS 트래픽을 복호화할 수 있는지, 있다면 무엇이 필요한지 가르는 순서.
# 원문의 RSA 경로와 DHE/ECDHE 불가 판정, 그리고 원문 뒤에 바뀐 TLS 1.3 조건을 함께 놓는다.
# 타입 스펙: type-flowchart — 조건에 따라 갈라지는 판단 논리. 도형이 종류를 나르고,
#           focal 은 실패 갈림길이 아니라 실제로 자주 쓰이는 경로 하나(세션 키 로그).
# 분기 순서: TLS 1.3 을 먼저 묻는다. 1.3 은 cipher suite 이름에 키 교환 방식이 실리지
#           않으므로(TLS_AES_128_GCM_SHA256 꼴) 이름 규칙을 먼저 적용할 수 없다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, BAD, WARN, PAPER2, RULE, KR, MONO

W, H = 1000, 700
d = D(W, H, "PACKET ANALYSIS WITH WIRESHARK · 04-02 §2",
      "복호화가 되는 경우와 안 되는 경우",
      "인증서 기반 연결의 복호화 경로. TLS 1.2 RSA 키 교환은 일치하는 서버 개인키와 원래 전체 핸드셰이크가 필요하다. DHE·ECDHE와 TLS 1.3은 종단에서 제공하는 세션 비밀값을 사용할 수 있다.",
      "버전을 먼저 확인하고, 해당 세션의 복호화 재료를 선택합니다")

CX = 272          # 본류(세로 축)
RX = 700          # 우측 결과 박스 중심
RW = 320          # 우측 결과 박스 폭
BUS = RX + RW / 2 + 40   # 우회 세로선 — 결과 박스 오른쪽 바깥

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
    d.t(cx, y + 44, sub, 12, MUTED, KR)

def diamond(cx, y, hw, hh, txt):
    cy = y + hh
    d.o.append(f'<polygon points="{cx},{y} {cx + hw},{cy} {cx},{y + 2 * hh} {cx - hw},{cy}" '
               f'fill="{PAPER2}" stroke="{INK}" stroke-width="1.1"/>')
    d.t(cx, cy + 5, txt, 13, INK, KR, "middle", 600)

Y_S, Y_D1, Y_R1, Y_D2, Y_R2, Y_KEY, Y_END = 96, 160, 166, 300, 306, 452, 588

# ── 본류 ──
d.arrow([(CX, Y_S + 40), (CX, Y_D1 - 4)], MUTED, "ar", 1.4)
d.arrow([(CX, Y_D1 + 80), (CX, Y_D2 - 4)], MUTED, "ar", 1.4)
d.arrow([(CX, Y_D2 + 80), (CX, Y_KEY - 4)], MUTED, "ar", 1.4)
d.arrow([(CX, Y_KEY + 68), (CX, Y_END - 4)], MUTED, "ar", 1.4)

# ── 분기 1: TLS 1.3 인가? → 예: 정적 RSA 자체가 없음 (열리지 않음) ──
d.arrow([(CX + 152, Y_D1 + 40), (RX - RW / 2 - 6, Y_R1 + 34)], BAD, "bad", 1.4)
# ── 분기 2: 이름에 DHE·ECDHE 가 없나? → 없음: 개인키로 열림 ──
d.arrow([(CX + 152, Y_D2 + 40), (RX - RW / 2 - 6, Y_R2 + 34)], OK, "ok", 1.4)

# ── 우회선: 결과 박스를 관통하지 않도록 BUS(박스 오른쪽 바깥)로 돌린다 ──
# TLS 1.3 → 세션 키 로그 (열리지 않으므로 로그가 필요)
d.arrow([(RX + RW / 2, Y_R1 + 34), (BUS, Y_R1 + 34), (BUS, Y_KEY + 34),
         (CX + 176 + 6, Y_KEY + 34)], BAD, "bad", 1.4)
# ── 노드 ──
oval(CX, Y_S, 330, 40, "인증서 기반 TLS 캡처")
diamond(CX, Y_D1, 152, 40, "TLS 1.3 인가?")
step(RX, Y_R1, RW, 68, "장기 개인키로 복호화 불가", "suite에 키 교환 정보 없음", c=BAD)
diamond(CX, Y_D2, 152, 40, "TLS 1.2 RSA 키 교환?")
step(RX, Y_R2, RW, 68, "RSA 복호화 조건 확인", "키 일치 · 원래 전체 handshake", c=OK)
step(CX, Y_KEY, 352, 68, "해당 세션의 비밀값 로그",
     "클라이언트 또는 서버에서 제공", focal=True)
oval(CX, Y_END, 330, 40, "비밀값·캡처 일치 → 복호화", OK)

# ── 분기 라벨 ──
d.t(CX + 214, Y_D1 + 26, "예", 12, BAD, KR, "middle", 600)
d.t(CX + 16, Y_D1 + 100, "아니오", 12, MUTED, KR, "start", 600)
d.t(CX + 214, Y_D2 + 26, "예", 12, OK, KR, "middle", 600)
d.t(CX + 16, Y_D2 + 100, "아니오", 12, MUTED, KR, "start", 600)
d.t(RX, Y_R2 + 96, "조건 충족 → RSA Keys에 등록", 12, OK, KR)

d.legend(H - 60, [("실무에서 실제로 쓰는 경로", ACC), ("RSA 조건부 경로", OK), ("장기 개인키 불가", BAD)])
d.save("04-02.decrypt-path.svg")

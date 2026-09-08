# 02-01 §6 — 소켓 안에 무엇이 있나. TCP 연결 소켓은 상대의 상태를 담고, UDP 소켓은 비어 있다.
# 노트의 읽기: 2026-09-08 Phase 1 되묻기 — "이게 소켓에 있어야 돌아가는 건지 흐름이 안 그려진다".
#       원문 §2.6.2 는 환영 소켓·연결 소켓의 이름만 대고 연결 소켓이 무엇을 담는지는 적지 않는다.
#       연결 상태 변수(순서 번호·확인 번호·rwnd·재전송 타이머)는 03-03·03-04 가 다룬다.
#   accept(2): "creates a new connected socket" · recvfrom(2): "that source address is placed in the
#       buffer pointed to by src_addr" — UDP 는 상대 주소가 소켓이 아니라 패킷에 실려 온다.
# 타입 스펙: type-uml-class — 클래스가 무엇을 소유하고(속성 칸) 무엇을 하는지(연산 칸)를 합성·의존·연관의
#       어휘로 잇는다. 같은 절의 tcp-two-sockets 는 swimlane(순서), §5 의 udp-socket-sequence 는
#       sequence 라 타입이 겹치지 않는다. 두 패널(TCP · UDP)을 나란히 두고 강조는 연결 소켓 하나.
#       축약: 스펙은 관계 어휘 여섯을 범례에 다 보이라 하므로 색 범례 위에 표식 여섯 줄을 따로 그렸다.
#       멤버 글자는 스펙의 9px 대신 스타일 계약의 한글 하한 12px 를 쓴다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 700
d = D(W, H, "COMPUTER NETWORKING TOP-DOWN · 02-01 §6",
      "소켓 안에 무엇이 있나",
      "TCP 서버는 환영 소켓 하나와 연결마다 하나씩의 연결 소켓을 갖고, 연결 소켓이 상대 주소·다음 순번·윈도우·재전송 "
      "타이머를 담는다. UDP 소켓은 담는 상태가 없어 하나로 다 받고 상대 주소는 패킷마다 실려 온다.",
      "상태가 상대마다 다르니 소켓도 상대마다 하나입니다")

# 관계 어휘 표식 — 스펙의 여섯 가지
d.o.append(
    '<defs>'
    f'<marker id="tri" viewBox="0 0 12 12" refX="11" refY="6" markerWidth="10" markerHeight="10" orient="auto">'
    f'<path d="M0 0 L12 6 L0 12 z" fill="{PAPER}" stroke="{INK}" stroke-width="1"/></marker>'
    f'<marker id="diaf" viewBox="0 0 12 12" refX="1" refY="6" markerWidth="10" markerHeight="10" orient="auto-start-reverse">'
    f'<path d="M0 6 L6 0 L12 6 L6 12 z" fill="{INK}"/></marker>'
    f'<marker id="diah" viewBox="0 0 12 12" refX="1" refY="6" markerWidth="10" markerHeight="10" orient="auto-start-reverse">'
    f'<path d="M0 6 L6 0 L12 6 L6 12 z" fill="{PAPER}" stroke="{INK}" stroke-width="1"/></marker>'
    f'<marker id="open" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="8" markerHeight="8" orient="auto">'
    f'<polyline points="0 0, 8 4, 0 8" fill="none" stroke="{MUTED}" stroke-width="1.2"/></marker>'
    '</defs>')

def rel(dpath, c=MUTED, start=None, end=None, dash=None):
    ms = f' marker-start="url(#{start})"' if start else ""
    me = f' marker-end="url(#{end})"' if end else ""
    ds = f' stroke-dasharray="{dash}"' if dash else ""
    d.o.append(f'<path d="{dpath}" fill="none" stroke="{c}" stroke-width="1.4"{ms}{me}{ds}/>')

def masked(x, y, txt, c=MUTED, size=12, fam=KR, anchor="middle"):
    w = sum(size if "가" <= ch <= "힣" else size * 0.62 for ch in txt) + 12
    x0 = x - w / 2 if anchor == "middle" else (x if anchor == "start" else x - w)
    d.box(x0, y - size, w, size + 6, PAPER, "none", 0, 2)
    d.t(x, y, txt, size, c, fam, anchor)

def klass(x, y, w, name, attrs, ops, c, focal=False, ghost=False):
    hn, ha, ho = 32, (8 + 20 * len(attrs)) if attrs else 0, (8 + 20 * len(ops)) if ops else 0
    h = hn + ha + ho
    if ghost:
        for o in (16, 8):
            d.box(x + o, y + o, w, h, PAPER, c, 0.8, 6)
    if focal:
        d.tone(x, y, w, h, c, 6, "14", 1.4)
    else:
        d.box(x, y, w, h, PAPER2, c, 1.0, 6)
    d.t(x + w / 2, y + 21, name, 13, c if focal else INK, KR, "middle", 600)
    yy = y + hn
    if attrs:
        d.line(x, yy, x + w, yy, RULE, 0.8)
        for i, (txt, col) in enumerate(attrs):
            d.t(x + 12, yy + 22 + i * 20, txt, 12, col, KR, "start")
        yy += ha
    if ops:
        d.line(x, yy, x + w, yy, RULE, 0.8)
        for i, txt in enumerate(ops):
            d.t(x + 12, yy + 22 + i * 20, txt, 12, INK, MONO if all(ord(ch) < 0x3000 for ch in txt) else KR, "start")
    return y + h

# ── 패널 ───────────────────────────────────────────────────────
for x, w, name, sub in ((24, 480, "TCP 서버", "상대마다 소켓 하나"), (520, 456, "UDP 서버", "소켓 하나가 다 받는다")):
    d.box(x, 104, w, 432, "rgba(245,245,245,0.02)", RULE, 1.0, 8)
    d.t(x + 20, 130, name, 15, INK, MONO, "start", 600)
    d.t(x + 110, 130, sub, 12, MUTED, KR, "start")

# ── TCP: 프로세스 ◆─ 환영 소켓 [1] · ◆─ 연결 소켓 [0..*] · 환영 ┈> 연결 ──
rel("M 214 212 L 214 244 L 134 244 L 134 272", MUTED, start="diaf")
rel("M 314 212 L 314 244 L 384 244 L 384 272", MUTED, start="diaf")
rel("M 134 380 L 134 452 L 384 452 L 384 436", MUTED, end="open", dash="4 3")
klass(164, 152, 200, "서버 프로세스", [], ["listen() · accept()"], MUTED)
klass(40, 272, 188, "환영 소켓", [("로컬 포트 80", INK), ("상대 주소 — 비어 있음", SOFT)], ["accept()"], MUTED)
klass(288, 272, 192, "연결 소켓", [("상대 주소 IP:포트", INK), ("다음 순번 seq · ack", INK), ("윈도우 크기 rwnd", INK), ("재전송 타이머 RTO", INK)],
      ["recv() · send()"], ACC, focal=True, ghost=True)
masked(146, 264, "1", MUTED, 12, MONO, "start")
masked(396, 264, "0..*", MUTED, 12, MONO, "start")
masked(259, 476, "accept() 가 연결마다 하나씩 만든다", MUTED)

# ── UDP: 프로세스 ◆─ UDP 소켓 [1] · UDP 소켓 ─> 데이터그램 [0..*] ────────
rel("M 748 212 L 748 244 L 630 244 L 630 272", MUTED, start="diaf")
rel("M 630 380 L 630 452 L 866 452 L 866 388", MUTED, end="open")
klass(648, 152, 200, "서버 프로세스", [], ["recvfrom() · sendto()"], MUTED)
klass(536, 272, 188, "UDP 소켓", [("로컬 포트 12000", INK), ("상대 상태 — 없음", SOFT)], ["recvfrom() · sendto()"], MUTED)
klass(776, 272, 180, "데이터그램", [("출발지 IP", INK), ("출발지 포트", INK), ("데이터", INK)], [], INFO, ghost=True)
masked(642, 264, "1", MUTED, 12, MONO, "start")
masked(642, 404, "1", MUTED, 12, MONO, "start")
masked(878, 412, "0..*", MUTED, 12, MONO, "start")
masked(748, 476, "recvfrom() 이 꼬리표째 꺼낸다", MUTED)

d.t(24, 568, "TCP: 상태가 상대마다 다르니 소켓도 상대마다 하나입니다. 신뢰성·순서·혼잡 제어가 전부 이 상태 위에서 돕니다.",
    12, MUTED, KR, "start")
d.t(24, 592, "UDP: 담는 상태가 없어 소켓 하나로 다 받고, 상대 주소는 패킷마다 실려 옵니다. recvfrom() 이 주소를 함께 돌려주는 이유입니다.",
    12, MUTED, KR, "start")

# 관계 어휘 범례 여섯 (스펙 요구) — 사용한 셋은 합성·연관·의존
LY = 624
for i, (lab, start, end, dash) in enumerate((("상속", None, "tri", None), ("실현", None, "tri", "5 4"), ("합성", "diaf", None, None),
                                            ("집합", "diah", None, None), ("연관", None, "open", None), ("의존", None, "open", "4 3"))):
    x = 24 + i * 160
    rel(f"M {x} {LY} L {x + 40} {LY}", MUTED, start=start, end=end, dash=dash)
    d.t(x + 52, LY + 4, lab, 12, SOFT, KR, "start")

d.legend(H - 44, [("상태를 담는 소켓", ACC), ("상태가 없는 소켓", MUTED), ("꼬리표를 단 패킷", INFO)])
d.save("02-01.socket-state.svg")
print("ok 02-01.socket-state")

# 13-04 학습 목표 뒤 전체 지도 — SYN 이 도착해 애플리케이션이 연결을 받기까지의 단계와, 각 단계에 걸린 절(§1–§3).
# 사실 출처: 원서 §13.7.1–13.7.4(대기 소켓 대조 · 두 큐 · accept), §13.8(SYN flood · SYN cookie · 위조 RST · 가짜 PTB).
# 타입 스펙: type-process — 칸마다 같은 의미 슬롯(절 번호 · 단계 이름 · 그 단계의 일)이 반복되고 화살표가 SYN 의 진행을 나른다.
#           축약: 주체(lane)가 없는 단계 지도라 §1 lanes 와 §2 공식을 쓰지 않고 카드 한 줄 stride 로 놓는다
#           (visual-diagram-selection §알려진 공백 "주체 없는 단계 지도" 관례, 13-01 chapter-overview 와 같은 선택).
#           아래 줄은 단계에서 갈라지는 결과(거절)와 단계를 겨냥하는 공격이다. focal 은 커널과 애플리케이션의 경계인 accept() 한 칸.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, BAD, WARN, PAPER2, RULE, KR, MONO

W, H = 920, 456
d = D(W, H, "TCP/IP ILLUSTRATED VOL.1 · 13-04",
      "SYN 도착부터 accept 까지 — 이 편의 지도",
      "위 줄은 SYN 하나가 서버에서 지나는 단계다. 대기 소켓이 목적지 주소와 포트를 대조하고(§1), 커널 TCP 가 SYN_RCVD 큐와 수락 큐에 연결을 쌓은 뒤(§2), "
      "애플리케이션이 accept() 로 받아 연결별 소켓으로 데이터를 주고받는다. 아래 줄은 주소가 맞지 않을 때의 RST 거절(§1)과, "
      "수립 전 상태를 노리는 SYN flood·열린 연결을 노리는 위조 입력(§3)이 어느 단계에 걸리는지 보인다.",
      "accept() 앞쪽은 전부 커널 TCP 가 처리합니다")

CW, CH, GAP, X0, Y = 152, 88, 24, 32, 140
XS = [X0 + i * (CW + GAP) for i in range(5)]
STAGES = [
    ("§1", "대기 소켓", "로컬 주소·포트 대조"),
    ("§2", "SYN_RCVD 큐", "마지막 ACK 대기"),
    ("§2", "수락 큐", "handshake 완료"),
    ("§2", "accept()", "애플리케이션이 받음"),
    ("§1·§3", "연결별 소켓", "4-tuple 별 데이터"),
]
FOCAL = 3

# 위 묶음 괄호 — 커널 TCP / 애플리케이션
def bracket(x0, x1, label, c):
    d.path(f"M {x0} {Y - 12} V {Y - 20} H {x1} V {Y - 12}", c, 1.2)
    d.t((x0 + x1) / 2, Y - 28, label, 12, c, KR, "middle", 600)
bracket(XS[0], XS[2] + CW, "커널 TCP · accept 전", SOFT)
bracket(XS[3], XS[4] + CW, "애플리케이션", SOFT)

# 단계 사이 화살표 먼저
for i in range(4):
    d.arrow([(XS[i] + CW + 2, Y + CH / 2), (XS[i + 1] - 4, Y + CH / 2)], MUTED, "ar", 1.4)

for i, (n, title, sub) in enumerate(STAGES):
    x = XS[i]
    if i == FOCAL:
        d.o.append(f'<rect x="{x}" y="{Y}" width="{CW}" height="{CH}" rx="8" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, Y, CW, CH, PAPER2, RULE, 1.0, 8)
    d.t(x + 16, Y + 24, n, 12, ACC if i == FOCAL else SOFT, MONO, "start", 600)
    d.t(x + 16, Y + 50, title, 15, ACC if i == FOCAL else INK, KR if any("가" <= c <= "힣" for c in title) else MONO, "start", 600)
    d.t(x + 16, Y + 72, sub, 12, MUTED, KR, "start")

# 아래 줄 — 갈라지는 결과와 공격
BY, BW, BH = 300, 160, 64
BRANCH = [
    (0, "§1 · 주소 불일치", "RST 로 거절", BAD, "down"),
    (1, "§3 · SYN flood", "SYN cookie 로 대응", WARN, "up"),
    (4, "§3 · 위조 RST · PTB", "열린 연결 교란", WARN, "up"),
]
for i, head, sub, c, way in BRANCH:
    cx = XS[i] + CW / 2
    bx = min(max(cx - BW / 2, 24), W - 24 - BW)
    if way == "down":
        d.arrow([(cx, Y + CH + 4), (cx, BY - 6)], c, "bad", 1.4)
    else:
        d.arrow([(cx, BY - 4), (cx, Y + CH + 6)], c, "warn", 1.4)
    d.tone(bx, BY, BW, BH, c, 6, "14", 1.1)
    d.t(bx + 14, BY + 26, head, 12, c, KR, "start", 600)
    d.t(bx + 14, BY + 48, sub, 12, MUTED, KR, "start")

d.legend(H - 56, [("커널과 애플리케이션의 경계", ACC), ("거절", BAD), ("공격 지점", WARN)])
d.save("13-04.chapter-overview.svg")

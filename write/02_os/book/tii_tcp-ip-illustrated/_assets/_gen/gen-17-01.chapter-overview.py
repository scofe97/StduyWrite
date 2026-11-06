# 17-01 학습 목표 뒤 전체 지도 — 유휴 연결에서 keepalive 탐침이 판정으로 이어지는 단계와, 각 단계에 걸린 소절(1–4).
# 사실 출처: 원서 §17.1–17.2(유휴 연결 · keepalive 시간/간격/횟수 · 탐침 세그먼트 · 상대 상태 네 가지), §17.3(위조 · 타이머 기반 관찰).
#   NAT 유휴 만료는 §17.1 의 ssh 예시, ETIMEDOUT 은 이 편의 OrbStack 실측과 tcp_timer.c 의 tcp_write_err().
# 타입 스펙: type-process — 칸마다 같은 의미 슬롯(소절 번호 · 단계 이름 · 그 단계의 일)이 반복되고 화살표가 한 연결의 진행을 나른다.
#           축약: 주체(lane)가 없는 단계 지도라 §1 lanes 와 §2 공식을 쓰지 않고 카드 한 줄 stride 로 놓는다
#           (13-04 chapter-overview 와 같은 선택). 아래 줄은 단계를 겨냥하는 위험이다. focal 은 판정이 갈리는 응답 한 칸.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, BAD, WARN, PAPER2, RULE, KR, MONO

def _kr(t): return KR if any("가" <= c <= "힣" for c in str(t)) else MONO

W, H = 920, 456
d = D(W, H, "TCP/IP ILLUSTRATED VOL.1 · 17-01",
      "유휴 연결에서 응답 판정까지 — 이 편의 지도",
      "위 줄은 데이터가 없는 연결 하나에서 keepalive 가 지나는 단계다. 아무것도 오가지 않는 연결(1)에 타이머가 만료되면 커널이 탐침을 보내고(2), "
      "돌아온 응답이 연결을 살릴지 끊을지 가른다(3). 아래 줄은 각 단계를 겨냥하는 위험이다. "
      "중간 장비의 상태 만료는 유휴 연결에(1), 탐침 간격 관찰은 탐침에(4), 위조 ACK 는 응답 판정에(4) 걸린다.",
      "응답이 없는 이유는 TCP 가 구별하지 못합니다")

CW, CH, GAP, X0, Y = 152, 88, 24, 32, 140
XS = [X0 + i * (CW + GAP) for i in range(5)]
STAGES = [
    ("1", "유휴 연결", "데이터 0 · 상태만 유지"),
    ("2", "keepalive 타이머", "유휴 시간 만료"),
    ("2", "탐침", "seq = SND.UNA − 1"),
    ("3", "응답 판정", "ACK · RST · 무응답"),
    ("3", "종료와 오류", "RST 송수신 · errno"),
]
FOCAL = 3

def bracket(x0, x1, label, c):
    d.path(f"M {x0} {Y - 12} V {Y - 20} H {x1} V {Y - 12}", c, 1.2)
    d.t((x0 + x1) / 2, Y - 28, label, 12, c, KR, "middle", 600)
bracket(XS[0], XS[1] + CW, "아무것도 오가지 않는 구간", SOFT)
bracket(XS[2], XS[4] + CW, "SO_KEEPALIVE 를 켠 쪽의 커널", SOFT)

for i in range(4):
    d.arrow([(XS[i] + CW + 2, Y + CH / 2), (XS[i + 1] - 4, Y + CH / 2)], MUTED, "ar", 1.4)

for i, (n, title, sub) in enumerate(STAGES):
    x = XS[i]
    if i == FOCAL:
        d.o.append(f'<rect x="{x}" y="{Y}" width="{CW}" height="{CH}" rx="8" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, Y, CW, CH, PAPER2, RULE, 1.0, 8)
    d.t(x + 16, Y + 24, n, 12, ACC if i == FOCAL else SOFT, MONO, "start", 600)
    d.t(x + 16, Y + 50, title, 15, ACC if i == FOCAL else INK, _kr(title), "start", 600)
    d.t(x + 16, Y + 72, sub, 12, MUTED, _kr(sub), "start")

BY, BW, BH = 300, 160, 64
BRANCH = [
    (0, "1 · 중간 장비 만료", "NAT 가 상태를 지움", WARN, "up"),
    (2, "4 · 간격 관찰", "설정값 추정", WARN, "up"),
    (3, "4 · 위조 ACK", "자원을 계속 붙잡음", WARN, "up"),
]
for i, head, sub, c, way in BRANCH:
    cx = XS[i] + CW / 2
    bx = min(max(cx - BW / 2, 24), W - 24 - BW)
    d.arrow([(cx, BY - 4), (cx, Y + CH + 6)], c, "warn", 1.4)
    d.tone(bx, BY, BW, BH, c, 6, "14", 1.1)
    d.t(bx + 14, BY + 26, head, 12, c, KR, "start", 600)
    d.t(bx + 14, BY + 48, sub, 12, MUTED, KR, "start")

d.legend(H - 56, [("판정이 갈리는 칸", ACC), ("위험", WARN)])
d.save("17-01.chapter-overview.svg")

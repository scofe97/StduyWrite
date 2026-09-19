# 2026-09-14 A(몇몇 사용자) 문항 · 원인 분석 — 줄이라는 알림이 연결을 가진 서버가 아닌 곳에 떨어진다.
# 무대(ecmp-topology)의 노드를 그대로 쓰되 인터넷을 접고 서버 셋을 라우터 아래로 펼쳤다.
# 번호 화살표 여섯이 사건 순서다. 학습자는 "목적지 IP 가 같으니 서버 2 로 가지 않나"에서 멈췄으므로
# 4 번 화살표 하나에 focal 을 건다 — 같은 목적지인데 출발지와 포트 칸이 달라 다른 서버로 간다.
# 타입 스펙: type-architecture — 실제 노드 그래프 위에 번호를 단 연결선. type-sequence 는
#           흐름을 노드 그래프 위의 번호 화살표로 보인다는 규칙에 따라 기각했다.
#           레인 시퀀스로 그리면 알림이 어느 서버로 갈라지는지가 레인 이름으로만 남는다.
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dd import D, ACC, WARN, BAD, INFO, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 540
d = D(W, H, "TROUBLESHOOTING DRILL · 2026-09-14 A",
      "알림이 연결 없는 서버에 떨어집니다",
      "서버 2 가 보낸 큰 패킷이 좁은 구간 앞에서 버려지고, 그 라우터가 서비스 주소로 Packet Too Big 을 돌려보낸다. "
      "데이터센터 라우터는 포트가 없는 이 알림을 주소 둘로만 해시해 서버 1 로 보내고, 서버 1 은 맞는 연결이 없어 버린다. "
      "서버 2 는 끝내 모르고 같은 크기로 다시 보낸다.",
      lead="알림에는 포트 칸이 없어 라우터가 주소 둘로만 해시하고, 연결을 가진 서버 2 는 줄이라는 말을 못 듣습니다")

def num(cx, cy, n, c):
    d.box(cx - 12, cy - 12, 24, 24, PAPER, c, 1.3, 12)
    d.t(cx, cy + 5, str(n), 12, c, MONO, "middle", 600)

# ── 윗줄: 사용자 · 경로 중간 라우터 · 데이터센터 라우터 ────────────────
BY, BH = 132, 88
L1, L3, L2 = 156, 176, 196          # 레인 — 1 흐름 → · 3 알림 → · 2 큰 패킷 ←

# 화살표를 먼저 그려 칩과 상자가 위에 앉게 한다
d.arrow([(152, L1), (278, L1)], INFO, "info", 1.6)
d.arrow([(440, L1), (566, L1)], INFO, "info", 1.6)
d.arrow([(440, L3), (566, L3)], WARN, "warn", 1.6)
d.arrow([(568, L2), (442, L2)], MUTED, "ar", 1.6)

# 좁은 구간 앞에서 버려진다
XC = 260
d.line(XC - 8, L2 - 8, XC + 8, L2 + 8, BAD, 2.0)
d.line(XC - 8, L2 + 8, XC + 8, L2 - 8, BAD, 2.0)
d.line(152, 240, 280, 240, WARN, 1.6)
d.t(216, 260, "MTU 작은 구간", 12, WARN, KR, "middle")

# ── 아래줄: 서버 셋 ─────────────────────────────────────────────
SY, SW, SH = 344, 136, 80
S_CX = [512, 664, 816]
d.arrow([(640, BY + BH), (640, SY - 2)], INFO, "info", 1.6)                        # 1 → 서버 2
d.arrow([(676, SY), (676, BY + BH + 2)], MUTED, "ar", 1.6)                         # 2 · 6 서버 2 에서 나감
d.arrow([(596, BY + BH), (596, 284), (512, 284), (512, SY - 2)], ACC, "acc", 1.8)  # 4 → 서버 1
d.path(f"M 712 {BY + BH} L 712 300 L 816 300 L 816 {SY}", RULE, 1.2)            # 서버 3 은 연결만

d.box(24, BY, 128, BH, PAPER2, RULE, 1.0, 6)
d.t(88, BY + 38, "사용자", 14, INK, KR, "middle", 600)
d.t(88, BY + 60, "터널 뒤", 12, SOFT, KR, "middle")

d.box(280, BY, 160, BH, PAPER2, RULE, 1.0, 6)
d.t(360, BY + 38, "경로 중간 라우터", 13, INK, KR, "middle", 600)
d.t(360, BY + 60, "다음 링크 MTU 작음", 12, WARN, KR, "middle")

d.box(568, BY, 160, BH, PAPER2, RULE, 1.0, 6)
d.t(648, BY + 38, "데이터센터 라우터", 13, INK, KR, "middle", 600)
d.t(648, BY + 60, "ECMP", 12, MUTED, MONO, "middle", 600)

def server(i, sub, c, tone=None):
    x = S_CX[i] - SW // 2
    if tone:
        d.tone(x, SY, SW, SH, tone, 6)
    else:
        d.box(x, SY, SW, SH, PAPER2, RULE, 1.0, 6)
    d.t(S_CX[i], SY + 34, f"서버 {i + 1}", 13, INK, KR, "middle", 600)
    d.t(S_CX[i], SY + 56, sub, 12, c, KR, "middle")

server(0, "연결 없음", BAD, BAD)
server(1, "연결 있음", INFO, INFO)
server(2, "연결 없음", SOFT)

num(216, L1, 1, INFO)
num(492, L3, 3, WARN)
num(524, L2, 2, MUTED)
num(552, 284, 4, ACC)
num(512, 448, 5, BAD)
num(664, 448, 6, MUTED)

# ── 순서 목록 — 칩 번호와 같은 색 ─────────────────────────────────
STEPS = [
    (1, INFO, "TCP 흐름 · 네 값 해시 · 서버 2"),
    (2, MUTED, "큰 패킷 · 좁은 구간 앞에서 버려짐"),
    (3, WARN, "Packet Too Big · 서비스 주소로"),
    (4, ACC, "같은 알림 · 주소 둘만 해시 · 서버 1"),
    (5, BAD, "서버 1 · 맞는 연결 없음 · 알림 버림"),
    (6, MUTED, "서버 2 · 같은 크기로 재전송"),
]
for i, (n, c, lab) in enumerate(STEPS):
    y = 308 + i * 28
    num(40, y, n, c)
    d.t(64, y + 5, lab, 13, INK if n == 4 else MUTED, KR, "start", 600 if n == 4 else 400)

d.legend(484, [("TCP 흐름", INFO), ("Packet Too Big", WARN), ("잘못 간 알림", ACC), ("버려짐", BAD)])

d.save(os.path.join(os.path.dirname(__file__), "..", "2026-09-14.ptb-misdelivery.svg"))
print("ok")

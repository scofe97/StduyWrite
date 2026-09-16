# 03-04 §3 — 같은 가짜 SYN 아래 두 경로를 나란히 놓고, 자원을 잡는 시점 하나가 갈림길임을 보인다.
# 2026-09-16: 정상 핸드셰이크와 쿠키 경로를 두 갈래로만 보이던 도식을 다시 그렸다.
#       「3 단계가 어디서 미완성인지」와 「플러드가 자원을 어떻게 갉는지」가 안 보인다는 지적에서 나왔다.
# 본문 §3 에 적힌 사실만 담는다 —
#   공격이 통하는 이유: 서버는 SYN 을 받으면 연결 변수와 버퍼를 할당하고 SYN,ACK 를 보낸 뒤 ACK 를
#       기다린다. 세 번째 단계가 완성되지 않으면 종종 1 분 이상 지나서야 반쯤 열린 연결을 정리한다.
#       그 사이 연결 자원이 고갈되고 정상 클라이언트는 서비스를 못 받는다.
#   SYN 쿠키: SYN 을 받아도 반쯤 열린 연결을 만들지 않고, 출발지·목적지 IP 와 포트 번호 그리고 서버만
#       아는 비밀 수로 해시를 계산해 초기 순서 번호로 삼는다. 쿠키도 그 밖의 어떤 상태도 기억하지 않는다.
#       ACK 가 오면 같은 해시를 다시 계산해 검산하고, 그때 비로소 연결과 소켓을 만든다.
#       ACK 가 오지 않으면 원래의 가짜 SYN 은 아무 해도 끼치지 않는다 — 할당한 적이 없기 때문이다.
# 타입 스펙: type-sequence — 참여자 레인 + 시간축. 세 가지를 스펙 문법 위에 얹었다.
#       (1) 오지 않은 3 단계는 마커 없는 성긴 파선을 가운데서 끊고 X 로 막아 「화살표의 부재」를 그린다.
#       (2) 대량 공격은 같은 메시지를 세 줄로 겹쳐 그려 되풀이를 도형 개수로 보인다.
#       (3) 서버의 연결 자리는 시간축 밖의 확대 컷이라 레인 사이에 칸 다섯으로 세운다.
#       focal 은 쿠키를 계산하는 자리 하나.
#       축약: 스펙은 레인 다섯까지 허용하지만 두 서버를 한 줄에 세우면 메시지 라벨이 남의 레인 위에
#       앉는다(스펙 안티패턴). 그래서 레인 셋짜리 컷을 위아래로 쌓고 공격자와 정상 클라이언트를 양쪽
#       끝에 고정해, 모든 메시지가 이웃 레인 사이에서만 오가게 했다.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, INK, OK, WARN, BAD, PAPER, PAPER2, RULE, KR, MONO


def _kr(t):
    return KR if any("가" <= c <= "힣" for c in str(t)) else MONO


class SeqKR(Seq):
    """Seq 가 한글 라벨을 mono 로 찍는 자리를 한글 스택으로 가른다(계약 §프리미티브가 한글을 mono 로)."""

    def lanes(s, names, y0=104, lane_w=210):
        s.LX = {}; n = len(names)
        span = (s.w - 48 - 24) - lane_w
        for i, (nm, sub) in enumerate(names):
            x = 24 + lane_w / 2 + (span * i / (n - 1) if n > 1 else 0)
            s.LX[nm] = x
            s.box(x - lane_w / 2, y0, lane_w, 44, PAPER2, RULE, 1.0)
            s.t(x, y0 + 19, nm, 14, INK, _kr(nm), "middle", 600)
            s.t(x, y0 + 37, sub, 13, MUTED, _kr(sub))
        s.lane_top = y0 + 44
        return s.LX

    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]; dr = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dr} {y} L {x2 - 12 * dr} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 10, label, 14, c, _kr(label), "middle", 600)
        if sub:
            s.t(mx, y + 19, sub, 13, MUTED, _kr(sub))

    def burst(s, a, b, label, y, c, mk="ar", n=3, gap=12, sub=None):
        """같은 메시지를 n 줄로 겹쳐 그린다 — 되풀이를 라벨이 아니라 도형 개수로 보인다."""
        x1, x2 = s.LX[a], s.LX[b]; dr = 1 if x2 > x1 else -1
        half = (n - 1) / 2 * gap
        for k in range(n):
            yy = y + (k - (n - 1) / 2) * gap
            s.path(f"M {x1 + 10 * dr} {yy} L {x2 - 12 * dr} {yy}", c, 1.5, m=mk)
        mx = (x1 + x2) / 2
        s.t(mx, y - half - 12, label, 14, c, _kr(label), "middle", 600)
        if sub:
            s.t(mx, y + half + 21, sub, 13, MUTED, _kr(sub))

    def absent(s, a, b, label, y, c, sub=None):
        """오지 않은 세그먼트. 마커를 달지 않고 가운데를 끊어 X 로 막는다 — 화살표의 부재가 논지다."""
        x1, x2 = s.LX[a], s.LX[b]; dr = 1 if x2 > x1 else -1
        mx = (x1 + x2) / 2
        s.path(f"M {x1 + 10 * dr} {y} L {mx - 16 * dr} {y}", c, 1.3, dash="3 7")
        s.path(f"M {mx + 16 * dr} {y} L {x2 - 12 * dr} {y}", c, 1.3, dash="3 7")
        s.line(mx - 9, y - 9, mx + 9, y + 9, c, 2.0)
        s.line(mx - 9, y + 9, mx + 9, y - 9, c, 2.0)
        s.t(mx, y - 22, label, 14, c, _kr(label), "middle", 600)
        if sub:
            s.t(mx, y + 26, sub, 13, MUTED, _kr(sub))

    def state(s, a, txt, y, c):
        """레인 위의 상태 칩. 파선 레일이 글자를 관통하지 않게 배경을 먼저 깐다."""
        x = s.LX[a]
        w = sum(13.0 if "가" <= ch <= "힣" else 7.6 for ch in str(txt)) + 26
        s.o.append(f'<rect x="{x - w / 2}" y="{y - 13}" width="{w}" height="26" rx="4" fill="{PAPER}"/>')
        s.o.append(f'<rect x="{x - w / 2}" y="{y - 13}" width="{w}" height="26" rx="4" '
                   f'fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
        s.t(x, y + 5, txt, 13, c, _kr(txt))

    def railtext(s, x, y, txt, size, c):
        """레인 위에 앉는 주석. 파선 레일이 글자를 관통하지 않게 배경을 먼저 깐다."""
        w = sum(size if "가" <= ch <= "힣" else size * 0.62 for ch in str(txt)) + 16
        s.o.append(f'<rect x="{x - w / 2}" y="{y - size}" width="{w}" height="{size + 8}" fill="{PAPER}"/>')
        s.t(x, y, txt, size, c, _kr(txt))


W, H = 1000, 1172
d = SeqKR(W, H, "COMPUTER NETWORKING TOP-DOWN · 03-04 §3",
          "자원을 언제 잡느냐 하나가 갈림길입니다",
          "위 컷은 기본 서버다. SYN 마다 연결 변수와 버퍼를 할당하고 SYNACK 를 보낸 뒤 ACK 를 "
          "기다리는데, 공격자는 세 번째 단계를 완성하지 않는다. 반쯤 열린 연결이 1 분 이상 남아 "
          "연결 자리를 채우고 정상 클라이언트는 서비스를 못 받는다. 아래 컷은 같은 공격 입력을 받는 "
          "SYN 쿠키 서버다. SYN 에는 아무것도 할당하지 않고 출발지·목적지 IP 와 포트, 서버만 아는 "
          "비밀 수로 해시를 계산해 초기 순서 번호로 실어 보낸다. ACK 가 오면 같은 해시를 다시 계산해 "
          "검산한 뒤에야 소켓을 만들고, ACK 가 오지 않으면 쓴 자원이 없다.",
          "공격 입력은 두 컷이 같습니다 — 다른 것은 서버가 자원을 잡는 시점 하나입니다")

LANE_W = 236
ATK, CLI = "공격자", "정상 클라이언트"

# ── 위 컷: 기본 서버 — SYN 을 받자마자 잡는다 ────────────────────────
d.t(24, 100, "기본 · SYN 을 받자마자 자원을 잡는 경로", 14, INK, KR, "start", 600)
d.lanes([(ATK, "가짜 SYN 대량"), ("서버 — 기본", "SYN 마다 할당"), (CLI, "connect()")],
        y0=112, lane_w=LANE_W)
d.rails(578)
SX = d.LX["서버 — 기본"]

d.burst(ATK, "서버 — 기본", "가짜 SYN", 212, BAD, "bad", sub="출발지를 속인 연결 요청이 대량으로")
d.state("서버 — 기본", "SYN 마다 연결 변수 + 버퍼 할당", 278, WARN)
d.msg("서버 — 기본", ATK, "SYNACK", 324, MUTED, "ar", dash="5 4", sub="서버가 ACK 를 기다림")
d.absent(ATK, "서버 — 기본", "ACK 안 옴 · 3 단계 미완성", 386, BAD)
d.state("서버 — 기본", "반쯤 열린 연결", 386, BAD)

# 연결 자리 — 가짜 SYN 이 하나씩 차지하는 모습을 칸으로 센다(시간축 밖의 확대 컷)
SLOT_W, SLOT_G, SLOT_N = 80, 8, 5
SLOT_X0 = SX - (SLOT_N * SLOT_W + (SLOT_N - 1) * SLOT_G) / 2
d.railtext(SX, 428, "서버의 연결 자리 · 가짜 SYN 이 하나씩 차지", 13, MUTED)
for i in range(SLOT_N):
    x = SLOT_X0 + i * (SLOT_W + SLOT_G)
    d.box(x, 436, SLOT_W, 30, PAPER, "none", 0, 4)
    d.tone(x, 436, SLOT_W, 30, BAD, 4, "14", 1.1)
    d.t(x + SLOT_W / 2, 456, "반쯤 열림", 12, BAD, KR)
d.railtext(SX, 490, "1 분 이상 지나서야 정리 · 그동안 자리가 안 비워짐", 13, MUTED)

d.absent(CLI, "서버 — 기본", "SYN", 534, WARN, sub="자리가 없어 서비스를 못 받음")

d.line(24, 600, W - 24, 600, RULE, 1.0)

# ── 아래 컷: SYN 쿠키 서버 — 검산한 뒤에야 잡는다 ────────────────────
d.t(24, 632, "SYN 쿠키 · 검산한 뒤에야 자원을 잡는 경로", 14, INK, KR, "start", 600)
d.lanes([(ATK, "같은 가짜 SYN"), ("서버 — SYN 쿠키", "SYN 에는 할당 없음"), (CLI, "connect()")],
        y0=644, lane_w=LANE_W)
d.rails(1092)
KX = d.LX["서버 — SYN 쿠키"]

d.burst(ATK, "서버 — SYN 쿠키", "가짜 SYN", 744, BAD, "bad", sub="위 컷과 똑같은 공격 입력")
d.state("서버 — SYN 쿠키", "반쯤 열린 연결을 안 만듦 · 할당 0", 810, ACC)
d.railtext(KX, 840, "isn = hash(출발지·목적지 IP·포트, 서버 비밀 수)", 13, ACC)
d.msg("서버 — SYN 쿠키", ATK, "SYNACK · seq = 쿠키", 886, MUTED, "ar", dash="5 4",
      sub="쿠키도 그 밖의 어떤 상태도 기억 안 함")
d.absent(ATK, "서버 — SYN 쿠키", "ACK 안 옴 · 쓴 자원 0", 948, OK)
d.state("서버 — SYN 쿠키", "아무 해도 없음", 948, OK)

d.msg(CLI, "서버 — SYN 쿠키", "ACK · ack = 쿠키 + 1", 996, OK, "ok", sub="정상 클라이언트가 보내옴")
d.state("서버 — SYN 쿠키", "같은 해시를 다시 계산해 검산", 1048, OK)
d.railtext(KX, 1078, "값이 맞으면 그때 비로소 연결과 소켓 생성", 13, MUTED)

d.legend(1108, [("가짜 SYN · 반쯤 열린 연결", BAD), ("자원을 잡는 자리 · 거부", WARN),
                ("검산 · 쓴 자원 0", OK), ("쿠키를 계산하는 자리", ACC)])
d.save("03-04.syn-cookie.svg")
print("ok 03-04.syn-cookie")

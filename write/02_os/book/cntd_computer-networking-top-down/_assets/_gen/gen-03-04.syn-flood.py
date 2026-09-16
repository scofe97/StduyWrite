# 03-04 §3 「공격이 통하는 이유」 — 세 번째 단계가 오지 않는 SYN 이 자리를 채우는 과정.
# 2026-09-16: 한 장에 기본 경로와 쿠키 경로를 쌓았더니 세로가 길어 읽기 어렵다는 지적에 두 장으로 갈랐다.
#       이 장은 공격이 통하는 경로만, 처방은 03-04.syn-cookie.svg 가 맡는다.
# 본문 §3 「공격이 통하는 이유」에 적힌 사실만 담는다 —
#   서버는 SYN 을 받으면 연결 변수와 버퍼를 할당하고 SYN,ACK 를 보낸 뒤 ACK 를 기다린다.
#   세 번째 단계가 완성되지 않으면 종종 1 분 이상 지나서야 반쯤 열린 연결을 정리한다.
#   그 사이 연결 자원이 쓰이지도 않을 반쯤 열린 연결에 묶인 채 고갈되고 정상 클라이언트는 서비스를 못 받는다.
# 타입 스펙: type-sequence — 참여자 레인 셋 + 시간축. 스펙 문법 위에 셋을 얹었다.
#       (1) 오지 않은 3 단계는 마커 없는 성긴 파선을 가운데서 끊고 X 로 막아 「화살표의 부재」를 그린다.
#       (2) 대량 공격은 같은 메시지를 세 줄로 겹쳐 그려 되풀이를 라벨이 아니라 도형 개수로 보인다.
#       (3) 서버의 연결 자리는 시간축 밖의 확대 컷이라 레인 사이에 칸 다섯으로 세운다.
#       focal 은 공격이 노리는 할당 시점 하나 — 절 요약이 짚는 단 하나의 논점이다.
#       축약: 공격자와 정상 클라이언트를 양쪽 끝에 고정해 모든 메시지가 이웃 레인 사이에서만 오가게 했다.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, INK, WARN, BAD, PAPER, PAPER2, RULE, KR, MONO


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

    def state(s, a, txt, y, c, op="22", sw=1.1):
        """레인 위의 상태 칩. 파선 레일이 글자를 관통하지 않게 배경을 먼저 깐다."""
        x = s.LX[a]
        w = sum(13.0 if "가" <= ch <= "힣" else 7.6 for ch in str(txt)) + 26
        s.o.append(f'<rect x="{x - w / 2}" y="{y - 13}" width="{w}" height="26" rx="4" fill="{PAPER}"/>')
        s.o.append(f'<rect x="{x - w / 2}" y="{y - 13}" width="{w}" height="26" rx="4" '
                   f'fill="{c}{op}" stroke="{c}" stroke-width="{sw}"/>')
        s.t(x, y + 5, txt, 13, c, _kr(txt))

    def railtext(s, x, y, txt, size, c):
        """레인 위에 앉는 주석. 파선 레일이 글자를 관통하지 않게 배경을 먼저 깐다."""
        w = sum(size if "가" <= ch <= "힣" else size * 0.62 for ch in str(txt)) + 16
        s.o.append(f'<rect x="{x - w / 2}" y="{y - size}" width="{w}" height="{size + 8}" fill="{PAPER}"/>')
        s.t(x, y, txt, size, c, _kr(txt))


W, H = 1000, 680
d = SeqKR(W, H, "COMPUTER NETWORKING TOP-DOWN · 03-04 §3",
          "SYN 을 받자마자 잡는 자원이 표적입니다",
          "서버는 SYN 을 받으면 연결 변수와 버퍼를 할당하고 SYNACK 를 보낸 뒤 ACK 를 기다린다. "
          "공격자는 그 세 번째 단계를 완성하지 않는 SYN 을 대량으로 보낸다. 반쯤 열린 연결은 종종 "
          "1 분 이상 지나서야 정리되므로 그 사이 연결 자리가 차고, 정상 클라이언트는 서비스를 못 받는다.",
          "쓰이지도 않을 반쯤 열린 연결에 자원이 묶인 채 고갈됩니다")

ATK, SRV, CLI = "공격자", "서버", "정상 클라이언트"
d.lanes([(ATK, "가짜 SYN 대량"), (SRV, "SYN 마다 할당"), (CLI, "connect()")], y0=100, lane_w=236)
d.rails(566)
SX = d.LX[SRV]

d.burst(ATK, SRV, "가짜 SYN", 200, BAD, "bad", sub="출발지를 속인 연결 요청이 대량으로")
d.state(SRV, "SYN 마다 연결 변수 + 버퍼 할당", 266, ACC, op="12", sw=1.4)
d.msg(SRV, ATK, "SYNACK", 312, MUTED, "ar", dash="5 4", sub="서버가 ACK 를 기다림")
d.absent(ATK, SRV, "ACK 안 옴 · 3 단계 미완성", 374, BAD)
d.state(SRV, "반쯤 열린 연결", 374, BAD)

# 연결 자리 — 가짜 SYN 이 하나씩 차지하는 모습을 칸으로 센다(시간축 밖의 확대 컷)
SLOT_W, SLOT_G, SLOT_N = 80, 8, 5
SLOT_X0 = SX - (SLOT_N * SLOT_W + (SLOT_N - 1) * SLOT_G) / 2
d.railtext(SX, 416, "서버의 연결 자리 · 가짜 SYN 이 하나씩 차지", 13, MUTED)
for i in range(SLOT_N):
    x = SLOT_X0 + i * (SLOT_W + SLOT_G)
    d.box(x, 424, SLOT_W, 30, PAPER, "none", 0, 4)
    d.tone(x, 424, SLOT_W, 30, BAD, 4, "14", 1.1)
    d.t(x + SLOT_W / 2, 444, "반쯤 열림", 12, BAD, KR)
d.railtext(SX, 478, "1 분 이상 지나서야 정리 · 그동안 자리가 안 비워짐", 13, MUTED)

d.absent(CLI, SRV, "SYN", 522, WARN, sub="자리가 없어 서비스를 못 받음")

d.t(24, 596, "처방은 다음 도식 · SYN 쿠키는 자원을 잡는 시점을 검산 뒤로 미룸", 13, MUTED, KR, "start")

d.legend(616, [("가짜 SYN · 반쯤 열린 연결", BAD), ("정상 클라이언트가 거부되는 자리", WARN),
               ("공격이 노리는 할당 시점", ACC)])
d.save("03-04.syn-flood.svg")
print("ok 03-04.syn-flood")

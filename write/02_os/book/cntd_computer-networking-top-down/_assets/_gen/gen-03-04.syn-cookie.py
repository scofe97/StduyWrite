# 03-04 §3 「SYN 쿠키」 — 같은 공격 입력을 받고도 자원을 쓰지 않는 경로.
# 2026-09-16: 한 장에 기본 경로와 쿠키 경로를 쌓았더니 세로가 길어 읽기 어렵다는 지적에 두 장으로 갈랐다.
#       공격이 통하는 경로는 03-04.syn-flood.svg 가 맡고, 이 장은 처방만 담는다.
#       두 장을 잇는 끈은 제목 아래 한 줄과 바닥 주석이다 — 공격 입력은 같고 달라지는 것은 할당 시점뿐이다.
# 본문 §3 「SYN 쿠키」 네 걸음을 그대로 담는다 —
#   1. SYN 을 받아도 반쯤 열린 연결을 만들지 않고, 출발지·목적지 IP 와 포트 번호 그리고 서버만 아는
#      비밀 수를 재료로 해시를 계산해 초기 순서 번호를 만든다. 이것이 쿠키다.
#   2. 그 쿠키를 초기 순서 번호로 실은 SYNACK 를 보낸다. 쿠키도 그 밖의 어떤 상태도 기억하지 않는다.
#   3. 정상 클라이언트가 ACK 를 보내오면 같은 해시를 다시 계산해 검산하고, 그때 비로소 연결과 소켓을 만든다.
#   4. ACK 가 오지 않으면 원래의 가짜 SYN 은 아무 해도 끼치지 않는다 — 자원을 할당한 적이 없기 때문이다.
# 타입 스펙: type-sequence — 참여자 레인 셋 + 시간축. 스펙 문법 위에 둘을 얹었다.
#       (1) 오지 않은 ACK 는 마커 없는 성긴 파선을 가운데서 끊고 X 로 막는다 — 앞 도식과 같은 자리에서
#           같은 일이 벌어지는데 결과만 다르다는 것이 대비의 축이다.
#       (2) 대량 공격은 같은 메시지를 세 줄로 겹쳐 그려 앞 도식과 입력이 같음을 도형으로 맞춘다.
#       focal 은 쿠키를 계산하는 자리 하나 — 앞 도식의 focal(할당 시점)과 짝을 이룬다.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, INK, OK, BAD, PAPER, PAPER2, RULE, KR, MONO


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


W, H = 1000, 652
d = SeqKR(W, H, "COMPUTER NETWORKING TOP-DOWN · 03-04 §3",
          "검산한 뒤에야 자원을 잡습니다",
          "서버는 SYN 을 받아도 반쯤 열린 연결을 만들지 않는다. 출발지·목적지 IP 와 포트 번호, 서버만 "
          "아는 비밀 수로 해시를 계산해 초기 순서 번호로 삼고 SYNACK 에 실어 보낸다. 쿠키도 그 밖의 "
          "어떤 상태도 기억하지 않는다. ACK 가 오면 같은 해시를 다시 계산해 검산한 뒤에야 연결과 "
          "소켓을 만들고, ACK 가 오지 않으면 쓴 자원이 없다.",
          "기본 경로가 SYN 을 받자마자 잡던 자원을 여기서는 검산 뒤에 잡습니다")

ATK, SRV, CLI = "공격자", "서버 — SYN 쿠키", "정상 클라이언트"
d.lanes([(ATK, "같은 가짜 SYN"), (SRV, "SYN 에는 할당 없음"), (CLI, "connect()")], y0=100, lane_w=236)
d.rails(552)
KX = d.LX[SRV]

d.burst(ATK, SRV, "가짜 SYN", 200, BAD, "bad", sub="앞 도식과 똑같은 공격 입력")
d.state(SRV, "반쯤 열린 연결을 안 만듦 · 할당 0", 266, ACC, op="12", sw=1.4)
d.railtext(KX, 296, "isn = hash(출발지·목적지 IP·포트, 서버 비밀 수)", 13, ACC)
d.msg(SRV, ATK, "SYNACK · seq = 쿠키", 342, MUTED, "ar", dash="5 4",
      sub="쿠키도 그 밖의 어떤 상태도 기억 안 함")
d.absent(ATK, SRV, "ACK 안 옴 · 쓴 자원 0", 404, OK)
d.state(SRV, "아무 해도 없음", 404, OK)

d.msg(CLI, SRV, "ACK · ack = 쿠키 + 1", 452, OK, "ok", sub="정상 클라이언트가 보내옴")
d.state(SRV, "같은 해시를 다시 계산해 검산", 504, OK)
d.railtext(KX, 534, "값이 맞으면 그때 비로소 연결과 소켓 생성", 13, MUTED)

d.t(24, 566, "앞 도식과 공격 입력은 같음 · 달라진 것은 자원을 잡는 시점 하나", 13, MUTED, KR, "start")

d.legend(588, [("가짜 SYN", BAD), ("검산 · 쓴 자원 0", OK), ("쿠키를 계산하는 자리", ACC)])
d.save("03-04.syn-cookie.svg")
print("ok 03-04.syn-cookie")

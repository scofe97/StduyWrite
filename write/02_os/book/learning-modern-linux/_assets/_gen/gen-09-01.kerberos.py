# 09-01 §4 — Kerberos 인증이 네 걸음으로 도는 순서.
# 원문("Kerberos"): "Conceptually, the Kerberos authn process, shown in Figure 9-2, works as follows:
#       1. A client (for example, a program on your laptop) sends a request to a Kerberos component
#       called the Key Distribution Center (KDC), asking for credentials for a given service, such as
#       printing or a directory.
#       2. The KDC responds with the requested credentials—that is, a ticket for the service and a
#       temporary encryption key (session key).
#       3. The client transmits the ticket (which contains the client's identity and a copy of the
#       session key) to the service.
#       4. The session key, shared by the client and service, is used to authenticate the client and may
#       optionally be used to authenticate the service."
#       과제는 "the central role that the KDC plays (a single point of failure) and its strict time
#       requirements (it requires clock synchronization between the client and the server via NTP)" 다.
# 주의: 이 도식은 원서 그림 9-2 를 옮긴 것이 아니라 위 네 문장과 본문 §5 로 다시 세운 것이다.
#       레인 부제의 "노트북 위의 프로그램 · 인쇄 · 디렉터리" 는 본문에 없어 뺐다.
# 타입 스펙: type-sequence — 주체 셋 사이의 시간순 메시지. 번호가 붙은 네 걸음이라 순서가 곧 논지다.
#           실제 객체를 보이려고, 3번 걸음이 나르는 티켓을 상자로 그려 안에 든 것(클라이언트 신원 ·
#           세션 키 사본)을 적고, 걸음마다 각 주체가 쥐게 되는 세션 키를 레인 위 칩으로 찍었다.
# 근거: 본문 §5 네 걸음, 시간 요구 문단(서버 시각 vs 인증자 안의 시각 · KRB_AP_ERR_SKEW · 37 ·
#       "Clock skew too great" · clockskew 기본 300초), 과제(KDC 단일 장애점 · NTP).
import sys; sys.path.insert(0, ".")
from dd import Seq, D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER2, RULE, KR, MONO


def _kr(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO


class SeqKR(Seq):
    def lanes(s, names, y0=104, lane_w=210):
        s.LX = {}; n = len(names)
        span = (s.w - 48 - 24) - lane_w
        for i, (nm, sub) in enumerate(names):
            x = 24 + lane_w / 2 + (span * i / (n - 1) if n > 1 else 0)
            s.LX[nm] = x
            s.box(x - lane_w / 2, y0, lane_w, 44, PAPER2, RULE, 1.0)
            s.t(x, y0 + 20, nm, 12, INK, KR, "middle", 600)
            s.t(x, y0 + 37, sub, 12, MUTED, _kr(sub))
        s.lane_top = y0 + 44
        return s.LX

    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]; dx = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dx} {y} L {x2 - 12 * dx} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 9, label, 12, c, _kr(label), "middle", 600)
        if sub:
            s.t(mx, y + 17, sub, 12, MUTED, _kr(sub))


W, H = 880, 708
d = SeqKR(W, H, "LEARNING MODERN LINUX · 09-01 §5",
          "믿을 수 없는 망 위에서 서로의 신원을 증명하는 네 걸음",
          "클라이언트, KDC, 서비스 셋 사이의 네 걸음을 시간축에 세운 것. 2번 걸음에서 KDC 가 서비스 티켓과 "
          "세션 키를 함께 내주고, 3번 걸음의 티켓 안에 클라이언트 신원과 세션 키 사본이 들어 있어 서비스도 "
          "같은 세션 키를 쥐게 된다. 4번 걸음은 그 키로 클라이언트를 인증한다. 서비스는 인증자 안의 시각을 "
          "자기 시각과 비교해 300초보다 벌어지면 KRB_AP_ERR_SKEW 로 거절한다.",
          "세션 키는 2번에서 클라이언트에, 3번의 티켓을 거쳐 서비스에 갑니다")

d.lanes([("클라이언트", "client"), ("KDC", "Key Distribution Center"),
         ("서비스", "service")], 104, 220)
d.rails(560)


def key_chip(x, y, txt, c):
    w = len(txt) * 12 + 24
    d.o.append(f'<rect x="{x - w / 2}" y="{y - 12}" width="{w}" height="24" rx="12" '
               f'fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
    d.t(x, y + 5, txt, 12, c, KR, "middle", 600)


XC, XK, XS = d.LX["클라이언트"], d.LX["KDC"], d.LX["서비스"]

d.msg("클라이언트", "KDC", "1 · 자격증명 요청", 196, INK, sub="어느 서비스용인지 지정")
d.msg("KDC", "클라이언트", "2 · 서비스 티켓 + 세션 키", 260, ACC, mk="acc",
      sub="세션 키 = 임시 암호화 키")
key_chip(XC, 316, "세션 키", ACC)

# 3번 — 티켓 상자를 화살표 아래에 붙인다
d.msg("클라이언트", "서비스", "3 · 티켓 전달", 372, MUTED)
TX0, TX1 = XK + 24, XS - 32
d.box(TX0, 388, TX1 - TX0, 52, PAPER2, ACC, 1.1, 6)
d.t(TX0 + 12, 408, "티켓", 12, ACC, KR, "start", 600)
d.t(TX0 + 12, 428, "클라이언트 신원 · 세션 키 사본", 12, INK, KR, "start")
key_chip(XS, 468, "세션 키 사본", ACC)

d.msg("서비스", "클라이언트", "4 · 세션 키로 클라이언트 인증", 524, OK, mk="ok",
      sub="선택: 같은 키로 서비스도 인증")

# 운영 조건 — 걸리는 자리의 레인 아래에 칩
key_chip(XK, 580, "단일 장애점", WARN)
key_chip(XS, 580, "시각 비교", WARN)
NY = 604
d.tone(24, NY, W - 48, 32, WARN, 6, "12", 1.2)
d.t(40, NY + 21, "서버 시각 vs 인증자 안의 시각 · 차 > 300초 → KRB_AP_ERR_SKEW (37, Clock skew too great) · NTP",
    12, MUTED, KR, "start")

d.legend(660, [("세션 키가 생기는 걸음", ACC), ("나눠 가진 키로 인증", OK),
                       ("나머지 걸음", MUTED), ("운영에서 걸리는 조건", WARN)])
d.save("09-01.kerberos.svg")
print("ok 09-01.kerberos")

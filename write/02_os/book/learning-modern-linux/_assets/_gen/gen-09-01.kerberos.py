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
# 주의: 이 도식은 원서 그림 9-2 를 옮긴 것이 아니라 위 네 문장으로 다시 세운 것이다.
# 타입 스펙: type-sequence — 주체 셋 사이의 시간순 메시지. 번호가 붙은 네 걸음이라 순서가 곧 논지다.
#           축약: 티켓 안에 무엇이 들었는지는 메시지 부제로 줄였다.
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
            s.t(x, y0 + 37, sub, 11, MUTED, _kr(sub))
        s.lane_top = y0 + 44
        return s.LX

    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]; dx = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dx} {y} L {x2 - 12 * dx} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 9, label, 11.5, c, _kr(label), "middle", 600)
        if sub:
            s.t(mx, y + 17, sub, 11, MUTED, _kr(sub))


W, H = 880, 568
d = SeqKR(W, H, "LEARNING MODERN LINUX · 09-01 §4",
          "믿을 수 없는 망 위에서 서로의 신원을 증명하는 네 걸음",
          "저자가 번호로 적은 네 단계를 시간축에 세운 것. 두 번째 걸음에서 KDC 가 티켓과 세션 키를 함께 "
          "내주는 것이 이 프로토콜의 중심이다.",
          "원서 그림을 옮긴 것이 아니라 저자의 네 문장으로 다시 세운 것입니다")

d.lanes([("클라이언트", "노트북 위의 프로그램"), ("KDC", "Key Distribution Center"),
         ("서비스", "인쇄 · 디렉터리 등")], 116, 236)
d.rails(430)

d.msg("클라이언트", "KDC", "1 · 자격증명을 요청한다", 200, INK,
      sub="어느 서비스에 쓸 것인지 지정한다")
d.msg("KDC", "클라이언트", "2 · 티켓과 세션 키를 내준다", 258, ACC, mk="acc",
      sub="세션 키는 임시 암호화 키다")
d.msg("클라이언트", "서비스", "3 · 티켓을 건넨다", 322, MUTED,
      sub="티켓 안에 신원과 세션 키 사본이 들어 있다")
d.msg("서비스", "클라이언트", "4 · 세션 키로 클라이언트를 인증한다", 386, OK, mk="ok",
      sub="선택적으로 서비스도 같은 키로 인증한다")

NY = 466
d.tone(24, NY - 26, W - 48, 62, WARN, 8, "12", 1.3)
d.t(44, NY, "저자가 든 과제도 둘입니다", 13, WARN, KR, "start", 600)
d.t(44, NY + 20, "KDC 가 중심이라 단일 장애점이 되고, 클라이언트와 서버가 NTP 로 시계를 맞춰야 합니다.",
    12, MUTED, KR, "start")

d.legend(H - 56, [("이 프로토콜의 중심", ACC), ("양쪽이 나눠 가진 키로 끝내는 자리", OK),
                  ("나머지 걸음", MUTED), ("운영에서 걸리는 조건", WARN)])
d.save("09-01.kerberos.svg")
print("ok 09-01.kerberos")

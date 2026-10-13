# 타입 스펙: type-sequence — HTML 파서가 토큰을 만나는 순서와 프리로드 스캐너·네트워크 서비스의 요청, script 에서 파서가 멈추는 자리(레인 3, 메시지 4 + 자기 호출 1).
# 사실 출처: Chrome for Developers, Inside look at modern web browser (part 3), 2018-09-20 "Subresource loading"·"JavaScript can block the parsing"(프리로드 스캐너가 토큰을 보고 네트워크 스레드에 요청, script 를 만나면 파싱을 멈추고 내려받아 실행한 뒤 재개, async·defer 는 막지 않음).
#   HTML 조각 `<link href="zzz.css">`·`<img src="horse.png">`·`<script src="zzz.js">` 는 추출본 v1.txt 그림 쪽 63 의 예 값.
# Layout conventions: 레인 3·폭 200, 메시지 stride 64(라벨 y-9, 부라벨 y+17), 첫 메시지 y=196, 자기 호출은 파서 레인 오른쪽 루프. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, Seq, ACC, OK, WARN, INFO, BAD, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO


def _kr(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO


class SeqKR(Seq):
    def lanes(s, names, y0=104, lane_w=210):
        s.LX = {}
        n = len(names)
        span = (s.w - 48 - 24) - lane_w
        for i, (nm, sub) in enumerate(names):
            x = 24 + lane_w / 2 + (span * i / (n - 1) if n > 1 else 0)
            s.LX[nm] = x
            s.box(x - lane_w / 2, y0, lane_w, 44, PAPER2, RULE, 1.0)
            s.t(x, y0 + 20, nm, 13, INK, _kr(nm), "middle", 600)
            s.t(x, y0 + 37, sub, 12, MUTED, _kr(sub))
        s.lane_top = y0 + 44
        return s.LX

    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None, sw=1.5, dx=0):
        x1, x2 = s.LX[a], s.LX[b]
        d_ = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * d_} {y} L {x2 - 12 * d_} {y}", c, sw, m=mk, dash=dash)
        mx = (x1 + x2) / 2 + dx
        s.t(mx, y - 9, label, 12, c, _kr(label), "middle", 600)
        if sub:
            s.t(mx, y + 17, sub, 12, MUTED, _kr(sub))

    def selfmsg(s, a, label, y, c=MUTED, mk="ar", sub=None):
        x = s.LX[a]
        s.path(f"M {x + 10} {y - 10} L {x + 58} {y - 10} L {x + 58} {y + 10} L {x + 13} {y + 10}", c, 1.5, m=mk)
        s.t(x + 68, y - 4, label, 12, c, _kr(label), "start", 600)
        if sub:
            s.t(x + 68, y + 14, sub, 12, MUTED, _kr(sub), "start")


W, H = 880, 580
d = SeqKR(W, H, "BYTEBYTEGO · 03-01 §5",
          "스크립트를 만나면 파서가 멈추고 스캐너는 앞서 요청한다",
          "메인 스레드가 HTML 을 읽는 순서와 네트워크 서비스로 가는 요청 두 건",
          "link 와 img 는 스캐너가 앞서 요청하고 script 는 받아 실행할 때까지 파싱이 기다립니다")
PA, SC, NW = "HTML 파서", "프리로드 스캐너", "네트워크 서비스"
d.lanes([(PA, "렌더러 메인 스레드"), (SC, "렌더러"), (NW, "대부분 별도 프로세스")], 100, 200)
d.rails(H - 80)

Y0, S = 196, 64
d.msg(PA, SC, '<link href="zzz.css">', Y0 + 0 * S, MUTED, "ar", sub="토큰")
d.msg(SC, NW, "GET zzz.css", Y0 + 1 * S, MUTED, "ar")
d.msg(PA, SC, '<img src="horse.png">', Y0 + 2 * S, MUTED, "ar", sub="토큰")
d.msg(SC, NW, "GET horse.png", Y0 + 3 * S, MUTED, "ar")
d.selfmsg(PA, '<script src="zzz.js">', Y0 + 4 * S + 8, ACC, "acc", "받아 실행할 때까지 대기")

d.legend(H - 56, [("요청과 토큰", MUTED), ("파싱을 멈추는 script", ACC)])
d.save("03-01.parse-sequence.svg")

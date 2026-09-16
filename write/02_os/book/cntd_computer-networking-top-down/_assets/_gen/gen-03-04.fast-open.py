# 03-04 §2 「0-RTT 로 줄이기」 — 쿠키를 언제 받아 두고 언제 쓰는가.
# 본문에 적힌 사실만 담는다 —
#   첫 연결: 평범한 핸드셰이크 도중에 클라이언트가 빠른 열기 쿠키를 요청하고 받아 양쪽이 저장한다.
#   다음 연결: 쿠키와 애플리케이션 데이터를 첫 메시지에 함께 보낸다 — 데이터가 왕복 한 번을 안 기다린다.
#   단서: 클라이언트 쪽의 최적화 가능성일 뿐이고 서버는 정책상 쿠키를 받아들이지 않을 수 있다.
#   값: 시뮬레이터 Cold TCP · Warm TCP 프리셋이 5 MB 전송에 353 ms 와 326 ms 로 갈리고
#       그 차이가 대략 이 경로의 왕복 한 번인 31 ms 다.
# 주석 한 줄: TCP Fast Open 은 RFC 7413 이고 같은 계열이 QUIC · TLS 의 0-RTT 다.
# 타입 스펙: type-sequence — 참여자 레인 둘 + 시간축 왕복. 되돌아오는 메시지는 파선 + 채운 마커,
#       coral 은 헤드라인 한 자리(쿠키와 데이터를 함께 실은 첫 메시지)에만 건다. 서버가 쿠키를 받는
#       경우와 거절하는 경우는 스펙대로 combined fragment(ALT · 2 구역)로 묶는다.
#       축약: dd.py 에 프레임 프리미티브가 없어 box + 탭 + 파선 구분선으로 직접 그린다.
#       값 띠는 시간축 밖의 계측이라 레인 밖에 두고 0-RTT 메시지와 세로 화살표 하나로만 잇는다.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO


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
            s.t(x, y0 + 20, nm, 13, INK, _kr(nm), "middle", 600)
            s.t(x, y0 + 37, sub, 12, MUTED, _kr(sub))
        s.lane_top = y0 + 44
        return s.LX

    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]; dr = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dr} {y} L {x2 - 12 * dr} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 9, label, 13, c, _kr(label), "middle", 600)
        if sub:
            s.t(mx, y + 18, sub, 12, MUTED, _kr(sub))

    def state(s, a, txt, y, c):
        """레인 위의 상태 칩. 파선 레일이 글자를 관통하지 않게 배경을 먼저 깐다."""
        x = s.LX[a]
        w = sum(12.0 if "가" <= ch <= "힣" else 7.0 for ch in str(txt)) + 24
        s.o.append(f'<rect x="{x - w / 2}" y="{y - 12}" width="{w}" height="24" rx="4" fill="{PAPER}"/>')
        s.o.append(f'<rect x="{x - w / 2}" y="{y - 12}" width="{w}" height="24" rx="4" '
                   f'fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
        s.t(x, y + 5, txt, 12, c, _kr(txt))


W, H = 880, 904
d = SeqKR(W, H, "COMPUTER NETWORKING TOP-DOWN · 03-04 §2",
          "쿠키를 받아 두고 다음 연결의 첫 메시지에 데이터를 싣습니다",
          "첫 연결에서는 평범한 3-way 핸드셰이크 도중에 클라이언트가 빠른 열기 쿠키를 요청하고 "
          "서버가 SYNACK 에 실어 보낸다. 양쪽이 저장한다. 다음 연결에서는 클라이언트가 그 쿠키와 "
          "애플리케이션 데이터를 첫 메시지에 함께 보내므로 데이터가 왕복 한 번을 기다리지 않는다. "
          "다만 클라이언트 쪽의 최적화 가능성일 뿐이고 서버는 정책상 쿠키를 받아들이지 않을 수 있다. "
          "시뮬레이터 프리셋 비교에서 5 MB 전송이 353 ms 와 326 ms 로 갈리고 차이는 31 ms 다.",
          "이전에 통신한 적이 있으면 연결 수립의 1 RTT 를 0 으로 줄일 수 있습니다")

LANE_W = 240
d.t(24, 96, "첫 연결 · 핸드셰이크 도중에 쿠키를 받아 둠", 13, INK, KR, "start", 600)
d.lanes([("클라이언트", "connect()"), ("서버", "listen()")], y0=108, lane_w=LANE_W)
d.rails(792)
CX = (d.LX["클라이언트"] + d.LX["서버"]) / 2

d.msg("클라이언트", "서버", "SYN · 빠른 열기 쿠키 요청", 196, INFO, "info",
      sub="다음 연결에 쓸 쿠키를 달라는 요청")
d.msg("서버", "클라이언트", "SYNACK · 빠른 열기 쿠키", 248, INFO, "info", dash="5 4",
      sub="다음 연결에 필요한 연결 정보를 부호화한 쿠키")
d.msg("클라이언트", "서버", "ACK", 300, MUTED, "ar",
      sub="여기까지 평범한 3-way 핸드셰이크 · 연결 수립에 1 RTT")
d.state("클라이언트", "쿠키 저장", 344, INFO)
d.state("서버", "쿠키 저장", 344, INFO)

d.line(24, 376, W - 24, 376, RULE, 1.0)
d.t(24, 404, "다음 연결 · 첫 메시지에 쿠키와 데이터를 함께", 13, INK, KR, "start", 600)

d.msg("클라이언트", "서버", "SYN · 쿠키 + 애플리케이션 데이터", 444, ACC, "acc",
      sub="데이터가 왕복 한 번을 기다리지 않음")

# ── 시간축 밖의 계측 — 왕복 한 번의 값 ──────────────────────────────
d.arrow([(CX, 474), (CX, 500)], MUTED)
d.box(24, 504, W - 48, 60, PAPER, "none", 0, 6)     # 레일이 계측 띠를 관통하지 않게
d.tone(24, 504, W - 48, 60, OK, 6, "12", 1.2)
d.t(CX, 526, "왕복 한 번을 덜어 낸 값 · 시뮬레이터 프리셋 · 5 MB 전송", 12, MUTED, KR)
d.t(200, 548, "Cold TCP 353 ms", 13, MUTED, MONO)
d.t(CX, 548, "Warm TCP 326 ms", 13, MUTED, MONO)
d.t(690, 548, "차이 31 ms · 왕복 한 번", 13, OK, KR)

# ── ALT — 서버가 받거나 정책상 거절하거나 ───────────────────────────
FX, FW, FY, FH = 132, 592, 580, 212
d.box(FX, FY, FW, FH, "none", RULE, 1.0, 4)
d.box(FX, FY, 48, 18, PAPER, RULE, 1.0, 2)
d.t(FX + 24, FY + 13, "ALT", 8, SOFT, MONO)

d.t(180, 620, "쿠키 수용", 12, OK, KR, "start")
d.msg("서버", "클라이언트", "SYNACK", 656, OK, "ok", dash="5 4",
      sub="데이터는 이미 서버에 닿음 · 0-RTT")

d.line(FX + 8, 694, FX + FW - 8, 694, RULE, 1.0, "4 3")

d.t(180, 720, "서버 정책상 거절", 12, WARN, KR, "start")
d.msg("서버", "클라이언트", "SYNACK · 쿠키를 받지 않음", 756, WARN, "warn", dash="5 4",
      sub="클라이언트 쪽의 최적화 가능성일 뿐")

d.t(24, 820, "흐름 밖 · TCP Fast Open 은 RFC 7413 · 같은 계열이 QUIC · TLS 의 0-RTT",
     12, MUTED, KR, "start")

d.legend(840, [("쿠키를 주고받는 자리", INFO), ("데이터를 실은 첫 메시지", ACC),
               ("왕복 한 번을 던 값", OK), ("서버 정책상 거절", WARN)])
d.save("03-04.fast-open.svg")
print("ok 03-04.fast-open")

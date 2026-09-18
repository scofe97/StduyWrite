# 03-03 §3 — 서버가 먼저 닫고 고아가 된 뒤, 클라이언트의 FIN 이 언제 오느냐로 갈리는 세 갈래.
# 타입 스펙: type-sequence — 주체 둘 사이의 시간순 메시지. 세 시나리오를 구분선으로 나눠 쌓고,
#           갈림의 기준은 그 연결의 서버 FIN 으로부터 잰 60초(tcp_fin_timeout)다.
#           프리미티브의 Seq.msg 가 한글 라벨을 MONO 로 하드코딩하므로 계약대로 서브클래스로 감싼다.
import sys; sys.path.insert(0, ".")
from dd import Seq, MUTED, SOFT, OK, BAD, INFO, PAPER, RULE, KR, MONO


def _kr(t): return KR if any("가" <= c <= "힣" for c in str(t)) else MONO


def _w(t):
    # 한글은 11px 에서 ASCII 보다 넓다. 칩 바탕이 글자보다 좁아지지 않게 폭을 따로 잰다
    return sum(10.6 if "가" <= c <= "힣" else 6.4 for c in str(t)) + 20


class SeqKR(Seq):
    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]; dd = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dd} {y} L {x2 - 12 * dd} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 9, label, 11, c, _kr(label), "middle", 600)
        if sub: s.t(mx, y + 17, sub, 11, MUTED, KR)

    def state(s, a, txt, y, c):
        # 레일 점선이 반투명 칩의 글자를 관통하지 않게, 같은 자리에 불투명 바탕을 먼저 깐다
        x = s.LX[a]; w = _w(txt)
        s.o.append(f'<rect x="{x - w / 2}" y="{y - 10}" width="{w}" height="20" rx="4" fill="{PAPER}"/>')
        s.o.append(f'<rect x="{x - w / 2}" y="{y - 10}" width="{w}" height="20" rx="4" '
                   f'fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
        s.t(x, y + 4, txt, 11, c, _kr(txt))


W, H = 940, 812
d = SeqKR(W, H, "PACKET ANALYSIS WITH WIRESHARK · 03-03 §3",
          "뒤늦은 FIN 의 세 갈래",
          "서버가 먼저 닫아 고아가 된 소켓은 60초를 셉니다. 그 안에 클라이언트의 FIN 이 오면 정상 확인을 받고, "
          "늦게 오면 RST 를 받고, 아예 오지 않으면 소켓이 조용히 사라집니다.",
          "기준 시각은 캡처의 0초가 아니라 그 연결의 서버 FIN 입니다")

d.lanes([("클라이언트", "close() 시점이 갈린다"), ("서버", "먼저 닫고 FIN_WAIT_2")], y0=104, lane_w=290)
d.rails(718)
# 구획 머리글 세 줄이 클라이언트 레일 위에 앉는다 — 그 높이만큼 레일 점선을 불투명 바탕으로 가린다
for top in (170, 364, 562):
    d.o.append(f'<rect x="{d.LX["클라이언트"] - 8}" y="{top}" width="16" height="42" fill="{PAPER}"/>')

# A — 끝내 닫지 않음
d.t(24, 184, "A · 끝내 닫지 않음", 12, SOFT, KR, "start", 600)
d.t(24, 202, "a2b-fin-wait2.pcap · a2d-orphan.pcap · 7프레임", 11, MUTED, MONO, "start")
d.msg("서버", "클라이언트", "FIN, ACK", 238, INFO, "info", sub="t=0.003 · 서버가 먼저 닫음")
d.msg("클라이언트", "서버", "ACK", 282, MUTED, sub="t=0.044 · 캡처의 마지막 프레임")
d.state("서버", "60초 뒤 소켓 소멸 · 프레임 0장", 322, BAD)

d.line(24, 350, W - 48, 350, RULE, 0.8, "4 6")

# B — 60초 안에 닫음
d.t(24, 378, "B · 60초 안에 닫음", 12, SOFT, KR, "start", 600)
d.t(24, 396, "a2c-late-fin.pcap · 19프레임 · 두 번째 연결", 11, MUTED, MONO, "start")
d.msg("서버", "클라이언트", "FIN, ACK", 432, INFO, "info", sub="t=32.700")
d.msg("클라이언트", "서버", "FIN, ACK", 476, OK, "ok", sub="t=65.781 · 서버 FIN 에서 33.08초")
d.msg("서버", "클라이언트", "ACK", 520, OK, "ok", sub="정상 확인 · 서버는 TIME_WAIT 로")

d.line(24, 548, W - 48, 548, RULE, 0.8, "4 6")

# C — 60초를 넘겨 닫음
d.t(24, 576, "C · 60초를 넘겨 닫음", 12, SOFT, KR, "start", 600)
d.t(24, 594, "a2e-orphan.pcap · 9프레임", 11, MUTED, MONO, "start")
d.msg("서버", "클라이언트", "FIN, ACK", 630, INFO, "info", sub="t=0.003")
d.msg("클라이언트", "서버", "FIN, ACK", 674, MUTED, sub="t=85.998 · 서버 FIN 에서 86.00초")
d.msg("서버", "클라이언트", "RST", 718, BAD, "bad", sub="ack = 0 · 그런 연결이 없음")

d.legend(H - 56, [("정상 확인", OK), ("끊거나 사라짐", BAD), ("종료를 시작하는 FIN", INFO)])
d.save("03-03.late-fin-fates.svg")

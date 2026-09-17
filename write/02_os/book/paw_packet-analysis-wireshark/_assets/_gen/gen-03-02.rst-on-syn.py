# 03-02 §1 「흔한 쪽」 — 첫 SYN 에 RST 가 오는 경우와, 아무것도 안 오는 경우를 갈라 놓는다.
# 원문 RST-02-ServerSocketCLOSED.pcap 이 위쪽이고, 아래쪽은 §5 재전송 절의 iptables DROP 상태다.
# 두 경우 모두 애플리케이션 로그에는 "연결 실패" 한 줄로 남아 구분이 안 되므로, 선 위에서 갈린다.
# 타입 스펙: type-sequence — 주체 둘 사이의 시간순 메시지. 레인 옆 칩이 클라이언트가 머무는 상태이고,
#           headline(bad)은 연결을 끊는 RST 하나다. 아래쪽 경우는 되돌아오는 메시지가 없는 것이 관찰 결과다.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, OK, BAD, INFO, PAPER, PAPER2, RULE, KR, MONO

def _kr(t): return KR if any("가" <= c <= "힣" for c in str(t)) else MONO

class SeqKR(Seq):
    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]; dd = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dd} {y} L {x2 - 12 * dd} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 9, label, 11, c, _kr(label), "middle", 600)
        if sub: s.t(mx, y + 17, sub, 11, MUTED, KR)
    def state(s, a, txt, y, c):
        # 레일 점선이 반투명 칩의 글자를 관통하지 않게, 같은 자리에 불투명 바탕을 먼저 깐다
        x = s.LX[a]; w = len(txt) * 7.0 + 18
        s.o.append(f'<rect x="{x - w / 2}" y="{y - 10}" width="{w}" height="20" rx="4" fill="{PAPER}"/>')
        super().state(a, txt, y, c)

W, H = 920, 700
d = SeqKR(W, H, "PACKET ANALYSIS WITH WIRESHARK · 03-02 §1",
          "거부와 차단은 선 위에서 갈립니다",
          "위는 그 포트에 LISTEN 이 없어 첫 SYN 에 곧바로 RST 가 돌아오는 경우이고, 아래는 방화벽이 조용히 버려 아무것도 돌아오지 않는 경우다. 아래쪽에서 SYN 을 되풀이하는 주체는 애플리케이션이 아니라 커널이다.",
          "돌아오는 것이 RST 인가 아무것도 없는가 — 애플리케이션 로그로는 못 가릅니다")

d.lanes([("클라이언트", "connect()"), ("서버", "10.0.0.221:8082")], y0=104, lane_w=280)
d.rails(580)
# 구획 머리글 두 줄이 클라이언트 레일 위에 앉는다 — 그 높이만큼 레일 점선을 불투명 바탕으로 가린다
for top in (168, 372):
    d.o.append(f'<rect x="{d.LX["클라이언트"] - 8}" y="{top}" width="16" height="40" fill="{PAPER}"/>')

MX = (d.LX["클라이언트"] + d.LX["서버"]) / 2

# 경우 A — 포트에 LISTEN 이 없음
d.t(24, 182, "A · 그 포트에 LISTEN 이 없음", 12, SOFT, KR, "start", 600)
d.t(24, 200, "원문 RST-02-ServerSocketCLOSED.pcap", 11, MUTED, MONO, "start")
d.msg("클라이언트", "서버", "SYN", 238, INFO, "info", sub="연결 시도")
d.msg("서버", "클라이언트", "RST, ACK", 290, BAD, "bad", sub="그 연결 없음 · 즉시 거부")
d.state("클라이언트", "connection refused", 330, BAD)

d.line(24, 356, W - 48, 356, RULE, 0.8, "4 6")

# 경우 B — 방화벽이 조용히 버림
d.t(24, 386, "B · 방화벽이 조용히 버림", 12, SOFT, KR, "start", 600)
d.t(24, 404, "§5 재전송 절의 OUTPUT DROP 상태", 11, MUTED, MONO, "start")
# 두 레인 사이에 차단벽 — SYN 은 여기서 멈추고 되돌아오는 화살표가 없다
d.line(MX, 426, MX, 576, BAD, 1.4, "5 5")
d.t(MX + 10, 422, "차단", 11, BAD, KR, "start", 600)
for y, sub in ((452, "1차 시도"), (504, "커널이 되풀이 · tcp_syn_retries 6"), (556, None)):
    d.path(f"M {d.LX['클라이언트'] + 10} {y} L {MX - 14} {y}", INFO, 1.5, m="info")
    d.t((d.LX["클라이언트"] + MX) / 2, y - 9, "SYN", 11, INFO, MONO, "middle", 600)
    if sub: d.t((d.LX["클라이언트"] + MX) / 2, y + 17, sub, 11, MUTED, KR)
d.state("클라이언트", "SYN_SENT 유지 · 131초 뒤 실패", 604, ACC)

d.legend(H - 48, [("연결을 끊는 패킷", BAD), ("클라이언트가 보낸 시도", INFO), ("갇히는 자리", ACC)])
d.save("03-02.rst-on-syn.svg")

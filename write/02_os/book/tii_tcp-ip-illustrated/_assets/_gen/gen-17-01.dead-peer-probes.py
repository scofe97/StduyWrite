# 17-01 §2 — 응답이 끊긴 상대에게 keepalive 가 탐침을 보내고 포기하기까지, OrbStack 실측(2026-11-06)을 시간순으로.
# 사실 출처: 이 편의 실측. 커널 7.2.12-orbstack, 클라이언트 소켓에 TCP_KEEPIDLE 2 · TCP_KEEPINTVL 1 · TCP_KEEPCNT 3.
#   tcpdump pcap 을 상대 번호로 풀어 읽은 값(왼쪽 시각은 첫 SYN 기준):
#   0.00 P. seq=1 len=2 → ack=3 / 2.06 seq=2 len=0 → ack=3 / 4.12 seq=2 len=0 → ack=3 /
#   6.16 · 7.19 · 8.21 seq=2 len=0 응답 없음 / 9.23 R. seq=3. recv 는 ETIMEDOUT.
#   seq=2 는 "hi" 2바이트가 확인된 뒤의 SND.UNA(3) − 1 이다(tcp_output.c tcp_xmit_probe_skb: tp->snd_una - !urgent).
# 타입 스펙: type-sequence — 주체 둘 사이의 시간순 메시지와 서버 쪽 수신 차단 구간 하나.
#           축약: 차단 구간은 activation bar 대신 서버 레인에 걸친 bad 색 띠로, 세로 간격은 시간에 비례하지 않는다.
#           focal 은 포기하는 쪽이 보내는 RST 하나.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, OK, BAD, INFO, WARN, PAPER, PAPER2 as s_PAPER2, RULE, KR, MONO

def _kr(t): return KR if any("가" <= c <= "힣" for c in str(t)) else MONO

class SeqKR(Seq):
    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]; dd = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dd} {y} L {x2 - 12 * dd} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 9, label, 12, c, _kr(label), "middle", 600)
        if sub: s.t(mx, y + 17, sub, 11, MUTED, _kr(sub))
    def lanes(s, names, y0=104, lane_w=210):
        s.LX = {}; n = len(names); span = (s.w - 48 - 24) - lane_w
        for i, (nm, sub) in enumerate(names):
            x = 24 + lane_w / 2 + (span * i / (n - 1) if n > 1 else 0)
            s.LX[nm] = x
            s.box(x - lane_w / 2, y0, lane_w, 44, s_PAPER2, RULE, 1.0)
            s.t(x, y0 + 20, nm, 12, INK, _kr(nm), "middle", 600)
            s.t(x, y0 + 37, sub, 11, MUTED, _kr(sub))
        s.lane_top = y0 + 44
        return s.LX

W, H = 920, 656
d = SeqKR(W, H, "TCP/IP ILLUSTRATED VOL.1 · 17-01",
          "응답이 끊긴 상대 — 탐침 3회 뒤 RST",
          "OrbStack Ubuntu 의 네임스페이스 두 개에서 클라이언트에 TCP_KEEPIDLE 2 · TCP_KEEPINTVL 1 · TCP_KEEPCNT 3 을 걸고 잡은 순서다. "
          "처음 두 탐침은 ACK 를 받아 타이머가 유휴 시간으로 돌아가고, 서버 쪽 수신을 막은 뒤의 세 탐침은 1초 간격으로 나가며 응답이 없다. "
          "마지막 탐침에서 한 간격이 지난 9.23초에 클라이언트가 RST 를 보내고 recv 는 ETIMEDOUT 로 끝난다. 세로 간격은 시간에 비례하지 않는다.",
          "유휴 2초 · 간격 1초 · 횟수 3")

C, S = "클라이언트", "서버"
d.lanes([(C, "10.77.0.1 · keepalive 켬"), (S, "10.77.0.2:9000")], y0=100, lane_w=300)
d.rails(552)
xc, xs = d.LX[C], d.LX[S]

def tm(y, txt):
    d.t(xc - 16, y + 4, txt, 12, SOFT, MONO, "end", 600)

# 데이터 한 번 — 이후 유휴
d.msg(C, S, "hi · seq 1 · len 2", 192, INFO, "info"); tm(192, "0.00")
d.msg(S, C, "ACK · ack 3", 220, OK, "ok")
# 응답받은 탐침 둘
d.msg(C, S, "탐침 · seq 2 · len 0", 268, INFO, "info"); tm(268, "2.06")
d.msg(S, C, "ACK · ack 3", 296, OK, "ok")
d.msg(C, S, "탐침 · seq 2 · len 0", 344, INFO, "info"); tm(344, "4.12")
d.msg(S, C, "ACK · ack 3", 372, OK, "ok")

# 서버 수신 차단 구간
B0, B1 = 392, 508
d.tone(xs - 16, B0, 32, B1 - B0, BAD, 4, "22", 1.2)
d.t(xs + 28, B0 + 30, "수신 차단", 12, BAD, KR, "start", 600)
d.t(xs + 28, B0 + 50, "nft input drop", 11, MUTED, MONO, "start")

# 응답 없는 탐침 셋
d.msg(C, S, "탐침 1 · seq 2", 424, BAD, "bad", dash="5 4"); tm(424, "6.16")
d.msg(C, S, "탐침 2 · seq 2", 460, BAD, "bad", dash="5 4"); tm(460, "7.19")
d.msg(C, S, "탐침 3 · seq 2", 496, BAD, "bad", dash="5 4"); tm(496, "8.21")
# 포기
d.msg(C, S, "RST · seq 3", 536, ACC, "acc"); tm(536, "9.23")
d.chip(xc, 574, "recv → ETIMEDOUT", ACC, 11)

d.legend(H - 56, [("탐침", INFO), ("ACK 응답", OK), ("응답 없는 탐침", BAD), ("포기 RST", ACC)])
d.save("17-01.dead-peer-probes.svg")

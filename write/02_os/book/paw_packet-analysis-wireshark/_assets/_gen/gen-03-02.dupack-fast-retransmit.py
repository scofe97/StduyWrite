# 03-02 §5 「중복 ACK」 — 인과 방향을 선 위에 그린다. 중복 ACK 가 먼저 쌓이고 그것이 빠른 재전송을 부른다.
# RFC 5681 §3.2 는 중복 ACK 3개의 도착을 유실의 표시로 삼아, 재전송 타이머를 기다리지 않고 다시 보내게 한다.
# 뒤 세그먼트가 하나 도착할 때마다 받는 쪽이 같은 확인 번호를 되풀이하므로 중복이 한 개씩 쌓인다.
# 타입 스펙: type-sequence — 주체 둘 사이의 시간순 메시지. 레인 옆 칩이 보내는 쪽이 세는 중복 개수이고,
#           headline(acc)은 타이머를 기다리지 않고 나가는 재전송 하나다.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, OK, BAD, WARN, INFO, PAPER, PAPER2, RULE, KR, MONO

def _kr(t): return KR if any("가" <= c <= "힣" for c in str(t)) else MONO

class SeqKR(Seq):
    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]; dd = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dd} {y} L {x2 - 12 * dd} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 9, label, 11, c, _kr(label), "middle", 600)
        if sub: s.t(mx, y + 17, sub, 11, MUTED, KR)
    def state(s, a, txt, y, c):
        x = s.LX[a]; w = len(txt) * 7.0 + 18
        s.o.append(f'<rect x="{x - w / 2}" y="{y - 10}" width="{w}" height="20" rx="4" fill="{PAPER}"/>')
        super().state(a, txt, y, c)

W, H = 920, 744
d = SeqKR(W, H, "PACKET ANALYSIS WITH WIRESHARK · 03-02 §5",
          "중복 ACK 가 쌓여야 빠른 재전송이 걸립니다",
          "가운데 세그먼트 하나가 사라지면 그 뒤 세그먼트가 도착할 때마다 받는 쪽은 같은 확인 번호를 되풀이한다. 보내는 쪽은 그 중복을 세다가 셋째에서 타이머를 기다리지 않고 사라진 세그먼트를 다시 보낸다. 순서는 중복 ACK 가 먼저이고 빠른 재전송이 뒤다.",
          "중복 ACK 는 결과가 아니라 원인입니다")

d.lanes([("보내는 쪽", "SND"), ("받는 쪽", "RCV")], y0=104, lane_w=280)
d.rails(656)
MX = (d.LX["보내는 쪽"] + d.LX["받는 쪽"]) / 2

d.msg("보내는 쪽", "받는 쪽", "seg 1", 196, MUTED, "ar", sub="순서대로 도착")

# seg 2 가 도중에 사라진다
d.path(f"M {d.LX['보내는 쪽'] + 10} 248 L {MX - 14} 248", BAD, 1.5, m="bad")
d.t((d.LX["보내는 쪽"] + MX) / 2, 239, "seg 2", 11, BAD, MONO, "middle", 600)
d.line(MX, 232, MX, 264, BAD, 1.4, "5 5")
d.t(MX + 10, 239, "유실", 11, BAD, KR, "start", 600)

d.msg("보내는 쪽", "받는 쪽", "seg 3", 300, MUTED)
d.msg("받는 쪽", "보내는 쪽", "ACK · seg 2 를 기다림", 336, WARN, "warn")
d.state("보내는 쪽", "중복 1", 372, WARN)

d.msg("보내는 쪽", "받는 쪽", "seg 4", 412, MUTED)
d.msg("받는 쪽", "보내는 쪽", "ACK · 같은 번호", 448, WARN, "warn")
d.state("보내는 쪽", "중복 2", 484, WARN)

d.msg("보내는 쪽", "받는 쪽", "seg 5", 524, MUTED)
d.msg("받는 쪽", "보내는 쪽", "ACK · 같은 번호", 560, WARN, "warn")
d.state("보내는 쪽", "중복 3 · 조건 충족", 596, ACC)

d.msg("보내는 쪽", "받는 쪽", "seg 2 재송신", 644, ACC, "acc",
      sub="재전송 타이머를 안 기다림 · TCP Fast Retransmission")

d.legend(H - 48, [("타이머 없이 나가는 재전송", ACC), ("같은 번호를 되풀이하는 확인", WARN), ("사라진 세그먼트", BAD)])
d.save("03-02.dupack-fast-retransmit.svg")

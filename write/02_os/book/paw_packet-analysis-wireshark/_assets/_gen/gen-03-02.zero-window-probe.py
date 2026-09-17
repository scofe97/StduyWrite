# 03-02 §5 「Window Update 와 ZeroWindowProbe」 — 창이 다시 열렸다는 소식이 사라졌을 때의 경로.
# RFC 9293 §3.8.4 는 데이터 없는 ACK 가 확실하게 전달되지 않는다고 적고, §3.8.6.1 은 그래서 보내는 쪽이
# 창을 떠보도록 정한다. 첫 패킷의 시점(재전송 타임아웃 뒤)과 간격(지수 증가)은 SHOULD 다.
# 타입 스펙: type-sequence — 주체 둘 사이의 시간순 메시지. 레인 옆 칩이 그 시점에 각 쪽이 놓인 자리이고,
#           headline(acc)은 교착을 푸는 패킷 하나(창을 떠보는 1바이트)다.
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

W, H = 920, 680
d = SeqKR(W, H, "PACKET ANALYSIS WITH WIRESHARK · 03-02 §5",
          "창이 열린 소식이 사라져도 풀리는 이유",
          "받는 쪽이 창 0 을 알려 송신이 멈춘다. 애플리케이션이 버퍼를 비운 뒤 보내는 Window Update 는 데이터 없는 ACK 라 사라져도 다시 보내지지 않고, 그러면 두 쪽이 서로를 기다린다. 규격은 그래서 보내는 쪽이 창을 떠보는 패킷을 되풀이하도록 정한다.",
          "알림에 기대지 않고 보내는 쪽이 되풀이해 떠봅니다")

d.lanes([("보내는 쪽", "SND"), ("받는 쪽", "RCV")], y0=104, lane_w=280)
d.rails(596)
MX = (d.LX["보내는 쪽"] + d.LX["받는 쪽"]) / 2

d.msg("받는 쪽", "보내는 쪽", "ACK · win=0", 196, BAD, "bad", sub="수신 버퍼가 가득 참")
d.state("보내는 쪽", "송신 멈춤", 236, BAD)

d.selfmsg("받는 쪽", "read()", 292, OK, sub="버퍼에 자리가 생김")

# Window Update 가 도중에 사라진다 — 화살표가 상대 레일에 닿지 못하고 끊긴다
d.path(f"M {d.LX['받는 쪽'] - 10} 356 L {MX + 14} 356", SOFT, 1.5, m="soft", dash="4,4")
d.t(MX + 40, 347, "Window Update · win>0", 11, SOFT, KR, "start", 600)
d.line(MX, 340, MX, 372, BAD, 1.4, "5 5")
d.t(MX - 10, 347, "유실", 11, BAD, KR, "end", 600)
d.t(MX + 40, 373, "데이터 없는 ACK 는 다시 보내지지 않음", 11, MUTED, KR, "start")

d.state("보내는 쪽", "알림을 기다림", 416, WARN)
d.state("받는 쪽", "데이터를 기다림", 416, WARN)
d.t(MX, 420, "서로 기다리기만 하는 자리", 11, WARN, KR, "middle", 600)

d.msg("보내는 쪽", "받는 쪽", "ZeroWindowProbe · 1바이트", 480, ACC, "acc",
      sub="재전송 타임아웃 뒤 · 간격은 지수로(SHOULD)")
d.msg("받는 쪽", "보내는 쪽", "ACK · 현재 창", 540, OK, "ok",
      sub="창이 0 이어도 답해야 함")
d.state("보내는 쪽", "송신 재개", 596, OK)

d.legend(H - 44, [("교착을 푸는 패킷", ACC), ("송신을 멈추는 신호", BAD), ("서로 기다리는 구간", WARN), ("정상 재개", OK)])
d.save("03-02.zero-window-probe.svg")

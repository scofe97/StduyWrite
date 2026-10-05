# 14-01 §3 — 원서 Figure 14-4 를 대신한다. 세그먼트 순서가 바뀌어 도착할 때 ACK 가 되돌려 주는 타임스탬프.
# 사실 출처: 원서 §14.3.5 — 1024바이트 세그먼트 셋이 1(1–1024), 3(2049–3072), 2(1025–2048) 순서로 도착한다.
#   돌아가는 ACK 는 ACK 1025(세그먼트 1 의 타임스탬프), ACK 1025(세그먼트 1, 중복 ACK), ACK 3073(세그먼트 3 이 아니라 2 의 타임스탬프).
#   수신자 규칙(§14.3.2.4): 새 세그먼트의 순서 번호가 LastACK 와 같을 때만 그 TSV 를 TsRecent 에 저장하고, ACK 의 TSER 에 TsRecent 를 넣는다.
#   LastACK 는 처음 1(SYN+ACK 직후), ACK 1025 를 보낸 뒤 1025.
# 타입 스펙: type-sequence — 주체 둘, 메시지 여섯을 수신자에 도착한 순서대로 그린다. 레인 바깥 글자는 그 순간 수신자의 LastACK 비교.
#           focal 은 세그먼트 3 이 아니라 2 의 시각을 되돌리는 ACK 3073.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, OK, WARN, INFO, PAPER, PAPER2, RULE, KR, MONO

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
            x = 24 + lane_w / 2 + span * i / (n - 1)
            s.LX[nm] = x
            s.box(x - lane_w / 2, y0, lane_w, 44, PAPER2, RULE, 1.0)
            s.t(x, y0 + 20, nm, 12, INK, KR, "middle", 600)
            s.t(x, y0 + 37, sub, 11, MUTED, _kr(sub))
        s.lane_top = y0 + 44

W, H = 920, 568
d = SeqKR(W, H, "TCP/IP ILLUSTRATED VOL.1 · 14-01 §3",
          "순서가 바뀐 도착과 되돌아오는 타임스탬프",
          "1024바이트 세그먼트 셋이 1, 3, 2 순서로 수신자에 도착했다(그림은 도착 순서). 수신자는 순서 번호가 LastACK 와 같은 세그먼트의 TSval 만 TsRecent 에 저장해 "
          "다음 ACK 의 TSecr 로 돌려준다. 그래서 ACK 3073 은 가장 뒤 바이트를 실은 세그먼트 3 이 아니라 구멍을 메운 세그먼트 2 의 시각을 싣는다.",
          "ACK 는 가장 큰 시각이 아니라 창을 전진시킨 세그먼트의 시각을 돌려줍니다")

S, R = "송신자", "수신자"
d.lanes([(S, "TSval 을 실어 보냄"), (R, "LastACK · TsRecent 유지")], y0=100, lane_w=360)
d.rails(480)
xr = d.LX[R]

def note(y, txt, c=SOFT):
    d.t(xr + 24, y + 4, txt, 12, c, _kr(txt), "start", 600)

d.msg(S, R, "세그먼트 1 · 1–1024", 192, INFO, "info", sub="TsRecent ← 세그먼트 1")
note(192, "LastACK 1 · 일치", OK)
d.msg(R, S, "ACK 1025", 244, MUTED, "ar", dash="5 4", sub="TSecr = 세그먼트 1")
d.msg(S, R, "세그먼트 3 · 2049–3072", 296, WARN, "warn", sub="순서 밖 · TsRecent 그대로")
note(296, "LastACK 1025 · 불일치", WARN)
d.msg(R, S, "ACK 1025 · 중복", 348, WARN, "warn", dash="5 4", sub="TSecr = 세그먼트 1")
d.msg(S, R, "세그먼트 2 · 1025–2048", 400, INFO, "info", sub="늦게 도착 · 구멍을 메움")
note(400, "LastACK 1025 · 일치", OK)
d.msg(R, S, "ACK 3073", 452, ACC, "acc", sub="TSecr = 세그먼트 2 · 3 이 아님")

d.legend(H - 56, [("구멍을 메운 세그먼트의 시각", ACC), ("순서대로 온 세그먼트", INFO), ("순서 밖 도착 · 중복 ACK", WARN), ("LastACK 일치", OK)])
d.save("14-01.timestamp-reorder.svg")

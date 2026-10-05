# 14-02 §1 — 원서 Figure 14-5 를 대신한다. 순서 번호 1401 의 세그먼트를 강제로 버렸을 때의 타이머 재전송.
# 사실 출처: 원서 §14.4.1 — 1번과 1401번 세그먼트 쌍을 보내고 둘째(1401)가 버려진다. 첫째는 수신자에 닿았지만 수신자가 ACK 를 지연한다.
#   219ms 동안 응답이 없어 타이머가 만료되고 1번을 다시 보낸다(TSV 577). 그 ACK 는 창을 전진시켜 TSER 로 srtt 34 · RTO 234 로 갱신.
#   다음 ACK 셋은 SACK 을 실은 중복 ACK 라 창을 못 움직여 TSER 를 쓰지 않는다. 1401 이 결국 재전송되어 TCP 시계 911 에 도착하면 ACK 7001.
#   ACK 1401 이라는 번호는 원서 텍스트가 직접 적지 않았고, 1–1400 만 받은 수신자의 누적 ACK 로서 이끌어 낸 값이다.
#   γ 의 1 · 2 · 4 · 8 과 TCP_RTO_MAX 120s 는 같은 절(§14.4)의 일반 규칙이며 이 실험에서 관측한 값이 아니다.
#   캡션의 "두 번 버림" 중 둘째 버림의 시점은 원서 텍스트에 없어 그리지 않는다.
#   축약: 중복 ACK 셋을 만든 1401 뒤의 새 데이터 세그먼트(원서: "packets that arrive at the receiver")는 한 줄로 줄이고 생략 표시를 단다.
#   1번이 도착했고 수신자가 ACK 를 지연했다는 것은 원서도 "Presumably" 로 쓴 추정이라 라벨에 추정을 표시한다.
# 타입 스펙: type-sequence — 주체 둘, 메시지 아홉(한 줄은 생략 표시). 레인 바깥 글자는 그 순간 수신자 쪽 사정.
#           focal 은 구멍이 메워져 돌아온 ACK 7001.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, OK, WARN, BAD, INFO, PAPER, PAPER2, RULE, KR, MONO

def _kr(t): return KR if any("가" <= c <= "힣" for c in str(t)) else MONO

class SeqKR(Seq):
    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]; dd = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dd} {y} L {x2 - 12 * dd} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 9, label, 12, c, _kr(label), "middle", 600)
        if sub: s.t(mx, y + 17, sub, 11, MUTED, _kr(sub))
    def selfmsg(s, a, label, y, c=MUTED, sub=None):
        x = s.LX[a]
        s.path(f"M {x + 10} {y - 10} L {x + 58} {y - 10} L {x + 58} {y + 10} L {x + 13} {y + 10}", c, 1.4, m="ar")
        s.t(x + 68, y + 4, label, 12, c, _kr(label), "start", 600)
    def lanes(s, names, y0=104, lane_w=210):
        s.LX = {}; n = len(names); span = (s.w - 48 - 24) - lane_w
        for i, (nm, sub) in enumerate(names):
            x = 24 + lane_w / 2 + span * i / (n - 1)
            s.LX[nm] = x
            s.box(x - lane_w / 2, y0, lane_w, 44, PAPER2, RULE, 1.0)
            s.t(x, y0 + 20, nm, 12, INK, KR, "middle", 600)
            s.t(x, y0 + 37, sub, 11, MUTED, _kr(sub))
        s.lane_top = y0 + 44

W, H = 920, 796
d = SeqKR(W, H, "TCP/IP ILLUSTRATED VOL.1 · 14-02 §1",
          "1401 을 잃었는데 1 을 다시 보내는 타이머",
          "송신자가 1번과 1401번 세그먼트를 보냈고 1401번이 버려졌다. 수신자가 1번의 ACK 를 지연한 것으로 보이는 사이 219ms 가 지나 타이머가 만료되자, 송신자는 미확인 구간의 맨 앞인 1번을 다시 보낸다. "
          "그 ACK 는 중복 ACK 셋과 달리 창을 전진시켜 RTT 추정에 쓰이고, 뒤에 보낸 새 데이터(그림에서 생략)가 만든 중복 ACK 셋은 쓰이지 않는다. 1401번이 마침내 도착하면 ACK 7001 이 모든 데이터를 확인한다.",
          "타이머는 무엇을 잃었는지 모른 채 맨 앞부터 다시 보냅니다")

S, R = "송신자", "수신자"
d.lanes([(S, "재전송 타이머 하나"), (R, "ACK 를 지연할 수 있음")], y0=100, lane_w=300)
d.rails(648)
xs, xr = d.LX[S], d.LX[R]

def note(y, txt, c=SOFT):
    d.t(xr + 24, y + 4, txt, 12, c, _kr(txt), "start", 600)

d.msg(S, R, "seq 1", 192, INFO, "info")
note(192, "추정 · 도착 후 ACK 지연", SOFT)
# 1401 — 가는 도중 버려짐
y = 244
d.path(f"M {xs + 10} {y} L 560 {y}", BAD, 1.5, dash="5 4")
d.t((xs + 560) / 2, y - 9, "seq 1401", 12, BAD, MONO, "middle", 600)
d.chip(604, y, "버려짐", BAD, 12)
d.selfmsg(S, "RTO 만료 · 219ms 무응답", 304, WARN)
d.msg(S, R, "seq 1 · 재전송", 364, WARN, "warn", sub="TSV 577")
d.msg(R, S, "ACK 1401", 416, OK, "ok", sub="창 전진 · srtt 34 · RTO 234")
d.msg(S, R, "1401 뒤 새 데이터", 468, INFO, "info", dash="2 4", sub="여러 세그먼트 · 그림에서 생략")
d.msg(R, S, "중복 ACK 1401 · 셋", 520, MUTED, "ar", dash="5 4", sub="SACK 포함 · 창 그대로 · TSER 미사용")
d.msg(S, R, "seq 1401 · 재전송", 572, INFO, "info", sub="TCP 시계 911 에 도착")
d.msg(R, S, "ACK 7001", 624, ACC, "acc", sub="구멍 복구 · 전부 수신")

# 같은 절의 일반 규칙 — 이 실험의 관측값이 아님
BY = 668
d.box(24, BY, 848, 48, PAPER2, RULE, 1.0)
d.t(44, BY + 29, "백오프 계수 γ", 13, WARN, KR, "start", 600)
d.t(196, BY + 29, "같은 세그먼트가 또 만료될 때마다 RTO × 1 · 2 · 4 · 8 · 상한 TCP_RTO_MAX 120s", 12, MUTED, KR, "start")

d.legend(H - 56, [("구멍이 메워진 ACK", ACC), ("타이머 재전송", WARN), ("RTT 추정에 쓰인 ACK", OK), ("버려진 세그먼트", BAD), ("보낸 데이터", INFO)])
d.save("14-02.timer-retransmit.svg")

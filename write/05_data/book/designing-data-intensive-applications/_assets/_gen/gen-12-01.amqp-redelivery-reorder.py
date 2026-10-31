# 12-01 §2 — AMQP/JMS 로드 밸런싱과 확인 응답(ACK) 재전달 시 메시지 순서 역전 시퀀스.
# 사실 출처: 12-01 §2(L52), 재전달 조건 "without the broker receiving an acknowledgment"(원서 p.9), 원서 Ch.12 Figure 12-2(PDF p.10 "Consumer 2 crashes while processing m3, so it is redelivered to consumer 1 at a later time")
# 타입 스펙: type-sequence
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, BAD, KR, MONO

W = 880
LEG = 744
H = LEG + 56

class AMQPReorderSeq(Seq):
    def lanes(self, names, y0=104, lane_w=144):
        self.LX = {}
        n = len(names)
        span = (self.w - 48) - lane_w
        for i, (nm, sub) in enumerate(names):
            x = 24 + lane_w / 2 + (span * i / (n - 1) if n > 1 else 0)
            self.LX[nm] = x
            self.box(x - lane_w / 2, y0, lane_w, 44, PAPER2, RULE, 1.0)
            self.t(x, y0 + 19, nm, 13, INK, KR, "middle", 600)
            self.t(x, y0 + 35, sub, 12, MUTED, KR if any("가" <= ch <= "힣" for ch in sub) else MONO)
        self.lane_top = y0 + 44
        return self.LX

    def seq_msg(self, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None, is_mono=False):
        x1, x2 = self.LX[a], self.LX[b]
        d = 1 if x2 > x1 else -1
        self.path(f"M {x1 + 10 * d} {y} L {x2 - 12 * d} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        self.t(mx, y - 7, label, 12, c, MONO if is_mono else KR, "middle", 600)
        if sub:
            self.t(mx, y + 15, sub, 11.5, MUTED, KR, "middle")

    def seq_state(self, a, txt, y, c, w=140):
        x = self.LX[a]
        self.o.append(f'<rect x="{x - w / 2}" y="{y - 12}" width="{w}" height="24" rx="4" fill="{c}22" stroke="{c}" stroke-width="1.2"/>')
        self.t(x, y + 5, txt, 12, c, KR, "middle", 600)

d = AMQPReorderSeq(W, H, "12-01 · §2 AMQP/JMS REDELIVERY & REORDERING", "확인 응답 재전달과 메시지 순서 역전",
                   "로드 밸런싱 환경에서 컨슈머 장애 시 미확인 메시지가 다른 컨슈머로 재전달되며 처리 순서가 역전되는 과정.",
                   "로드 밸런싱 · 확인 응답(ACK) · 컨슈머 2 크래시 · m3 재전달 · 수신 순서 역전(m4 → m3 → m5)")

actors = [
    ("프로듀서 1", "Producer 1"),
    ("프로듀서 2", "Producer 2"),
    ("브로커", "Message Broker"),
    ("컨슈머 1", "Consumer 1"),
    ("컨슈머 2", "Consumer 2"),
]
d.lanes(actors, y0=96, lane_w=144)
d.rails(LEG - 44)

# 1. m1 발행 및 전달
d.seq_msg("프로듀서 1", "브로커", "발행 m1", 166, INFO)
d.seq_msg("브로커", "컨슈머 2", "전달 m1", 190, INFO)

# 2. m2 발행 및 전달
d.seq_msg("프로듀서 2", "브로커", "발행 m2", 220, INFO)
d.seq_msg("브로커", "컨슈머 1", "전달 m2", 250, INFO)

# 3. m1 확인 응답 및 m3 발행·전달
d.seq_msg("컨슈머 2", "브로커", "확인 응답 ACK (m1)", 280, OK, dash="3 3")
d.seq_msg("프로듀서 1", "브로커", "발행 m3", 310, INFO)
d.seq_msg("브로커", "컨슈머 2", "전달 m3", 340, INFO)

# 4. m2 확인 응답 및 m4 발행·전달
d.seq_msg("컨슈머 1", "브로커", "확인 응답 ACK (m2)", 370, OK, dash="3 3")
d.seq_msg("프로듀서 1", "브로커", "발행 m4", 400, INFO)
d.seq_msg("브로커", "컨슈머 1", "전달 m4", 430, INFO)

# 5. 컨슈머 2 크래시 (m3 처리 중 장애, ACK 미도달)
d.seq_state("컨슈머 2", "크래시 (m3 미확인)", 464, BAD, w=136)

# 6. m4 확인 응답 및 m3 재전달 (FOCAL: 순서 역전의 원인)
d.seq_msg("컨슈머 1", "브로커", "확인 응답 ACK (m4)", 496, OK, dash="3 3")
d.seq_msg("브로커", "컨슈머 1", "m3 재전달 (ACK 없음)", 536, ACC, mk="acc")
d.seq_msg("컨슈머 1", "브로커", "확인 응답 ACK (m3)", 572, OK, dash="3 3")

# 7. m5 발행 및 전달
d.seq_msg("프로듀서 2", "브로커", "발행 m5", 608, INFO)
d.seq_msg("브로커", "컨슈머 1", "전달 m5", 638, INFO)

# 하단 요약 칩: 컨슈머 1 최종 처리 순서 역전
d.tone(480, 668, 360, 28, ACC, 4, "18", 1.2)
d.t(660, 686, "컨슈머 1 최종 처리 순서: m4 → m3 → m5 (순서 역전 발생)", 12, INK, KR, "middle", 600)

# 범례
d.legend(LEG, [
    ("정상 메시지 전달", INFO),
    ("확인 응답 (ACK)", OK),
    ("컨슈머 크래시", BAD),
    ("m3 재전달 (focal)", ACC)
])

d.save("12-01.amqp-redelivery-reorder.svg")

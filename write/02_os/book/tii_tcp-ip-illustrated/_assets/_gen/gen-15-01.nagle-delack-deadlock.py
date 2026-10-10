# 타입 스펙: type-sequence — Nagle 과 지연 ACK 가 만났을 때의 일시적 상호 교착 흐름.
# 사실 출처: ch15.txt 375~413행, Linux tcp.h — 송신자 Nagle 미확인 대기, 수신자 세그먼트 1개 수신 후 지연 ACK 대기, 타이머 만료(Linux 40~200ms, 여기서는 200ms 상한 예시).
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, OK, WARN, BAD, INFO, PAPER2, RULE, KR, MONO

def _kr(t): return KR if any("가" <= c <= "힣" for c in str(t)) else MONO

class SeqKR(Seq):
    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]; dd = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 4 * dd} {y} L {x2 - 4 * dd} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 9, label, 12, c, _kr(label), "middle", 600)
        if sub: s.t(mx, y + 17, sub, 11, MUTED, _kr(sub))

W, H = 920, 600
d = SeqKR(W, H, "TCP/IP ILLUSTRATED VOL.1 · 15-01 §4",
          "지연 ACK 와 Nagle 알고리즘의 상호 교착 (예시)",
          "송신자가 작은 데이터를 연속으로 보낼 때(예: HTTP 400B 연속 쓰기 예시), 첫 세그먼트 하나만 받은 수신자는 지연 ACK 타이머를 켠다. "
          "송신자는 이전 패킷의 ACK 가 오지 않아 Nagle 에 의해 두 번째 전송을 보류한다. 두 호스트가 서로를 기다려 회선이 멈추고, "
          "수신자의 지연 ACK 타이머가 만료(시스템에 따라 40~200ms, 200ms 예시)되어 순수 ACK 가 전송된 뒤에야 전송이 재개된다.",
          "서로 상대 신호를 기다리는 동안 회선은 타이머 만료까지 멈춥니다(예시)")

S, R = "송신자", "수신자"
d.LX = {S: 280, R: 660}
for nm, sub in ((S, "Nagle 알고리즘 켬"), (R, "지연 ACK 켬")):
    x = d.LX[nm]
    d.box(x - 90, 104, 180, 44, PAPER2, RULE, 1.0, 6)
    d.t(x, 124, nm, 13, INK, KR, "middle", 600)
    d.t(x, 141, sub, 11, MUTED, _kr(sub))
d.lane_top = 148
d.rails(510)
xs, xr = d.LX[S], d.LX[R]

def when(y, t, note_txt=None, c=SOFT):
    d.t(150, y + 4, t, 12, c, MONO, "end", 600)
    if note_txt: d.t(150, y + 21, note_txt, 11, MUTED, KR, "end")

def note(side, y, txt, c=SOFT):
    if side == S: d.t(xs - 20, y + 4, txt, 11, c, _kr(txt), "end")
    else: d.t(xr + 20, y + 4, txt, 11, c, _kr(txt), "start")

# 1. 0ms: 첫 번째 작은 세그먼트 송신 (예시)
Y1 = 180
d.msg(S, R, "write 1 (400B) 송신 (예시)", Y1, INFO, "info", sub="미확인 데이터 없음 · 즉시 전송")
when(Y1, "0ms (예시)", "첫 세그먼트 송신")
note(R, Y1, "세그먼트 1개 수신", WARN)

# 2. 1ms: 수신자 지연 ACK 가동, 송신자 write 2 보류 (예시)
Y2 = 236
# 수신자 측 지연 ACK 가동 상자
d.tone(xr + 16, Y2 - 12, 230, 38, WARN, 4, "16", 1.0)
d.t(xr + 26, Y2 + 2, "지연 ACK 타이머 (상한 200ms 예시)", 11, WARN, KR, "start", 600)
d.t(xr + 26, Y2 + 18, "Linux 보통 40ms~ · ACK 보류", 11, MUTED, KR, "start")

# 송신자 측 write 2 보류 상자
d.tone(xs + 20, Y2 + 36, 180, 38, BAD, 4, "16", 1.0)
d.t(xs + 30, Y2 + 50, "write 2 (400B) 버퍼링", 11, BAD, KR, "start", 600)
d.t(xs + 30, Y2 + 66, "미확인 세그먼트 대기", 11, MUTED, KR, "start")
when(Y2 + 20, "1ms (예시)", "두 번째 write 호출")

# 3. 교착 구간 띠
Y_ZONE = 330
d.tone(xs + 20, Y_ZONE - 14, xr - xs - 40, 48, BAD, 6, "14", 1.2)
d.t((xs + xr) / 2, Y_ZONE + 8, "상호 교착 상태 (회선 공백 idle)", 13, BAD, KR, "middle", 600)
d.t((xs + xr) / 2, Y_ZONE + 26, "송신자 ACK 대기 ↔ 수신자 데이터 대기", 11, MUTED, KR, "middle")
when(Y_ZONE + 10, "1~200ms (예시)", "타이머 만료까지 정지", BAD)

# 4. 200ms: 타이머 만료로 순수 ACK 전송 (예시)
Y3 = 415
d.msg(R, S, "순수 ACK 전송 (ack 400)", Y3, WARN, "warn", dash="4 4", sub="지연 타이머 만료 (예시 200ms)")
when(Y3, "200ms (예시)", "타이머 강제 만료", WARN)
note(S, Y3, "미확인 해소", OK)

# 5. 201ms: 보류했던 두 번째 세그먼트 송신 (예시)
Y4 = 475
d.msg(S, R, "write 2 (400B) 지연 송신", Y4, OK, "ok", sub="ACK 확인 후 버퍼링 해제")
when(Y4, "201ms (예시)", "보류분 전송 재개", OK)
note(R, Y4, "두 번째 수신", MUTED)

d.legend(H - 46, [
    ("정상 세그먼트 전송", INFO),
    ("지연 ACK 대기 및 만료", WARN),
    ("Nagle 송신 보류 및 교착", BAD),
    ("교착 해제 후 전송 재개", OK)
])

d.save("15-01.nagle-delack-deadlock.svg")

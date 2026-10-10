# 타입 스펙: type-sequence — 0 창 광고 후 persist 타이머 5초 간격 3회 탐침 및 창 업데이트 재개.
# 사실 출처: 원서 §15.5.2–15.5.2.1 Mac OS X 10.6 송신자 · Windows 7 수신자 — 327B 완충, 4.979s win 0, 5초 간격 3회 1B 탐침, 20.143s 앱 소비 시작 및 창 업데이트(최대 64KB).
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, OK, WARN, BAD, INFO, PAPER, PAPER2, RULE, KR, MONO

def _kr(t): return KR if any("가" <= c <= "힣" for c in str(t)) else MONO

class SeqKR(Seq):
    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]
        dd = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dd} {y} L {x2 - 12 * dd} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 9, label, 12, c, _kr(label), "middle", 600)
        if sub: s.t(mx, y + 17, sub, 11, MUTED, _kr(sub))

W, H = 920, 730
d = SeqKR(W, H, "TCP/IP ILLUSTRATED VOL.1 · 15-02 §2",
          "0 창 광고와 persist 타이머의 창 탐침",
          "수신 버퍼가 차면 win 0을 광고해 송신을 멈춘다. 수신 앱이 읽기를 멈춘 동안 송신자는 5초 간격으로 세 차례 1바이트 창 탐침을 보내 최신 창 상태를 확인하고, 소비 시작 후 창 업데이트로 전송을 재개한다.",
          "0 창 광고 후 5초 간격 세 차례 탐침을 거쳐 창 업데이트로 전송이 재개됩니다")

S, R = "송신자", "수신자"
d.LX = {S: 320, R: 760}
for nm, sub in ((S, "Mac OS X 10.6 · 송신"), (R, "Windows 7 · 수신 버퍼")):
    x = d.LX[nm]
    d.box(x - 110, 100, 220, 44, PAPER2, RULE, 1.0)
    d.t(x, 120, nm, 13, INK, KR, "middle", 600)
    d.t(x, 137, sub, 11, MUTED, _kr(sub))

d.lane_top = 144
d.rails(675)
xs = d.LX[S]
xr = d.LX[R]

def when(y, t, note=None, c=SOFT):
    d.t(176, y + 4, t, 12, c, MONO, "end", 600)
    if note: d.t(176, y + 20, note, 11, MUTED, KR, "end")

# 1. 마지막 327B 완충
y = 175
d.msg(S, R, "패킷 151 (327B 전송)", y, OK, "ok", sub="잔여 수신 버퍼 327B 완충")
when(y, "패킷 151", "Window Full", OK)

# 2. 0 창 광고
y = 230
d.msg(R, S, "ACK · win 0 (0 창 광고)", y, BAD, "bad", sub="수신 버퍼 포화 · 송신 전면 중단")
when(y, "4.979s", "0 창 광고", BAD)

# 3. 1회차 창 탐침 (5초 간격)
y = 295
d.msg(S, R, "1회차 창 탐침 (1B ZWP)", y, ACC, "acc", sub="persist 만료 · 최신 창 크기 조회")
when(y, "약 5초 뒤", "1회차 탐침", ACC)

# 4. 1회차 탐침 응답
y = 350
d.msg(R, S, "ACK · win 0", y, MUTED, "ar", sub="버퍼 미소비 · 여전히 0 창")
when(y, "", "탐침 응답", MUTED)

# 5. 2회차 창 탐침 (5초 간격)
y = 415
d.msg(S, R, "2회차 창 탐침 (1B ZWP)", y, ACC, "acc", sub="5초 간격 유지 · persist 2차 만료")
when(y, "약 5초 뒤", "2차 탐침", ACC)

# 6. 2회차 탐침 응답
y = 470
d.msg(R, S, "ACK · win 0", y, MUTED, "ar", sub="버퍼 미소비 · 여전히 0 창")
when(y, "", "탐침 응답", MUTED)

# 7. 3회차 창 탐침 (5초 간격)
y = 535
d.msg(S, R, "3회차 창 탐침 (1B ZWP)", y, ACC, "acc", sub="5초 간격 유지 · persist 3차 만료")
when(y, "약 5초 뒤", "3차 탐침", ACC)

# 8. 3회차 탐침 응답
y = 590
d.msg(R, S, "ACK · win 0", y, MUTED, "ar", sub="버퍼 미소비 · 여전히 0 창")
when(y, "", "탐침 응답", MUTED)

# 9. 수신 앱 소비 시작 및 창 업데이트로 재개
y = 650
d.msg(R, S, "창 업데이트 (최대 64KB)", y, OK, "ok", sub="수신 앱 큐 읽기 시작 · 창 열림")
when(y, "20.143s", "창 업데이트", OK)

d.legend(H - 46, [("정상 송수신 및 재개", OK), ("0 창 광고", BAD), ("persist 1바이트 창 탐침", ACC), ("0 창 유지 응답", MUTED)])
d.save("15-02.zero-window-probe.svg")

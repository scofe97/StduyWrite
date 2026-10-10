# 타입 스펙: type-sequence — 0 창 상태에서 긴급 데이터(URG) 세그먼트 전송과 긴급 모드 탈출.
# 사실 출처: 원서 §15.6.1 Wireshark 실측치 — Mac OS X 송신 · Linux 수신. 5.012s win 0, 6.0113s seq 6145(1B) URG urg_ptr 1(탈출점 6146), 10.006s 창 업데이트, 10.009s 탈출.
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

W, H = 920, 620
d = SeqKR(W, H, "TCP/IP ILLUSTRATED VOL.1 · 15-03 §3",
          "0 창 상태에서의 긴급 데이터 전송과 위치 포인터",
          "수신 창이 0으로 닫힌 상태에서도 긴급 데이터(URG)는 창 탐침 형태로 즉시 전송될 수 있다. 긴급 포인터는 데이터를 새치기하지 않고 인라인 바이트 스트림상의 첫 비긴급 바이트 위치(6146)를 가리킨다.",
          "긴급 포인터는 새치기가 아니라 바이트 스트림 내 위치 표시(오프셋)입니다")

S, R = "송신자", "수신자"
d.LX = {S: 320, R: 760}
for nm, sub in ((S, "Mac OS X · 송신 버퍼"), (R, "Linux · 4KB 제한 버퍼")):
    x = d.LX[nm]
    d.box(x - 110, 100, 220, 44, PAPER2, RULE, 1.0)
    d.t(x, 120, nm, 13, INK, KR, "middle", 600)
    d.t(x, 137, sub, 11, MUTED, _kr(sub))

d.lane_top = 144
d.rails(530)

def when(y, t, note=None, c=SOFT):
    d.t(176, y + 4, t, 12, c, MONO, "end", 600)
    if note: d.t(176, y + 20, note, 11, MUTED, KR, "end")

# 1. 0 창 수신 (버퍼 4KB 한계 포화)
y = 180
d.msg(R, S, "ACK 6145 · win 0", y, BAD, "bad", sub="수신 버퍼 4KB 포화 · 0 창 광고")
when(y, "5.012s", "0 창 광고", BAD)

# 2. 0 창 중 긴급 데이터 전송 (1B + URG 플래그)
y = 235
d.msg(S, R, "seq 6145 (1B) · [URG] urg_ptr 1", y, ACC, "acc", sub="긴급 데이터 1B 전송 · 탈출점 6146")
when(y, "6.0113s", "긴급 모드 진입", ACC)

# 3. 수신자의 0 창 ACK (탐침 응답)
y = 290
d.msg(R, S, "ACK 6145 · win 0", y, MUTED, "ar", sub="창 탐침 응답 · 여전히 0 창")
when(y, "6.0114s", "0 창 응답", MUTED)

# 4. 수신 앱 읽기 시작 및 창 업데이트
y = 345
d.msg(R, S, "창 업데이트 (win > 0)", y, OK, "ok", sub="수신 앱 10초 후 읽기 시작 · 창 열림")
when(y, "10.006s", "창 업데이트", OK)

# 5. 전송 재개 (데이터 전송)
y = 400
d.msg(S, R, "seq 6145 (데이터 전송)", y, INFO, "info", sub="창 열림에 따라 데이터 전송 재개")
when(y, "10.007s", "데이터 전송 재개", INFO)

# 6. 긴급 포인터 확인 및 긴급 모드 탈출 (0 창 재발생)
y = 455
d.msg(R, S, "ACK 확인 · win 0", y, OK, "ok", sub="탈출점 6146 승인 · 긴급 모드 탈출")
when(y, "10.009s", "긴급 모드 탈출", OK)

# 7. 마지막 데이터 바이트와 FIN
y = 510
d.msg(S, R, "seq ... [FIN]", y, INFO, "info", sub="마지막 데이터 바이트 전송 및 종료")
when(y, "11.007s", "전송 완료 (FIN)", INFO)

d.legend(H - 46, [("0 창 차단", BAD), ("긴급 데이터(URG)", ACC), ("창 열림·탈출", OK), ("정상 데이터·FIN", INFO)])
d.save("15-03.urgent-pointer-zero-window.svg")

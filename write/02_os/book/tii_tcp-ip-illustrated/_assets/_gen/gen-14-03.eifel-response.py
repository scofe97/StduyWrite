# 14-03 §3 — Eifel 응답 알고리즘(RFC 4015)의 분기와 RTO 추정값 복원 흐름.
# 사실 출처(ch14.txt §14.7.4):
#   첫 재전송 타이머 이벤트에서만 동작하고, 복구가 끝나기 전에 다음 타임아웃이 나면 실행하지 않는다.
#   타이머 만료 때 srtt_prev = srtt + 2(G), rttvar_prev = rttvar 를 보관한다(G = TCP 시계 정밀도).
#   탐지 알고리즘 결과가 SpuriousRecovery 에 들어간다: 오탐이면 SPUR_TO, 뒤늦은 오탐이면 LATE_SPUR_TO, 아니면 일반 타임아웃 처리.
#   SPUR_TO 면 SND.NXT 를 SND.MAX 로 옮겨 go-back-N 을 피한다. LATE_SPUR_TO 면 재전송에 대한 ACK 가 이미 왔으므로 SND.NXT 를 바꾸지 않는다.
#   두 경우 모두 혼잡 제어 상태를 다시 맞춘다(16장). 타임아웃 뒤 보낸 데이터의 첫 정상 ACK 에서 RTT 표본 m 을 얻으면
#   srtt ← max(srtt_prev, m), rttvar ← max(rttvar_prev, m/2), RTO = srtt + max(G, 4(rttvar)).
# 타입 스펙: type-flowchart — 위→아래, 결정 하나에 출구 셋(≤3). Layout conventions: 80px stride.
#           focal 은 마지막 추정값 복원 상자 — 이 절이 앞 편의 RTO 공식과 이어지는 자리.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

def _kr(t): return KR if any("가" <= c <= "힣" for c in str(t)) else MONO

W, H = 920, 808
d = D(W, H, "TCP/IP ILLUSTRATED VOL.1 · 14-03 §3",
      "Eifel 응답 — 오탐 판정 뒤 송신 위치와 RTO 를 고친다",
      "첫 RTO 만료 때 srtt 에 2G 를 더한 값과 rttvar 를 보관하고 탐지 알고리즘을 돌린다. 오탐이 아니면 일반 타임아웃 처리로 간다. "
      "일찍 잡은 오탐(SPUR_TO)이면 다음 송신 위치를 새 데이터 시작점으로 옮기고, 늦게 잡은 오탐(LATE_SPUR_TO)이면 그대로 둔다. "
      "어느 쪽이든 혼잡 제어 상태를 다시 맞춘 뒤, 타임아웃 뒤 보낸 데이터의 첫 정상 ACK 로 얻은 RTT 표본 m 과 보관값 중 큰 쪽으로 추정값을 정한다.",
      "판정 결과에 따라 갈리는 것은 송신 위치이고, RTO 추정값은 두 오탐 모두 같은 식으로 고칩니다")

CX, CW, CH = 460, 400, 56

def node(y, name, sub=None, color=INK, oval=False, x=None, w=CW, h=CH, tone=None):
    x = CX - w / 2 if x is None else x
    if tone: d.tone(x, y, w, h, tone, 20 if oval else 6, "12", 1.2)
    else: d.box(x, y, w, h, PAPER2, RULE, 1, 20 if oval else 6)
    cx = x + w / 2
    d.t(cx, y + (24 if sub else 33), name, 13, color, _kr(name), "middle", 600)
    if sub: d.t(cx, y + 44, sub, 11, MUTED, _kr(sub))
    return cx

node(104, "첫 RTO 만료", "다음 타임아웃이 먼저 오면 미적용", oval=True)
d.arrow([(CX, 164), (CX, 176)], MUTED, "ar", 1.5)
node(184, "srtt_prev = srtt + 2G", "rttvar_prev = rttvar 보관", color=INK)
d.arrow([(CX, 244), (CX, 256)], MUTED, "ar", 1.5)
node(264, "탐지 알고리즘 실행", "Eifel · F-RTO · DSACK")
d.arrow([(CX, 324), (CX, 336)], MUTED, "ar", 1.5)

DY, DW, DH = 344, 220, 72
d.o.append(f'<polygon points="{CX},{DY} {CX + DW / 2},{DY + DH / 2} {CX},{DY + DH} {CX - DW / 2},{DY + DH / 2}" fill="{PAPER2}" stroke="{RULE}" stroke-width="1"/>')
d.t(CX, DY + DH / 2 + 5, "SpuriousRecovery", 12, INK, MONO, "middle", 600)

BY, BW = 464, 240
LXb, MXb, RXb = 24, 340, 656
node(BY, "일반 타임아웃 처리", "오탐 아님", color=WARN, x=LXb, w=BW, tone=WARN)
node(BY, "SND.NXT ← SND.MAX", "go-back-N 연쇄 차단", color=OK, x=MXb, w=BW, tone=OK)
node(BY, "SND.NXT 유지", "재전송의 ACK 이미 도착", color=OK, x=RXb, w=BW, tone=OK)
mid = DY + DH / 2
d.arrow([(CX - DW / 2, mid), (LXb + BW / 2, mid), (LXb + BW / 2, BY - 8)], WARN, "warn", 1.5)
d.arrow([(CX, DY + DH), (CX, BY - 8)], OK, "ok", 1.5)
d.arrow([(CX + DW / 2, mid), (RXb + BW / 2, mid), (RXb + BW / 2, BY - 8)], OK, "ok", 1.5)
d.t(LXb + BW / 2 + 48, mid - 10, "아님", 11, WARN, KR)
d.t(CX + 12, BY - 20, "SPUR_TO", 11, OK, MONO, "start")
d.t(RXb + BW / 2 - 64, mid - 10, "LATE_SPUR_TO", 11, OK, MONO)

SX, SW = MXb, RXb + BW - MXb
SC = SX + SW / 2
d.arrow([(MXb + BW / 2, BY + CH), (MXb + BW / 2, 552 - 8)], OK, "ok", 1.5)
d.arrow([(RXb + BW / 2, BY + CH), (RXb + BW / 2, 552 - 8)], OK, "ok", 1.5)
node(552, "혼잡 제어 상태 조정", "16장", x=SX, w=SW)
d.arrow([(SC, 552 + CH), (SC, 632 - 8)], MUTED, "ar", 1.5)

FY, FH = 632, 112
d.o.append(f'<rect x="{SX}" y="{FY}" width="{SW}" height="{FH}" rx="6" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t(SC, FY + 22, "첫 정상 ACK 의 RTT 표본 m", 12, MUTED, KR, "middle")
for i, f in enumerate(("srtt ← max(srtt_prev, m)", "rttvar ← max(rttvar_prev, m/2)", "RTO = srtt + max(G, 4·rttvar)")):
    d.t(SC, FY + 50 + 24 * i, f, 13, ACC, MONO, "middle", 600)

d.legend(H - 48, [("추정값 복원", ACC), ("오탐 뒤 응답", OK), ("오탐 아님", WARN)])
d.save("14-03.eifel-response.svg")

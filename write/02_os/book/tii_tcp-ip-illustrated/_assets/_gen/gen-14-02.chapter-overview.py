# 타입 스펙: type-flowchart — 수신 구멍을 송신자가 알아채는 세 경로.
# Layout conventions: 같은 유형의 56px 카드, 24px 여백, 24px 열 간격.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, MUTED, INK, PAPER2, RULE, KR

W, H = 920, 432
d = D(W, H, "TCP/IP ILLUSTRATED VOL.1 · 14-02", "수신자 구멍을 찾는 세 가지 신호",
      "순서 밖 데이터는 중복 ACK를 만들고 SACK을 사용할 때 받은 범위도 알린다. 피드백이 없으면 재전송 타이머가 만료될 때 확인되지 않은 데이터부터 다시 보낸다.",
      "빠른 재전송은 ACK를, 최후의 복구는 타이머를 봅니다")

TOP_X, TOP_Y, TOP_W, TOP_H = 260, 112, 400, 56
d.box(TOP_X, TOP_Y, TOP_W, TOP_H, PAPER2, RULE, 1, 20)
d.t(W/2, TOP_Y+26, "수신 측 바이트 구멍", 15, INK, KR, "middle", 600)
d.t(W/2, TOP_Y+46, "앞쪽은 비고 뒤쪽 데이터는 도착", 11, MUTED)

CW, CH, GAP, X0, Y = 272, 88, 28, 24, 240
cards = [("중복 ACK", "같은 다음 기대 번호 반복", "빠른 재전송", ACC),
         ("SACK 블록", "구멍 뒤 수신 범위 알림", "선택적 복구", OK),
         ("RTO 만료", "필요한 ACK가 안 돌아옴", "타이머 재전송", WARN)]
for i, (name, evidence, result, color) in enumerate(cards):
    x = X0 + i*(CW+GAP)
    d.arrow([(W/2, TOP_Y+TOP_H+4), (W/2, 208), (x+CW/2, 208), (x+CW/2, Y-8)], color, "acc" if i==0 else "ok" if i==1 else "warn", 1.5)
    d.tone(x, Y, CW, CH, color, 6, "12", 1.2)
    d.t(x+CW/2, Y+28, name, 15, color, KR, "middle", 600)
    d.t(x+CW/2, Y+51, evidence, 11, MUTED)
    d.t(x+CW/2, Y+73, result, 12, INK, KR, "middle", 600)

d.save("14-02.chapter-overview.svg")

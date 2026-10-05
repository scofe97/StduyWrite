# 타입 스펙: type-flowchart — RTT 표본에서 타이머 판정까지의 분기.
# Layout conventions: 920px 캔버스, 56px 단계 카드, 24px 여백, 80px 세로 stride.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, MUTED, INK, PAPER2, RULE, KR, MONO

W, H = 920, 520
d = D(W, H, "TCP/IP ILLUSTRATED VOL.1 · 14-01", "RTO를 정한 뒤 ACK를 기다리는 과정",
      "RTT 표본으로 평균과 변동 폭을 갱신해 재전송 대기 시간을 정한다. 제때 ACK가 오면 다음 표본을 얻고, 만료되면 다시 보내며 대기 간격을 늘린다.",
      "표본 → 추정 → 대기, 그리고 ACK 도착 여부로 갈라집니다")

CW, CH, X, Y0, STEP = 400, 56, 260, 112, 80
steps = [("RTT 표본", "보낸 바이트를 덮는 ACK의 왕복 시간"),
         ("srtt · rttvar 갱신", "평균과 편차를 따로 추정"),
         ("RTO 산정", "평균 + 변동 폭에 따른 여유"),
         ("ACK 대기 타이머", "미확인 데이터가 남아 있는 동안 유지")]
for i, (title, sub) in enumerate(steps):
    y = Y0 + i * STEP
    if i < len(steps)-1:
        d.arrow([(W/2, y+CH+4), (W/2, y+STEP-8)], MUTED, "ar", 1.5)
    d.box(X, y, CW, CH, PAPER2, RULE, 1.0, 20 if i==0 else 6)
    d.t(W/2, y+24, title, 14, ACC if i==2 else INK, KR, "middle", 600)
    d.t(W/2, y+44, sub, 11, MUTED)

# 마지막 타이머에서 나온 두 결과는 아래 상태 칸으로 갈라진다.
BX, BY, BW, BH = [24, 488], 432, 408, 56
for x, title, sub, color in [(BX[0], "제때 ACK", "다음 RTT 표본에 반영", OK),
                              (BX[1], "RTO 만료", "재전송 · 백오프, 모호한 표본 보류", WARN)]:
    d.tone(x, BY, BW, BH, color, 6, "12", 1.2)
    d.t(x+BW/2, BY+24, title, 14, color, KR, "middle", 600)
    d.t(x+BW/2, BY+44, sub, 11, MUTED)
# 위 카드와 분기 카드를 수평·수직 직각 선으로 연결한다.
d.arrow([(X+40, Y0+3*STEP+CH), (X+40, BY-16), (BX[0]+BW/2, BY-16), (BX[0]+BW/2, BY-6)], OK, "ok", 1.5)
d.arrow([(X+CW-40, Y0+3*STEP+CH), (X+CW-40, BY-16), (BX[1]+BW/2, BY-16), (BX[1]+BW/2, BY-6)], WARN, "warn", 1.5)
d.save("14-01.chapter-overview.svg")

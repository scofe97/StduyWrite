# 14-01 §2 — RTT 표본 하나가 RTO 로 바뀌는 계산 순서. 문서 §2 의 식과 기호를 그대로 쓴다.
# 사실 출처: 원서 §14.3.2(Err · srtt · rttvar 갱신, 이득 g = 1/8 · h = 1/4), §14.3.2.1(RTO = max(srtt + max(G, 4·rttvar), 1000ms)),
#   RFC 6298 §2(2.3 RTO ← SRTT + max(G, K·RTTVAR), K = 4; 2.4 1초 미만이면 1초로 올림).
# 타입 스펙: type-flowchart — 위에서 아래로. 시작·끝은 둥근 칸, 계산은 사각, 1초 하한 판단은 마름모, 두 갱신이 합류하는 점은 작은 점.
#           Layout conventions: 920px 캔버스, 계산 칸 높이 56–64px, 세로 stride 88px, 좌표 4의 배수.
#           focal 은 평균과 편차가 합쳐지는 RTO 식 한 칸.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, WARN, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 712
CX = 460
d = D(W, H, "TCP/IP ILLUSTRATED VOL.1 · 14-01 §2",
      "RTT 표본 하나가 RTO 가 되는 순서",
      "새 RTT 표본 M 이 오면 갱신 전 srtt 와의 차이 Err 를 먼저 구한다. 같은 Err 로 평균 srtt 는 1/8, 편차 rttvar 는 1/4 만큼 움직이고, "
      "RTO 는 평균에 편차 네 배(또는 타이머 정밀도 G 중 큰 값)를 더해 정한다. RFC 6298 은 그 결과가 1초보다 작으면 1초로 올리도록 권고한다.",
      "평균과 편차를 따로 갱신한 뒤 한 식에서 합칩니다")

def card(x, y, w, h, title, sub, c=INK, rx=6, focal=False, tc=None):
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, y, w, h, PAPER2, RULE, 1.0, rx)
    mono = all(ord(ch) < 0x3000 for ch in title)
    d.t(x + w / 2, y + h / 2 - 3, title, 14, tc or (ACC if focal else c), MONO if mono else KR, "middle", 600)
    d.t(x + w / 2, y + h / 2 + 17, sub, 12, MUTED, KR)

# 1 · 시작
card(260, 104, 400, 56, "RTT 표본 M", "보낸 바이트를 덮는 ACK 의 왕복 시간", rx=24)
d.arrow([(CX, 164), (CX, 188)], MUTED, "ar", 1.5)
# 2 · 오차
card(260, 192, 400, 56, "Err = M − srtt", "갱신 전 srtt 로 계산")
# 3 · 두 갈래 갱신
d.path(f"M {CX} 252 L {CX} 264 L 248 264 L 248 276", MUTED, 1.5, m="ar")
d.path(f"M {CX} 264 L 672 264 L 672 276", MUTED, 1.5, m="ar")
card(48, 280, 400, 64, "srtt ← srtt + (1/8)·Err", "평균 · 이득 g = 1/8", tc=INFO)
card(472, 280, 400, 64, "rttvar ← rttvar + (1/4)·(|Err| − rttvar)", "편차 · 이득 h = 1/4 · 더 빨리 반응", tc=WARN)
# 합류
d.path("M 248 344 L 248 364 L 456 364", MUTED, 1.5)
d.path("M 672 344 L 672 364 L 464 364", MUTED, 1.5)
d.o.append(f'<circle cx="{CX}" cy="364" r="4" fill="{INK}"/>')
d.arrow([(CX, 368), (CX, 380)], MUTED, "ar", 1.5)
# 4 · RTO 식 (focal)
card(220, 384, 480, 64, "RTO ← SRTT + max(G, 4·RTTVAR)", "RFC 6298 · G 는 타이머 정밀도", focal=True)
d.arrow([(CX, 452), (CX, 468)], MUTED, "ar", 1.5)
# 5 · 1초 하한 판단
DY, HW, HH = 508, 120, 36
d.o.append(f'<polygon points="{CX},{DY - HH} {CX + HW},{DY} {CX},{DY + HH} {CX - HW},{DY}" fill="{PAPER2}" stroke="{RULE}" stroke-width="1.0"/>')
d.t(CX, DY + 5, "RTO 가 1초 미만", 13, INK, KR, "middle", 600)
d.arrow([(CX + HW + 4, DY), (676, DY)], WARN, "warn", 1.5)
d.t(CX + HW + 32, DY - 8, "예", 12, WARN, KR, "middle", 600)
card(680, 484, 192, 48, "1초로 올림", "RFC 6298 권고 하한", tc=WARN)
d.arrow([(CX, DY + HH + 4), (CX, 572)], OK, "ok", 1.5)
d.t(CX + 28, DY + HH + 20, "아니오", 12, OK, KR, "middle", 600)
# 6 · 끝
card(300, 576, 320, 48, "재전송 타이머 설정", "다음 표본이 올 때까지 이 값으로 대기", rx=24)
d.arrow([(776, 536), (776, 600), (624, 600)], WARN, "warn", 1.5)

d.legend(H - 56, [("평균과 편차가 합쳐지는 식", ACC), ("평균 갱신", INFO), ("편차 갱신 · 하한 적용", WARN), ("그대로 사용", OK)])
d.save("14-01.rto-estimator.svg")

# 00-03-broadcast-scope — 브로드캐스트는 한 동네를 벗어나지 못한다
# 본문 요구: "점선 안이 ARP 물음이 닿는 범위. 라우터가 경계이고 그 너머로는 한 발짝도 안 나간다."
# 타입 스펙: type-nested.md — 점선 경계 안이 브로드캐스트 도메인이고, 라우터와 그 너머 호스트는
#           경계 밖에 둔다. 안과 밖의 구분 자체가 논지라 포함이 배치 문법이다.
# 이력: 2026-08-28 신설. 생성기 없이 손으로 만들어진 SVG 였다. 주소·좌표를 그대로 옮겼다.
import ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, BAD, INFO, PAPER2, KR, MONO

W, H = 1000, 430
d = D(W, H, "SCOPE · BROADCAST DOMAIN",
      "브로드캐스트는 한 동네를 벗어나지 못한다",
      "스위치에 붙은 호스트 넷을 점선 경계로 묶어 브로드캐스트가 닿는 범위를 보이고, "
      "라우터 너머의 호스트는 경계 밖에 두어 닿지 않음을 표시한 도식.",
      lead="점선 안이 ARP 물음이 닿는 범위입니다. 라우터가 경계이고, 그 너머로는 한 발짝도 나가지 않습니다.")

# 브로드캐스트 도메인 경계
d.o.append(f'<rect x="60" y="132" width="560" height="196" rx="8" fill="none" '
           f'stroke="{ACC}" stroke-width="1.2" stroke-dasharray="6 5"/>')
ddx.ring_label(d, 60, 132, "브로드캐스트 도메인 · 192.168.0.0/24", 12, ACC, off=24)

# 스위치와 그 아래 호스트 넷
d.box(290, 176, 120, 60, PAPER2, RULE, 1.0, 6)
d.t(350, 204, "스위치", 13, INK, KR, "middle", 600)
d.t(350, 222, "L2", 11, MUTED, MONO)
HOSTS = [(84, "192.168.0.11"), (196, "192.168.0.12"), (400, "192.168.0.13"), (512, "192.168.0.14")]
d.line(350, 236, 350, 252, RULE, 0.8)
d.line(128, 252, 556, 252, RULE, 0.8)
for x, ip in HOSTS:
    cx = x + 44
    d.line(cx, 252, cx, 268, RULE, 0.8)
    d.box(x, 268, 88, 48, PAPER2, RULE, 1.0, 6)
    d.t(cx, 298, ip, 11, INFO, MONO)

# 경계 밖 — 라우터와 그 너머
d.line(620, 206, 656, 206, RULE, 0.8)
d.box(660, 176, 120, 60, PAPER2, BAD, 1.1, 6)
d.t(720, 204, "라우터", 13, INK, KR, "middle", 600)
d.t(720, 222, "여기서 막힌다", 12, BAD, KR)
d.box(838, 176, 120, 60, PAPER2, RULE, 1.0, 6)
d.t(898, 200, "10.0.5.9", 11, MUTED, MONO)
d.t(898, 222, "못 듣는다", 12, MUTED, KR)

d.t(60, 356, "그래서 다른 동네 기계의 MAC 은 알아낼 방법이 없고, 대신 게이트웨이의 MAC 을 적습니다.", 12, MUTED, KR, "start")
d.legend(372, [("도메인 안 호스트", INFO), ("경계", ACC), ("여기서 멈춘다", BAD)])
d.save("00-03-broadcast-scope.svg")
print("ok broadcast-scope")

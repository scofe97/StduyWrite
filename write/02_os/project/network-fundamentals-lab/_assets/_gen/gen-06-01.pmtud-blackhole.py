# 06-01 학습 목표 뒤 — PMTUD 가 도는 길과 ICMP 가 막혔을 때 빠지는 자리.
# 타입 스펙: type-flowchart — 두 번째 걸음에서 ICMP 허용 여부로 갈라져 서로 다른 결말로
#           간다. 분기가 그림의 논점이라 단계 나열(process)이 아니라 flowchart 를 쓴다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, BAD, OK, WARN, KR, MONO

W, H = 880, 460
d = D(W, H, "NETWORK FUNDAMENTALS LAB · 06-01",
      "PMTUD 가 도는 길과 침묵당하는 자리",
      "발신자가 DF 로 보내고 좁은 링크의 라우터가 ICMP frag-needed 로 알려 주면 경로 MTU 를 학습한다. 그 ICMP 가 막히면 학습이 영원히 일어나지 않는다.",
      "메커니즘 전체가 ICMP 한 종류에 걸려 있다")

# 1·2 단계
d.box(24, 104, 392, 76, PAPER2, RULE, 1.0, 8)
d.t(44, 132, "1. 발신자가 DF 를 켜고 보낸다", 14, INK, KR, "start", 600)
d.t(44, 158, "자기 링크 MTU 기준 — 경로는 모른다", 12, MUTED, KR, "start")

d.box(464, 104, 392, 76, PAPER2, RULE, 1.0, 8)
d.t(484, 132, "2. 좁은 라우터가 버리고 알린다", 14, INK, KR, "start", 600)
d.t(484, 158, "ICMP frag-needed — \"MTU 는 1400 이다\"", 12, MUTED, KR, "start")

d.arrow([(416, 142), (460, 142)], MUTED, "ar", 1.4)

# 분기점
d.path("M 660 180 V 206", MUTED, 1.4)
d.chip(660, 218, "그 ICMP 가 발신자에게 닿는가", SOFT)

# 두 결말
d.path("M 660 232 V 252 H 220 V 272", OK, 1.5, m="ok")
d.path("M 660 232 V 252 H 660 V 272", BAD, 1.5, m="bad")
d.t(300, 246, "닿는다", 12, OK, KR, "middle", 600)
d.t(700, 246, "막혀 있다", 12, BAD, KR, "middle", 600)

d.tone(24, 276, 392, 110, OK, 8, "10", 1.3)
d.t(44, 306, "3. 경로 MTU 를 학습한다", 14, OK, KR, "start", 600)
d.t(44, 332, "ip route get 의 캐시에 mtu 가 붙는다", 12, MUTED, KR, "start")
d.t(44, 358, "모든 프로토콜이 경로를 배운다", 12, OK, KR, "start", 600)

d.tone(464, 276, 392, 110, BAD, 8, "10", 1.3)
d.t(484, 306, "블랙홀 — 영원히 모른다", 14, BAD, KR, "start", 600)
d.t(484, 332, "같은 크기로 재전송하다 포기한다", 12, MUTED, KR, "start")
d.t(484, 358, "작은 것은 통과하므로 연결은 된다", 12, BAD, KR, "start", 600)

d.t(24, 428, "MSS clamp 는 오른쪽 결말에서 TCP 만 건져 낸다 — UDP·ICMP·터널은 그대로 죽는다",
    12, WARN, KR, "start", 600)
d.save("06-01.pmtud-blackhole.svg")

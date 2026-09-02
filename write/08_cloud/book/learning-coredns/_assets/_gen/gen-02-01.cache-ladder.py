# 02-01 §7 — 캐시가 차 있으면 같은 질의도 사다리의 아래쪽에서 시작한다.
# 원문 근거: www.google.com 의 AAAA 를 푼 서버는 com 의 NS 와 주소, google.com 의 NS 와 주소,
#            www.google.com 의 IPv6 주소를 알게 된다 / 곧이어 maps.google.com 질의가 오면
#            "it can skip querying a root DNS server or a com DNS server and query a google.com
#             DNS server first" / infoblox.com 의 MX 는 "could begin at the com DNS servers,
#            saving at least the roundtrip to a root DNS server".
# 타입 스펙: type-gantt — 막대의 시작점과 길이가 곧 밟아야 할 구간이다.
#           축약: 가로축이 시간이 아니라 해석 사다리(루트 → TLD → 권한 서버)의 단계다.
#           축 라벨을 특정 도메인으로 적으면 infoblox.com 행이 google.com 서버를 거치는 것처럼
#           읽히므로 단계 이름으로 일반화한다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, RULE, INFO, KR, MONO

W, H = 1000, 484
d = D(W, H, "LEARNING COREDNS · 02-01 §7",
      "캐시는 사다리의 시작점을 끌어내린다",
      "가로축은 시간이 아니라 해석 사다리의 단계다. 막대가 짧을수록 그 질의가 실제로 밟은 구간이 짧고, "
      "짧아진 만큼이 앞선 질의가 캐시에 남긴 것이다.",
      "첫 막대가 다음 두 막대의 시작점을 만들었습니다")

LX, TX, TW = 20, 220, 740
STEPS = ["루트 서버", "TLD 서버", "권한 서버", "응답"]
PITCH = TW / len(STEPS)
for i, nm in enumerate(STEPS):
    d.t(TX + PITCH * i + PITCH / 2, 112, nm, 12, SOFT, MONO)
d.line(TX, 124, TX + TW, 124, RULE, 1.0)

rows = [
    ("www.google.com AAAA", "맨 처음 · 캐시가 비어 있다", 0, 4, ACC),
    ("maps.google.com", "루트와 com 을 건너뛴다", 2, 2, INFO),
    ("infoblox.com MX", "루트만 건너뛴다 · 권한 서버는 infoblox.com", 1, 3, INFO),
]
for i, (nm, sub, start, span, color) in enumerate(rows):
    ry = 148 + i * 76
    d.t(LX, ry + 22, nm, 13, INK, MONO, "start", 600)
    d.t(LX, ry + 44, sub, 12, MUTED, KR, "start")
    for s in range(len(STEPS)):
        d.line(TX + PITCH * s, ry + 4, TX + PITCH * s, ry + 60, RULE, 0.6, "3 5")
    x = TX + PITCH * start
    w = PITCH * span
    d.tone(x, ry + 14, w, 34, color, 4, "16", 1.2)
    d.t(x + w / 2, ry + 36, f"{span}단계", 13, color, KR)

d.t(LX, 388, "TTL 이 남아 있는 동안만 짧아진다 — 루트 서버 열세 대가 버티는 이유가 이 절약이다", 13, MUTED, KR, "start")

d.legend(412, [("캐시가 빈 첫 질의", ACC), ("캐시가 만든 지름길", INFO)])
d.save("02-01.cache-ladder.svg")

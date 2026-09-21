# 2026-09-14 E(힙은 평평한데) 문항 · 문제 소개 — 무대.
# 어떤 겹 안에서 무엇이 한도를 받고 무엇이 그 한도를 모르는지 그린다. 사건은 heap-flat-rss-climb 가 맡는다.
# 타입 스펙: type-nested — 포함·범위로 드러나는 계층. 겹마다 "누가 정한 한도인가"를 적는다.
#           type-architecture 를 검토했으나 호출 경로가 아니라 포함 관계가 논지라 기각.
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dd import D, ACC, OK, INFO, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 476
d = D(W, H, "TROUBLESHOOTING DRILL · 2026-09-14 E",
      "한도를 받은 겹과 그 한도를 모르는 겹",
      "40 코어 노드 위에 CPU 2 코어와 메모리 4 GB 를 받은 컨테이너가 있고, 그 안의 JVM 은 한도의 70% 를 최대 힙으로 잡는다. "
      "JVM 은 cgroup 을 읽어 자기 몫을 알지만, 그 밑의 C 라이브러리는 cgroup 이 아니라 기계에 코어 수를 묻는다.",
      lead="같은 컨테이너 안에서 JVM 은 2 를 보고 C 라이브러리는 40 을 봅니다")

RINGS = [(24, 96, 600, 336), (64, 144, 520, 264), (104, 192, 440, 176)]
STROKE = [f"{INK}30", f"{INK}44", f"{INK}58"]
for i, (x, y, w, h) in enumerate(RINGS):
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="none" '
               f'stroke="{STROKE[i]}" stroke-width="1.0"/>')

d.t(40, 124, "노드", 12, SOFT, KR, "start", 600)
d.t(40, 144, "40 코어", 12, MUTED, MONO, "start")
d.t(80, 172, "컨테이너 · cgroup 한도", 12, SOFT, KR, "start", 600)
d.t(80, 192, "CPU 2 · MEM 4 GB · requests = limits", 12, MUTED, MONO, "start")
d.t(120, 220, "JVM", 12, SOFT, KR, "start", 600)
d.t(120, 240, "G1 · MaxRAMPercentage=70 → 최대 힙 2.8 GB", 12, MUTED, MONO, "start")

# 가장 안쪽 — 이 문항의 focal 은 한도를 모르는 쪽이다
IX, IY, IW, IH = 136, 264, 376, 88
d.tone(IX, IY, IW, IH, ACC, 6)
d.t(IX + 20, IY + 30, "C 라이브러리의 malloc", 13, ACC, KR, "start", 600)
d.t(IX + 20, IY + 54, "코어 수를 기계에 묻는다 · cgroup 을 읽지 않음", 12, MUTED, KR, "start")
d.t(IX + 20, IY + 74, "JVM 이 세지 않는 몫", 12, ACC, KR, "start")

# 오른쪽 — 컨테이너 안에서 도는 것들
BX, BW, BH2 = 672, 288, 76
ROWS = [("Lettuce · Netty", "Redis 경로 · 이벤트 루프 스레드", INFO),
        ("OpenTelemetry 에이전트", "계측 스레드와 할당 경로", INFO),
        ("힙 대시보드", "최대 힙의 40~50% 에서 평평", OK)]
for i, (t1, t2, c) in enumerate(ROWS):
    y2 = 112 + i * 100
    d.box(BX, y2, BW, BH2, PAPER2, RULE, 0.9, 6)
    d.t(BX + 20, y2 + 30, t1, 13, c, KR, "start", 600)
    d.t(BX + 20, y2 + 54, t2, 12, MUTED, KR, "start")

d.legend(420, [("한도를 모르는 겹", ACC), ("스레드를 늘리는 것", INFO),
               ("평평했던 지표", OK), ("겹의 경계", INK)])
d.save(os.path.join(os.path.dirname(__file__), "..", "2026-09-21.runtime-stage.svg"))
print("ok")

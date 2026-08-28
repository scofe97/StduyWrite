# 18-03 전체 지도 — Job 을 넓히고 시간표에 올린다
# 본문이 "위 두 층은 Job 하나를 넓히는 이야기이고, 맨 아래 CronJob 은 층위가 다르다"고 못박는다.
# 그러니 셋을 나란히 두면 안 되고, CronJob 이 바깥 껍질로 보여야 한다.
# 타입 스펙: type-architecture.md — 안쪽 경계 상자가 "Job 하나를 넓히는" 영역이고, 바깥 CronJob 이 그 영역으로 되돌아오는
#           화살표로 Job 을 만들어 넣는다 — 영역 경계와 그것을 먹이는 초점 노드라는 architecture 의
#           구성이다. nested 는 후보에서 뺐다 — 그 정본은 동심 링 3~5 겹이 계약인데 여기 껍질은
#           둘러싸는 대신 아래에 놓이고 화살표로만 안을 가리킨다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO
import ddx

d = D(1200, 704, "KUBERNETES IN ACTION · 18-03",
      "Job 을 넓히는 일과 시간표에 올리는 일",
      "앞 두 축은 Job 하나 안에서 무엇을 더 할 수 있는지를 다룬다. CronJob 은 그 Job 을 고치는 것이 "
      "아니라, 만들어 주는 바깥 껍질이다.",
      "§1 큐 · §2 통신 · §3 사이드카 · §4~§6 CronJob")

d.box(90, 168, 1020, 244, PAPER, RULE, 0.9, 8)
d.t(600, 196, "Job 하나를 넓힌다", 11, SOFT, KR)
INNER = [("§1  큐", "일을 미리 나누지 않고", "파드가 꺼내 쓴다"),
         ("§2  통신", "인덱스 Job 의 파드가", "DNS 로 서로를 찾는다"),
         ("§3  사이드카", "Job 파드에 넣는", "자리가 따로 있다")]
for i, (t, l1, l2) in enumerate(INNER):
    cx = 250 + i * 350
    d.box(cx - 150, 232, 300, 144, PAPER2, INFO, 1.1, 6)
    d.t(cx, 268, t, 13, INFO, KR, "middle", 600)
    d.t(cx, 300, l1, 11, MUTED, KR)
    d.t(cx, 324, l2, 11, MUTED, KR)

d.o.append(f'<rect x="60" y="440" width="1080" height="128" rx="8" '
           f'fill="{ACC}0A" stroke="{ACC}" stroke-width="1.4"/>')
d.t(600, 470, "§4~§6  CronJob — 층위가 다르다", 13, ACC, KR, "middle", 600)
d.t(600, 500, "Job 을 고치는 것이 아니라, 시간표에 올려 그 Job 을 만들어 주는 바깥 껍질이다", 11, MUTED, KR)
d.t(600, 534, "schedule · concurrencyPolicy · 보존 개수", 11, ACC, MONO)
d.path("M 600 576 L 600 600 L 40 600 L 40 290 L 84 290", ACC, 1.4, m="acc", dash="6 5")
# y=330 은 안쪽 상자(168~412) 높이 안이라 그 왼쪽 변이 글자를 지나갔다. 두 블록 사이 빈
# 구간(412~440)으로 내리면 같은 화살표 옆에 있으면서 어느 상자도 건드리지 않는다.
d.t(56, 430, "때가 되면 Job 을 만든다", 10, ACC, KR, "start")

d.t(24, 624, "그래서 CronJob 안에는 jobTemplate 이 통째로 들어간다 — 위 두 층에서 정한 것이 그 안에 그대로 실린다.",
     11, MUTED, KR, "start")
d.legend(656, [("Job 하나 안", INFO), ("바깥 껍질", ACC)])
d.save("18-03.chapter-overview.svg")
print("ok")

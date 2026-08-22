# 18-03 §4 — 껍질이 만드는 것은 Job 이지 파드가 아니다
# CronJob 이 파드를 직접 만든다고 오해하기 쉬운 자리다. 그러니 층을 하나 더 두어
# CronJob → Job → 파드 순서가 그림에서 강제돼야 한다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO
import ddx

d = D(1240, 620, "KUBERNETES IN ACTION · 18-03",
      "CronJob 이 만드는 것은 Job 이다",
      "시간표에 맞춰 CronJob 컨트롤러가 새 Job 오브젝트를 만든다. 파드를 만드는 것은 그 Job 이고, "
      "컨테이너를 띄우는 것은 kubelet 이다 — 층이 하나 더 늘었을 뿐이다.",
      "schedule: 0 * * * *")

ddx.node(d, 170, 300, "CronJob", "schedule · jobTemplate", 240, 96, ACC)

d.path("M 292 300 L 380 300", ACC, 1.3)
d.path("M 380 200 L 380 400", ACC, 1.3)
for i, (t, when) in enumerate((("Job  #1", "01:00"), ("Job  #2", "02:00"), ("Job  #3", "03:00"))):
    cy = 200 + i * 100
    ddx.node(d, 600, cy, t, when, 240, 72, INFO)
    d.path(f"M 380 {cy} L 474 {cy}", ACC, 1.3, m="acc")
    ddx.node(d, 1000, cy, "파드", "완료까지 실행", 220, 72, OK)
    d.path(f"M 722 {cy} L 884 {cy}", OK, 1.3, m="ok")

d.t(383, 176, "때가 되면 만든다", 10, ACC, KR)
d.t(803, 176, "Job 이 만든다", 10, OK, KR)

d.t(24, 470, "그래서 CronJob 안에는 jobTemplate 이 통째로 들어간다. completions·parallelism·backoffLimit 처럼 "
             "18-02 에서 정한 것이 그 안에 그대로 실린다.", 11, MUTED, KR, "start")
d.t(24, 492, "보존 개수(successfulJobsHistoryLimit·failedJobsHistoryLimit)를 두는 이유도 여기 있다 — "
             "때마다 Job 오브젝트가 하나씩 쌓이기 때문이다.", 11, MUTED, KR, "start")
d.legend(520, [("시간표", ACC), ("만들어지는 Job", INFO), ("그 Job 의 파드", OK)])
d.save("18-03-cronjob-operation.svg")
print("ok")

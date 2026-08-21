# 18-01 §2 — Always 는 끝을 못 본다
# 캡션이 "성공해도 재시작해 CrashLoopBackOff 에 머문다"고 결과까지 말한다. 그러니 세 값을
# 비교하는 표가 아니라, 성공 뒤에 무슨 일이 나는지가 경로로 갈려야 한다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, WARN, BAD, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO
import ddx

d = D(1240, 640, "KUBERNETES IN ACTION · 18-01",
      "성공했는데 다시 시작한다",
      "Always 는 컨테이너가 끝나면 이유를 묻지 않고 다시 띄운다. 그래서 Job 이 기다리는 "
      "'성공하고 끝난 상태'에 도달하지 못한다.",
      "그래서 Job 의 restartPolicy 는 OnFailure 나 Never 여야 한다")

ddx.node(d, 170, 300, "컨테이너 종료", "exit 0 — 성공", 220, 84, INFO)

d.path("M 282 268 L 380 200", BAD, 1.5, m="bad")
ddx.node(d, 560, 200, "Always", "이유를 묻지 않고 재시작", 280, 76, BAD)
d.path("M 702 200 L 800 200", BAD, 1.4, m="bad")
ddx.tag(d, 990, 200, "CrashLoopBackOff", BAD, 300)
d.t(990, 240, "Completed 에 이르지 못한다", 10, BAD, KR)

d.path("M 282 332 L 380 400", OK, 1.5, m="ok")
d.o.append(f'<rect x="{560-140}" y="362" width="280" height="76" rx="6" '
           f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t(560, 392, "OnFailure · Never", 13, ACC, KR, "middle", 600)
d.t(560, 416, "성공하면 그대로 둔다", 10, MUTED, KR)
d.path("M 702 400 L 800 400", OK, 1.4, m="ok")
ddx.node(d, 990, 400, "Completed", "Job 이 한 번 채워진다", 300, 76, OK)

d.t(24, 500, "Deployment 의 기본값이 Always 인 것은 계속 도는 것이 정상이기 때문이다. Job 은 반대라, "
             "같은 기본값이 여기서는 끝을 막는다.", 11, MUTED, KR, "start")
d.t(24, 522, "그래서 Job 매니페스트에서 restartPolicy 는 생략할 수 없는 필드가 된다 — API 가 Always 를 거부한다.",
     11, MUTED, KR, "start")
d.legend(552, [("끝나지 못한다", BAD), ("끝에 이른다", OK), ("Job 이 쓸 수 있는 값", ACC)])
d.save("18-01-always-blocks.svg")
print("ok")

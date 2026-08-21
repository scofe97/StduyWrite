# 09-02 §2 — 같은 파드가 다른 노드로 가면 다른 데이터를 본다
# hostPath 의 위험은 "노드에 묶인다"는 문장보다 그 결과에 있다. 그러니 노드 둘을 놓고 같은
# 경로가 서로 다른 내용을 담고 있음을 보여야 한다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, WARN, BAD, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO
import ddx

d = D(1200, 620, "KUBERNETES IN ACTION · 09-02",
      "경로는 같은데 내용이 다르다",
      "hostPath 는 그 파드가 뜬 노드의 파일시스템을 가리킨다. 파드가 다른 노드로 옮겨 가면 같은 경로를 "
      "마운트하고도 전혀 다른 내용을 본다.",
      "데이터베이스 데이터를 hostPath 에 두면 안 되는 이유")

for i, (nm, files, c) in enumerate((("노드 A", ("questions.json", "answers.json"), OK),
                                    ("노드 B", ("(비어 있다)",), BAD))):
    x0 = 90 + i * 560
    d.box(x0, 176, 460, 224, PAPER, RULE, 0.9, 8)
    d.t(x0 + 230, 204, nm, 11, SOFT, KR)
    d.t(x0 + 230, 236, "/var/lib/quiz-data", 11, MUTED, MONO)
    for j, f in enumerate(files):
        d.t(x0 + 230, 288 + j * 26, f, 11, c, MONO)
    ddx.node(d, x0 + 230, 366, "파드", "같은 매니페스트", 240, 48, c)

ddx.focal_tag(d, 600, 288, "같은 경로", 150)
d.t(600, 328, "다른 파일시스템", 11, ACC, KR)

d.t(24, 456, "그래서 hostPath 는 노드 자신의 것을 읽어야 할 때만 쓴다 — 로그 수집기가 /var/log 를 읽거나, "
             "모니터링 에이전트가 노드 메트릭을 보는 경우다.", 11, MUTED, KR, "start")
d.t(24, 478, "그런 워크로드는 대개 DaemonSet 으로 배포돼 노드마다 하나씩 도므로, '노드에 묶인다'는 성질이 "
             "결함이 아니라 조건이 된다(17 장).", 11, MUTED, KR, "start")
d.legend(508, [("데이터가 있는 노드", OK), ("옮겨 간 노드", BAD), ("같은 선언, 다른 실체", ACC)])
d.save("09-02-hostpath-node-bound.svg")
print("ok")

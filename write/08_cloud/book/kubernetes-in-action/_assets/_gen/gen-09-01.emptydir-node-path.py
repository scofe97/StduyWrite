# 09-01 §3 — 복사본이 아니라 같은 실체를 두 곳에서 본다
# 본문이 "노드의 ls 결과와 컨테이너 안 ls 가 한 글자도 다르지 않았다"를 근거로 든다.
# 그러니 두 경로를 잇는 화살표가 아니라, 같은 것을 가리키고 있음이 보여야 한다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO
import ddx

d = D(1220, 640, "KUBERNETES IN ACTION · 09-01",
      "복사본이 아니라 같은 디렉터리다",
      "emptyDir 의 파일은 호스트 노드 파일시스템의 평범한 디렉터리에 있다. 마운트는 그것을 컨테이너의 "
      "원하는 위치에서 보이게 할 뿐, 별도의 복사본을 만들지 않는다.",
      "kind 워커에서 두 ls 결과가 한 글자도 다르지 않았다")

d.box(60, 176, 480, 200, PAPER, RULE, 0.9, 8)
d.t(300, 204, "노드에서 본 경로", 11, SOFT, KR)
d.t(84, 240, "/var/lib/kubelet/pods/<pod_UID>", 11, MUTED, MONO, "start")
d.t(84, 262, "  /volumes/kubernetes.io~empty-dir/quiz-data", 11, MUTED, MONO, "start")
for i, f in enumerate(("WiredTiger", "_mdb_catalog.wt", "collection-5b3e9bdf-….wt")):
    d.t(104, 300 + i * 22, f, 10, SOFT, MONO, "start")

d.box(680, 176, 480, 200, PAPER, RULE, 0.9, 8)
d.t(920, 204, "컨테이너에서 본 경로", 11, SOFT, KR)
d.t(704, 252, "/data/db", 11, MUTED, MONO, "start")
for i, f in enumerate(("WiredTiger", "_mdb_catalog.wt", "collection-5b3e9bdf-….wt")):
    d.t(724, 300 + i * 22, f, 10, SOFT, MONO, "start")

d.o.append(f'<rect x="{610-130}" y="420" width="260" height="56" rx="6" '
           f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t(610, 454, "같은 실체", 14, ACC, KR, "middle", 600)
d.path("M 300 380 L 540 424", ACC, 1.5, m="acc")
d.path("M 920 380 L 680 424", ACC, 1.5, m="acc")
d.t(610, 400, "mount", 11, SOFT, MONO)

d.t(24, 522, "이 경로는 kubelet 의 구현 세부이지 보장된 API 가 아니다. 실습에서 눈으로 확인하는 데는 쓸모 있지만 "
             "스크립트가 이 경로를 전제로 동작하게 짜지 않는다.", 11, MUTED, KR, "start")
d.t(24, 544, "디렉터리 이름에 pod_UID 가 들어간다. 같은 파드가 유지되는 한 UID 가 그대로라 재시작해도 같은 디렉터리를 "
             "다시 마운트하지만, 파드가 교체되면 UID 가 바뀌어 데이터가 따라오지 않는다.", 11, MUTED, KR, "start")
d.legend(572, [("두 경로가 가리키는 하나", ACC)])
d.save("09-01-emptydir-node-path.svg")
print("ok")

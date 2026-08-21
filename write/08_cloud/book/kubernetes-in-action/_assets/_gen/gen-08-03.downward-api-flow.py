# 08-03 §4 — 값의 출처가 Pod 자신이다
# 본문이 "ConfigMap·Secret 주입과 다를 게 없고, 값의 출처가 Pod 오브젝트 자신이라는 점만
# 다르다"고 못박는다. 그러니 새 구조로 그리면 안 되고, 같은 골격에 출처만 바뀐 그림이어야 한다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO
import ddx

d = D(1240, 660, "KUBERNETES IN ACTION · 08-03",
      "값의 출처가 Pod 오브젝트 자신이다",
      "애플리케이션이 호출하는 REST 엔드포인트가 아니다. Pod 매니페스트의 metadata·spec·status 값을 "
      "컨테이너로 주입하는 방식이라 '아래로'라는 이름이 붙었다.",
      "ConfigMap·Secret 주입과 골격이 같다 — 출처만 다르다")

d.box(60, 168, 320, 268, PAPER, RULE, 0.9, 8)
d.t(220, 196, "Pod 오브젝트", 11, SOFT, KR)
for i, (t, s) in enumerate((("metadata", "name · namespace · labels"),
                            ("spec", "nodeName · serviceAccountName"),
                            ("status", "podIP · hostIP"))):
    ddx.node(d, 220, 250 + i * 68, t, s, 280, 54, INFO)

REF = [("fieldRef", "Pod 의 일반 메타데이터", 250, ACC),
       ("resourceFieldRef", "컨테이너의 CPU·메모리 제약", 340, ACC)]
for t, s, cy, c in REF:
    d.box(460, cy - 32, 300, 64, PAPER2, c, 1.2, 6)
    d.t(610, cy - 6, t, 12, c, MONO, "middle", 600)
    d.t(610, cy + 16, s, 10, MUTED, KR)
d.path("M 362 290 L 452 262", ACC, 1.4, m="acc")
d.path("M 362 350 L 452 340", ACC, 1.4, m="acc")
d.t(610, 400, "valueFrom 아래 — configMapKeyRef 가 있던 그 자리", 10, SOFT, KR)

d.box(830, 168, 350, 268, PAPER, RULE, 0.9, 8)
d.t(1005, 196, "컨테이너", 11, SOFT, KR)
ddx.node(d, 1005, 262, "환경변수", "POD_IP · NODE_NAME", 300, 62, OK)
ddx.node(d, 1005, 366, "downwardAPI 볼륨", "파일로도 받는다", 300, 62, OK)
d.path("M 762 262 L 848 262", OK, 1.4, m="ok")
d.path("M 762 348 L 848 360", OK, 1.4, m="ok")

d.t(24, 496, "이렇게 전달할 수밖에 없는 값이 두 부류다. 하나는 Pod 가 생성·스케줄링되기 전에는 알 수 없는 값 — "
             "Pod IP, 노드 이름, Pod 이름 자신이다.", 11, MUTED, KR, "start")
d.t(24, 518, "다른 하나는 매니페스트의 다른 곳에 이미 적힌 값이다. 컨테이너의 CPU·메모리 할당량이 그렇고, "
             "직접 적으면 같은 값을 두 번 쓰게 된다.", 11, MUTED, KR, "start")
d.legend(548, [("값의 출처", INFO), ("주입 방식", ACC), ("받는 자리", OK)])
d.save("08-03-downward-api-flow.svg")
print("ok")

# 08-02 §1 — 같은 값이 두 경로로 들어간다
# 본문이 "앱이 REST API 로 ConfigMap 을 읽게 하지 않는다"를 전제로 깔고 두 주입 경로를 든다.
# 그러니 앱이 쿠버네티스를 모른다는 사실이 그림에 남아 있어야 한다.
# 타입 스펙: type-architecture.md — ConfigMap 에서 환경변수 경로와 볼륨 경로 둘로 갈려 컨테이너 상자 안으로 들어가는 구성도다.
#           앱이 쿠버네티스를 모른다는 사실이 컨테이너 경계 안쪽 노드로 남아 있다.
#           type-data-flow 는 역할 레인 1~4 × 단계 열 × 타입 있는 페이로드 칩이 입력 계약인
#           데이터 플랫폼 전용 타입이라 여기엔 맞지 않는다. type-architecture 의 Best for 에
#           "data-flow diagrams" 가 그대로 들어 있다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO
import ddx

d = D(1200, 620, "KUBERNETES IN ACTION · 08-02",
      "앱은 쿠버네티스를 모른 채로 값을 받는다",
      "애플리케이션이 REST API 로 ConfigMap 을 읽게 하지 않는다. 쿠버네티스가 값을 프로세스 환경이나 "
      "파일시스템에 미리 놓아 주고, 앱은 평소 하던 대로 읽는다.",
      "Pod 는 ConfigMap 을 이름으로 참조한다")

ddx.node(d, 170, 300, "ConfigMap", "key-value 목록", 240, 96, INFO)

d.box(430, 168, 320, 112, PAPER2, OK, 1.1, 6)
d.t(590, 200, "환경변수로", 13, OK, KR, "middle", 600)
d.t(590, 226, "valueFrom.configMapKeyRef", 10, MUTED, MONO)
d.t(590, 252, "envFrom 으로 통째로도", 10, MUTED, KR)
d.path("M 292 276 L 356 276 L 356 224 L 424 224", OK, 1.5, m="ok")

d.box(430, 320, 320, 112, PAPER2, ACC, 1.1, 6)
d.t(590, 352, "configMap 볼륨으로", 13, ACC, KR, "middle", 600)
d.t(590, 378, "컨테이너 파일시스템에 파일로", 10, MUTED, KR)
d.t(590, 404, "/etc/config/app.yaml", 10, MUTED, MONO)
d.path("M 292 324 L 356 324 L 356 376 L 424 376", ACC, 1.5, m="acc")

d.box(830, 168, 330, 264, PAPER, RULE, 0.9, 8)
d.t(995, 196, "컨테이너", 11, SOFT, KR)
ddx.node(d, 995, 250, "프로세스 환경", "System.getenv()", 280, 62, OK)
ddx.node(d, 995, 360, "파일시스템", "평소처럼 파일을 읽는다", 280, 62, ACC)
d.path("M 754 224 L 800 224 L 800 244 L 848 244", OK, 1.4, m="ok")
d.path("M 754 376 L 800 376 L 800 356 L 848 356", ACC, 1.4, m="acc")

d.t(24, 490, "핵심 이점은 환경 분리다. Pod 는 ConfigMap 을 이름으로 참조하므로, 환경마다 같은 이름의 다른 "
             "ConfigMap 을 적용해 두면 같은 Pod 매니페스트를 모든 환경에 배포할 수 있다.", 11, MUTED, KR, "start")
d.t(24, 512, "ConfigMap 과 이를 참조하는 Pod 는 같은 namespace 에 있어야 한다 — 다른 namespace 의 것은 직접 참조하지 못한다.",
     11, MUTED, KR, "start")
d.legend(540, [("설정의 출처", INFO), ("환경변수 경로", OK), ("파일 경로", ACC)])
d.save("08-02-configmap-injection.svg")
print("ok")

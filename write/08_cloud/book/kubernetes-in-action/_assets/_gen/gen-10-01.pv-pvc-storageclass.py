# 10-01 §1 — 요구와 실체 사이에 클래스가 선다
# 세 오브젝트를 나열하면 "왜 셋인가"가 안 보인다. 요구하는 쪽·만들어지는 쪽·그 사이에서
# 방법을 정하는 쪽으로 역할을 갈라 놓아야 한다.
# 타입 스펙: type-architecture.md — 파드·PVC·StorageClass·PV 네 구성 요소와 그 사이 흐름을 그린 구성도다.
#           코럴 초점은 방법을 정하는 StorageClass 하나다.
#           type-data-flow 는 역할 레인 1~4 × 단계 열 × 타입 있는 페이로드 칩이 입력 계약인
#           데이터 플랫폼 전용 타입이라 여기엔 맞지 않는다. type-architecture 의 Best for 에
#           "data-flow diagrams" 가 그대로 들어 있다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO
import ddx

d = D(1220, 640, "KUBERNETES IN ACTION · 10-01",
      "요구하는 쪽과 만들어지는 쪽",
      "파드는 얼마나·어떻게 쓸지를 PVC 로 요구하고, 그 요구를 어떤 스토리지로 어떻게 만들지는 "
      "StorageClass 가 정한다. PV 는 그 결과로 생긴 실체다.",
      "동적 프로비저닝 — 요청이 오면 그때 만든다")

ddx.node(d, 160, 220, "파드", "volumes.persistentVolumeClaim", 240, 76, INFO)
ddx.node(d, 160, 380, "PVC", "1Gi · RWOP · 클래스 이름", 240, 96, INFO)
d.path("M 160 262 L 160 328", INFO, 1.5, m="info")
d.t(176, 300, "이름으로 요구한다", 10, SOFT, KR, "start")

d.o.append(f'<rect x="{610-160}" y="332" width="320" height="96" rx="6" '
           f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t(610, 366, "StorageClass", 13, ACC, KR, "middle", 600)
d.t(610, 390, "provisioner · parameters", 10, MUTED, MONO)
d.t(610, 412, "reclaimPolicy · 볼륨 바인딩 시점", 10, MUTED, KR)
d.path("M 284 380 L 442 380", ACC, 1.5, m="acc")
d.t(363, 360, "어떻게 만들지", 10, ACC, KR)

ddx.node(d, 1060, 380, "PV", "만들어진 실체", 240, 96, OK)
d.path("M 774 380 L 932 380", OK, 1.5, m="ok")
d.t(853, 360, "프로비저너가 만든다", 10, OK, KR)
d.path("M 1060 328 L 1060 220 L 284 220", OK, 1.4, m="ok", dash="6 5")
d.t(700, 248, "바인딩된 뒤 파드에 마운트된다", 10, SOFT, KR)

d.t(24, 500, "PVC 를 쓰는 파드를 모두 지워도 PVC 는 지울 때까지 남고, PV 는 PVC 에 바인딩된 채로 있다. "
             "그래서 같은 PVC 를 다른 파드에서 다시 쓸 수 있다.", 11, MUTED, KR, "start")
d.t(24, 522, "파드는 휘발성이라 늘 교체되지만, PV 를 쓰면 노드를 몇 번 옮겨도 최신 인스턴스에 데이터가 남는다.",
     11, MUTED, KR, "start")
d.legend(548, [("요구하는 쪽", INFO), ("방법을 정하는 쪽", ACC), ("만들어진 실체", OK)])
d.save("10-01-pv-pvc-storageclass.svg")
print("ok")

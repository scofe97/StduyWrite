# 10-01 §1 — 요구와 실체 사이에 클래스가 선다
# 세 오브젝트를 나열하면 "왜 셋인가"가 안 보인다. 요구하는 쪽·만들어지는 쪽·그 사이에서
# 방법을 정하는 쪽으로 역할을 갈라 놓아야 한다.
# 타입 스펙: type-architecture.md — 파드·PVC·StorageClass·PV 네 구성 요소와 그 사이 흐름을 그린 구성도다.
#           코럴 초점은 방법을 정하는 StorageClass 하나다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, MUTED, SOFT, PAPER2, KR, MONO
import ddx

d = D(920, 530, "KUBERNETES IN ACTION · 10-01",
      "요구하는 쪽과 만들어지는 쪽",
      "파드는 얼마나·어떻게 쓸지를 PVC 로 요구하고, 그 요구를 어떤 스토리지로 어떻게 만들지는 "
      "StorageClass 가 정한다. PV 는 그 결과로 생긴 실체다.",
      "동적 프로비저닝 — 요청이 오면 그때 만든다")

ddx.node(d, 130, 195, "파드", "volumes.persistentVolumeClaim", 220, 68, INFO)
ddx.node(d, 130, 335, "PVC", "1Gi · RWOP · 클래스 이름", 220, 84, INFO)
d.path("M 130 229 L 130 288", INFO, 1.5, m="info")
d.t(145, 260, "이름으로 요구", 12, SOFT, KR, "start")

d.o.append(f'<rect x="340" y="285" width="230" height="100" rx="6" '
           f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t(455, 314, "StorageClass", 14, ACC, MONO, "middle", 600)
d.t(455, 340, "provisioner · parameters", 12, MUTED, MONO)
d.t(455, 362, "reclaimPolicy · 볼륨 바인딩 시점", 12, MUTED, KR)
d.path("M 240 335 L 335 335", ACC, 1.5, m="acc")
d.t(288, 318, "어떻게 만들지", 12, ACC, KR)

ddx.node(d, 800, 335, "PV", "만들어진 실체", 200, 84, OK)
d.path("M 570 335 L 695 335", OK, 1.5, m="ok")
d.t(632, 318, "프로비저너가 만든다", 12, OK, KR)
d.path("M 800 293 L 800 195 L 245 195", OK, 1.4, m="ok", dash="6 5")
d.t(520, 180, "바인딩 후 파드에 마운트", 12, SOFT, KR)

d.t(24, 420, "파드를 모두 지워도 PVC 는 남고 PV 는 바인딩된 채 · 같은 PVC 를 다른 파드가 다시 씀", 12, MUTED, KR, "start")
d.t(24, 444, "파드는 휘발성 · 노드를 몇 번 옮겨도 PV 의 데이터는 최신 인스턴스에 남음", 12, MUTED, KR, "start")
d.legend(470, [("요구하는 쪽", INFO), ("방법을 정하는 쪽", ACC), ("만들어진 실체", OK)])
d.save("10-01-pv-pvc-storageclass.svg")
print("ok")

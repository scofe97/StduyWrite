# 10-03 §4 — 한 번에 지워지지 않는다
# 본문이 "이 정리는 한 번에 일어나지 않고 두 단계로 진행된다"고 못박고, 2 단이 분기라고 한다.
# 그러니 삭제를 한 화살표로 그리면 안 되고 단계와 분기가 함께 보여야 한다.
# 타입 스펙: type-flowchart.md — 파드 삭제에서 1 단을 거쳐 2 단에서 reclaim policy 에 따라 두 결말로 갈린다.
#           판정 하나가 배타적 결말 둘을 만드는 구조다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, WARN, BAD, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO
import ddx

d = D(1240, 640, "KUBERNETES IN ACTION · 10-03",
      "두 단계로 지워지고, 둘째에서 갈린다",
      "1 단은 ownerReferences 가 정한다 — 자동 생성된 PVC 가 파드를 주인으로 두므로 주인이 사라지면 "
      "가비지 컬렉터가 따라 지운다. 2 단은 PV 의 reclaim policy 가 정한다.",
      "PVC 이름은 파드 이름 + 볼륨 이름 — demo-ephemeral-my-volume")

ddx.node(d, 150, 300, "파드 삭제", "demo-ephemeral", 200, 84, INFO)
d.o.append(f'<rect x="{450-140}" y="258" width="280" height="84" rx="6" '
           f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t(450, 288, "1 단 — PVC 삭제", 13, ACC, KR, "middle", 600)
d.t(450, 312, "ownerReferences 를 따라 GC", 10, MUTED, MONO)
d.path("M 254 300 L 304 300", ACC, 1.5, m="acc")

d.path("M 594 276 L 666 276 L 666 200 L 690 200", OK, 1.5, m="ok")
ddx.node(d, 900, 200, "Delete 면", "PV 와 밑바탕 볼륨까지 삭제", 320, 76, OK)
d.path("M 594 324 L 666 324 L 666 400 L 690 400", WARN, 1.5, m="warn")
ddx.node(d, 900, 400, "Retain 이면", "PV 가 Released 로 남는다", 320, 76, WARN)
d.t(900, 452, "운영자가 수동으로 정리한다", 10, WARN, KR)
# x=642 에 가운데 정렬하면 왼쪽 끝이 1 단 상자(310~590)를 파고든다. 갈림 아래 빈 구간으로 내린다.
d.t(450, 372, "2 단 — PV 의 reclaim policy 가 정한다", 11, SOFT, KR)

d.t(24, 512, "ephemeral PVC 의 생애주기가 파드에 묶이는 것은 이 ownerReferences 때문이다. "
             "직접 만든 PVC 에는 그 주인이 없어 파드를 지워도 남는다.", 11, MUTED, KR, "start")
d.t(24, 534, "emptyDir 과 달리 만들어지는 것이 진짜 PV 라, 스냅샷·data source·용량 강제 같은 PV 의 기능을 그대로 쓴다.",
     11, MUTED, KR, "start")
d.legend(560, [("삭제의 출발", INFO), ("주인을 따라 지워진다", ACC), ("함께 사라진다", OK), ("남는다", WARN)])
d.save("10-03-ephemeral-2stage-deletion.svg")
print("ok")

# 10-03 §5 — emptyDir 하나면 되는데 왜
# 본문이 그 물음을 직접 던진다. 답은 "만들어지는 것이 진짜 PV 라서"이므로, 두 볼륨의 실체가
# 무엇인지가 그림의 축이어야 하고 거기서 기능 차이가 따라 나와야 한다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, MUTED, SOFT, KR
import ddx

d = D(1240, 604, "KUBERNETES IN ACTION · 10-03",
      "실체가 무엇이냐가 쓸 수 있는 기능을 정한다",
      "둘 다 파드가 독점하는 임시 공간이고 파드가 끝나면 데이터가 버려진다. 다른 것은 그 공간의 "
      "실체다 — 하나는 노드 디렉터리, 하나는 정상 PV 다.",
      "그래서 ephemeral 은 PV 의 기능을 그대로 쓴다")

ddx.matrix(
    d, x0=24, hdr_y=148, row_h=88, gap=12, focal_col=1,
    cols=[(230, "볼륨"), (300, "실체"), (325, "쓸 수 있는 것"), (320, "고르는 자리")],
    rows=[
        ([("emptyDir", "가장 단순한 타입"), ("노드의 한 디렉터리", "/var/lib/kubelet/pods/…"),
          ("없다", "용량 강제도 스냅샷도"),
          ("스크래치면 충분할 때", "오브젝트가 늘지 않는다")], INFO),
        ([("ephemeral", "volumeClaimTemplate"), ("정상 PV", "PVC 와 PV 가 실제로 생긴다"),
          ("PV 의 모든 기능", "스냅샷 · dataSource · 용량 강제"),
          ("그 기능이 필요할 때", "PVC·PV 오브젝트가 는다")], ACC),
    ])

d.t(24, 436, "ephemeral 은 emptyDir 을 대체하려는 것이 아니다. 임시 공간에도 PV 의 기능이 필요할 때 "
             "쓰라고 만든 자리다.", 11, MUTED, KR, "start")
d.t(24, 458, "이름이 같은 volumeClaimTemplate 이 StatefulSet 에도 있지만 그쪽은 파드마다 남는 볼륨을 만든다 — "
             "여기는 파드와 함께 사라진다.", 11, MUTED, KR, "start")
d.legend(484, [("단순한 쪽", INFO), ("기능을 얻는 쪽", ACC)])
d.save("10-03-emptydir-vs-ephemeral.svg")
print("ok")

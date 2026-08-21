# 15-01 §4 — 해시가 있고 없고가 흡수를 가른다
# 본문의 물음은 "selector 가 맞는데 왜 흡수하지 않았나"다. 그러니 selector 문자열만 보여선
# 안 되고, 해시 label 유무가 판정을 뒤집는 열로 서 있어야 한다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, BAD, MUTED, SOFT, KR
import ddx

d = D(1240, 560, "KUBERNETES IN ACTION · 15-01",
      "selector 는 맞는데 흡수하지 않는다",
      "Deployment 는 파드를 직접 제어하지 않고 ReplicaSet 에 위임한다. 그 ReplicaSet 의 selector 에는 "
      "Deployment 에 없던 pod-template-hash 가 한 줄 더 붙어 있다.",
      "Deployment selector: app=kiada, rel=stable")

ddx.matrix(
    d, x0=24, hdr_y=148, row_h=92, gap=12, focal_col=2,
    cols=[(250, "파드"), (330, "가진 label"), (280, "pod-template-hash"), (300, "ReplicaSet 판정")],
    rows=[
        ([("kiada-4t87s", "14 장이 남긴 것"), ("app=kiada, rel=stable", "ver=0.5"),
          ("없다", "이 label 자체가 없다"),
          ("흡수하지 않는다", "selector 에 안 맞는다")], BAD),
        ([("kiada-7bffb9bf96-4knb6", "Deployment 가 만든 것"), ("app=kiada, rel=stable", "ver=0.5"),
          ("7bffb9bf96", "template 내용에서 계산"),
          ("이 세트의 파드", "selector 에 맞는다")], OK),
    ])

d.t(24, 404, "해시 값은 랜덤이 아니라 Pod 템플릿 내용에서 계산되고, 같은 값이 ReplicaSet 이름에도 쓰인다. "
             "그래서 템플릿을 바꿀 때마다 새 ReplicaSet 이 생긴다.", 11, MUTED, KR, "start")
d.t(24, 426, "이것이 15-02 업데이트의 핵심이다 — 옛 파드가 새 세트에 흡수되지 않아야 두 세대가 나란히 설 수 있다.",
     11, MUTED, KR, "start")
d.legend(452, [("남는 파드", BAD), ("세트의 파드", OK), ("판정을 뒤집는 열", ACC)])
d.save("15-01-pod-template-hash.svg")
print("ok")

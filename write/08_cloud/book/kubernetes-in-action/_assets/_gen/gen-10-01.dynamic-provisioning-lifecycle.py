# 10-01 §2 — 언제 만들어지고 언제 사라지는가
# 세 오브젝트의 수명이 서로 다른 시점에 시작하고 끝난다. 그러니 관계도가 아니라 시간축 위의
# 세 레인이어야 "PVC 는 남고 PV 는 바인딩된 채"라는 서술이 보인다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, MUTED, SOFT, INK, RULE, KR, MONO
import ddx

d = D(1240, 644, "KUBERNETES IN ACTION · 10-01",
      "셋의 수명이 서로 다른 지점에서 끝난다",
      "PVC 를 만들면 PV 가 그때 만들어진다. 파드를 지워도 PVC 와 PV 는 남아, 같은 요구를 다른 파드가 "
      "이어받을 수 있다.",
      "동적 프로비저닝 · reclaimPolicy: Delete")

X = lambda t: 150 + t * 105
LANES = [("PVC", 0, 8, INFO, "만들면 남는다 — 지울 때까지"),
         ("PV", 1, 8.6, OK, "PVC 를 만든 직후 프로비저너가 만든다"),
         ("파드 1", 2, 4, ACC, "볼륨을 마운트해 쓴다"),
         ("파드 2", 5, 7, ACC, "같은 PVC 를 이어받는다")]
for i, (nm, t0, t1, c, note) in enumerate(LANES):
    y = 200 + i * 76
    d.t(40, y + 6, nm, 11, SOFT, KR, "start")
    d.o.append(f'<rect x="{X(t0)}" y="{y-20}" width="{X(t1)-X(t0)}" height="40" rx="5" '
               f'fill="{c}12" stroke="{c}" stroke-width="1.2"/>')
    d.t((X(t0) + X(t1)) / 2, y + 6, note, 10, c, KR)

d.line(X(0) - 12, 520, X(9) + 12, 520, RULE, 1.0)
for t, lab in ((0, "PVC 생성"), (2, "파드 1 생성"), (4, "파드 1 삭제"),
               (5, "파드 2 생성"), (8, "PVC 삭제"), (8.6, "PV 삭제")):
    d.line(X(t), 496, X(t), 526, RULE, 0.9, "4 4")
    d.t(X(t), 548, lab, 9, SOFT, KR)

d.t(24, 584 - 8, "파드를 지우면 밑바탕 스토리지가 노드에서 detach 되지만, 그것은 그 노드에서 그 볼륨을 쓰는 "
                 "마지막 파드였을 때의 이야기다.", 11, MUTED, KR, "start")
d.legend(596 - 4, [("요구", INFO), ("실체", OK), ("쓰는 쪽", ACC)])
d.save("10-01-dynamic-provisioning-lifecycle.svg")
print("ok")

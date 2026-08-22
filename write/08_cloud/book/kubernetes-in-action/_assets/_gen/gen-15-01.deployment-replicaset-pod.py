# 15-01 §1 — 각 층이 모르는 것이 층을 나눈 이유다
# 본문이 표의 "오른쪽 열이 더 중요하다"고 직접 말한다. 그러니 위임 화살표만 그리면 요점이
# 빠지고, 층마다 '모르는 것'이 나란히 보여야 한다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO
import ddx

d = D(1180, 644, "KUBERNETES IN ACTION · 15-01",
      "각 층은 바로 아래만 안다",
      "Deployment 는 파드 하나하나를 모르고, ReplicaSet 은 버전을 모르며, 파드는 자기 바깥을 모른다. "
      "이 무지가 층을 나눈 이유다.",
      "Deployment → ReplicaSet → Pod")

LAYER = [("Deployment", "버전 전환 — 어느 템플릿을 몇 개로 굴릴지", "파드 하나하나", INFO),
         ("ReplicaSet", "개수 유지 — 라벨에 맞는 파드를 정해진 수만큼", "버전, 파드 내부", INFO),
         ("Pod", "공유 실행 환경 — IP·볼륨을 공유하고 함께 뜨고 죽는 한 몸", "자기 바깥", INFO)]
for i, (t, duty, blind, c) in enumerate(LAYER):
    y = 168 + i * 108
    d.box(60, y, 640, 84, PAPER2, c, 1.1, 6)
    d.t(84, y + 32, t, 13, c, KR, "start", 600)
    d.t(84, y + 58, duty, 11, MUTED, KR, "start")
    d.box(730, y, 380, 84, PAPER2, RULE, 0.9, 6)
    d.t(750, y + 32, "모르는 것", 10, SOFT, KR, "start")
    d.t(750, y + 58, blind, 12, SOFT, KR, "start")
    if i < 2:
        d.path(f"M 200 {y+88} L 200 {y+104}", INFO, 1.5, m="info")
        d.t(216, y + 102, "위임한다", 10, SOFT, KR, "start")

ddx.focal_tag(d, 380, 506, "이 무지가 층을 나눈 이유다", 260)

d.t(24, 552, "ReplicaSet 에 업데이트를 넣으려면 '구 템플릿 2 개 + 신 템플릿 3 개' 같은 상태를 한 오브젝트가 들어야 하고, "
             "그러면 개수 유지라는 단일 책임이 깨진다.", 11, MUTED, KR, "start")
d.t(24, 574, "그래서 ReplicaSet 을 손대는 대신 그런 ReplicaSet 을 둘 두고 숫자만 반대로 움직이는 층을 위에 얹었다.",
     11, MUTED, KR, "start")
d.legend(596, [("각 층", INFO), ("층을 나눈 이유", ACC)])
d.save("15-01-deployment-replicaset-pod.svg")
print("ok")

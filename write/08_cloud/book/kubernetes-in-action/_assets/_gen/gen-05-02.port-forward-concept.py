# 05-02 §방법 ③ — port-forward 가 쓰는 쪽에 보이는 모습
# 본문: "로컬 컴퓨터의 포트에 바인딩된 프록시를 통해 Pod 와 통신합니다."
#       "Pod IP 를 찾을 필요 없이 이름과 포트만 지정하면 됩니다."
# 타입 스펙: 세 칸짜리 한 줄 사슬. 같은 편의 port-forward-path 는 *속*의 긴 경로를 그리므로,
#           이 장은 쓰는 사람이 실제로 치는 것과 보는 것만 남긴다 — 둘의 역할을 갈라 둔다.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO
import ddx

W, H = 1000, 520
d = D(W, H, "KUBERNETES IN ACTION · 05-02",
      "쓰는 쪽에서는 로컬 포트 하나만 보인다",
      "kubectl port-forward 가 로컬 포트에 프록시를 바인딩하고, curl 은 그 포트로만 말한다. "
      "Pod IP 를 찾을 필요 없이 Pod 이름과 포트만 지정하면 된다.",
      lead="속은 네 홉을 거치지만 쓰는 쪽에는 그 복잡함이 드러나지 않는다")

ddx.band(d, 104, 464, "이 편의 port-forward-path 가 같은 일을 속에서 본 그림이다")

ddx.stage_chain(
    # 3*268 + 2*68 + 48 = 988 — x0 + n*bw + (n-1)*gap 이 viewBox 를 넘지 않게 잡는다
    d, cy=286, stage_y=196, bw=268, gap=68, x0=48,
    stages=["내 컴퓨터", "로컬에 선 프록시", "클러스터 안"],
    nodes=[("curl", "localhost:8080", "Pod IP 를 모른다", INFO),
           ("kubectl port-forward", "kiada 8080", "127.0.0.1:8080 에 바인딩", ACC),
           ("kiada 컨테이너", "8080", "요청을 받는다", OK)],
    edges=["로컬 포트", "터널"])

d.t(36, 412, "Pod 이름과 포트만 있으면 되므로 Pod IP 가 바뀌어도 명령이 그대로다 — "
             "개발 중 특정 Pod 와 통신하는 가장 쉬운 방법인 이유다", 12, MUTED, KR, "start")
d.legend(480, [("치는 쪽", INFO), ("로컬에 서는 것", ACC), ("받는 쪽", OK)])
d.save("05-02-port-forward-concept.svg")
print("ok port-forward-concept")

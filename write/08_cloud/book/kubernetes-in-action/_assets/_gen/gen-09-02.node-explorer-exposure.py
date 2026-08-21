# 09-02 §2 — path: / 하나가 여는 것
# 위험을 문장으로 적으면 크기가 안 잡힌다. 노드 루트 아래 무엇이 함께 딸려 오는지를
# 실제 경로로 늘어놓아야 노출면의 넓이가 보인다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, WARN, BAD, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO
import ddx

d = D(1200, 620, "KUBERNETES IN ACTION · 09-02",
      "한 줄이 노드 전체를 연다",
      "path 를 / 로 주면 그 노드의 파일시스템이 통째로 컨테이너 안에 보인다. 검사도 없고 경고도 없이 "
      "조용히 성공하므로, 무엇이 열렸는지는 열어 봐야 안다.",
      "hostPath: { path: / }  ·  type 없음")

d.o.append(f'<rect x="60" y="176" width="320" height="88" rx="6" '
           f'fill="{BAD}12" stroke="{BAD}" stroke-width="1.4"/>')
d.t(220, 208, "hostPath  path: /", 13, BAD, MONO, "middle", 600)
d.t(220, 232, "type 을 안 적었다", 11, MUTED, KR)
d.path("M 384 220 L 448 220", BAD, 1.5, m="bad")
d.t(416, 202, "마운트", 10, SOFT, KR)

d.box(470, 168, 660, 264, PAPER, RULE, 0.9, 8)
d.t(800, 196, "컨테이너 안에서 보이는 것", 11, SOFT, KR)
EXPOSED = [("/etc/kubernetes/", "kubelet 설정 · 인증서"),
           ("/var/lib/kubelet/pods/", "그 노드 모든 파드의 볼륨"),
           ("/var/lib/docker/", "이미지와 컨테이너 레이어"),
           ("/root/  ·  /home/", "노드 사용자 홈")]
for i, (p, s) in enumerate(EXPOSED):
    y = 236 + i * 44
    d.t(500, y, p, 11, BAD, MONO, "start")
    d.t(790, y, s, 11, MUTED, KR, "start")

ddx.focal_tag(d, 600, 476, "검사도 경고도 없이 성공한다", 300)

d.t(24, 528, "그래서 hostPath 는 파드를 만들 권한이 곧 노드 접근 권한이 될 수 있는 자리다. "
             "실무에서는 PodSecurity 나 정책 엔진으로 hostPath 사용 자체를 막는 편이다.", 11, MUTED, KR, "start")
d.t(24, 550, "노드 자신의 것을 읽어야 하는 워크로드라면 필요한 경로만 좁게 주고 type 을 함께 지정한다.",
     11, MUTED, KR, "start")
d.legend(572, [("열리는 것", BAD), ("조용히 지나간다", ACC)])
d.save("09-02-node-explorer-exposure.svg")
print("ok")

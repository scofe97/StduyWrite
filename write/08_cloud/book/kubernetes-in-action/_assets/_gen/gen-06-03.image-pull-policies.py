# 06-03 §3 — imagePullPolicy 세 가지가 갈리는 자리
# 본문: "레지스트리를 매번 조회할지, 로컬 이미지를 재사용할지 결정합니다."
#       "미지정이면 :latest 는 Always, 그 외 태그는 IfNotPresent 가 기본값"
# 타입 스펙: type-dp-security-matrix.md — 값이 셋이고 축이 넷이라 비교 행렬. 옛 판은 같은 모양의 흐름도를 셋 그려
#           같은 분기를 세 번 반복했다 — 세 정책이 *어디서 갈리는지* 는 오히려 안 보였다.
#           본문 표는 조회·캐시 조건을 적으므로, 도식은 그 결과인 운영상의 차이를 진다.
#           판정 열은 본문이 지목한 축("레지스트리를 매번 조회할지, 로컬 이미지를 재사용할지")
#           이다. 재시작 열을 판정 축으로 두면 IfNotPresent 와 Never 가 같은 값이라 행 색만
#           어긋나 보인다 — 셋이 실제로 갈리는 열은 조회 시점 하나뿐이다.
#           행은 정책 셋, 열은 조회 시점·재시작·이미지가 없을 때인 격자다. focal 열이 조회 시점이라
#           셋이 실제로 갈리는 유일한 축이 판정 축으로 선다.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO
import ddx

W, H = 1000, 628
d = D(W, H, "KUBERNETES IN ACTION · 06-03",
      "세 정책은 레지스트리를 언제 보는가에서 갈린다",
      "Always 는 (재)시작마다 레지스트리에서 digest 를 확인하고, IfNotPresent 는 로컬에 없을 "
      "때만 조회하며, Never 는 아예 조회하지 않는다.",
      lead="첫 시작은 셋이 비슷해 보인다 — 차이는 재시작과 이미지가 없을 때 드러난다")

ddx.band(d, 104, 572, "미지정이면 :latest 는 Always, 그 외 태그는 IfNotPresent 가 기본값이 된다")

ddx.matrix(
    d, x0=36, hdr_y=210, row_h=88, gap=12, focal_col=1,
    cols=[(210, "imagePullPolicy"), (215, "언제 레지스트리를 보는가"),
          (215, "재시작할 때"), (250, "로컬에 이미지가 없으면")],
    rows=[
        ([("Always", ":latest 의 기본값"), ("(재)시작마다", "digest 를 확인한다"),
          ("또 조회한다", "레지스트리가 죽으면 못 뜬다"), ("pull 한다", "받아서 시작한다")], WARN),
        ([("IfNotPresent", "그 외 태그의 기본값"), ("로컬에 없을 때만", "있으면 안 본다"),
          ("캐시를 쓴다", "레지스트리와 무관하다"), ("pull 한다", "받아서 시작한다")], OK),
        ([("Never", "기본값이 되지 않는다"), ("보지 않는다", "조회 자체를 안 한다"),
          ("캐시를 쓴다", "레지스트리와 무관하다"), ("시작하지 못한다", "ErrImageNeverPull")], BAD),
    ])

# 행렬 3행은 434~522 를 쓴다 — 산문은 그 아래로
d.t(36, 548, "노드에 이미지를 미리 심어 두는 운영이라면 Never 가 맞고, 태그를 덮어쓰는 운영이라면 "
             "Always 여야 한다 — 대신 레지스트리가 재시작 경로에 들어온다", 12, MUTED, KR, "start")
d.legend(588, [("매번 조회", WARN), ("있으면 재사용", OK), ("없으면 실패", BAD)])
d.save("06-03-image-pull-policies.svg")
print("ok image-pull-policies")

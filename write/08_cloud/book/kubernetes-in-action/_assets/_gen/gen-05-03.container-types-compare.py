# 05-03 §셋 비교 — init · 일반 사이드카 · 네이티브 사이드카
# 본문: 시작 시점·종료 시점·정의 위치가 다르다. 네이티브만 initContainers + restartPolicy: Always.
#       일반 사이드카는 containers 라 주 컨테이너와 동급이 되어 먼저 죽을 위험이 있다.
# 타입 스펙: 값 셋 × 축 넷이라 비교 행렬. 정의 위치가 나머지 셋을 결정하므로 그 열을 판정 축으로 세운다.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO
import ddx

W, H = 1000, 588
d = D(W, H, "KUBERNETES IN ACTION · 05-03",
      "정의 위치가 시작·종료 시점을 결정한다",
      "init 컨테이너는 끝나면 죽고, 일반 사이드카는 주 컨테이너와 동급이며, 네이티브 사이드카만 "
      "먼저 뜨고 맨 나중에 죽는다. 세 성질의 차이는 어디에 어떻게 적었는가에서 온다.",
      lead="같은 '사이드카' 라는 말이 두 가지를 가리킨다 — 정의 위치를 봐야 어느 쪽인지 안다")

ddx.band(d, 104, 532, "판정 열 하나가 나머지 세 열을 결정한다")

ddx.matrix(
    d, x0=36, hdr_y=196, row_h=88, gap=12, focal_col=1,
    cols=[(180, "종류"), (250, "정의 위치"), (250, "시작 시점"), (240, "종료 시점")],
    rows=[
        ([("init 컨테이너", "일회성"), ("initContainers", "정책 없음"),
          ("주 컨테이너 전에", "정의된 순서대로 하나씩"),
          ("끝나면 죽는다", "Completed 후 사라진다")], INFO),
        ([("일반 사이드카", "주 컨테이너와 동급"), ("containers", "주 컨테이너와 같은 자리"),
          ("주 컨테이너와 동시", "순서 보장이 없다"),
          ("함께 죽는다", "먼저 죽을 위험이 있다")], WARN),
        ([("네이티브 사이드카", "먼저·계속·마지막"), ("initContainers", "restartPolicy: Always"),
          ("주 컨테이너보다 먼저", "뒤따르는 init 도 쓸 수 있다"),
          ("맨 나중에 죽는다", "주 컨테이너가 다 죽은 뒤")], OK),
    ])

d.t(36, 484, "네이티브 사이드카를 쓸 자리는 Pod 에 반드시 있어야 하는 보조다 — 로그 수집기·프록시, "
             "그리고 배치 Job(18장)의 사이드카.", 12, MUTED, KR, "start")
d.legend(548, [("일회성", INFO), ("동급이라 순서가 없다", WARN), ("순서가 보장된다", OK)])
d.save("05-03-container-types-compare.svg")
print("ok container-types-compare")

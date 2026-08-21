# 17-02 §3 — CNI 가 그 파드를 식별하느냐에 갈린다
# 캡션이 "CNI 의 식별 여부에 따라 갈리는 두 결과"라 못박는다. 그러니 정책 자체가 아니라
# 식별 여부가 판정 축이어야 한다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, WARN, BAD, MUTED, SOFT, KR
import ddx

d = D(1240, 600, "KUBERNETES IN ACTION · 17-02",
      "정책이 걸리느냐는 CNI 가 정한다",
      "NetworkPolicy 는 파드를 라벨로 고른다. 그런데 hostNetwork 파드는 자기 IP 가 없어 노드 주소로 "
      "보이므로, CNI 가 그 트래픽을 그 파드의 것으로 식별하느냐에 따라 결과가 갈린다.",
      "구현에 따라 다르다 — 쓰는 CNI 의 문서를 확인한다")

ddx.matrix(
    d, x0=24, hdr_y=148, row_h=92, gap=12, focal_col=1,
    cols=[(280, "상황"), (300, "CNI 가 식별하나"), (320, "정책 적용"), (270, "결과")],
    rows=[
        ([("일반 파드", "자기 IP 가 있다"), ("식별한다", "파드 IP 로 구분된다"),
          ("걸린다", "라벨 selector 대로"), ("의도대로", "")], OK),
        ([("hostNetwork 파드", "노드 IP 로 보인다"), ("식별하지 못하면", "노드 트래픽과 뒤섞인다"),
          ("걸리지 않는다", "정책 밖으로 새어 나간다"), ("의도와 다르다", "")], BAD),
    ])

d.t(24, 420, "그래서 hostNetwork 를 켜는 순간 NetworkPolicy 로 막고 있다고 믿던 경로가 열려 있을 수 있다. "
             "정책을 걸어 뒀다는 사실이 그 파드에도 적용된다는 뜻은 아니다.", 11, MUTED, KR, "start")
d.t(24, 442, "노드 자신의 트래픽을 정책 대상으로 삼을 수 있는지도 CNI 마다 다르다 — 확인하지 않고 전제하지 않는다.",
     11, MUTED, KR, "start")
d.legend(472, [("걸린다", OK), ("새어 나간다", BAD), ("판정 축", ACC)])
d.save("17-02-hostnetwork-networkpolicy.svg")
print("ok")

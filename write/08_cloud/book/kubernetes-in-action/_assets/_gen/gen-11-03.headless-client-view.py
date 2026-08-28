# 11-03 §2 — 목적지를 누가 확정하는가
# 본문이 '주소를 누가 확정하는가 한 지점'이라 못박으므로 그 열을 focal 로 둔 행렬.
# 타입 스펙: type-dp-security-matrix.md — 행은 Service 두 종류, 열은 앱이 쥔 주소·목적지를 정하는 곳·앱이 알 수 있는 것.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, MUTED, SOFT, KR
import ddx

d = D(1124, 500, "KUBERNETES IN ACTION · 11-03",
      "목적지를 누가 확정하는가",
      "일반 Service 에서 앱이 쥔 주소는 cluster IP 하나뿐이고, 넷 중 어디로 갈지는 커널이 확률로 고른다. "
      "headless 는 파드 IP 를 그대로 건네주므로 앱이 직접 고르고, 그래서 무엇에 닿았는지 셀 수 있다.",
      "파드 4 개를 뒷받침하는 quote 서비스")

ddx.matrix(
    d, x0=24, hdr_y=140, row_h=92, gap=12, focal_col=2,
    cols=[(210, "Service 종류"), (260, "앱이 쥔 주소"), (270, "목적지를 정하는 곳"), (300, "앱이 알 수 있는 것")],
    rows=[
        ([("일반 Service", "clusterIP 있음"), ("cluster IP 하나", "10.96.74.151"),
          ("노드 커널", "확률로 고른다"), ("모른다", "어느 파드에 닿았는지")], INFO),
        ([("headless", "clusterIP: None"), ("파드 IP 전부", "A 레코드 4 개"),
          ("앱 코드", "받은 목록을 직접 순회"), ("전부 안다", "몇 개 보냈고 어디가 실패했는지")], ACC),
    ])

d.t(24, 396, "순회는 쿠버네티스 기능이 아니라 앱 코드가 하는 일이다. headless 는 목록을 건네줄 뿐이고, "
             "그 목록을 어떻게 쓸지는 전적으로 앱이 정한다.", 11, MUTED, KR, "start")
d.legend(422, [("커널이 고른다", INFO), ("앱이 고른다", ACC)])
d.save("11-03-headless-client-view.svg")
print("ok")

# 10-01 §2 워크로드가 불건강해진 뒤 데이터 플레인이 갱신되기까지 — 원문 그림 10.3.
# 본문(원문 10.2.1): 데이터 플레인 설정은 설계상 eventually consistent 다. 엔드포인트 하나가 불건강해지면
#       쿠버네티스가 그것을 인식해 파드를 unhealthy 로 표시하는 데 시간이 걸리고, 어느 시점에 컨트롤
#       플레인도 그 문제를 인식해 데이터 플레인에서 엔드포인트를 제거한다. 그러면 다시 일관된 상태가 된다.
#       클러스터가 커져 워크로드와 이벤트가 늘면 이 기간도 비례해 늘어난다(11 장).
# 저자가 구간별 소요 시간을 적지 않았으므로 눈금 없는 순서로만 그린다.
# 타입 스펙: type-sequence — 시간 순서가 논점이다. 참여자 4(최대 5), 메시지 6(최대 12), coral 은 한 곳.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, KR, MONO

W, H = 1000, 620
d = Seq(W, H, "ISTIO IN ACTION · 10-01 §2",
        "설정이 늦게 도착하는 것은 고장이 아니다",
        "워크로드가 불건강해진 뒤 프록시가 그 사실을 반영하기까지 네 참여자가 차례로 움직인다. "
        "색이 붙은 자리까지 와야 SYNCED 로 관측되고, 그 전까지는 프록시가 옛 설정으로 돈다.",
        "저자가 구간별 소요 시간을 적지 않아 눈금 없이 순서만 그립니다")

d.lanes([("워크로드", "catalog pod"),
         ("쿠버네티스", "kubelet · API"),
         ("istiod", "control plane"),
         ("Envoy 프록시", "data plane")], y0=104, lane_w=250)
d.rails(524)

d.msg("워크로드", "쿠버네티스", "응답 실패", 196, MUTED, "ar", sub="엔드포인트가 불건강해진다")
d.selfmsg("쿠버네티스", "unhealthy 표시", 252, MUTED, sub="인식에 시간이 걸린다")
d.msg("쿠버네티스", "istiod", "엔드포인트 목록 변경", 316, MUTED, "ar", sub="서비스 레지스트리")
d.selfmsg("istiod", "변경 인식", 372, MUTED, sub="여기도 즉시가 아니다")
d.msg("istiod", "Envoy 프록시", "EDS 갱신 전송", 436, MUTED, "ar", sub="그 엔드포인트를 뺀 목록")
d.msg("Envoy 프록시", "istiod", "수신 확인", 494, ACC, "acc", sub="여기까지 와야 SYNCED 다")

d.t(20, 556, "proxy-status 가 이 파이프라인의 끝을 보여 준다 — STALE 이면 보냈는데 확인이 안 온 것이다", 11, SOFT, KR, "start")
d.legend(576, [("proxy-status 가 SYNCED 로 적는 지점", ACC)])
d.save("10-01.sync-events.svg")

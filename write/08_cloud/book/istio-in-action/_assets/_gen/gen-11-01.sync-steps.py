# 11-01 §2 이벤트가 프록시에 닿기까지 — 원문 그림 11.2.
# 본문(원문 11.1.1): (1) 들어온 이벤트가 동기화를 촉발한다 (2) istiod 의 DiscoveryServer 가 이벤트를 듣고,
#       성능을 위해 푸시 큐에 넣는 것을 정해진 시간만큼 미뤄 그 사이의 이벤트를 묶는다 — 디바운싱이다
#       (3) 지연 기간이 끝나면 병합된 이벤트를 푸시 큐에 넣는다 (4) istiod 는 동시에 처리하는 푸시 요청
#       수를 제한한다 — 스로틀링이며, 컨텍스트 전환에 CPU 를 쓰지 않게 한다 (5) 처리된 항목이 Envoy 설정으로
#       변환돼 워크로드로 푸시된다.
# 저자가 구간별 소요 시간을 적지 않으므로 눈금 없이 순서만 그린다.
# 타입 스펙: type-sequence — 시간 순서가 논점이다. 참여자 4(최대 5), 메시지 6(최대 12), coral 은 한 곳.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, INFO, MUTED, SOFT, INK, KR, MONO

W, H = 1000, 620
d = Seq(W, H, "ISTIO IN ACTION · 11-01 §2",
        "다섯 걸음 중 둘은 일부러 늦추는 자리다",
        "이벤트 하나가 프록시에 닿기까지 네 참여자를 지난다. 색이 붙은 자리가 이벤트를 묶으려고 "
        "일부러 미루는 구간이고, 파란 자리가 동시에 처리하는 수를 제한하는 구간이다.",
        "istiod 는 이 둘로 스스로를 과부하에서 지킵니다")

d.lanes([("쿠버네티스", "service · endpoint"),
         ("DiscoveryServer", "istiod"),
         ("푸시 큐", "push queue"),
         ("서비스 프록시", "data plane")], y0=104, lane_w=216)
d.rails(524)

d.msg("쿠버네티스", "DiscoveryServer", "이벤트 발생", 196, MUTED, "ar", sub="서비스 · 엔드포인트 · 설정")
d.selfmsg("DiscoveryServer", "디바운스", 252, ACC, sub="그 사이 이벤트를 병합한다")
d.msg("DiscoveryServer", "푸시 큐", "병합된 배치 투입", 316, MUTED, "ar", sub="처리 대기 목록")
d.selfmsg("푸시 큐", "동시 처리 수 제한", 372, INFO, sub="컨텍스트 전환을 줄인다")
d.msg("푸시 큐", "서비스 프록시", "Envoy 설정 푸시", 436, MUTED, "ar", sub="변환한 뒤 내려보낸다")
d.selfmsg("서비스 프록시", "설정 반영", 494, MUTED, sub="한 바퀴 끝")

d.t(24, 556, "디바운스는 일을 줄이려고 늦추고, 스로틀은 진행을 빠르게 하려고 동시 수를 줄인다 — 방향이 반대다", 11, SOFT, KR, "start")
d.legend(576, [("이벤트를 묶으려고 미루는 자리", ACC), ("동시 처리 수를 제한하는 자리", INFO)])
d.save("11-01.sync-steps.svg")

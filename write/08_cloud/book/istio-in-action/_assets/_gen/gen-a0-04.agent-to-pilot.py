# a0-04 §3 질의가 에이전트를 거쳐 가는 길.
# 본문(부록 D.1.2): 15004 로 온 요청은 "forwarded securely to istiod as xDS events, which is a
#       good way to verify connectivity to the control plane from the agent". 응답의
#       genericXdsConfigs 안 configStatus 가 SYNCED 면 최신이다.
# 타입 스펙: type-sequence — 참여자 사이 시간 순 주고받기가 논점이다. 레인 + 메시지, 상태는 칩으로.
#           축약: 이 경로 자체가 연결 확인 수단이라는 것이 논점이라 응답이 온 자리에 상태 칩을 둔다.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, INFO, OK, KR, MONO

W, H = 1000, 528
d = Seq(W, H, "ISTIO IN ACTION · A0-04 §3",
        "답이 온다는 것 자체가 연결이 살아 있다는 뜻이다",
        "15004 로 던진 질의는 xDS 이벤트로 istiod 에 안전하게 전달된다. 그래서 이 왕복은 동기화 "
        "상태를 묻는 일이면서 동시에 에이전트와 컨트롤 플레인 사이 연결을 확인하는 일이 된다.",
        "여기서 보이는 것은 Pilot 디버그 엔드포인트가 내놓는 것의 부분집합입니다")

d.lanes([("사람", "kubectl exec"),
         ("파일럿 에이전트", "포트 15004"),
         ("istiod", "debug endpoints")], y0=104, lane_w=240)
d.rails(392)

d.msg("사람", "파일럿 에이전트", "curl /debug/syncz", 196, MUTED, "ar", sub="프록시 안에서 친다")
d.msg("파일럿 에이전트", "istiod", "xDS 이벤트로 전달", 260, ACC, "acc", sub="평문으로 나가지 않는다")
d.msg("istiod", "파일럿 에이전트", "genericXdsConfigs", 324, MUTED, "ar", sub="xDS API 별 configStatus")
d.msg("파일럿 에이전트", "사람", "SYNCED", 372, OK, "ok", sub="리스너 · 라우트 · 엔드포인트 · 클러스터")

d.state("파일럿 에이전트", "연결 확인됨", 428, INFO)

d.t(24, 460, "같은 엔드포인트를 istioctl x internal-debug 로도 쓸 수 있다 — istioctl 에 새로 더해진 것이다", 11, SOFT, KR, "start")
d.legend(480, [("안전하게 전달되는 구간", ACC), ("이 왕복이 함께 알려 주는 것", INFO), ("최신 상태", OK)])
d.save("a0-04.agent-to-pilot.svg")

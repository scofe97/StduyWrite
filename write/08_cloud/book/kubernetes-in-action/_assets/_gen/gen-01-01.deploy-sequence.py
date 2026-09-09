# 01-01 §6 — 매니페스트 하나가 컨테이너가 되기까지
# 본문 근거(01-01 §6 여섯 단계):
#   ① 매니페스트를 API 에 제출하면 API 서버가 오브젝트를 etcd 에 쓴다
#   ② 컨트롤러가 새 오브젝트를 감지하고 인스턴스마다 새 오브젝트를 만든다
#   ③ 스케줄러가 각 인스턴스에 노드를 배정한다
#   ④ Kubelet 이 자기 노드에 배정된 인스턴스를 감지해 컨테이너 런타임에 지시한다
#   ⑤ kube-proxy 가 준비를 감지해 로드밸런서를 구성한다
#   ⑥ Kubelet 과 컨트롤러가 계속 모니터링하며 유지한다
#   "컨트롤러 대부분이 직접 실행하지 않는다 … 실제로 컨테이너를 띄우는 것은 각 노드의 Kubelet"
# 타입 스펙: 주체가 여섯이고 순서가 논지다 → type-sequence.
#   focal 은 '실제로 띄우는 곳' 하나 — 본문이 간접성의 요점으로 짚는 지점이다.
#   재생·시나리오 토글이 필요한 독자는 같은 절의 독립 HTML 로 간다(도구 선택 규칙).
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, INFO, OK, WARN, MUTED, SOFT, INK, KR, MONO
import ddx

Y0, STEP = 206, 52
y = lambda i: Y0 + i * STEP
RAIL, NOTE_Y, LEG_Y = y(11) + 26, y(11) + 66, y(11) + 82
d = Seq(1400, LEG_Y + 56, "KUBERNETES IN ACTION · 01-01",
        "매니페스트 하나가 컨테이너가 되기까지",
        "제출부터 노출까지 여섯 단계가 순서대로 반응한다. 모든 단계가 API Server 를 거치고, "
        "컨트롤러는 오브젝트만 만들 뿐 컨테이너를 직접 띄우지는 않는다.",
        "여섯 단계 — 제출 · 저장 · 생성 · 배정 · 실행 · 노출")

ddx.lanes(d, [("사용자", "kubectl"),
              ("API Server", "유일한 허브"),
              ("Controller", "부족분을 만든다"),
              ("Scheduler", "노드를 정한다"),
              ("Kubelet", "노드 에이전트"),
              ("kube-proxy", "트래픽을 잇는다")], y0=110, lane_w=196)
d.rails(RAIL)

ddx.msg(d, "사용자", "API Server", "① 매니페스트 제출", y(0), INFO)
ddx.selfmsg(d, "API Server", "② etcd 에 오브젝트 저장", y(1), INFO)
ddx.msg(d, "API Server", "Controller", "오브젝트 생성 알림", y(2), OK, mk="ok", dash="6 5")
ddx.msg(d, "Controller", "API Server", "③ 인스턴스별 오브젝트 생성", y(3), INFO,
        sub="컨테이너를 직접 띄우지는 않는다")
ddx.msg(d, "API Server", "Scheduler", "새 오브젝트 알림", y(4), OK, mk="ok", dash="6 5")
ddx.msg(d, "Scheduler", "API Server", "④ 각 인스턴스에 노드 배정", y(5), INFO)
ddx.msg(d, "API Server", "Kubelet", "배정된 인스턴스 알림", y(6), OK, mk="ok", dash="6 5")
ddx.selfmsg(d, "Kubelet", "⑤ 컨테이너 런타임으로 실행", y(7), INFO,
            sub="여기가 컨테이너가 뜨는 자리다")
ddx.state(d, "Kubelet", "실행은 노드의 몫이다", y(8), ACC)
ddx.msg(d, "Kubelet", "API Server", "상태 보고", y(9), INFO)
ddx.msg(d, "API Server", "kube-proxy", "준비된 인스턴스 알림", y(10), OK, mk="ok", dash="6 5")
ddx.state(d, "kube-proxy", "⑥ 로드밸런서 설정", y(11), INFO)

d.t(24, NOTE_Y, "컴포넌트끼리 직접 잇는 선이 하나도 없다 — 여섯 단계가 모두 API Server 를 지난다. "
                "그래서 노드 하나가 죽어도 컨트롤 플레인은 조율을 계속한다.", 11, MUTED, KR, "start")
d.legend(LEG_Y, [("실제로 컨테이너가 뜨는 자리", ACC), ("API 로 쓰는 호출", INFO),
                 ("API 가 알리는 변화", OK)])
d.save("01-01-deploy-sequence.svg")
print("ok deploy-sequence")

# 05-03 §네이티브 사이드카 — 세 단계로 산다
# 본문: initContainers 에 restartPolicy: Always 한 줄을 붙이면 만들어진다.
#       ① init 단계에서 먼저 뜬다(뒤따르는 것들에 서비스 제공)
#       ② Pod 수명 내내 산다(끝나기를 기다리지 않고, 종료되면 kubelet 이 다시 띄운다)
#       ③ 주 컨테이너가 모두 죽은 뒤에야 SIGTERM 을 받는다
# 타입 스펙: type-process.md — 한 대상의 시간순 세 국면이라 한 줄 사슬(stage_chain). 정의 한 줄이 이 셋을
#           동시에 만드는 것이 요점이므로 사슬 위에 그 선언을 못 박는다.
#           세 국면이 같은 슬롯(무엇을 한다 · 언제 · 그래서)으로 반복되고 그 사이를 전환 라벨이 잇는다.
#           type-state 도 후보였다 — 전환 라벨(Ready 되면 · 종료 시작)이 사건이기 때문이다. 다만 상자에
#           든 것은 컨테이너가 오가는 상태가 아니라 선언 한 줄이 만드는 성질 셋이고, 정본이 요구하는
#           시작 점·끝 링 표식도 없어 process 를 택했다.
#           type-process 정본의 입력 계약은 역할 레인 1~6 이 전제인데 이 그림에 레인은 없다.
#           그래도 process 를 두는 것은, 주체를 요구하지 않는 유일한 라우팅 규칙이
#           semantic-patterns 의 "Stage framework with semantic slots" 한 줄이기 때문이다.
#           38개 메뉴의 공백이라 visual-diagram-selection 의 "알려진 공백" 에 같이 적어 두었다.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO
import ddx

W, H = 1000, 588
d = D(W, H, "KUBERNETES IN ACTION · 05-03",
      "한 줄이 세 성질을 한꺼번에 만든다",
      "initContainers 에 restartPolicy: Always 를 붙이면 init 의 '먼저' 와 사이드카의 '계속' 과 "
      "맨 마지막 종료가 함께 온다. 쿠버네티스는 끝나기를 기다리지 않고, 끝나면 다시 띄운다.",
      lead="일반 사이드카는 주 컨테이너와 동시에 뜨고 함께 죽는다 — 먼저 죽을 위험이 있다")

ddx.band(d, 104, 532, "restartPolicy: Always 한 줄 — 세 성질이 함께 생김")

d.chip(420, 178, "initContainers: [ { name: sidecar, restartPolicy: Always } ]", ACC, 11)
d.t(700, 182, "← 끝나도 기다리지 않음, 죽으면 다시 띄움", 11, SOFT, KR, "start")

ddx.stage_chain(
    # 코리도어 라벨('Ready 되면' 63px)이 들어가도록 gap 을 76 으로 — fit 가드가 잡아 준다
    d, cy=326, stage_y=240, bw=264, gap=76, x0=28,
    stages=["① init 단계", "② Pod 수명 내내", "③ 종료 단계"],
    nodes=[("먼저 뜬다", "주 컨테이너보다 앞", "뒤따르는 것들이 이미 쓸 수 있다", OK),
           ("계속 산다", "Pod 가 도는 내내", "종료되면 kubelet 이 다시 띄운다", ACC),
           ("맨 나중에 죽는다", "주 컨테이너가 다 죽은 뒤", "필요할 때 먼저 멈추지 않는다", INFO)],
    edges=["시작되면", "종료 시작"])

d.t(36, 452, "일반 사이드카(containers 에 정의): 주 컨테이너와 동급 — 시작·종료 순서 보장 없음",
     12, MUTED, KR, "start")
d.t(36, 476, "배치 Job(18장): 네이티브 사이드카여야 주 컨테이너 완료 시 Pod 도 완료",
     12, MUTED, KR, "start")
d.legend(548, [("먼저 뜨는 성질", OK), ("계속 사는 성질 — 정책 한 줄이 만든다", ACC),
               ("맨 나중에 죽는 성질", INFO)])
d.save("05-03-native-sidecar-lifecycle.svg")
print("ok native-sidecar-lifecycle")

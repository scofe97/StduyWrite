# 03-01 §로컬 클러스터 셋 — 컴포넌트가 어디서 도는가
# 본문·옛 도식: Docker Desktop 은 Linux VM 안, Minikube 는 VM(또는 --vm-driver none 이면 호스트),
#   kind 는 노드마다 컨테이너 하나(VM 없음). 노드 안 접근은 각각 특수 컨테이너 / minikube ssh /
#   docker exec + crictl 로 갈린다.
# 타입 스펙: type-dp-security-matrix.md — 축이 넷(어디서 도나·노드 안 접근·노드 수·쓰임)이고 값이 셋이라 비교 행렬.
#           갈리는 축은 'VM 층이 있는가' 하나이므로 그 열을 판정 축으로 세운다.
#           행은 도구 셋, 열은 네 축(어디서 도나 · 노드 안 접근 · 노드 수)인 격자다.
#           focal 열이 "컴포넌트가 어디서 도나"라 VM 층 유무 하나가 나머지를 정한다.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO
import ddx

# 좌표는 행렬 아래끝에서 산출한다 — 상수 y 를 두면 산문이 마지막 행을 뚫는다.
# y=484·508 은 3 행 행렬의 마지막 행(420~508) 안이라 실제로 글자가 겹쳤다.
MTOP, ROW_H, GAP, NROWS = 196, 88, 12, 3
MBOT = MTOP + 24 + NROWS * (ROW_H + GAP) - GAP   # 508
NOTE_Y, NOTE2_Y = MBOT + 28, MBOT + 52
BAND_Y1, LEG_Y = NOTE2_Y + 24, NOTE2_Y + 40
W, H = 1000, LEG_Y + 40
d = D(W, H, "KUBERNETES IN ACTION · 03-01",
      "갈리는 것은 VM 층이 있는가 하나다",
      "Docker Desktop 과 Minikube 는 리눅스 VM 을 한 겹 두고 그 안에서 컴포넌트를 돌리고, "
      "kind 는 그 VM 층을 컨테이너로 대체해 호스트에 더 가깝다.",
      lead="노드 안에 들어가는 방법도 그 층 구조를 그대로 따라간다")

ddx.band(d, 104, BAND_Y1, "VM 층이 있으면 노드 안에 들어가는 데 한 단계가 더 든다")

ddx.matrix(
    d, x0=36, hdr_y=MTOP, row_h=ROW_H, gap=GAP, focal_col=1,
    cols=[(210, "도구"), (250, "컴포넌트가 어디서 도나"),
          (240, "노드 안에 들어가려면"), (188, "노드 수")],
    rows=[
        ([("Docker Desktop", "가장 간편하다"), ("리눅스 VM 안", "VM 층이 한 겹 있다"),
          ("특수 컨테이너로 우회", "--net=host 등"), ("단일 노드", "")], WARN),
        ([("Minikube", "로컬 개발용"), ("리눅스 VM 안", "--vm-driver none 이면 호스트"),
          ("minikube ssh", "VM 에 바로 들어간다"), ("단일 노드", "")], WARN),
        ([("kind", "Kubernetes in Docker"), ("컨테이너 안", "VM 층이 없다"),
          ("docker exec + crictl", "노드가 컨테이너라서"), ("여러 노드", "컨테이너를 늘리면 된다")], OK),
    ])

d.t(36, NOTE_Y, "kind 의 노드는 컨테이너이므로 02장의 원리가 그대로 적용된다 — 컨테이너 안 프로세스는 "
             "호스트 OS 의 프로세스다.", 12, MUTED, KR, "start")
d.t(36, NOTE2_Y, "그래서 노드 안 컨테이너는 Docker 가 아니라 CRI-O 를 crictl 로 조회한다.",
     12, MUTED, KR, "start")
d.legend(LEG_Y, [("VM 층이 있다", WARN), ("VM 층이 없다 — 호스트에 더 가깝다", OK)])
d.save("03-01-local-cluster-architectures.svg")
print("ok local-cluster-architectures")

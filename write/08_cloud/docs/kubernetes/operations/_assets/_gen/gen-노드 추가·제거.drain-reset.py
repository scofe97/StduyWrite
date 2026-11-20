# 타입 스펙: type-process
# 노드 추가·제거 노드 안전 격리와 단계별 퇴역 파이프라인
import sys
sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 880, 420

d = D(W, H, "KUBERNETES · OPERATIONS",
      "노드 안전 격리와 단계별 퇴역 파이프라인",
      "스케줄링 차단과 축출 뒤 호스트를 초기화하고 마지막에 Node 객체를 지웁니다",
      lead="워크로드 축출(좌측 두 단계)과 호스트 초기화·객체 삭제(우측 두 단계)")

BOX_Y = 110
BOX_H = 220
BOX_W = 188
BOX_GAP = 24
START_X = 28

STAGES = [
    ("1. Cordon", "스케줄링 차단", [
        ("명령", "kubectl cordon", MONO),
        ("상태", "SchedulingDisabled", MONO),
        ("동작", "신규 파드 배정 차단", KR),
        ("영향", "기존 파드는 실행 유지", KR),
    ], ACC, "acc"),
    ("2. Drain", "안전한 워크로드 축출", [
        ("명령", "kubectl drain", MONO),
        ("메커니즘", "Eviction API 사용", KR),
        ("정책", "PodDisruptionBudget 준수", KR),
        ("옵션", "--ignore-daemonsets", MONO),
    ], WARN, "warn"),
    ("3. Reset", "호스트 설정 초기화", [
        ("명령", "kubeadm reset", MONO),
        ("제거", "pki · manifests · etcd", MONO),
        ("etcd", "제어부면 멤버 제거", KR),
        ("남음", "CNI · kubeconfig", KR),
    ], BAD, "bad"),
    ("4. Delete", "클러스터 자원 삭제", [
        ("명령", "kubectl delete node", MONO),
        ("객체", "Node API 리소스 삭제", KR),
        ("확인", "get nodes 에서 사라짐", KR),
        ("결과", "스케줄링 대상 해제", KR),
    ], INFO, "info"),
]

for idx, (title, sub, items, col, marker) in enumerate(STAGES):
    x = START_X + idx * (BOX_W + BOX_GAP)
    # 배경 상자
    d.box(x, BOX_Y, BOX_W, BOX_H, PAPER2, col, 1.1)
    
    # 상단 헤더
    d.tone(x + 6, BOX_Y + 6, BOX_W - 12, 40, col, 4, "18", 1.0)
    d.t(x + BOX_W // 2, BOX_Y + 24, title, 14, col, KR, "middle", 600)
    d.t(x + BOX_W // 2, BOX_Y + 40, sub, 12, SOFT, KR, "middle")
    
    # 항목 목록
    cur_y = BOX_Y + 70
    for label, val, fam in items:
        d.t(x + 14, cur_y, label, 12, MUTED, KR, "start")
        d.t(x + 14, cur_y + 16, val, 12, INK, fam, "start", 500)
        cur_y += 36

    # 다음 단계 연결 화살표
    if idx < len(STAGES) - 1:
        arr_x1 = x + BOX_W + 2
        arr_x2 = arr_x1 + BOX_GAP - 4
        arr_y = BOX_Y + BOX_H // 2
        d.arrow([(arr_x1, arr_y), (arr_x2, arr_y)], MUTED, "ar", 1.4)

# 범례
LEG_Y = 360
d.legend(LEG_Y, [
    ("스케줄링 차단", ACC),
    ("워크로드 축출", WARN),
    ("호스트 초기화", BAD),
    ("클러스터 객체 삭제", INFO),
])

d.save("노드 추가·제거.drain-reset.svg")

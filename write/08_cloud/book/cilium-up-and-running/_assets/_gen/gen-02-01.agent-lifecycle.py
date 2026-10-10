# 타입 스펙: type-process — Cilium Agent 노드 생애주기 5대 핵심 책임.
# 사실 출처: Cilium Up and Running 2장 The Cilium Agent (§Figure 2-2).
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 480
d = D(W, H, "CILIUM UP AND RUNNING · 02-01 §2", "Cilium Agent 생애주기 5대 핵심 책임",
      "노드 데이터패스 확립과 쿠버네티스 상태 유지를 위한 에이전트의 역할 영역",
      "에이전트가 노드에서 독립적으로 수행하는 다섯 가지 핵심 생애주기 책임입니다")

X0 = 25
W_STEP = 158
GAP = 20
Y_STEP = 114
H_STEP = 276

steps = [
    ("런타임 설정 적용", [
        ("cilium-config", "클러스터 ConfigMap 판독"),
        ("CRD 매개변수", "기능별 플래그 확정"),
        ("라우팅 모드 설정", "네이티브 또는 오버레이")
    ], WARN, False),
    ("CNI 플러그인 설치", [
        ("/opt/cni/bin/", "cilium-cni 바이너리"),
        ("/etc/cni/net.d/", "05-cilium.conflist"),
        ("호스트 파일시스템", "바이너리·설정 복사")
    ], SOFT, False),
    ("eBPF 적재 및 맵 생성", [
        ("/sys/fs/bpf", "BPF 파일시스템 마운트"),
        ("tc (tcx) 후크", "패킷 처리 바이트코드"),
        ("BPF 맵 · XDP 가속", "연결 추적 · 선택적 가속")
    ], ACC, True),
    ("K8s 상태 동기화", [
        ("kube-apiserver", "객체 변경 이벤트 감시"),
        ("CiliumNode · CNP", "엔드포인트·정책 수신"),
        ("BPF 맵 원자적 갱신", "커널 테이블 실시간 반영")
    ], INFO, False),
    ("진단 인터페이스 노출", [
        ("cilium-dbg", "노드 내부 진단 CLI"),
        ("cilium.sock", "로컬 REST API 소켓"),
        ("헬스 엔드포인트", "프로브 상태 보고")
    ], OK, False),
]

for i, (title, details, color, focal) in enumerate(steps):
    x = X0 + i * (W_STEP + GAP)
    
    # 카드 본체
    if focal:
        d.tone(x, Y_STEP, W_STEP, H_STEP, color, r=6, op="18", sw=1.4)
    else:
        d.box(x, Y_STEP, W_STEP, H_STEP, PAPER2, RULE, sw=0.9, r=6)
        
    # 역할 제목 (번호 칩 제거로 순차 실행 오해 방지)
    d.t(x + W_STEP/2, Y_STEP + 32, title, 12, INK, KR, "middle", 600)
    d.line(x + 12, Y_STEP + 46, x + W_STEP - 12, Y_STEP + 46, RULE, sw=0.7)
    
    # 세부 항목 상자들
    for j, (top_txt, btm_txt) in enumerate(details):
        yj = Y_STEP + 58 + j * 66
        d.box(x + 8, yj, W_STEP - 16, 56, PAPER, RULE, sw=0.7, r=4)
        is_path = ("/" in top_txt or "." in top_txt) and not any('가' <= ch <= '힣' for ch in top_txt)
        d.t(x + W_STEP/2, yj + 22, top_txt, 10 if is_path else 11, color if j == 0 else INK, MONO if is_path else KR, "middle", 600)
        d.t(x + W_STEP/2, yj + 40, btm_txt, 11, MUTED, KR, "middle")

# 하단 범례 (카드 순서 일치)
d.legend(428, [
    ("런타임 설정", WARN),
    ("호스트 CNI 배포", SOFT),
    ("커널 데이터패스 (핵심)", ACC),
    ("API 동기화", INFO),
    ("진단 엔드포인트", OK),
])

d.save("02-01.agent-lifecycle.svg")

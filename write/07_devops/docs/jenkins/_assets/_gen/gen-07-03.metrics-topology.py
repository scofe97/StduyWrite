# 타입 스펙: type-architecture
# 5절 컨트롤러 단일 수집 지점과 관측성 구조 — Prometheus 수집기와 컨트롤러 단일 지점 및 에이전트 OS 수집 토폴로지
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, INFO, PAPER, PAPER2, KR, MONO

W, H = 960, 460
d = D(W, H, "JENKINS · METRICS TOPOLOGY",
      "컨트롤러 단일 수집 지점과 관측성 구조",
      "Prometheus 수집기가 컨트롤러와 에이전트 OS 수집기를 스크랩하는 관측성 토폴로지",
      lead="컨트롤러 한 곳에서 Jenkins 지표 수집 · 에이전트 머신의 OS 계층 지표 수집 분리")

# ── 1. 구역 (Zones) ──────────────────────────────────────────────────────
# Zone 1: 외부 관측성 계층 (상단)
d.o.append(f'<rect x="240" y="92" width="480" height="68" rx="8" fill="{PAPER2}" stroke="{RULE}" stroke-width="0.8" stroke-dasharray="5 4"/>')
d.t(254, 108, "OBSERVABILITY TIER", 9, SOFT, MONO, "start", 600)

# Zone 2: 컨트롤러 JVM 계층 (하단 좌측 - 단일 원천)
d.o.append(f'<rect x="24" y="184" width="384" height="216" rx="8" fill="{PAPER2}" stroke="{ACC}" stroke-width="0.9" stroke-dasharray="5 4"/>')
d.t(38, 200, "CONTROLLER TIER · SINGLE SOURCE", 9, ACC, MONO, "start", 600)

# Zone 3: 에이전트 OS 계층 (하단 우측 - 환경별 분기)
d.o.append(f'<rect x="420" y="184" width="516" height="216" rx="8" fill="{PAPER2}" stroke="{RULE}" stroke-width="0.8" stroke-dasharray="5 4"/>')
d.t(434, 200, "AGENT TIER", 9, SOFT, MONO, "start", 600)


# ── 2. 연결선 (Connectors) — z-order 상 노드보다 먼저 그림 ──────────────
# 화살표 1: Prometheus -> Controller (좌측으로 꺾여 컨트롤러 상단 진입)
d.arrow([(252, 134), (216, 134), (216, 208)], c=ACC, m="acc", sw=1.4)
d.t(206, 170, "스크랩", 11, ACC, KR, "end", 600)

# 화살표 2: Prometheus -> 정적 VM (수직 하강하여 정적 VM 상단 진입)
d.arrow([(552, 154), (552, 208)], c=OK, m="ok", sw=1.4)
d.t(562, 170, "스크랩", 11, OK, KR, "start", 600)

# 화살표 3: Prometheus -> 동적 Pod (우측으로 꺾여 Pod 상단 진입)
d.arrow([(708, 134), (804, 134), (804, 208)], c=OK, m="ok", sw=1.4)
d.t(814, 170, "스크랩", 11, OK, KR, "start", 600)


# ── 3. 컴포넌트 노드 (Components) ────────────────────────────────────────

# [Zone 1] Prometheus 수집기 박스
d.box(252, 114, 456, 40, fill=PAPER, stroke=RULE, sw=1.0, r=6)
d.t(480, 130, "Prometheus 수집기", 13, INK, KR, "middle", 600)
d.t(480, 146, "시계열 저장소 저장 · 외부 관측성 도구 위임", 11, MUTED, KR, "middle")


# [Zone 2] Jenkins 컨트롤러 (Focal · 단일 원천)
d.tone(36, 208, 360, 182, c=ACC, r=6, op="12", sw=1.4)
d.t(48, 226, "Jenkins 컨트롤러", 13, ACC, KR, "start", 600)
d.t(48, 242, "애플리케이션 지표의 단일 원천", 11, MUTED, KR, "start")

# 엔드포인트 두 경로
d.box(48, 252, 162, 34, fill=PAPER, stroke=INFO, sw=0.9, r=4)
d.t(129, 266, "/prometheus/", 11, INFO, MONO, "middle", 600)
d.t(129, 279, "Prometheus 플러그인", 11, MUTED, KR, "middle")

d.box(222, 252, 162, 34, fill=PAPER, stroke=INFO, sw=0.9, r=4)
d.t(303, 266, "/metrics/", 11, INFO, MONO, "middle", 600)
d.t(303, 279, "Metrics 플러그인", 11, MUTED, KR, "middle")

# 노출 지표 그룹 (3절 표 지표)
d.box(48, 294, 336, 86, fill=PAPER, stroke=RULE, sw=0.8, r=4)
d.t(60, 312, "큐", 11, SOFT, KR, "start", 600)
d.t(90, 312, "jenkins.queue.size.value", 11, INK, MONO, "start")

d.t(60, 330, "실행기", 11, SOFT, KR, "start", 600)
d.t(106, 330, "jenkins.executor.in-use.value", 11, INK, MONO, "start")

d.t(60, 348, "빌드", 11, SOFT, KR, "start", 600)
d.t(96, 348, "jenkins.job.building.duration", 11, INK, MONO, "start")

d.t(60, 366, "JVM", 11, SOFT, KR, "start", 600)
d.t(94, 366, "vm.memory.heap.usage · vm.gc.X.time", 11, INK, MONO, "start")


# [Zone 3] 에이전트 카드 1: 정적 VM 에이전트
d.box(434, 208, 236, 182, fill=PAPER2, stroke=OK, sw=1.1, r=6)
d.t(446, 226, "정적 VM 에이전트", 13, OK, KR, "start", 600)
d.t(446, 242, "가상 머신 환경", 11, MUTED, KR, "start")

# 정적 VM 수집기
d.box(446, 252, 212, 34, fill=PAPER, stroke=OK, sw=0.9, r=4)
d.t(552, 266, "node_exporter", 11, OK, MONO, "middle", 600)
d.t(552, 279, "가상 머신 상주 수집", 11, MUTED, KR, "middle")

# 정적 VM OS 수집 대상
d.box(446, 294, 212, 86, fill=PAPER, stroke=RULE, sw=0.8, r=4)
d.t(458, 312, "OS 계층 지표 수집", 11, SOFT, KR, "start", 600)
d.t(458, 334, "CPU · 메모리", 12, INK, KR, "start")
d.t(458, 356, "디스크 I/O", 12, INK, KR, "start")


# [Zone 3] 에이전트 카드 2: 동적 Kubernetes Pod 에이전트
d.box(686, 208, 236, 182, fill=PAPER2, stroke=OK, sw=1.1, r=6)
d.t(698, 226, "동적 Kubernetes Pod 에이전트", 12, OK, KR, "start", 600)
d.t(698, 242, "컨테이너 환경", 11, MUTED, KR, "start")

# 동적 Pod 수집기
d.box(698, 252, 212, 34, fill=PAPER, stroke=OK, sw=0.9, r=4)
d.t(804, 266, "cAdvisor · kube-state-metrics", 10, OK, MONO, "middle", 600)
d.t(804, 279, "노드 계층 수집", 11, MUTED, KR, "middle")

# 동적 Pod OS 수집 대상
d.box(698, 294, 212, 86, fill=PAPER, stroke=RULE, sw=0.8, r=4)
d.t(710, 312, "컨테이너 자원 수집", 11, SOFT, KR, "start", 600)
d.t(710, 334, "노드 계층 지표 수집", 12, INK, KR, "start")
d.t(710, 356, "빌드마다 Pod 생성", 11, MUTED, KR, "start")


# ── 4. 범례 ────────────────────────────────────────────────────────────
d.legend(412, [
    ("컨트롤러 단일 수집 지점", ACC),
    ("에이전트 OS 계층 수집", OK),
    ("지표 노출 엔드포인트", INFO),
])

out_path = sys.argv[1] if len(sys.argv) > 1 else str(pathlib.Path(__file__).resolve().parent.parent / "07-03.metrics-topology.svg")
d.save(out_path)
print("ok 07-03.metrics-topology.svg")

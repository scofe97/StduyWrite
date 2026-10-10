# 타입 스펙: type-data-flow — 노드별 Hubble 서버에서 중앙 Relay 및 CLI·UI 로 흐르는 관측 데이터 흐름.
# 사실 출처: Cilium Up and Running 2장 Hubble (§Figure 2-5).
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 480
d = D(W, H, "CILIUM UP AND RUNNING · 02-01 §5", "Hubble 관측 데이터 수집 및 집계 흐름",
      "노드별 커널 이벤트 캡처부터 중앙 Relay 집계 및 UI/CLI 실시간 시각화까지",
      "노드 로컬 버퍼에서 이벤트를 수집해 Relay 가 단일 스트림으로 엮어냅니다")

Y_TOP = 106
H_MAIN = 308

# 좌측 영역: 노드 레벨 로컬 관측 (Worker Node 1 & 2)
# 노드 1
d.box(24, Y_TOP, 280, 146, PAPER2, RULE, sw=0.9, r=6)
d.t(36, Y_TOP + 22, "Worker Node 1", 10, SOFT, MONO, "start", 600)
d.tone(36, Y_TOP + 36, 116, 96, ACC, r=4, op="14", sw=1.0)
d.t(94, Y_TOP + 60, "eBPF 이벤트", 11, ACC, KR, "middle", 600)
d.t(94, Y_TOP + 80, "링 버퍼 기록", 11, INK, KR, "middle")
d.t(94, Y_TOP + 100, "커널 드롭·전달", 11, MUTED, KR, "middle")

d.box(172, Y_TOP + 36, 120, 96, PAPER, INFO, sw=0.9, r=4)
d.t(232, Y_TOP + 60, "Hubble Server", 11, INFO, MONO, "middle", 600)
d.t(232, Y_TOP + 80, "메타데이터 보강", 11, INK, KR, "middle")
d.chip(232, Y_TOP + 106, "gRPC :4244", INFO, size=9)

d.arrow([(152, Y_TOP + 84), (172, Y_TOP + 84)], ACC, "acc", sw=1.2)

# 노드 2
d.box(24, Y_TOP + 162, 280, 146, PAPER2, RULE, sw=0.9, r=6)
d.t(36, Y_TOP + 184, "Worker Node 2", 10, SOFT, MONO, "start", 600)
d.tone(36, Y_TOP + 198, 116, 96, ACC, r=4, op="14", sw=1.0)
d.t(94, Y_TOP + 222, "eBPF 이벤트", 11, ACC, KR, "middle", 600)
d.t(94, Y_TOP + 242, "링 버퍼 기록", 11, INK, KR, "middle")
d.t(94, Y_TOP + 262, "커널 드롭·전달", 11, MUTED, KR, "middle")

d.box(172, Y_TOP + 198, 120, 96, PAPER, INFO, sw=0.9, r=4)
d.t(232, Y_TOP + 222, "Hubble Server", 11, INFO, MONO, "middle", 600)
d.t(232, Y_TOP + 242, "메타데이터 보강", 11, INK, KR, "middle")
d.chip(232, Y_TOP + 268, "gRPC :4244", INFO, size=9)

d.arrow([(152, Y_TOP + 246), (172, Y_TOP + 246)], ACC, "acc", sw=1.2)


# 중앙 영역: Hubble Relay (클러스터 단위 집계)
X_RELAY = 348
W_RELAY = 240
d.tone(X_RELAY, Y_TOP + 40, W_RELAY, 228, INFO, r=6, op="18", sw=1.4)
d.box(X_RELAY + 14, Y_TOP + 54, 130, 24, PAPER, INFO, sw=1.0, r=4)
d.t(X_RELAY + 79, Y_TOP + 70, "Hubble Relay", 11, INFO, MONO, "middle", 600)

d.t(X_RELAY + W_RELAY/2, Y_TOP + 116, "피어 자동 탐색 및 스트림 병합", 11, INK, KR, "middle", 600)
d.t(X_RELAY + W_RELAY/2, Y_TOP + 138, "노드별 gRPC 엔드포인트 연결", 11, MUTED, KR, "middle")
d.t(X_RELAY + W_RELAY/2, Y_TOP + 160, "클러스터 전역 플로우 버퍼", 11, MUTED, KR, "middle")

d.chip(X_RELAY + W_RELAY/2, Y_TOP + 210, "Service :80 (:4245)", INFO, size=10)

# 노드 1 & 2 -> Relay 연결선
d.arrow([(292, Y_TOP + 84), (320, Y_TOP + 84), (320, Y_TOP + 130), (X_RELAY, Y_TOP + 130)], INFO, "info", sw=1.3)
d.arrow([(292, Y_TOP + 246), (320, Y_TOP + 246), (320, Y_TOP + 178), (X_RELAY, Y_TOP + 178)], INFO, "info", sw=1.3)


# 우측 영역: 분석 및 시각화 도구 (Hubble CLI & UI)
X_CLI = 632
W_CLI = 264
d.box(X_CLI, Y_TOP, W_CLI, H_MAIN, PAPER2, RULE, sw=0.9, r=6)
d.t(X_CLI + 16, Y_TOP + 22, "관측 클라이언트", 11, SOFT, KR, "start", 600)

# Hubble CLI
d.box(X_CLI + 14, Y_TOP + 36, W_CLI - 28, 116, PAPER, WARN, sw=0.9, r=4)
d.t(X_CLI + 26, Y_TOP + 60, "Hubble CLI", 11, WARN, MONO, "start", 600)
d.t(X_CLI + 26, Y_TOP + 84, "실시간 패킷 흐름 쿼리", 11, INK, KR, "start")
d.chip(X_CLI + 124, Y_TOP + 114, "hubble observe", WARN, size=10)

# Hubble UI
d.box(X_CLI + 14, Y_TOP + 168, W_CLI - 28, 116, PAPER, OK, sw=0.9, r=4)
d.t(X_CLI + 26, Y_TOP + 192, "Hubble UI", 11, OK, MONO, "start", 600)
d.t(X_CLI + 26, Y_TOP + 216, "토폴로지 서비스 맵 대시보드", 11, INK, KR, "start")
d.chip(X_CLI + 124, Y_TOP + 246, "Service :80 (:8081)", OK, size=10)

# Relay -> CLI & UI 연결선
d.arrow([(X_RELAY + W_RELAY, Y_TOP + 120), (610, Y_TOP + 120), (610, Y_TOP + 94), (X_CLI + 14, Y_TOP + 94)], WARN, "warn", sw=1.3)
d.arrow([(X_RELAY + W_RELAY, Y_TOP + 188), (610, Y_TOP + 188), (610, Y_TOP + 226), (X_CLI + 14, Y_TOP + 226)], OK, "ok", sw=1.3)


# 하단 범례
d.legend(430, [
    ("커널 eBPF 수집", ACC),
    ("중앙 스트림 집계 (핵심)", INFO),
    ("CLI 터미널 쿼리", WARN),
    ("UI 그래픽 시각화", OK),
])

d.save("02-01.hubble-flow-architecture.svg")

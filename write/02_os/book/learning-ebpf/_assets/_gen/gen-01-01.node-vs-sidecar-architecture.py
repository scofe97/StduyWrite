# 타입 스펙: type-architecture — 사이드카 프록시 모델과 노드 커널 eBPF 모델의 패킷 경로 및 관측 범위 비교
# 사실 출처: 원문 ebpf1.txt 433-508(단일 노드 Pod 3개 공유 커널·사이드카 4대 비용·사이드카 미주입 채굴 컨테이너 탐지)
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, BAD, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 520
d = D(W, H, "LEARNING EBPF · 01-01 §5", "사이드카 프록시 모델과 노드 커널 eBPF 모델의 구조 비교",
      "사이드카는 프록시에 닿으려 커널 네트워크 스택을 한 번 더 지나지만 eBPF 는 단일 커널에서 모든 컨테이너를 봅니다",
      "사이드카 4대 비용: 재기동 · YAML 주입 · 기동 레이스 · 지연 vs eBPF: 단일 커널 전역 관측")

# 좌측 영역: 사이드카 모델
Z1_X, Z1_Y, Z1_W, Z1_H = 36, 104, 404, 340
d.box(Z1_X, Z1_Y, Z1_W, Z1_H, PAPER2, RULE, 1.0, 8)
d.t(Z1_X + 16, Z1_Y + 24, "전통적인 사이드카 프록시 모델", 13, WARN, KR, "start", 600)
d.t(Z1_X + Z1_W - 16, Z1_Y + 24, "Pod 단위 컨테이너 주입", 12, MUTED, KR, "end")
d.line(Z1_X + 12, Z1_Y + 36, Z1_X + Z1_W - 12, Z1_Y + 36, RULE, 0.6)

# 좌측 Pod 1 (앱 + 사이드카)
P1_Y = Z1_Y + 48
d.box(Z1_X + 16, P1_Y, Z1_W - 32, 80, PAPER, RULE, 0.8, 6)
d.t(Z1_X + 28, P1_Y + 20, "Pod A 트래픽 경로", 12, INK, KR, "start", 600)
PW, PG = 96, 30
px = [Z1_X + 28 + k * (PW + PG) for k in range(3)]
for k, (lab1, lab2, ec) in enumerate([("App", "컨테이너", RULE), ("커널", "네트워크 스택", INFO), ("Envoy", "사이드카", WARN)]):
    d.box(px[k], P1_Y + 28, PW, 44, PAPER2, ec, 0.8, 4)
    d.t(px[k] + PW / 2, P1_Y + 46, lab1, 12, INK if k != 2 else WARN, KR, "middle", 600)
    d.t(px[k] + PW / 2, P1_Y + 62, lab2, 11, MUTED, KR, "middle")
for k in range(2):
    d.arrow([(px[k] + PW + 2, P1_Y + 50), (px[k + 1] - 2, P1_Y + 50)], MUTED, "ar", 1.2)

# 좌측 Pod 2 (YAML 주입 및 지연)
P2_Y = P1_Y + 90
d.box(Z1_X + 16, P2_Y, Z1_W - 32, 70, PAPER, RULE, 0.8, 6)
d.t(Z1_X + 28, P2_Y + 20, "Pod B (애플리케이션 + 사이드카)", 12, INK, KR, "start", 600)
d.t(Z1_X + 28, P2_Y + 42, "YAML 수정 필수 · 어드미션 제어 의존", 12, MUTED, KR, "start")
d.t(Z1_X + 28, P2_Y + 58, "컨테이너 기동 순서 레이스 컨디션 발생 가능", 12, WARN, KR, "start")

# 좌측 Pod 3 (채굴기 - 사이드카 미주입)
P3_Y = P2_Y + 80
d.tone(Z1_X + 16, P3_Y, Z1_W - 32, 90, BAD, r=6, op="10", sw=1.2)
d.t(Z1_X + 28, P3_Y + 22, "악성 Pod C (암호화폐 채굴기 침투)", 12, BAD, KR, "start", 600)
d.t(Z1_X + 28, P3_Y + 46, "공격자가 사이드카 주입 라벨을 의도적 누락", 12, INK, KR, "start")
d.t(Z1_X + 28, P3_Y + 68, "사이드카 미주입으로 감시 우회 · 마이닝 풀 연결", 12, BAD, KR, "start", 600)

# 우측 영역: eBPF 모델
Z2_X = 480
d.box(Z2_X, Z1_Y, Z1_W, Z1_H, PAPER2, RULE, 1.0, 8)
d.t(Z2_X + 16, Z1_Y + 24, "호스트 커널 eBPF 모델", 13, OK, KR, "start", 600)
d.t(Z2_X + Z1_W - 16, Z1_Y + 24, "단일 커널 전역 가시성", 12, MUTED, KR, "end")
d.line(Z2_X + 12, Z1_Y + 36, Z2_X + Z1_W - 12, Z1_Y + 36, RULE, 0.6)

# 우측 상단: 모든 컨테이너 워크로드
CW_Y = Z1_Y + 48
d.box(Z2_X + 16, CW_Y, Z1_W - 32, 100, PAPER, RULE, 0.8, 6)
d.t(Z2_X + 28, CW_Y + 22, "노드 내 모든 워크로드 (Pod A · B · 악성 Pod C)", 12, INK, KR, "start", 600)

d.box(Z2_X + 28, CW_Y + 36, 106, 50, PAPER2, RULE, 0.8, 4)
d.t(Z2_X + 81, CW_Y + 58, "Pod A", 12, INK, MONO, "middle", 600)
d.t(Z2_X + 81, CW_Y + 74, "일반 앱", 12, MUTED, KR, "middle")

d.box(Z2_X + 148, CW_Y + 36, 106, 50, PAPER2, RULE, 0.8, 4)
d.t(Z2_X + 201, CW_Y + 58, "Pod B", 12, INK, MONO, "middle", 600)
d.t(Z2_X + 201, CW_Y + 74, "일반 앱", 12, MUTED, KR, "middle")

d.box(Z2_X + 268, CW_Y + 36, 106, 50, PAPER2, BAD, 0.8, 4)
d.t(Z2_X + 321, CW_Y + 58, "Pod C", 12, BAD, MONO, "middle", 600)
d.t(Z2_X + 321, CW_Y + 74, "채굴 앱", 12, BAD, KR, "middle")

# 워크로드 -> 커널 화살표
d.arrow([(Z2_X + Z1_W / 2, CW_Y + 102), (Z2_X + Z1_W / 2, CW_Y + 126)], MUTED, "ar", 1.2)

# 우측 하단: 커널 eBPF 핵심 (FOCAL)
EK_Y = CW_Y + 128
d.tone(Z2_X + 16, EK_Y, Z1_W - 32, 140, ACC, r=6, op="14", sw=1.4)
d.t(Z2_X + 28, EK_Y + 26, "단일 호스트 Linux 커널 eBPF 프로그램", 13, ACC, KR, "start", 600)
d.t(Z2_X + 28, EK_Y + 50, "커널 관측 지점: 모든 컨테이너 프로세스", 12, INK, KR, "start")
d.t(Z2_X + 28, EK_Y + 72, "네트워크 보안 정책", 12, INK, KR, "start")
d.t(Z2_X + 28, EK_Y + 96, "마이닝 풀 연결을 정책으로 차단", 12, ACC, KR, "start", 600)
d.t(Z2_X + 28, EK_Y + 118, "사이드카 주입 여부와 무관한 감시", 12, OK, KR, "start")

d.legend(470, [
    ("사이드카 오버헤드", WARN),
    ("커널 스택 경유", INFO),
    ("미주입 사각지대", BAD),
    ("공유 커널 모델", OK),
    ("eBPF 전역 감시", ACC),
])
d.save("01-01.node-vs-sidecar-architecture.svg")

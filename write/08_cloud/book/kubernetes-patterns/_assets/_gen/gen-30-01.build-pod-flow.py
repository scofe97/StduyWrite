# 타입 스펙: type-data-flow
# 30-01 Build Pod — init container 기반 순차 빌드-배포와 데이터 흐름
# 본문: 책은 in-cluster 빌드의 핵심 재료를 드러내기 위해 Pod 하나로 완전한
#   빌드-배포 사이클을 구성한다. git-sync init container 가 소스를 받아
#   emptyDir 에 두고, BuildKit rootless init container 가 이미지를 빌드해
#   레지스트리에 push 하며, 주 컨테이너 image-update 가 Deployment 를 패치한다.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 960, 390

d = D(W, H, "KUBERNETES PATTERNS · 30-01",
      "Build Pod 순차 실행과 데이터 흐름",
      "init container 기반 소스 동기화와 BuildKit rootless 빌드, 주 컨테이너 배포 패치 순차 데이터 파이프라인",
      lead="git-sync · BuildKit rootless · image-update 순차 데이터 전달")

# ── Build Pod 경계 영역 ──────────────────────────────────────────────────────
POD_X = 20
POD_Y = 88
POD_W = 630
POD_H = 244
d.box(POD_X, POD_Y, POD_W, POD_H, PAPER2, RULE, 1.0, 8)
d.t(POD_X + 16, POD_Y + 18, "Build Pod 경계 (단일 Pod 내 순차 실행)", 11, SOFT, KR, "start")

# ── 1행: 빌드 및 push 파이프라인 (좌 → 우) ──────────────────────────────────
ROW1_Y = 114
BOX_H = 78

# 1. git-sync (init)
G_X = 32
G_W = 150
d.tone(G_X, ROW1_Y, G_W, BOX_H, INFO, 6, "10", 1.1)
d.t(G_X + G_W // 2, ROW1_Y + 24, "1단계: git-sync", 14, INFO, KR, "middle", 600)
d.t(G_X + G_W // 2, ROW1_Y + 44, "원격 소스 동기화", 13, INK, KR, "middle")
d.t(G_X + G_W // 2, ROW1_Y + 64, "init container", 11, SOFT, MONO, "middle")

# 화살표: git-sync -> emptyDir (간격: 64px, x=182..246)
E_X = 246
E_W = 150
d.arrow([(G_X + G_W + 2, ROW1_Y + BOX_H // 2), (E_X - 2, ROW1_Y + BOX_H // 2)], MUTED, "ar", 1.3)
d.t(214, ROW1_Y + BOX_H // 2 - 8, "소스 저장", 13, MUTED, KR, "middle")

# 2. 공유 emptyDir
d.box(E_X, ROW1_Y, E_W, BOX_H, PAPER, RULE, 0.9, 6)
d.t(E_X + E_W // 2, ROW1_Y + 24, "공유 emptyDir", 13, MUTED, KR, "middle", 600)
d.t(E_X + E_W // 2, ROW1_Y + 44, "체크아웃 소스 보관", 13, INK, KR, "middle")
d.t(E_X + E_W // 2, ROW1_Y + 64, "/workspace", 11, SOFT, MONO, "middle")

# 화살표: emptyDir -> BuildKit (간격: 54px, x=396..450)
B_X = 450
B_W = 186
d.arrow([(E_X + E_W + 2, ROW1_Y + BOX_H // 2), (B_X - 2, ROW1_Y + BOX_H // 2)], MUTED, "ar", 1.3)
d.t(423, ROW1_Y + BOX_H // 2 - 8, "소스 전달", 13, MUTED, KR, "middle")

# 3. BuildKit rootless (init) — FOCAL
d.tone(B_X, ROW1_Y, B_W, BOX_H, ACC, 6, "16", 1.4)
d.t(B_X + B_W // 2, ROW1_Y + 24, "2단계: BuildKit", 14, ACC, KR, "middle", 600)
d.t(B_X + B_W // 2, ROW1_Y + 44, "rootless 비특권 빌드", 13, INK, KR, "middle", 500)
d.t(B_X + B_W // 2, ROW1_Y + 64, "buildctl-daemonless", 11, ACC, MONO, "middle")

# 화살표: BuildKit -> 이미지 레지스트리 (복도: x=650..730, 중심 x=690)
REG_X = 730
REG_W = 210
d.arrow([(B_X + B_W + 2, ROW1_Y + BOX_H // 2), (REG_X - 2, ROW1_Y + BOX_H // 2)], OK, "ok", 1.4)
d.t(690, ROW1_Y + BOX_H // 2 - 8, "이미지 push", 13, OK, KR, "middle")

# 4. 이미지 레지스트리 (외부)
d.tone(REG_X, ROW1_Y, REG_W, BOX_H, OK, 6, "0E", 1.1)
d.t(REG_X + REG_W // 2, ROW1_Y + 24, "이미지 레지스트리", 14, OK, KR, "middle", 600)
d.t(REG_X + REG_W // 2, ROW1_Y + 44, "app:1.0 태그 저장", 13, INK, KR, "middle")
d.t(REG_X + REG_W // 2, ROW1_Y + 64, "registry.example.com", 11, SOFT, MONO, "middle")


# ── 2행: 배포 패치 및 보안 설정 ─────────────────────────────────────────────
ROW2_Y = 236

# 보안 및 자격증명 요약 박스 (Pod 내부 좌측)
SEC_X = 32
SEC_W = 364
d.tone(SEC_X, ROW2_Y, SEC_W, BOX_H, WARN, 6, "0A", 0.9)
d.t(SEC_X + 16, ROW2_Y + 22, "보안 및 자격증명 주입", 13, WARN, KR, "start", 600)
d.t(SEC_X + 16, ROW2_Y + 44, "2단계: UID 1000 · push용 Secret 주입", 13, INK, KR, "start")
d.t(SEC_X + 16, ROW2_Y + 66, "3단계: Deployment patch 권한 ServiceAccount", 13, MUTED, KR, "start")

# 수직 화살표: BuildKit -> image-update (간격: 44px)
d.arrow([(B_X + B_W // 2, ROW1_Y + BOX_H + 2), (B_X + B_W // 2, ROW2_Y - 2)], MUTED, "ar", 1.3)
d.t(B_X + B_W // 2 - 36, (ROW1_Y + BOX_H + ROW2_Y) // 2 + 4, "빌드 완료", 13, MUTED, KR, "middle")

# 5. image-update (주 컨테이너)
U_X = B_X
U_W = B_W
d.tone(U_X, ROW2_Y, U_W, BOX_H, OK, 6, "10", 1.1)
d.t(U_X + U_W // 2, ROW2_Y + 24, "3단계: image-update", 14, OK, KR, "middle", 600)
d.t(U_X + U_W // 2, ROW2_Y + 44, "kubectl patch 실행", 13, INK, KR, "middle")
d.t(U_X + U_W // 2, ROW2_Y + 64, "patch 권한 SA 사용", 13, WARN, KR, "middle")

# 화살표: image-update -> Deployment (복도: x=650..730, 중심 x=690)
DEP_X = REG_X
DEP_W = REG_W
d.arrow([(U_X + U_W + 2, ROW2_Y + BOX_H // 2), (DEP_X - 2, ROW2_Y + BOX_H // 2)], INFO, "info", 1.4)
d.t(690, ROW2_Y + BOX_H // 2 - 8, "배포 패치", 13, INFO, KR, "middle")

# 수직 화살표: 이미지 레지스트리 -> Deployment
d.arrow([(REG_X + REG_W // 2, ROW1_Y + BOX_H + 2), (DEP_X + DEP_W // 2, ROW2_Y - 2)], MUTED, "ar", 1.3)
d.t(REG_X + REG_W // 2 + 48, (ROW1_Y + BOX_H + ROW2_Y) // 2 + 4, "새 이미지 참조", 13, MUTED, KR, "middle")

# 6. 대상 Deployment (외부)
d.tone(DEP_X, ROW2_Y, DEP_W, BOX_H, INFO, 6, "0E", 1.1)
d.t(DEP_X + DEP_W // 2, ROW2_Y + 24, "대상 Deployment", 14, INFO, KR, "middle", 600)
d.t(DEP_X + DEP_W // 2, ROW2_Y + 44, "image 필드 갱신", 13, INK, KR, "middle")
d.t(DEP_X + DEP_W // 2, ROW2_Y + 64, "새 Pod 롤아웃 시작", 13, MUTED, KR, "middle")


# ── 범례 ─────────────────────────────────────────────────────────────────
LEG_Y = ROW2_Y + BOX_H + 20
d.legend(LEG_Y, [
    ("초기화 (init)", INFO),
    ("rootless 빌더 (focal)", ACC),
    ("주 컨테이너 / 레지스트리", OK),
    ("권한 · 보안 설정", WARN),
])

d.save("30-01.build-pod-flow.svg")
print("ok gen-30-01.build-pod-flow")

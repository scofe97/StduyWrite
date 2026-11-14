# 타입 스펙: type-layers
# 30-01 두 계층 — 빌드 오케스트레이터와 컨테이너 이미지 빌더 계층 구조
# 본문: 이미지 빌드 도구는 이미지만 만드는 빌더 계층과, 파이프라인 조율과
#   배포 갱신을 맡는 오케스트레이터 계층으로 나뉜다.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 960, 380

d = D(W, H, "KUBERNETES PATTERNS · 30-01",
      "빌드 오케스트레이터와 이미지 빌더의 계층 분리",
      "상위 파이프라인 조율 계층과 하위 OCI 이미지 생성 빌더 계층의 역할 및 도구 분리 구조",
      lead="파이프라인 조율 · OCI 이미지 생성 · rootless 빌드 계층 분리")

# ── 좌측 방향 지시자 ─────────────────────────────────────────────────────────
d.t(20, 195, "추상화 ↑", 11, SOFT, KR, "start")

# ── 층 2 (상위): 빌드 오케스트레이터 ─────────────────────────────────────────
L_X = 80
L_W = 856
L2_Y = 100
L2_H = 86

# focal 층 (ACC 테두리 및 틴트)
d.tone(L_X, L2_Y, L_W, L2_H, ACC, 6, "10", 1.4)

# 층 헤더 (태그 · 이름 · 역할)
d.t(L_X + 20, L2_Y + 24, "L2", 11, ACC, MONO, "start", 600)
d.t(L_X + 48, L2_Y + 24, "빌드 오케스트레이터", 15, ACC, KR, "start", 600)
d.t(L_X + L_W - 20, L2_Y + 24, "파이프라인 조율 · 배포 갱신", 13, INK, KR, "end", 500)

d.line(L_X + 16, L2_Y + 36, L_X + L_W - 16, L2_Y + 36, RULE, 0.8)

# 오케스트레이터 하위 구분 (범용 vs 특화)
BOX_W = (L_W - 32 - 16) // 2
B1_X = L_X + 16
B2_X = B1_X + BOX_W + 16
BOX_Y = L2_Y + 44
BOX_H = 32

d.box(B1_X, BOX_Y, BOX_W, BOX_H, PAPER, RULE, 0.8, 4)
d.t(B1_X + 14, BOX_Y + 21, "범용 CI/CD:", 13, INK, KR, "start", 600)
d.t(B1_X + 96, BOX_Y + 21, "Tekton · Argo CD · Flux", 13, MUTED, KR, "start")

d.box(B2_X, BOX_Y, BOX_W, BOX_H, PAPER, RULE, 0.8, 4)
d.t(B2_X + 14, BOX_Y + 21, "특화 도구:", 13, INK, KR, "start", 600)
d.t(B2_X + 80, BOX_Y + 21, "OpenShift Builds · Carvel kbld · Job", 13, MUTED, KR, "start")


# ── 층 1 (하위): 컨테이너 이미지 빌더 ─────────────────────────────────────────
L1_Y = 196
L1_H = 114

d.box(L_X, L1_Y, L_W, L1_H, PAPER2, RULE, 1.0, 6)

# 층 헤더 (태그 · 이름 · 역할)
d.t(L_X + 20, L1_Y + 24, "L1", 11, SOFT, MONO, "start", 600)
d.t(L_X + 48, L1_Y + 24, "컨테이너 이미지 빌더", 15, INK, KR, "start", 600)
d.t(L_X + L_W - 20, L1_Y + 24, "OCI 이미지 생성 · rootless 빌드", 13, MUTED, KR, "end")

d.line(L_X + 16, L1_Y + 36, L_X + L_W - 16, L1_Y + 36, RULE, 0.8)

# 빌더 3분할 열 (카드 형태, 2줄 구성)
COL_GAP = 12
COL_W = (L_W - 32 - COL_GAP * 2) // 3
C1_X = L_X + 16
C2_X = C1_X + COL_W + COL_GAP
C3_X = C2_X + COL_W + COL_GAP
COL_Y = L1_Y + 44
COL_H = 58

# 1. Dockerfile 기반
d.tone(C1_X, COL_Y, COL_W, COL_H, OK, 4, "0A", 0.9)
d.t(C1_X + COL_W // 2, COL_Y + 22, "Dockerfile 기반 빌더", 13, OK, KR, "middle", 600)
d.t(C1_X + COL_W // 2, COL_Y + 44, "BuildKit · Buildah · Kaniko", 13, INK, KR, "middle")

# 2. 다언어 빌더
d.tone(C2_X, COL_Y, COL_W, COL_H, OK, 4, "0A", 0.9)
d.t(C2_X + COL_W // 2, COL_Y + 22, "다언어 소스 빌더", 13, OK, KR, "middle", 600)
d.t(C2_X + COL_W // 2, COL_Y + 44, "Buildpacks (pack · kpack) · S2I", 13, INK, KR, "middle")

# 3. 특화 빌더
d.tone(C3_X, COL_Y, COL_W, COL_H, OK, 4, "0A", 0.9)
d.t(C3_X + COL_W // 2, COL_Y + 22, "특화 빌더 (RUN 없는 rootless)", 13, OK, KR, "middle", 600)
d.t(C3_X + COL_W // 2, COL_Y + 44, "Jib (Java) · ko (Go) · Apko", 13, INK, KR, "middle")


# ── 범례 ─────────────────────────────────────────────────────────────────
LEG_Y = L1_Y + L1_H + 20
d.legend(LEG_Y, [
    ("파이프라인 조율 (상위)", ACC),
    ("이미지 빌더 (하위)", OK),
])

d.save("30-01.builder-orchestrator-layers.svg")
print("ok gen-30-01.builder-orchestrator-layers")

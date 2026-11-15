# 타입 스펙: type-process
# 01-02 rootless 빌드의 조건 — 전체 지도
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 960, 360

d = D(W, H, "DEVOPS · CONTAINER · 01-02",
      "rootless 빌드의 전제와 조건 전체 지도",
      "Dockerfile RUN 명령 격리 요구부터 user namespace, OverlayFS, 보안 프로필 완화 및 실행 모델 비교 흐름",
      lead="RUN 격리 문제(§1) → 세 가지 핵심 조건(§2) → 실행 모델 비교(§3) → 보안 제약과 분리(§4)")

Y0 = 104
BOX_H = 160

# 1. 문제 (§1)
X1 = 24
W1 = 205
d.tone(X1, Y0, W1, BOX_H, BAD, 6, "10", 1.2)
d.t(X1 + W1 // 2, Y0 + 24, "1. RUN 과 권한 문제", 14, BAD, KR, "middle", 600)
d.t(X1 + 14, Y0 + 52, "· 임시 컨테이너 격리", 13, INK, KR, "start")
d.t(X1 + 14, Y0 + 74, "· unshare 호출 실패", 13, MUTED, KR, "start")
d.t(X1 + 14, Y0 + 96, "· 파일 마운트 차단", 13, MUTED, KR, "start")
d.t(X1 + 14, Y0 + 118, "· 데몬 부재 시 문제", 13, SOFT, KR, "start")
d.chip(X1 + W1 // 2, Y0 + 142, "권한 부족 오류", BAD, 11)

# 화살표 1 -> 2
X1_END = X1 + W1
X2 = 253
d.arrow([(X1_END + 2, Y0 + BOX_H // 2), (X2 - 2, Y0 + BOX_H // 2)], MUTED, "ar", 1.3)

# 2. 원리 (§2) — FOCAL
W2 = 224
d.tone(X2, Y0, W2, BOX_H, ACC, 6, "14", 1.4)
d.t(X2 + W2 // 2, Y0 + 24, "2. 세 가지 핵심 조건", 14, ACC, KR, "middle", 600)
d.t(X2 + 14, Y0 + 52, "· user namespace: UID 매핑", 13, INK, KR, "start")
d.t(X2 + 14, Y0 + 74, "· OverlayFS: 커널 5.11+", 13, INK, KR, "start")
d.t(X2 + 14, Y0 + 96, "· seccomp: unshare 허용", 13, MUTED, KR, "start")
d.t(X2 + 14, Y0 + 118, "· AppArmor: mount 허용", 13, MUTED, KR, "start")
d.chip(X2 + W2 // 2, Y0 + 142, "비특권 rootless 성립", ACC, 11)

# 화살표 2 -> 3
X2_END = X2 + W2
X3 = 501
d.arrow([(X2_END + 2, Y0 + BOX_H // 2), (X3 - 2, Y0 + BOX_H // 2)], MUTED, "ar", 1.3)

# 3. 비교 (§3)
W3 = 205
d.tone(X3, Y0, W3, BOX_H, INFO, 6, "10", 1.2)
d.t(X3 + W3 // 2, Y0 + 24, "3. RUN 실행 모델 비교", 14, INFO, KR, "middle", 600)
d.t(X3 + 14, Y0 + 52, "· BuildKit: runc 격리", 13, INK, KR, "start")
d.t(X3 + 14, Y0 + 74, "· Kaniko: 자체 스냅숏", 13, MUTED, KR, "start")
d.t(X3 + 14, Y0 + 96, "· 격리 책임 주체 차이", 13, MUTED, KR, "start")
d.t(X3 + 14, Y0 + 118, "· 실행 형태 3종 비교", 13, SOFT, KR, "start")
d.chip(X3 + W3 // 2, Y0 + 142, "격리 모델 선택", INFO, 11)

# 화살표 3 -> 4
X3_END = X3 + W3
X4 = 730
W4 = 206
d.arrow([(X3_END + 2, Y0 + BOX_H // 2), (X4 - 2, Y0 + BOX_H // 2)], MUTED, "ar", 1.3)

# 4. 한계와 아키텍처 (§4)
d.tone(X4, Y0, W4, BOX_H, WARN, 6, "10", 1.2)
d.t(X4 + W4 // 2, Y0 + 24, "4. 보안 제약과 분리", 14, WARN, KR, "middle", 600)
d.t(X4 + 14, Y0 + 52, "· PSS baseline 위반", 13, INK, KR, "start")
d.t(X4 + 14, Y0 + 74, "· restricted 프로필 제약", 13, MUTED, KR, "start")
d.t(X4 + 14, Y0 + 96, "· 전용 네임스페이스", 13, MUTED, KR, "start")
d.t(X4 + 14, Y0 + 118, "· 노드풀 격리 아키텍처", 13, SOFT, KR, "start")
d.chip(X4 + W4 // 2, Y0 + 142, "인프라 분리 설계", WARN, 11)

# 범례
LEG_Y = Y0 + BOX_H + 34
d.legend(LEG_Y, [
    ("문제 상황", BAD),
    ("핵심 원리 (focal)", ACC),
    ("실행 모델 비교", INFO),
    ("인프라 한계 및 대응", WARN),
])

d.save("01-02.chapter-overview.svg")
print("ok gen-01-02.chapter-overview")

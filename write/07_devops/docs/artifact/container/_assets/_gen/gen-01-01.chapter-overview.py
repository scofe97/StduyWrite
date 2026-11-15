# 타입 스펙: type-process
# 01-01 컨테이너 안 빌드가 문제가 되는 이유 — 전체 지도
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 960, 360

d = D(W, H, "DEVOPS · CONTAINER · 01-01",
      "컨테이너 안 이미지 빌드 문제와 접근 방식 전체 지도",
      "CLI 와 데몬 분리에서 시작해 DooD 와 DinD 의 권한 문제, 쿠버네티스 제약, 데몬 없는 빌드 비교와 과제",
      lead="데몬 부재 문제(§1) → DooD·DinD 권한 모델(§2) → 쿠버네티스 보안 제약(§2) → 비교와 한계(§3, §4)")

Y0 = 104
BOX_H = 160

# 1. 문제 (§1)
X1 = 24
W1 = 205
d.tone(X1, Y0, W1, BOX_H, BAD, 6, "10", 1.2)
d.t(X1 + W1 // 2, Y0 + 24, "1. 데몬 부재 문제", 14, BAD, KR, "middle", 600)
d.t(X1 + 14, Y0 + 52, "· CLI 와 dockerd 분리", 13, INK, KR, "start")
d.t(X1 + 14, Y0 + 74, "· VM: 로컬 데몬 존재", 13, MUTED, KR, "start")
d.t(X1 + 14, Y0 + 96, "· Pod: 컨테이너 안 실행", 13, MUTED, KR, "start")
d.t(X1 + 14, Y0 + 118, "· 빌드 전담 데몬 부재", 13, SOFT, KR, "start")
d.chip(X1 + W1 // 2, Y0 + 142, "데몬 위치 문제", BAD, 11)

# 화살표 1 -> 2
X1_END = X1 + W1
X2 = 253
d.arrow([(X1_END + 2, Y0 + BOX_H // 2), (X2 - 2, Y0 + BOX_H // 2)], MUTED, "ar", 1.3)

# 2. 우회 원리와 권한 (§2) — FOCAL
W2 = 224
d.tone(X2, Y0, W2, BOX_H, ACC, 6, "14", 1.4)
d.t(X2 + W2 // 2, Y0 + 24, "2. 우회 원리와 권한", 14, ACC, KR, "middle", 600)
d.t(X2 + 14, Y0 + 52, "· DooD: docker.sock 공유", 13, INK, KR, "start")
d.t(X2 + 14, Y0 + 74, "· 호스트 root 제어권 전달", 13, INK, KR, "start")
d.t(X2 + 14, Y0 + 96, "· DinD: 내부 데몬 구동", 13, MUTED, KR, "start")
d.t(X2 + 14, Y0 + 118, "· --privileged 특권 요구", 13, MUTED, KR, "start")
d.chip(X2 + W2 // 2, Y0 + 142, "보안 특권 위임", ACC, 11)

# 화살표 2 -> 3
X2_END = X2 + W2
X3 = 501
d.arrow([(X2_END + 2, Y0 + BOX_H // 2), (X3 - 2, Y0 + BOX_H // 2)], MUTED, "ar", 1.3)

# 3. 쿠버네티스 제약 (§2)
W3 = 205
d.tone(X3, Y0, W3, BOX_H, WARN, 6, "10", 1.2)
d.t(X3 + W3 // 2, Y0 + 24, "3. 쿠버네티스 제약", 14, WARN, KR, "middle", 600)
d.t(X3 + 14, Y0 + 52, "· dockershim 제거(v1.24)", 13, INK, KR, "start")
d.t(X3 + 14, Y0 + 74, "· 노드 containerd 런타임", 13, MUTED, KR, "start")
d.t(X3 + 14, Y0 + 96, "· 노드 Docker 소켓 부재", 13, MUTED, KR, "start")
d.t(X3 + 14, Y0 + 118, "· PSS Baseline 강제 시 차단", 13, SOFT, KR, "start")
d.chip(X3 + W3 // 2, Y0 + 142, "클러스터 정책 차단", WARN, 11)

# 화살표 3 -> 4
X3_END = X3 + W3
X4 = 730
W4 = 206
d.arrow([(X3_END + 2, Y0 + BOX_H // 2), (X4 - 2, Y0 + BOX_H // 2)], MUTED, "ar", 1.3)

# 4. 비교와 다음 과제 (§3, §4)
d.tone(X4, Y0, W4, BOX_H, INFO, 6, "10", 1.2)
d.t(X4 + W4 // 2, Y0 + 24, "4. 비교와 다음 과제", 14, INFO, KR, "middle", 600)
d.t(X4 + 14, Y0 + 52, "· 빌드 방식 3종 비교", 13, INK, KR, "start")
d.t(X4 + 14, Y0 + 74, "· 캐시·격리 트레이드오프", 13, MUTED, KR, "start")
d.t(X4 + 14, Y0 + 96, "· RUN 실행 격리 한계", 13, MUTED, KR, "start")
d.t(X4 + 14, Y0 + 118, "· 01-02 rootless 로 연결", 13, SOFT, KR, "start")
d.chip(X4 + W4 // 2, Y0 + 142, "다음 편으로 확장", INFO, 11)

# 범례
LEG_Y = Y0 + BOX_H + 34
d.legend(LEG_Y, [
    ("문제 제기", BAD),
    ("우회 원리와 권한 (focal)", ACC),
    ("쿠버네티스 보안 제약", WARN),
    ("비교와 다음 과제", INFO),
])

d.save("01-01.chapter-overview.svg")
print("ok gen-01-01.chapter-overview")

# 타입 스펙: type-data-flow
# 01-02 user namespace 와 UID 매핑 구조 (moby/buildkit rootless 이미지 기준 값)
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 960, 400

d = D(W, H, "DEVOPS · CONTAINER · 01-02",
      "user namespace 와 UID 매핑 데이터 흐름",
      "RUN 안 UID 0 은 빌더 사용자 자신의 UID 1000 으로, UID 1~65536 은 /etc/subuid 로 위임받은 100000~165535 로 바뀌는 구조",
      lead="RUN 안 UID → uid_map 한 줄 → 호스트에서 보이는 UID")

Y0 = 100
BOX_H = 184
ROW_A = Y0 + 40
ROW_B = Y0 + 112
ROW_H = 60

# 1. 좌측: RUN 컨테이너 안
C_X, C_W = 24, 260
d.box(C_X, Y0, C_W, BOX_H, PAPER2, RULE, 1.0, 8)
d.t(C_X + 16, Y0 + 24, "RUN 컨테이너 안", 13, INFO, KR, "start", 600)
d.tone(C_X + 16, ROW_A, C_W - 32, ROW_H, INFO, 6, "14", 1.2)
d.t(C_X + C_W // 2, ROW_A + 24, "UID 0 (root)", 13, INK, MONO, "middle", 600)
d.t(C_X + C_W // 2, ROW_A + 46, "apk · apt 가 쓰는 root", 11, MUTED, KR, "middle")
d.box(C_X + 16, ROW_B, C_W - 32, ROW_H, PAPER, RULE, 0.9, 6)
d.t(C_X + C_W // 2, ROW_B + 24, "UID 1 ~ 65536", 13, INK, MONO, "middle", 600)
d.t(C_X + C_W // 2, ROW_B + 46, "이미지 안 일반 계정", 11, MUTED, KR, "middle")

# 2. 중앙: uid_map — FOCAL
M_X, M_W = 344, 280
d.tone(M_X, Y0, M_W, BOX_H, ACC, 6, "16", 1.4)
d.t(M_X + 16, Y0 + 24, "/proc/[pid]/uid_map", 13, ACC, MONO, "start", 600)
d.box(M_X + 16, ROW_A, M_W - 32, ROW_H, PAPER, RULE, 0.9, 6)
d.t(M_X + 28, ROW_A + 24, "0   1000   1", 13, INK, MONO, "start", 600)
d.t(M_X + 28, ROW_A + 46, "자기 UID 한 개", 11, MUTED, KR, "start")
d.box(M_X + 16, ROW_B, M_W - 32, ROW_H, PAPER, RULE, 0.9, 6)
d.t(M_X + 28, ROW_B + 24, "1   100000   65536", 13, ACC, MONO, "start", 600)
d.t(M_X + 28, ROW_B + 46, "newuidmap · user:100000:65536", 11, MUTED, MONO, "start")

# 3. 우측: 호스트에서 보이는 UID
H_X, H_W = 684, 252
d.box(H_X, Y0, H_W, BOX_H, PAPER2, RULE, 1.0, 8)
d.t(H_X + 16, Y0 + 24, "호스트에서 보이는 UID", 13, OK, KR, "start", 600)
d.tone(H_X + 16, ROW_A, H_W - 32, ROW_H, OK, 6, "14", 1.2)
d.t(H_X + H_W // 2, ROW_A + 24, "UID 1000", 13, INK, MONO, "middle", 600)
d.t(H_X + H_W // 2, ROW_A + 46, "빌더 사용자 자신", 11, MUTED, KR, "middle")
d.box(H_X + 16, ROW_B, H_W - 32, ROW_H, PAPER, RULE, 0.9, 6)
d.t(H_X + H_W // 2, ROW_B + 24, "UID 100000 ~ 165535", 13, INK, MONO, "middle", 600)
d.t(H_X + H_W // 2, ROW_B + 46, "위임받은 하위 범위", 11, MUTED, KR, "middle")

# 화살표: 행마다 좌 → 중앙 → 우 (간격 60px)
for y in (ROW_A + ROW_H // 2, ROW_B + ROW_H // 2):
    d.arrow([(C_X + C_W - 14, y), (M_X + 14, y)], MUTED, "ar", 1.3)
    d.arrow([(M_X + M_W - 14, y), (H_X + 14, y)], OK, "ok", 1.4)

# 결론 한 줄
d.t(W // 2, Y0 + BOX_H + 30, "어느 행도 호스트 UID 0 이 아님 → RUN 의 root 로 호스트 root 파일을 고칠 수 없음", 13, WARN, KR, "middle", 600)

# 범례
LEG_Y = Y0 + BOX_H + 50
d.legend(LEG_Y, [
    ("RUN 안 UID", INFO),
    ("uid_map (focal)", ACC),
    ("호스트 UID", OK),
    ("결론", WARN),
])

d.save("01-02.uid-mapping.svg")
print("ok gen-01-02.uid-mapping")

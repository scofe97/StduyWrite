# 타입 스펙: type-process
# 02-01.jdk-layers — OpenJDK 소스부터 베이스 OS까지 다섯 층 흐름
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 960, 430

d = D(W, H, "CONTAINER · 02-01",
      "JDK 구성의 다섯 층",
      "5단계 흐름과 실제 이미지별 경로",
      lead="Jenkins(상단)와 Corretto AL2023(하단)의 층별 구성 비교")

X0 = 24
STEP_W = 164
STEP_GAP = 22
STEPS = [
    ("1. 소스", "OpenJDK 버전"),
    ("2. 배포판", "벤더 빌드"),
    ("3. 포장", "tar vs RPM"),
    ("4. Dockerfile", "설치 방식"),
    ("5. 베이스 OS", "C 라이브러리"),
]

# 헤더 스테이지 바
for i, (st, desc) in enumerate(STEPS):
    x = X0 + i * (STEP_W + STEP_GAP)
    d.box(x, 88, STEP_W, 44, PAPER2, RULE, 1.0, 6)
    d.t(x + STEP_W // 2, 106, st, 12, INK, KR, "middle", 600)
    d.t(x + STEP_W // 2, 122, desc, 10, MUTED, KR, "middle")
    if i < len(STEPS) - 1:
        ax = x + STEP_W + 2
        d.arrow([(ax, 110), (ax + STEP_GAP - 4, 110)], MUTED, "ar", 1.2)

# ── 상단 행: Jenkins (jenkins/jenkins:2.462.3-jdk17) ──────────────────
ROW1_Y = 150
ROW_H = 108
d.box(X0, ROW1_Y, 912, ROW_H, PAPER, RULE, 0.8, 6)
d.t(X0 + 12, ROW1_Y + 18, "Jenkins jdk17", 11, ACC, MONO, "start", 600)

J_VALS = [
    ("OpenJDK 17", "17.0.12+7"),
    ("Temurin", "Adoptium"),
    ("tar.gz", "공식 아카이브"),
    ("jlink + COPY", "멀티 스테이지"),
    ("Debian 12", "glibc 2.36"),
]

for i, (v1, v2) in enumerate(J_VALS):
    x = X0 + i * (STEP_W + STEP_GAP) + 6
    bx_w = STEP_W - 12
    d.tone(x, ROW1_Y + 28, bx_w, 66, ACC, 4, "12", 1.1)
    d.t(x + bx_w // 2, ROW1_Y + 54, v1, 12, INK, KR, "middle", 600)
    d.t(x + bx_w // 2, ROW1_Y + 74, v2, 10, MUTED, KR, "middle")
    if i < len(J_VALS) - 1:
        d.arrow([(x + bx_w + 2, ROW1_Y + 61), (x + bx_w + STEP_GAP + 8, ROW1_Y + 61)], ACC, "acc", 1.2)

# ── 하단 행: Amazon Corretto (amazoncorretto:17-al2023) ───────────────
ROW2_Y = 272
d.box(X0, ROW2_Y, 912, ROW_H, PAPER, RULE, 0.8, 6)
d.t(X0 + 12, ROW2_Y + 18, "Corretto al2023", 11, OK, MONO, "start", 600)

C_VALS = [
    ("OpenJDK 17", "17.0.21.1.2"),
    ("Corretto", "Amazon"),
    ("RPM", "dnf 패키지"),
    ("dnf install", "RPM 설치"),
    ("AL2023", "glibc 2.34"),
]

for i, (v1, v2) in enumerate(C_VALS):
    x = X0 + i * (STEP_W + STEP_GAP) + 6
    bx_w = STEP_W - 12
    d.tone(x, ROW2_Y + 28, bx_w, 66, OK, 4, "12", 1.1)
    d.t(x + bx_w // 2, ROW2_Y + 54, v1, 12, INK, KR, "middle", 600)
    d.t(x + bx_w // 2, ROW2_Y + 74, v2, 10, MUTED, KR, "middle")
    if i < len(C_VALS) - 1:
        d.arrow([(x + bx_w + 2, ROW2_Y + 61), (x + bx_w + STEP_GAP + 8, ROW2_Y + 61)], OK, "ok", 1.2)

# 범례
LEG_Y = 396
d.legend(LEG_Y, [
    ("tar 기반 멀티 스테이지", ACC),
    ("RPM 기반 패키지 매니저", OK),
])

out_path = sys.argv[1] if len(sys.argv) > 1 else str(pathlib.Path(__file__).resolve().parent.parent / "02-01.jdk-layers.svg")
d.save(out_path)
print("ok gen-02-01.jdk-layers")

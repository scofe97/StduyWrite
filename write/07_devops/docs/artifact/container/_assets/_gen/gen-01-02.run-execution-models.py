# 타입 스펙: type-flowchart
# 01-02 RUN 실행 모델 비교 — BuildKit 과 Kaniko
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 960, 390

d = D(W, H, "DEVOPS · CONTAINER · 01-02",
      "RUN 실행 모델 비교 — BuildKit 과 Kaniko 의 두 경로",
      "동일한 RUN 명령이 BuildKit 에서는 runc 컨테이너 격리로, Kaniko 에서는 빌더 파일시스템 변경과 스냅숏으로 처리되는 흐름",
      lead="입력 지시어 → BuildKit OCI 런타임 격리 경로 vs Kaniko 유저스페이스 스냅숏 경로")

# 공통 입력 (좌측)
IN_X = 24
IN_Y = 160
IN_W = 180
IN_H = 76
d.tone(IN_X, IN_Y, IN_W, IN_H, INFO, 6, "12", 1.2)
d.t(IN_X + IN_W // 2, IN_Y + 22, "Dockerfile RUN 지시어", 13, INFO, KR, "middle", 600)
d.t(IN_X + IN_W // 2, IN_Y + 44, "RUN apt-get install ...", 12, INK, MONO, "middle")
d.t(IN_X + IN_W // 2, IN_Y + 64, "패키지 설치 및 환경 변경", 13, MUTED, KR, "middle")

# 분기 좌표
PATH_X = 250
PATH_W = 310
OUT_X = 630
OUT_W = 306
PATH_H = 100

# ── 상단 분기: BuildKit (runc OCI 워커) ─────────────────────────
UP_Y = 94

# 화살표: 입력 -> BuildKit 경로
d.arrow([(IN_X + IN_W + 2, IN_Y + 24), (227, IN_Y + 24), (227, UP_Y + PATH_H // 2), (PATH_X - 2, UP_Y + PATH_H // 2)], ACC, "acc", 1.4)

d.tone(PATH_X, UP_Y, PATH_W, PATH_H, ACC, 6, "14", 1.3)
d.t(PATH_X + 16, UP_Y + 24, "BuildKit: OCI 컨테이너 격리", 13, ACC, KR, "start", 600)
d.t(PATH_X + 16, UP_Y + 46, "· runc 임시 컨테이너 생성", 13, INK, KR, "start")
d.t(PATH_X + 16, UP_Y + 68, "· user namespace & OverlayFS", 13, MUTED, KR, "start")
d.t(PATH_X + 16, UP_Y + 88, "· 독립 네임스페이스 내 명령 격리", 13, MUTED, KR, "start")

# 화살표: BuildKit 실행 -> 산출 (간격: 560..630 = 70px)
d.arrow([(PATH_X + PATH_W + 2, UP_Y + PATH_H // 2), (OUT_X - 2, UP_Y + PATH_H // 2)], ACC, "acc", 1.3)
d.t(595, UP_Y + PATH_H // 2 - 8, "diff 추출", 12, ACC, KR, "middle")

d.box(OUT_X, UP_Y, OUT_W, PATH_H, PAPER2, RULE, 1.0, 6)
d.t(OUT_X + 16, UP_Y + 24, "결과: OverlayFS 레이어 커밋", 13, ACC, KR, "start", 600)
d.t(OUT_X + 16, UP_Y + 46, "· upperdir 변경분을 레이어로 저장", 13, INK, KR, "start")
d.t(OUT_X + 16, UP_Y + 68, "· 격리 근거: 커널 네임스페이스", 13, MUTED, KR, "start")
d.t(OUT_X + 16, UP_Y + 88, "· 전제: seccomp Unconfined 요구", 13, WARN, KR, "start")


# ── 하단 분기: Kaniko (유저스페이스 스냅숏) ─────────────────────
DN_Y = 224

# 화살표: 입력 -> Kaniko 경로
d.arrow([(IN_X + IN_W + 2, IN_Y + 52), (227, IN_Y + 52), (227, DN_Y + PATH_H // 2), (PATH_X - 2, DN_Y + PATH_H // 2)], MUTED, "ar", 1.4)

d.box(PATH_X, DN_Y, PATH_W, PATH_H, PAPER2, RULE, 1.0, 6)
d.t(PATH_X + 16, DN_Y + 24, "Kaniko: 자체 프로세스 스냅숏", 13, MUTED, KR, "start", 600)
d.t(PATH_X + 16, DN_Y + 46, "· 빌더 컨테이너 안에서 명령 직접 실행", 13, INK, KR, "start")
d.t(PATH_X + 16, DN_Y + 68, "· 빌더 파일시스템 직접 수정", 13, MUTED, KR, "start")
d.t(PATH_X + 16, DN_Y + 88, "· 별도 컨테이너 생성 없음", 13, MUTED, KR, "start")

# 화살표: Kaniko 실행 -> 산출 (간격: 560..630 = 70px)
d.arrow([(PATH_X + PATH_W + 2, DN_Y + PATH_H // 2), (OUT_X - 2, DN_Y + PATH_H // 2)], MUTED, "ar", 1.3)
d.t(595, DN_Y + PATH_H // 2 - 8, "스냅숏", 12, MUTED, KR, "middle")

d.box(OUT_X, DN_Y, OUT_W, PATH_H, PAPER2, RULE, 1.0, 6)
d.t(OUT_X + 16, DN_Y + 24, "결과: 유저스페이스 diff 아카이브", 13, MUTED, KR, "start", 600)
d.t(OUT_X + 16, DN_Y + 46, "· 파일시스템 변경 감지 후 tar 생성", 13, INK, KR, "start")
d.t(OUT_X + 16, DN_Y + 68, "· 격리 근거: 외부 Pod 런타임 의존", 13, WARN, KR, "start")
d.t(OUT_X + 16, DN_Y + 88, "· 장점: unshare·mount 미요구", 13, MUTED, KR, "start")

# 범례 (4개 항목으로 캔버스 폭 내 배치)
LEG_Y = DN_Y + PATH_H + 24
d.legend(LEG_Y, [
    ("입력 지시어", INFO),
    ("BuildKit 격리 (focal)", ACC),
    ("Kaniko 직접 실행", MUTED),
    ("보안 유의점", WARN),
])

d.save("01-02.run-execution-models.svg")
print("ok gen-01-02.run-execution-models")

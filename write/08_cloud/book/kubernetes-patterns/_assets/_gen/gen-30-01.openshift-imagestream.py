# 타입 스펙: type-architecture
# 30-01 OpenShift ImageStream — BuildConfig와 ImageStream 트리거 자동 연계
# 본문: 자동 연계의 핵심은 ImageStream과 trigger다. BuildConfig 가 빌드한
#   이미지가 ImageStreamTag 에 매핑되면 imageChange trigger 가 이벤트를 감지해
#   후속 이미지를 재빌드하거나 대상 Deployment/Pod 를 자동으로 재배포한다.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 960, 380

d = D(W, H, "KUBERNETES PATTERNS · 30-01",
      "OpenShift ImageStream과 트리거 자동 연계",
      "BuildConfig 빌드 완료 시 ImageStreamTag 변경 이벤트를 감지해 자동 재빌드와 재배포를 조율하는 아키텍처",
      lead="BuildConfig · ImageStream · imageChange trigger 자동 연계 파이프라인")

# ── 1행: 빌드 및 이미지 등록 (좌 → 우) ──────────────────────────────────────
ROW1_Y = 106
BOX_H = 80

# 1. BuildConfig (열 1: x=40..240)
BC_X = 40
BC_W = 200
d.tone(BC_X, ROW1_Y, BC_W, BOX_H, INFO, 6, "10", 1.1)
d.t(BC_X + BC_W // 2, ROW1_Y + 24, "BuildConfig", 14, INFO, KR, "middle", 600)
d.t(BC_X + BC_W // 2, ROW1_Y + 44, "S2I · Docker 빌드 명세", 13, INK, KR, "middle")
d.t(BC_X + BC_W // 2, ROW1_Y + 64, "빌드 파이프라인 설정", 13, MUTED, KR, "middle")

# 화살표 (1): BuildConfig -> Build 실행 (간격: x=240..350, 폭 110px)
BLD_X = 350
BLD_W = 260
d.arrow([(BC_X + BC_W + 2, ROW1_Y + BOX_H // 2), (BLD_X - 2, ROW1_Y + BOX_H // 2)], MUTED, "ar", 1.3)
d.t((BC_X + BC_W + BLD_X) // 2, ROW1_Y + BOX_H // 2 - 8, "(1) 빌드 기동", 13, INK, KR, "middle")

# 2. Build 실행 (열 2: x=350..610)
d.tone(BLD_X, ROW1_Y, BLD_W, BOX_H, OK, 6, "10", 1.1)
d.t(BLD_X + BLD_W // 2, ROW1_Y + 24, "Build 실행 (S2I / Docker)", 14, OK, KR, "middle", 600)
d.t(BLD_X + BLD_W // 2, ROW1_Y + 44, "S2I: assemble 로 컴파일", 13, INK, KR, "middle")
d.t(BLD_X + BLD_W // 2, ROW1_Y + 64, "클러스터 통합 실행", 13, MUTED, KR, "middle")

# 화살표 (2): Build 실행 -> ImageStream (간격: x=610..710, 폭 100px)
IS_X = 710
IS_W = 210
d.arrow([(BLD_X + BLD_W + 2, ROW1_Y + BOX_H // 2), (IS_X - 2, ROW1_Y + BOX_H // 2)], OK, "ok", 1.4)
d.t((BLD_X + BLD_W + IS_X) // 2, ROW1_Y + BOX_H // 2 - 8, "(2) 이미지 등록", 13, OK, KR, "middle")

# 3. ImageStream (열 3: x=710..920) — FOCAL
d.tone(IS_X, ROW1_Y, IS_W, BOX_H, ACC, 6, "16", 1.4)
d.t(IS_X + IS_W // 2, ROW1_Y + 24, "ImageStream", 14, ACC, KR, "middle", 600)
d.t(IS_X + IS_W // 2, ROW1_Y + 44, "ImageStreamTag 갱신", 13, INK, KR, "middle", 500)
d.t(IS_X + IS_W // 2, ROW1_Y + 64, "변경 이벤트 자동 발행", 13, ACC, KR, "middle")


# ── 2행: 이벤트 감지 및 후속 분기 ───────────────────────────────────────────
ROW2_Y = 230

# 화살표 (3): ImageStream -> imageChange trigger (직교 연결선)
TRIG_X = BLD_X
TRIG_W = BLD_W
MID_Y = 208
d.arrow([(IS_X + 40, ROW1_Y + BOX_H + 2),
         (IS_X + 40, MID_Y),
         (TRIG_X + TRIG_W // 2, MID_Y),
         (TRIG_X + TRIG_W // 2, ROW2_Y - 2)], ACC, "acc", 1.4)
d.t(610, MID_Y - 8, "(3) 태그 변경 감지", 13, ACC, KR, "middle")

# 4. imageChange trigger (열 2: x=350..610) — FOCAL
d.tone(TRIG_X, ROW2_Y, TRIG_W, BOX_H, ACC, 6, "14", 1.4)
d.t(TRIG_X + TRIG_W // 2, ROW2_Y + 24, "imageChange 트리거", 14, ACC, KR, "middle", 600)
d.t(TRIG_X + TRIG_W // 2, ROW2_Y + 44, "태그 변경 감지 컨트롤러", 13, INK, KR, "middle")
d.t(TRIG_X + TRIG_W // 2, ROW2_Y + 64, "후속 파이프라인 자동 조율", 13, ACC, KR, "middle")

# 화살표 (4a): trigger -> chained build (좌측 분기, 간격 x=240..350)
CH_X = BC_X
CH_W = BC_W
d.arrow([(TRIG_X - 2, ROW2_Y + BOX_H // 2), (CH_X + CH_W + 2, ROW2_Y + BOX_H // 2)], WARN, "warn", 1.3)
d.t((CH_X + CH_W + TRIG_X) // 2, ROW2_Y + BOX_H // 2 - 8, "(4a) 연쇄 빌드", 13, WARN, KR, "middle")

# 5. chained build (열 1: x=40..240)
d.tone(CH_X, ROW2_Y, CH_W, BOX_H, WARN, 6, "10", 1.1)
d.t(CH_X + CH_W // 2, ROW2_Y + 24, "chained build (2차)", 14, WARN, KR, "middle", 600)
d.t(CH_X + CH_W // 2, ROW2_Y + 44, "S2I 산출물 → Docker 전달", 13, INK, KR, "middle")
d.t(CH_X + CH_W // 2, ROW2_Y + 64, "슬림 런타임 이미지 완성", 13, MUTED, KR, "middle")

# 수직 화살표: chained build -> BuildConfig
d.arrow([(CH_X + 50, ROW2_Y - 2), (CH_X + 50, ROW1_Y + BOX_H + 2)], MUTED, "ar", 1.3)
d.t(CH_X + 60, (ROW1_Y + BOX_H + ROW2_Y) // 2 + 4, "BuildConfig 로 정의", 13, MUTED, KR, "start")

# 화살표 (4b): trigger -> Deployment (우측 분기, 간격 x=610..710)
DEP_X = IS_X
DEP_W = IS_W
d.arrow([(TRIG_X + TRIG_W + 2, ROW2_Y + BOX_H // 2), (DEP_X - 2, ROW2_Y + BOX_H // 2)], INFO, "info", 1.3)
d.t((TRIG_X + TRIG_W + DEP_X) // 2, ROW2_Y + BOX_H // 2 - 8, "(4b) 자동 배포", 13, INFO, KR, "middle")

# 6. 대상 Deployment (열 3: x=710..920)
d.tone(DEP_X, ROW2_Y, DEP_W, BOX_H, INFO, 6, "10", 1.1)
d.t(DEP_X + DEP_W // 2, ROW2_Y + 24, "대상 Deployment / Pod", 14, INFO, KR, "middle", 600)
d.t(DEP_X + DEP_W // 2, ROW2_Y + 44, "새 이미지 자동 롤아웃", 13, INK, KR, "middle")
d.t(DEP_X + DEP_W // 2, ROW2_Y + 64, "대상 Pod 재배포", 13, MUTED, KR, "middle")

# 수직 화살표: ImageStream -> Deployment (새 이미지 참조)
d.arrow([(IS_X + IS_W - 40, ROW1_Y + BOX_H + 2), (IS_X + IS_W - 40, ROW2_Y - 2)], MUTED, "ar", 1.3)
d.t(IS_X + IS_W - 50, (ROW1_Y + BOX_H + ROW2_Y) // 2 + 4, "새 이미지 참조", 13, MUTED, KR, "end")


# ── 범례 ─────────────────────────────────────────────────────────────────
LEG_Y = ROW2_Y + BOX_H + 20
d.legend(LEG_Y, [
    ("빌드 설정 · 실행", OK),
    ("트리거 연계 (focal)", ACC),
    ("배포 롤아웃", INFO),
    ("연쇄 빌드", WARN),
])

d.save("30-01.openshift-imagestream.svg")
print("ok gen-30-01.openshift-imagestream")

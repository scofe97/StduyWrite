# 타입 스펙: type-process
# 6절 ConfigMap 변경 감지와 파드 롤링 — checksum 주석 유무에 따른 롤링 비교
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, PAPER, PAPER2, KR, MONO

W, H = 960, 452

d = D(W, H, "HELM · CONFIGMAP ROLLOUT",
      "ConfigMap 변경에 따른 파드 롤링 비교",
      "checksum 주석 유무에 따른 ConfigMap 변경 감지와 파드 롤링 업데이트 동작 비교",
      lead="주석 없음: template 불변으로 파드 유지(상단) vs 주석 있음: 해시 변경으로 롤링(하단)")

# ── 4단계 컬럼 정의 ──────────────────────────────────────────────────────
COL_W = 216
COL_GAP = 16
X0 = 24

STEPS = [
    ("1. ConfigMap 설정", "appConfig.message 변경", INFO),
    ("2. Pod template 주석", "metadata.annotations", ACC),
    ("3. 파드 해시 및 상태", "Deployment 컨트롤러", INFO),
    ("4. 컨테이너 환경 변수", "printenv message", OK),
]

HEADER_Y = 96
HEADER_H = 46

for i, (title, sub, col) in enumerate(STEPS):
    x = X0 + i * (COL_W + COL_GAP)
    d.box(x, HEADER_Y, COL_W, HEADER_H, PAPER2, RULE, 1.0)
    d.t(x + COL_W // 2, HEADER_Y + 18, title, 13, col, KR, "middle", 600)
    d.t(x + COL_W // 2, HEADER_Y + 34, sub, 11, MUTED, MONO if "message" in sub or "metadata" in sub else KR, "middle")

    if i < len(STEPS) - 1:
        ax1 = x + COL_W + 2
        ax2 = x + COL_W + COL_GAP - 2
        ay = HEADER_Y + HEADER_H // 2
        d.arrow([(ax1, ay), (ax2, ay)], MUTED, "ar", 1.2)


# ── 트랙 배경 렌더러 ────────────────────────────────────────────────────
def render_track_bg(y, h, title, sub):
    d.o.append(f'<rect x="{X0}" y="{y}" width="912" height="{h}" rx="6" fill="{PAPER2}" stroke="{RULE}" stroke-width="0.8"/>')
    d.t(X0 + 14, y + 17, title, 12, INK, KR, "start", 600)
    d.t(X0 + 14, y + 32, sub, 11, MUTED, KR, "start")


# ── 트랙 1: 주석 없음 (configChecksum=false) ───────────────────────────
T1_Y = 154
T1_H = 104
render_track_bg(T1_Y, T1_H, "주석 없음 (configChecksum=false)", "ConfigMap 변경 · Pod template 불변")

CARD_Y1 = T1_Y + 38
CARD_W = 200
CARD_H = 58

# Col 0: ConfigMap
cx0 = X0 + 8
d.box(cx0, CARD_Y1, CARD_W, CARD_H, PAPER, RULE, 1.0)
d.t(cx0 + 10, CARD_Y1 + 17, "hl-cht-demo-app-config", 11, INK, MONO, "start")
d.t(cx0 + 10, CARD_Y1 + 33, "message: updated-v2", 11, INFO, MONO, "start")
d.t(cx0 + 10, CARD_Y1 + 49, "설정 값 갱신", 12, MUTED, KR, "start")

# Col 1: Pod Template Annotations
cx1 = cx0 + COL_W + COL_GAP
d.box(cx1, CARD_Y1, CARD_W, CARD_H, PAPER, RULE, 1.0)
d.t(cx1 + 10, CARD_Y1 + 17, "주석 없음", 12, INK, KR, "start")
d.t(cx1 + 10, CARD_Y1 + 33, "checksum/config 부재", 11, MUTED, MONO, "start")
d.t(cx1 + 10, CARD_Y1 + 49, "template 불변", 12, MUTED, KR, "start")

# Col 2: Pod Hash / Status
cx2 = cx1 + COL_W + COL_GAP
d.box(cx2, CARD_Y1, CARD_W, CARD_H, PAPER, WARN, 1.1)
d.t(cx2 + 10, CARD_Y1 + 17, "해시: 6696464976", 11, WARN, MONO, "start")
d.t(cx2 + 10, CARD_Y1 + 33, "...-6696464976-8z8t4", 11, INK, MONO, "start")
d.t(cx2 + 10, CARD_Y1 + 49, "Running 2s (유지)", 12, WARN, KR, "start")

# Col 3: Container Env
cx3 = cx2 + COL_W + COL_GAP
d.box(cx3, CARD_Y1, CARD_W, CARD_H, PAPER, WARN, 1.1)
d.t(cx3 + 10, CARD_Y1 + 17, "printenv message", 11, MUTED, MONO, "start")
d.t(cx3 + 10, CARD_Y1 + 33, "initial-v1", 12, WARN, MONO, "start", 600)
d.t(cx3 + 10, CARD_Y1 + 49, "옛 설정 잔존 (미반영)", 12, WARN, KR, "start")

# Track 1 화살표
ay1 = CARD_Y1 + CARD_H // 2
d.arrow([(cx0 + CARD_W + 2, ay1), (cx1 - 2, ay1)], MUTED, "ar", 1.2)
d.arrow([(cx1 + CARD_W + 2, ay1), (cx2 - 2, ay1)], MUTED, "ar", 1.2)
d.arrow([(cx2 + CARD_W + 2, ay1), (cx3 - 2, ay1)], WARN, "warn", 1.2)


# ── 트랙 2: 주석 있음 (configChecksum=true) ───────────────────────────
T2_Y = 270
T2_H = 104
render_track_bg(T2_Y, T2_H, "주석 있음 (configChecksum=true)", "sha256 주석 갱신 · Pod template 변경")

CARD_Y2 = T2_Y + 38

# Col 0: ConfigMap
d.box(cx0, CARD_Y2, CARD_W, CARD_H, PAPER, RULE, 1.0)
d.t(cx0 + 10, CARD_Y2 + 17, "hl-cht-demo-app-config", 11, INK, MONO, "start")
d.t(cx0 + 10, CARD_Y2 + 33, "message: updated-v2", 11, INFO, MONO, "start")
d.t(cx0 + 10, CARD_Y2 + 49, "설정 값 갱신", 12, MUTED, KR, "start")

# Col 1: Pod Template Annotations (Focal)
d.tone(cx1, CARD_Y2, CARD_W, CARD_H, ACC, 6, "14", 1.4)
d.t(cx1 + 10, CARD_Y2 + 17, "checksum/config", 11, ACC, MONO, "start", 600)
d.t(cx1 + 10, CARD_Y2 + 33, "sha256sum 주석 주입", 11, ACC, KR, "start")
d.t(cx1 + 10, CARD_Y2 + 49, "template 변경 감지", 12, INK, KR, "start")

# Col 2: Pod Hash / Status
d.tone(cx2, CARD_Y2, CARD_W, CARD_H, OK, 6, "12", 1.2)
d.t(cx2 + 10, CARD_Y2 + 17, "6696464976 Terminating", 11, MUTED, MONO, "start")
d.t(cx2 + 10, CARD_Y2 + 33, "86b7899dbf Running 1s", 11, OK, MONO, "start", 600)
d.t(cx2 + 10, CARD_Y2 + 49, "새 파드 롤링 진행", 12, OK, KR, "start")

# Col 3: Container Env
d.tone(cx3, CARD_Y2, CARD_W, CARD_H, OK, 6, "12", 1.2)
d.t(cx3 + 10, CARD_Y2 + 17, "printenv message", 11, MUTED, MONO, "start")
d.t(cx3 + 10, CARD_Y2 + 33, "updated-v2", 12, OK, MONO, "start", 600)
d.t(cx3 + 10, CARD_Y2 + 49, "새 설정 반영 완료", 12, OK, KR, "start")

# Track 2 화살표
ay2 = CARD_Y2 + CARD_H // 2
d.arrow([(cx0 + CARD_W + 2, ay2), (cx1 - 2, ay2)], ACC, "acc", 1.4)
d.arrow([(cx1 + CARD_W + 2, ay2), (cx2 - 2, ay2)], ACC, "acc", 1.4)
d.arrow([(cx2 + CARD_W + 2, ay2), (cx3 - 2, ay2)], OK, "ok", 1.4)


# ── 범례 ────────────────────────────────────────────────────────────────
LEG_Y = 398
d.legend(LEG_Y, [
    ("주석 갱신", ACC),
    ("파드 롤링 · 새 설정", OK),
    ("옛 설정 잔존 (누락)", WARN),
    ("ConfigMap 리소스", INFO),
])

out_path = sys.argv[1] if len(sys.argv) > 1 else str(pathlib.Path(__file__).resolve().parent.parent / "Helm 차트 작성.checksum-rollout.svg")
d.save(out_path)
print("ok gen-Helm 차트 작성.checksum-rollout")

# 타입 스펙: type-process
# 5절 Chart.yaml 의존성과 Chart.lock 생애주기
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, PAPER, PAPER2, KR, MONO

W, H = 960, 468

d = D(W, H, "HELM · DEPENDENCY & LOCK",
      "Chart.yaml 의존성 선언과 Chart.lock 생애주기",
      "의존성 선언(Chart.yaml)부터 update(lock 생성), 저장소 배포, build(lock 기반 charts/ 복원) 흐름",
      lead="동일 객체(Chart.yaml · Chart.lock · charts/)의 4단계 상태 변화 추적")

# ── 4단계 컬럼 정의 ──────────────────────────────────────────────────────
COL_W = 216
COL_GAP = 16
X0 = 24

STEPS = [
    ("1. 의존성 선언", "parent-app / Chart.yaml", INFO),
    ("2. 의존성 갱신", "helm dependency update", ACC),
    ("3. 새로 받은 저장소", "git clone (charts/ 제외)", WARN),
    ("4. 재현 빌드", "helm dependency build", OK),
]

HEADER_Y = 96
HEADER_H = 46

for i, (title, sub, col) in enumerate(STEPS):
    x = X0 + i * (COL_W + COL_GAP)
    d.box(x, HEADER_Y, COL_W, HEADER_H, PAPER2, RULE, 1.0)
    d.t(x + COL_W // 2, HEADER_Y + 18, title, 13, col, KR, "middle", 600)
    d.t(x + COL_W // 2, HEADER_Y + 34, sub, 11, MUTED, MONO if "/" in sub or "helm" in sub else KR, "middle")

    if i < len(STEPS) - 1:
        ax1 = x + COL_W + 2
        ax2 = x + COL_W + COL_GAP - 2
        ay = HEADER_Y + HEADER_H // 2
        d.arrow([(ax1, ay), (ax2, ay)], MUTED, "ar", 1.2)


# ── 트랙 공통 라벨 렌더러 ────────────────────────────────────────────────
def render_track_bg(y, h, title, sub):
    d.o.append(f'<rect x="{X0}" y="{y}" width="912" height="{h}" rx="6" fill="{PAPER2}" stroke="{RULE}" stroke-width="0.8"/>')
    d.t(X0 + 14, y + 17, title, 12, INK, KR, "start", 600)
    d.t(X0 + 14, y + 32, sub, 11, MUTED, KR, "start")


# ── 트랙 1: Chart.yaml (선언 파일) ──────────────────────────────────────
T1_Y = 152
T1_H = 78
render_track_bg(T1_Y, T1_H, "Chart.yaml (의존성 선언)", "dependencies 블록 유지 및 버전 일치 검증")

C1_Y = T1_Y + 38
CARD_W = 200
CARD_H = 32

T1_DATA = [
    ("sub-backend: 0.1.0", INFO),
    ("sub-backend 0.1.0 (선언 유지)", MUTED),
    ("sub-backend 0.1.0 (커밋 보존)", MUTED),
    ("sub-backend 0.1.0 (일치 검증)", OK),
]

for i, (main_txt, col) in enumerate(T1_DATA):
    cx = X0 + 8 + i * (COL_W + COL_GAP)
    d.box(cx, C1_Y, CARD_W, CARD_H, PAPER, col if col in (OK, INFO) else RULE, 0.9)
    fam = KR if any("가" <= c <= "힣" for c in main_txt) else MONO
    d.t(cx + CARD_W // 2, C1_Y + 20, main_txt, 11, col if col in (OK, INFO) else INK, fam, "middle", 600 if col in (OK, INFO) else 400)


# ── 트랙 2: Chart.lock (잠금 파일 - Focal) ──────────────────────────────
T2_Y = 238
T2_H = 78
render_track_bg(T2_Y, T2_H, "Chart.lock (잠금 파일)", "다이제스트 기록으로 빌드 재현성 보장")

C2_Y = T2_Y + 38
CARD2_H = 32

# Step 0: 미생성 상태
cx0 = X0 + 8
d.o.append(f'<rect x="{cx0}" y="{C2_Y}" width="{CARD_W}" height="{CARD2_H}" rx="6" fill="{PAPER}" stroke="{RULE}" stroke-width="0.8" stroke-dasharray="4 3"/>')
d.t(cx0 + CARD_W // 2, C2_Y + 20, "(미생성 상태 · lock 없음)", 11, SOFT, KR, "middle")

# Step 1: lock 생성 (Focal)
cx1 = X0 + 8 + (COL_W + COL_GAP)
d.tone(cx1, C2_Y, CARD_W, CARD2_H, ACC, 6, "16", 1.4)
d.t(cx1 + CARD_W // 2, C2_Y + 20, "Chart.lock 생성", 11, ACC, KR, "middle", 600)

# Step 2: git 커밋 보존
cx2 = X0 + 8 + 2 * (COL_W + COL_GAP)
d.box(cx2, C2_Y, CARD_W, CARD2_H, PAPER, INFO, 1.0)
d.t(cx2 + CARD_W // 2, C2_Y + 20, "Chart.lock 보존 (git 관리)", 11, INFO, KR, "middle", 600)

# Step 3: build 검증 및 복원 기준
cx3 = X0 + 8 + 3 * (COL_W + COL_GAP)
d.box(cx3, C2_Y, CARD_W, CARD2_H, PAPER, OK, 1.0)
d.t(cx3 + CARD_W // 2, C2_Y + 20, "복원 기준 파일 (검증 통과)", 11, OK, KR, "middle", 600)


# ── 트랙 3: charts/ (하위 아카이브 디렉터리) ────────────────────────────
T3_Y = 324
T3_H = 78
render_track_bg(T3_Y, T3_H, "charts/ (하위 차트 디렉터리)", "실제 렌더링에 사용되는 tgz 압축 아카이브")

C3_Y = T3_Y + 38

# Step 0: missing
d.box(cx0, C3_Y, CARD_W, CARD_H, PAPER, WARN, 0.9)
d.t(cx0 + CARD_W // 2, C3_Y + 20, "비어 있음 (missing)", 11, WARN, KR, "middle", 600)

# Step 1: 아카이브 저장
d.box(cx1, C3_Y, CARD_W, CARD_H, PAPER, OK, 0.9)
d.t(cx1 + CARD_W // 2, C3_Y + 20, "sub-backend-0.1.0.tgz", 11, OK, MONO, "middle", 600)

# Step 2: clean (git 미추적)
d.box(cx2, C3_Y, CARD_W, CARD_H, PAPER, WARN, 0.9)
d.t(cx2 + CARD_W // 2, C3_Y + 20, "비어 있음 (git 미추적)", 11, WARN, KR, "middle", 600)

# Step 3: 복원 완료
d.box(cx3, C3_Y, CARD_W, CARD_H, PAPER, OK, 0.9)
d.t(cx3 + CARD_W // 2, C3_Y + 20, "sub-backend-0.1.0.tgz", 11, OK, MONO, "middle", 600)


# ── 범례 ──────────────────────────────────────────────────────────────
d.legend(420, [
    ("선언 및 기준 파일", INFO),
    ("신규 생성 (Chart.lock)", ACC),
    ("정상 복원 / 통과", OK),
    ("부재 / 복원 필요", WARN)
])

d.save("Helm 차트 의존성과 저장소.dependency-lock.svg")
print("ok Helm 차트 의존성과 저장소.dependency-lock.svg")

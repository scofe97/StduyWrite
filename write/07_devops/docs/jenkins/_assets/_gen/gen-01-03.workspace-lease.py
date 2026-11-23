# 타입 스펙: type-swimlane
# 3절 동시 빌드와 WorkspaceList 분기 — 같은 잡 빌드 셋이 시간 순으로 기본 경로와 @2 를 임대·반납·재사용하는 흐름
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import (D, PAPER2, INK, MUTED, SOFT, RULE, ACC,  # noqa: E402
                OK, WARN, INFO, KR, MONO)

W, H = 960, 500

d = D(
    W, H,
    "JENKINS · WORKSPACELIST ALLOCATE & RELEASE",
    "동시 빌드의 WorkspaceList 임대와 반납",
    "같은 잡 빌드 셋이 시간 순으로 도착할 때 Controller JVM 의 WorkspaceList.inUse 맵과 Agent 기계 디스크의 작업 경로 변화",
    lead="같은 잡 빌드 셋이 시간 순으로 들어올 때 Controller JVM 의 inUse 와 Agent 디스크 경로 변화"
)

COLS = [
    ("t1 · 빌드 #1 도착", 176),
    ("t2 · 빌드 #2 겹침", 368),
    ("t3 · 빌드 #1 반납", 560),
    ("t4 · 빌드 #3 도착", 752),
]
BOX_W = 164
BOX_H = 60

LANES = [
    ("Executor 슬롯", "요청 · 반납", 148),
    ("Controller JVM", "Computer · inUse", 248),
    ("Agent 디스크", "작업 디렉터리", 348),
]


def cell_box(x, y, title, sub, c, focal=False):
    if focal:
        d.tone(x, y, BOX_W, BOX_H, c, r=6, op="12", sw=1.4)
        tc = c
    else:
        d.box(x, y, BOX_W, BOX_H, PAPER2, c, 1.1, 6)
        tc = INK
    tfam = KR if any("가" <= ch <= "힣" for ch in title) else MONO
    sfam = KR if any("가" <= ch <= "힣" for ch in sub) else MONO
    tsz = 13 if (tfam == KR and len(title) > 9) or (tfam == MONO and len(title) > 15) else 14
    ssz = 12 if sfam == MONO and len(sub) > 16 else 13
    d.t(x + BOX_W / 2, y + 24, title, tsz, tc, tfam, "middle", 600)
    d.t(x + BOX_W / 2, y + 46, sub, ssz, MUTED, sfam, "middle")


# ── 레인 배경·구분선 ──────────────────────────────────────────────────
for idx, (name, sub, ly) in enumerate(LANES):
    d.box(24, ly, 136, 76, PAPER2, RULE, 0.9, 6)
    nfam = KR if any("가" <= ch <= "힣" for ch in name) else MONO
    sfam = KR if any("가" <= ch <= "힣" for ch in sub) else MONO
    d.t(92, ly + 32, name, 14, INK, nfam, "middle", 600)
    d.t(92, ly + 52, sub, 12 if sfam == MONO and len(sub) > 14 else 13, MUTED, sfam, "middle")
    if idx > 0:
        d.line(24, ly - 12, 920, ly - 12, RULE, 0.8)

# ── 시간 열 헤더 ───────────────────────────────────────────────────────
for label, x in COLS:
    d.box(x, 104, BOX_W, 32, PAPER2, RULE, 0.9, 4)
    d.t(x + BOX_W / 2, 125, label, 13, SOFT, KR, "middle", 600)

# ── 시간 흐름 화살표 (상단 레인 좌→우) + 계층 연결 화살표 (위→아래) ──
for i in range(3):
    x_from = COLS[i][1] + BOX_W
    x_to = COLS[i + 1][1]
    d.arrow([(x_from, 186), (x_to, 186)], MUTED, "ar", 1.2)

col_colors = [(INFO, "info"), (WARN, "warn"), (OK, "ok"), (ACC, "acc")]
for (_, x), (c, mk) in zip(COLS, col_colors):
    cx = x + BOX_W / 2
    d.arrow([(cx, 216), (cx, 256)], c, mk, 1.3)
    d.arrow([(cx, 316), (cx, 356)], c, mk, 1.3)

# ── 셀 내용 (focal 1곳: t4 Agent 디스크 재사용) ────────────────────────
# Row 0: Executor 슬롯 요청·반납
cell_box(COLS[0][1], 156, "빌드 #1 시작", "allocate(job)", INFO)
cell_box(COLS[1][1], 156, "빌드 #2 겹침", "!quick · 다른 context", WARN)
cell_box(COLS[2][1], 156, "빌드 #1 종료", "Callback.finished", OK)
cell_box(COLS[3][1], 156, "빌드 #3 도착", "allocate(job)", INFO)

# Row 1: Controller JVM (WorkspaceList.inUse)
cell_box(COLS[0][1], 256, "inUse 등록", "{job: #1}", INFO)
cell_box(COLS[1][1], 256, "i=1 충돌 → i=2", "{job: #1, job@2: #2}", WARN)
cell_box(COLS[2][1], 256, "job 항목 제거", "{job@2: #2}", OK)
cell_box(COLS[3][1], 256, "i=1 빈 자리 획득", "{job@2: #2, job: #3}", INFO)

# Row 2: Agent 디스크 (실제 작업 경로)
cell_box(COLS[0][1], 356, "ws/job", "빌드 #1 사용", INFO)
cell_box(COLS[1][1], 356, "ws/job · ws/job@2", "#1 · #2 분리 사용", WARN)
cell_box(COLS[2][1], 356, "ws/job 임대 풀림", "ws/job@2 는 #2 유지", OK)
cell_box(COLS[3][1], 356, "ws/job 재사용", "빌드 #3 배정", ACC, focal=True)

# ── Legend ─────────────────────────────────────────────────────────────
d.legend(444, [
    ("기본 경로 배정", INFO),
    ("충돌 회피 (@2)", WARN),
    ("임대 반납", OK),
    ("반납 뒤 재사용", ACC),
])

out_path = sys.argv[1] if len(sys.argv) > 1 else str(pathlib.Path(__file__).resolve().parent.parent / "01-03.workspace-lease.svg")
d.save(out_path)
print(f"saved: {out_path}")

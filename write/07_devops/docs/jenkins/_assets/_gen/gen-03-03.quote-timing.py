# 사실 출처: 03-03.sh step 이 실패를 삼키는 이유.md:103-114
# 타입 스펙: type-process
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, BAD, INFO, KR, MONO

W, H = 960, 452

d = D(
    W, H,
    "JENKINS · STRING INTERPOLATION",
    "작은따옴표와 큰따옴표의 시크릿 전달 시점",
    "Groovy 평가부터 셸 프로세스까지의 값 바인딩 단계와 프로세스 노출 위험 비교",
    lead="작은따옴표는 셸이 환경변수로 읽고 큰따옴표는 Groovy 가 먼저 문자열에 값을 박습니다"
)

# ── 3단계 컬럼 정의 ──────────────────────────────────────────────────────
COL_W = 280
COL_GAP = 24
X0 = 36

STEPS = [
    ("1. Groovy 평가", "문자열 해석 시점", INFO),
    ("2. step 에 넘어가는 문자열", "sh 호출 인자", ACC),
    ("3. 셸 프로세스", "에이전트 실행 환경", OK),
]

HEADER_Y = 96
HEADER_H = 44

for i, (title, sub, col) in enumerate(STEPS):
    x = X0 + i * (COL_W + COL_GAP)
    d.box(x, HEADER_Y, COL_W, HEADER_H, PAPER2, RULE, 1.0)
    d.t(x + COL_W // 2, HEADER_Y + 18, title, 13, col, KR, "middle", 600)
    d.t(x + COL_W // 2, HEADER_Y + 34, sub, 11, MUTED, KR, "middle")

    if i < len(STEPS) - 1:
        ax1 = x + COL_W + 2
        ax2 = x + COL_W + COL_GAP - 2
        ay = HEADER_Y + HEADER_H // 2
        d.arrow([(ax1, ay), (ax2, ay)], MUTED, "ar", 1.2)


# ── 트랙 배경 렌더러 ────────────────────────────────────────────────────
def render_track_bg(y, h, title, sub):
    d.o.append(f'<rect x="{X0}" y="{y}" width="888" height="{h}" rx="6" fill="{PAPER2}" stroke="{RULE}" stroke-width="0.8"/>')
    d.t(X0 + 14, y + 17, title, 12, INK, KR, "start", 600)
    d.t(X0 + 14, y + 32, sub, 11, MUTED, KR, "start")


# ── 트랙 1: 작은따옴표 (sh '...') ───────────────────────────────────────
T1_Y = 152
T1_H = 104
render_track_bg(T1_Y, T1_H, "작은따옴표 (sh '...')", "Groovy 는 손대지 않음 · 셸이 환경변수를 읽음")

CARD_Y1 = T1_Y + 38
CARD_W = 264
CARD_H = 56

# Col 0: Groovy 평가
cx0 = X0 + 8
d.box(cx0, CARD_Y1, CARD_W, CARD_H, PAPER, RULE, 1.0)
d.t(cx0 + 10, CARD_Y1 + 17, "sh 'curl -H \"$TOKEN\" ...'", 11, INK, MONO, "start")
d.t(cx0 + 10, CARD_Y1 + 33, "Groovy 보간 없음", 11, MUTED, KR, "start")
d.t(cx0 + 10, CARD_Y1 + 49, "문자열 그대로 전달", 11, INFO, KR, "start")

# Col 1: step 에 넘어가는 문자열
cx1 = cx0 + COL_W + COL_GAP
d.box(cx1, CARD_Y1, CARD_W, CARD_H, PAPER, RULE, 1.0)
d.t(cx1 + 10, CARD_Y1 + 17, "curl -H \"$TOKEN\" ...", 11, INK, MONO, "start")
d.t(cx1 + 10, CARD_Y1 + 33, "$TOKEN 글자 그대로", 11, MUTED, KR, "start")
d.t(cx1 + 10, CARD_Y1 + 49, "토큰 값 미노출", 11, OK, KR, "start")

# Col 2: 셸 프로세스
cx2 = cx1 + COL_W + COL_GAP
d.box(cx2, CARD_Y1, CARD_W, CARD_H, PAPER, OK, 1.2)
d.t(cx2 + 10, CARD_Y1 + 17, "환경변수 TOKEN 조회", 11, OK, MONO, "start")
d.t(cx2 + 10, CARD_Y1 + 33, "셸의 환경변수로만 존재", 11, OK, KR, "start")
d.t(cx2 + 10, CARD_Y1 + 49, "안전한 시크릿 전달", 11, OK, KR, "start")

# Track 1 화살표
ay1 = CARD_Y1 + CARD_H // 2
d.arrow([(cx0 + CARD_W + 2, ay1), (cx1 - 2, ay1)], MUTED, "ar", 1.2)
d.arrow([(cx1 + CARD_W + 2, ay1), (cx2 - 2, ay1)], OK, "ok", 1.2)


# ── 트랙 2: 큰따옴표 (sh "...") ─────────────────────────────────────────
T2_Y = 268
T2_H = 104
render_track_bg(T2_Y, T2_H, "큰따옴표 (sh \"...\")", "Groovy 가 먼저 펼침 · 값이 문자열에 박힘")

CARD_Y2 = T2_Y + 38

# Col 0: Groovy 평가
d.box(cx0, CARD_Y2, CARD_W, CARD_H, PAPER, ACC, 1.1)
d.t(cx0 + 10, CARD_Y2 + 17, "sh \"curl -H \\\"${TOKEN}\\\" ...\"", 11, INK, MONO, "start")
d.t(cx0 + 10, CARD_Y2 + 33, "Groovy 가 ${TOKEN} 을 펼침", 11, ACC, KR, "start")
d.t(cx0 + 10, CARD_Y2 + 49, "명령 전달 전 값 치환", 11, ACC, KR, "start")

# Col 1: step 에 넘어가는 문자열
d.box(cx1, CARD_Y2, CARD_W, CARD_H, PAPER, BAD, 1.1)
d.t(cx1 + 10, CARD_Y2 + 17, "curl -H \"(토큰 값)\" ...", 11, BAD, MONO, "start")
d.t(cx1 + 10, CARD_Y2 + 33, "토큰 값이 문자열에 박힘", 11, BAD, KR, "start")
d.t(cx1 + 10, CARD_Y2 + 49, "평문 시크릿 노출", 11, BAD, KR, "start")

# Col 2: 셸 프로세스
d.box(cx2, CARD_Y2, CARD_W, CARD_H, PAPER, BAD, 1.2)
d.t(cx2 + 10, CARD_Y2 + 17, "ps 프로세스 인자에 노출", 11, BAD, MONO, "start")
d.t(cx2 + 10, CARD_Y2 + 33, "프로세스 인자 노출", 11, BAD, KR, "start", 600)
d.t(cx2 + 10, CARD_Y2 + 49, "명령 주입 위험", 11, BAD, KR, "start", 600)

# Track 2 화살표
ay2 = CARD_Y2 + CARD_H // 2
d.arrow([(cx0 + CARD_W + 2, ay2), (cx1 - 2, ay2)], ACC, "acc", 1.2)
d.arrow([(cx1 + CARD_W + 2, ay2), (cx2 - 2, ay2)], BAD, "bad", 1.2)


# ── 범례 ────────────────────────────────────────────────────────────────
LEG_Y = 396
d.legend(LEG_Y, [
    ("환경변수 참조 (안전)", OK),
    ("Groovy 치환", ACC),
    ("프로세스 인자 노출 · 명령 주입", BAD),
    ("기본 전달", INFO),
])

out_path = sys.argv[1] if len(sys.argv) > 1 else str(pathlib.Path(__file__).resolve().parent.parent / "03-03.quote-timing.svg")
d.save(out_path)
print(f"saved: {out_path}")

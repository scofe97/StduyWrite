# 타입 스펙: type-process
# 2절 Values 우선순위와 덮어쓰기 규칙 — 병합 메커니즘
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, BAD, PAPER, PAPER2, KR, MONO

W, H = 960, 424

d = D(W, H, "HELM · VALUES PRECEDENCE",
      "Values 우선순위와 덮어쓰기 병합 메커니즘",
      "차트 기본값부터 --set까지 단계별 값 변경 경로 및 맵 키 병합과 리스트 대체",
      lead="오른쪽 입력이 이전 값을 덮어씀 · 맵은 키 단위 합침, 리스트는 배열 통째 대체")

# 4개 단계 컬럼 좌표
COL_W = 216
COL_GAP = 16
X0 = 24

STEPS = [
    ("1. 차트 기본값", "values.yaml", INFO),
    ("2. 공통 파일", "-f values-base.yaml", INFO),
    ("3. 환경 파일", "-f values-dev.yaml", INFO),
    ("4. CLI 플래그", "--set settings.logLevel=ERROR", ACC),
]

# 단계 헤더 박스 및 화살표
HEADER_Y = 96
HEADER_H = 46

for i, (title, sub, col) in enumerate(STEPS):
    x = X0 + i * (COL_W + COL_GAP)
    d.box(x, HEADER_Y, COL_W, HEADER_H, PAPER2, RULE, 1.0)
    d.t(x + COL_W // 2, HEADER_Y + 18, title, 13, col, KR, "middle", 600)
    d.t(x + COL_W // 2, HEADER_Y + 34, sub, 11, MUTED, MONO, "middle")

    if i < len(STEPS) - 1:
        ax1 = x + COL_W + 2
        ax2 = x + COL_W + COL_GAP - 2
        ay = HEADER_Y + HEADER_H // 2
        d.arrow([(ax1, ay), (ax2, ay)], MUTED, "ar", 1.2)

# 트랙 1: 맵 (settings) 키 단위 병합
T1_Y = 158
T1_H = 112

def render_track_label(y, h, title, sub):
    d.o.append(f'<rect x="{X0}" y="{y}" width="912" height="{h}" rx="6" fill="{PAPER2}" stroke="{RULE}" stroke-width="0.8"/>')
    d.t(X0 + 12, y + 18, title, 13, INK, KR, "start", 600)
    d.t(X0 + 12, y + 34, sub, 12, MUTED, KR, "start")

render_track_label(T1_Y, T1_H, "맵 병합 (settings)", "키 단위 덮어쓰기 · 미지정 키 보존")

MAP_DATA = [
    ("logLevel: INFO", "tracing: false", "metrics: true", INFO, MUTED, MUTED),
    ("logLevel: WARN", "tracing: true", "metrics: true", ACC, ACC, INFO),
    ("logLevel: DEBUG", "tracing: true", "metrics: true", ACC, INFO, INFO),
    ("logLevel: ERROR", "tracing: true", "metrics: true", ACC, INFO, INFO),
]

CARD_Y = T1_Y + 46
CARD_H = 56
INNER_W = 200

for i, (log_val, tr_val, met_val, c_log, c_tr, c_met) in enumerate(MAP_DATA):
    cx = X0 + 8 + i * (COL_W + COL_GAP)
    border_c = ACC if i == 3 else RULE
    d.box(cx, CARD_Y, INNER_W, CARD_H, PAPER, border_c, 1.0)
    d.t(cx + 10, CARD_Y + 17, log_val, 11, c_log, MONO, "start", 600 if c_log == ACC else 400)
    d.t(cx + 10, CARD_Y + 33, tr_val, 11, c_tr, MONO, "start")
    d.t(cx + 10, CARD_Y + 48, met_val, 11, c_met, MONO, "start")

    if i < 3:
        ax1 = cx + INNER_W + 2
        ax2 = cx + INNER_W + COL_GAP + 12
        ay = CARD_Y + CARD_H // 2
        d.arrow([(ax1, ay), (ax2, ay)], MUTED, "ar", 1.0)

# 트랙 2: 리스트 (settings.tags) 통째 대체
T2_Y = 282
T2_H = 82

render_track_label(T2_Y, T2_H, "리스트 대체 (settings.tags)", "원소 병합 없이 배열 통째 교체")

LIST_DATA = [
    ("[web, frontend]", "기본 배열", MUTED),
    ("[base]", "배열 교체", WARN),
    ("[dev-only]", "배열 교체", WARN),
    ("[dev-only]", "배열 유지", INFO),
]

L_CARD_Y = T2_Y + 42
L_CARD_H = 32

for i, (tags_val, status_desc, tag_c) in enumerate(LIST_DATA):
    cx = X0 + 8 + i * (COL_W + COL_GAP)
    d.box(cx, L_CARD_Y, INNER_W, L_CARD_H, PAPER, RULE, 1.0)
    d.t(cx + 8, L_CARD_Y + 20, tags_val, 11, tag_c, MONO, "start", 600 if tag_c == WARN else 400)
    
    # 칩 너비 60px, 우측 여백 6px 두고 카드 내부 완벽 중첩
    chip_w = 64
    chip_x = cx + INNER_W - chip_w // 2 - 6
    d.o.append(f'<rect x="{chip_x - chip_w // 2}" y="{L_CARD_Y + 6}" width="{chip_w}" height="20" rx="4" fill="{PAPER}" stroke="{tag_c}" stroke-width="0.8"/>')
    d.t(chip_x, L_CARD_Y + 20, status_desc, 11, tag_c, KR, "middle")

    if i < 3:
        ax1 = cx + INNER_W + 2
        ax2 = cx + INNER_W + COL_GAP + 12
        ay = L_CARD_Y + L_CARD_H // 2
        d.arrow([(ax1, ay), (ax2, ay)], MUTED, "ar", 1.0)

# 범례
LEG_Y = 382
d.legend(LEG_Y, [
    ("기본값 및 유지", INFO),
    ("키 단위 덮어쓰기 (맵)", ACC),
    ("배열 통째 대체 (리스트)", WARN),
])

out_path = sys.argv[1] if len(sys.argv) > 1 else str(pathlib.Path(__file__).resolve().parent.parent / "Helm values와 렌더 검증.values-precedence.svg")
d.save(out_path)
print("ok gen-Helm values와 렌더 검증.values-precedence")

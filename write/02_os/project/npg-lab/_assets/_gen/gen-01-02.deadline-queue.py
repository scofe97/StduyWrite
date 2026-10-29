# 01-02-deadline-queue — 프록시 요청 기한 15초 안에서 줄 대기와 백엔드 처리가 200 과 504 UT 로 갈리는 시간축
# 본문 요구: 줄 대기 약 7초 + 백엔드 8초가 15초 기한 경계에 걸려, 7초를 넘겨 기다린 검색은 UT 로 끝나고 백엔드 일이 헛일이 됨을 가로 시간축으로 보인다.
# 타입 스펙: type-timeline
# 사실 출처: ch08-slow-search-starves-lookup.md:16-17,72-75(반은 14.8초에 200, 반은 15초에 UT), ADR 0012:71,81,86,100
import sys
from pathlib import Path

# _assets 및 _gen 경로 등록
ASSETS_DIR = Path(__file__).resolve().parent.parent
GEN_DIR = Path(__file__).resolve().parent
if str(ASSETS_DIR) not in sys.path:
    sys.path.insert(0, str(ASSETS_DIR))
if str(GEN_DIR) not in sys.path:
    sys.path.insert(0, str(GEN_DIR))

from dd import D, INK, MUTED, SOFT, RULE, PAPER, PAPER2, ACC, OK, BAD, WARN, INFO, KR, MONO

W = 960
H = 528

d = D(
    W,
    H,
    "TIMELINE · CH08 DEADLINE & QUEUE TIMEOUT",
    "요청 기한 15초 안의 줄 대기·백엔드 처리 시간축",
    "줄 대기 약 7초와 백엔드 처리 8초가 요청 기한 15초 경계에 걸려, 7초 안에 칸을 얻은 검색은 200 으로 끝나고 7초를 넘겨 기다린 검색은 15초에 504 UT 로 끝나 백엔드 일이 헛일이 되는 시간축",
    lead="줄 대기 약 7초와 백엔드 8초가 15초 기한에 걸려, 7초를 넘겨 기다린 검색은 504 UT 로 끝나고 백엔드 일은 헛일이 됩니다.",
)

# 1초 = 48px, t=0s 는 x=96. 모든 막대는 15s(x=816) 안에서 끝난다.
def X(sec):
    return round(96 + sec * 48, 1)

# 1. 상단: 프록시 요청 전체 기한 15초 구간 막대 (t=0s..15s)
top_x0, top_w, top_y, top_h = 96, 720, 116, 28
d.box(top_x0, top_y, top_w, top_h, fill=PAPER2, stroke=INFO, sw=1.2, r=4)
d.t(top_x0 + top_w // 2, top_y + 19, "프록시 요청 전체 기한 15s (context.WithTimeout)", 14, INK, KR, "middle", 600)

# 2. 두 갈래 막대
# 2-1. 7초 안에 칸을 얻은 검색: 대기 + 8s 처리 → 14.8s 에 200
a_y, row_h = 160, 44
a_wait_end = 14.8 - 8
d.tone(X(0), a_y, X(a_wait_end) - X(0), row_h, INFO, r=6, op="14", sw=1.2)
d.t((X(0) + X(a_wait_end)) / 2, a_y + 27, "줄 대기 7s 미만", 14, INFO, KR, "middle", 600)
d.tone(X(a_wait_end), a_y, X(14.8) - X(a_wait_end), row_h, OK, r=6, op="14", sw=1.2)
d.t((X(a_wait_end) + X(14.8)) / 2, a_y + 27, "백엔드 처리 8s → 14.8s 에 200", 14, OK, KR, "middle", 600)
d.t(84, a_y + 27, "200", 14, OK, MONO, "end", 600)

# 2-2. 7초를 넘겨 기다린 검색: 처리 도중 15s 에 UT, 그때까지의 백엔드 일이 헛일
b_y = 212
b_wait_end = 7.25
d.tone(X(0), b_y, X(b_wait_end) - X(0), row_h, INFO, r=6, op="14", sw=1.2)
d.t((X(0) + X(b_wait_end)) / 2, b_y + 27, "줄 대기 7s 넘게", 14, INFO, KR, "middle", 600)
d.tone(X(b_wait_end), b_y, X(15) - X(b_wait_end), row_h, BAD, r=6, op="20", sw=1.4)
d.t((X(b_wait_end) + X(15)) / 2, b_y + 27, "백엔드 처리 중 15s 에 손님 이탈 · 헛일", 14, BAD, KR, "middle", 600)
d.t(84, b_y + 27, "UT", 14, BAD, MONO, "end", 600)

# 3. 시간축 기준선 (Timeline Baseline) 및 눈금 (Ticks)
base_y = 276
d.line(72, base_y, 888, base_y, RULE, 1.0)

# 0s 눈금 (도착)
d.line(96, base_y - 4, 96, base_y + 4, SOFT, 0.8)
d.t(96, base_y + 19, "0s (도착)", 13, SOFT, KR, "middle")

# 7s 눈금 (전달)
d.line(432, base_y - 4, 432, base_y + 4, SOFT, 0.8)
d.t(432, base_y + 19, "약 7s (전달)", 13, SOFT, KR, "middle")

# 15s Focal 눈금 (기한 초과) — 기준선 위 동심원 + 바로 아래 15s 라벨
d.line(816, 108, 816, base_y + 4, ACC, 1.8, dash="4 3")
d.t(816, 98, "15s 기한 초과 (504 UT)", 14, ACC, KR, "middle", 600)
d.o.append(f'<circle cx="816" cy="{base_y}" r="8" fill="none" stroke="{ACC}" stroke-width="2.0"/>')
d.o.append(f'<circle cx="816" cy="{base_y}" r="5" fill="{ACC}"/>')
d.t(816, base_y + 28, "15s (기한)", 14, ACC, KR, "middle", 600)


# 4. 하단 띠: 리틀의 법칙 L = λW 및 ADR 0012 결정 6 계산 근거
card_x, card_y, card_w, card_h = 48, 332, 864, 124
d.box(card_x, card_y, card_w, card_h, fill=PAPER2, stroke=RULE, sw=0.9, r=8)

# 카드 제목
d.t(card_x + 24, card_y + 24, "리틀의 법칙 L = λW 및 ADR 0012 결정 6", 15, INK, KR, "start", 600)

# 3열 계산 지표
# 열 1: 처리량 계산
col1_x = card_x + 24
d.t(col1_x, card_y + 50, "처리량 계산 (초당 처리 건수)", 14, SOFT, KR, "start")
d.t(col1_x, card_y + 74, "검색 8칸 ÷ 8초 = 처리량 초당 1건", 14, INK, KR, "start")
d.t(col1_x, card_y + 98, "k번째 줄 대기시간 W ≈ k초", 14, MUTED, KR, "start")

# 열 2: 줄 상한 7 결정
col2_x = card_x + 316
d.t(col2_x, card_y + 50, "줄 상한 7 결정 (searchPending)", 14, SOFT, KR, "start")
d.t(col2_x, card_y + 74, "k + 8 ≤ 15s 기한 경계 조건", 14, INK, KR, "start")
d.t(col2_x, card_y + 98, "칸 8 + 줄 7 가득 차면 503 UO", 14, MUTED, KR, "start")

# 열 3: 실측 경계 결과
col3_x = card_x + 600
d.t(col3_x, card_y + 50, "실측 경계 결과 (ch08 I1)", 14, SOFT, KR, "start")
d.t(col3_x, card_y + 74, "대기 7s + 처리 8s ≈ 15s 경계", 14, WARN, KR, "start", 600)
d.t(col3_x, card_y + 98, "성공 200 (0.53/s) · UT (0.48/s)", 14, BAD, KR, "start")

# 5. 범례
d.legend(476, [
    ("줄 대기 구간", INFO),
    ("백엔드 처리", OK),
    ("15s 기한선 (focal)", ACC),
    ("기한 넘긴 헛일", BAD),
])

out_path = ASSETS_DIR / "01-02-deadline-queue.svg"
d.save(str(out_path))
print(f"saved: {out_path}")

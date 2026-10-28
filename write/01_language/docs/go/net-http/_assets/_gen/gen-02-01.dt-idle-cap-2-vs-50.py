# 본문 요구: §1 ### 함정·관찰: DefaultMaxIdleConnsPerHost=2. 동시 50 요청을 세 번 보냈을 때 기본값은 라운드마다 48개를 새로 열고 닫아 TIME_WAIT 가 쌓이고, 50 으로 올리면 2라운드부터 모두 재사용된다는 것.
# 타입 스펙: type-bar
# 사실 출처: go1.25.1 src/net/http/transport.go:60, transport.go:1040-1045, 실측 보고서 시험 1
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, KR, MONO

W, H = 960, 596

d = D(W, H,
      "HTTP TRANSPORT MAXIDLECONNSPERHOST MEASUREMENT",
      "호스트당 유휴 연결 한도 2 vs 50 실측 비교",
      "동시 50 요청을 3회 반복했을 때 MaxIdleConnsPerHost 기본값(2)과 50 설정 시의 연결 재사용 및 TIME_WAIT 누적 차이",
      "기본값은 매 라운드 48개 소켓을 닫아 TIME_WAIT가 급증하나, 50 설정 시 2라운드부터 전량 재사용되어 소켓 누적이 없습니다")

# 공통 좌표 상수
PANEL_X = 24
PANEL_W = 912
PANEL_H = 196
BAR_W = 92
PLOT_LEFT = 76
PLOT_RIGHT = 910

# X축 라운드 중심 위치 (3개)
ROUND_CX = [210, 480, 750]
ROUND_NAMES = ["1 라운드 (50 요청)", "2 라운드 (50 요청)", "3 라운드 (50 요청)"]

def draw_panel_axes(py0, title, subtitle):
    # 패널 외곽 상자
    d.box(PANEL_X, py0, PANEL_W, PANEL_H, fill=PAPER2, stroke=RULE, sw=0.8, r=6)
    d.t(PANEL_X + 16, py0 + 22, title, 13, INK, fam=KR, anchor="start", weight=600)
    d.t(PANEL_X + 320, py0 + 22, subtitle, 11, SOFT, fam=KR, anchor="start")
    
    # Y축 눈금 (0 ~ 50, 10단위)
    base_y = py0 + 156
    top_y = py0 + 56
    
    # 눈금선 6개 (바와 배지가 없는 구간에만 그려 텍스트 관통 방지)
    for val in range(0, 51, 10):
        y = base_y - val * 2
        d.t(PLOT_LEFT - 10, y + 4, str(val), 11, MUTED, fam=MONO, anchor="end")
        if val == 0:
            d.line(PLOT_LEFT, y, PLOT_RIGHT, y, RULE, 0.8)
        else:
            # 눈금 틱
            d.line(PLOT_LEFT - 4, y, PLOT_LEFT, y, RULE, 0.8)
            # 배경 보조선 (바 사이 빈 공간에만 은은하게)
            for x1, x2 in [(PLOT_LEFT, 155), (395, 430), (665, 700)]:
                d.line(x1, y, x2, y, RULE, 0.5, dash="3 3")
    
    # Y축 세로선
    d.line(PLOT_LEFT, top_y, PLOT_LEFT, base_y, RULE, 0.8)
    
    # X축 라운드 라벨
    for cx, r_name in zip(ROUND_CX, ROUND_NAMES):
        d.t(cx, base_y + 24, r_name, 11, MUTED, fam=KR, anchor="middle", weight=600)
        
    return base_y

# ── 패널 1 (위): MaxIdleConnsPerHost 기본 (0 → 2) ─────────────
P1_Y = 100
base_y1 = draw_panel_axes(P1_Y, "MaxIdleConnsPerHost 기본 (0 → 2)", "동시 50 요청마다 2개만 풀에 보관 · 48개 폐기로 TIME_WAIT 급증")

# 라운드 1: 새 연결 50, 재사용 0, TIME_WAIT 48
r1_cx = ROUND_CX[0]
bx1 = r1_cx - BAR_W // 2
# 새 연결 50개 막대 (h=100)
d.box(bx1, base_y1 - 100, BAR_W, 100, fill=f"{INFO}16", stroke=INFO, sw=1.0, r=4)
d.t(r1_cx, base_y1 - 50, "새 연결 50", 12, INK, fam=KR, anchor="middle", weight=600)
# TIME_WAIT 48 배지
d.box(r1_cx + BAR_W // 2 + 14, base_y1 - 74, 112, 44, fill=PAPER, stroke=WARN, sw=0.9, r=4)
d.t(r1_cx + BAR_W // 2 + 70, base_y1 - 55, "TIME_WAIT 48", 12, WARN, fam=MONO, anchor="middle", weight=600)
d.t(r1_cx + BAR_W // 2 + 70, base_y1 - 39, "누적 48 소켓", 11, SOFT, fam=KR, anchor="middle")

# 라운드 2: 재사용 2, 새 연결 48, TIME_WAIT 96
r2_cx = ROUND_CX[1]
bx2 = r2_cx - BAR_W // 2
# 재사용 2개 막대 (바닥 h=5)
d.box(bx2, base_y1 - 5, BAR_W, 5, fill=OK, stroke=OK, sw=0.8, r=2)
# 새 연결 48개 막대 (위 h=95)
d.box(bx2, base_y1 - 100, BAR_W, 95, fill=f"{INFO}16", stroke=INFO, sw=1.0, r=4)
d.t(r2_cx, base_y1 - 52, "새 연결 48", 12, INK, fam=KR, anchor="middle", weight=600)
d.t(bx2 - 8, base_y1 - 5, "재사용 2", 11, OK, fam=KR, anchor="end", weight=600)
# TIME_WAIT 96 배지
d.box(r2_cx + BAR_W // 2 + 14, base_y1 - 74, 112, 44, fill=PAPER, stroke=WARN, sw=0.9, r=4)
d.t(r2_cx + BAR_W // 2 + 70, base_y1 - 55, "TIME_WAIT 96", 12, WARN, fam=MONO, anchor="middle", weight=600)
d.t(r2_cx + BAR_W // 2 + 70, base_y1 - 39, "누적 96 소켓", 11, SOFT, fam=KR, anchor="middle")

# 라운드 3: 재사용 2, 새 연결 48, TIME_WAIT 144 (focal)
r3_cx = ROUND_CX[2]
bx3 = r3_cx - BAR_W // 2
# 재사용 2개 막대
d.box(bx3, base_y1 - 5, BAR_W, 5, fill=OK, stroke=OK, sw=0.8, r=2)
# 새 연결 48개 막대
d.box(bx3, base_y1 - 100, BAR_W, 95, fill=f"{INFO}16", stroke=INFO, sw=1.0, r=4)
d.t(r3_cx, base_y1 - 52, "새 연결 48", 12, INK, fam=KR, anchor="middle", weight=600)
d.t(bx3 - 8, base_y1 - 5, "재사용 2", 11, OK, fam=KR, anchor="end", weight=600)
# TIME_WAIT 144 배지 (focal)
d.o.append(f'<rect x="{r3_cx + BAR_W // 2 + 14}" y="{base_y1 - 74}" width="124" height="44" rx="4" fill="{ACC}20" stroke="{ACC}" stroke-width="1.5"/>')
d.t(r3_cx + BAR_W // 2 + 76, base_y1 - 55, "TIME_WAIT 144", 12, ACC, fam=MONO, anchor="middle", weight=600)
d.t(r3_cx + BAR_W // 2 + 76, base_y1 - 39, "누적 144 (focal)", 11, ACC, fam=KR, anchor="middle", weight=600)

# ── 패널 2 (아래): MaxIdleConnsPerHost 50 ──────────────────────
P2_Y = 312
base_y2 = draw_panel_axes(P2_Y, "MaxIdleConnsPerHost 50", "호스트당 50개 유지 · 2라운드부터 전량 재사용으로 TIME_WAIT 0")

# 라운드 1: 새 연결 50, 재사용 0, TIME_WAIT 0
r1_cx2 = ROUND_CX[0]
bx1_2 = r1_cx2 - BAR_W // 2
d.box(bx1_2, base_y2 - 100, BAR_W, 100, fill=f"{INFO}16", stroke=INFO, sw=1.0, r=4)
d.t(r1_cx2, base_y2 - 50, "새 연결 50", 12, INK, fam=KR, anchor="middle", weight=600)
# TIME_WAIT 0 배지
d.box(r1_cx2 + BAR_W // 2 + 14, base_y2 - 74, 112, 44, fill=PAPER, stroke=RULE, sw=0.8, r=4)
d.t(r1_cx2 + BAR_W // 2 + 70, base_y2 - 55, "TIME_WAIT 0", 12, MUTED, fam=MONO, anchor="middle", weight=600)
d.t(r1_cx2 + BAR_W // 2 + 70, base_y2 - 39, "소켓 누적 없음", 11, SOFT, fam=KR, anchor="middle")

# 라운드 2: 재사용 50, 새 연결 0, TIME_WAIT 0
r2_cx2 = ROUND_CX[1]
bx2_2 = r2_cx2 - BAR_W // 2
d.box(bx2_2, base_y2 - 100, BAR_W, 100, fill=f"{OK}20", stroke=OK, sw=1.2, r=4)
d.t(r2_cx2, base_y2 - 58, "재사용 50", 12, OK, fam=KR, anchor="middle", weight=600)
d.t(r2_cx2, base_y2 - 42, "100% 풀 재사용", 11, OK, fam=KR, anchor="middle")
# TIME_WAIT 0 배지
d.box(r2_cx2 + BAR_W // 2 + 14, base_y2 - 74, 112, 44, fill=PAPER, stroke=RULE, sw=0.8, r=4)
d.t(r2_cx2 + BAR_W // 2 + 70, base_y2 - 55, "TIME_WAIT 0", 12, MUTED, fam=MONO, anchor="middle", weight=600)
d.t(r2_cx2 + BAR_W // 2 + 70, base_y2 - 39, "소켓 누적 없음", 11, SOFT, fam=KR, anchor="middle")

# 라운드 3: 재사용 50, 새 연결 0, TIME_WAIT 0
r3_cx2 = ROUND_CX[2]
bx3_2 = r3_cx2 - BAR_W // 2
d.box(bx3_2, base_y2 - 100, BAR_W, 100, fill=f"{OK}20", stroke=OK, sw=1.2, r=4)
d.t(r3_cx2, base_y2 - 58, "재사용 50", 12, OK, fam=KR, anchor="middle", weight=600)
d.t(r3_cx2, base_y2 - 42, "100% 풀 재사용", 11, OK, fam=KR, anchor="middle")
# TIME_WAIT 0 배지
d.box(r3_cx2 + BAR_W // 2 + 14, base_y2 - 74, 112, 44, fill=PAPER, stroke=RULE, sw=0.8, r=4)
d.t(r3_cx2 + BAR_W // 2 + 70, base_y2 - 55, "TIME_WAIT 0", 12, MUTED, fam=MONO, anchor="middle", weight=600)
d.t(r3_cx2 + BAR_W // 2 + 70, base_y2 - 39, "소켓 누적 없음", 11, SOFT, fam=KR, anchor="middle")

# 캡션 줄
CAPTION_Y = 524
d.t(PANEL_X + 16, CAPTION_Y, "측정 조건: 동시 50 · 3 라운드 · Go 1.25.1 · Linux (OrbStack ubuntu eth0, 핸들러 20ms)", 11, SOFT, fam=KR, anchor="start")

# 범례
LEGEND_Y = 544
d.legend(LEGEND_Y, [
    ("재사용 (Reused)", OK),
    ("새 연결 (New)", INFO),
    ("누적 TIME_WAIT", WARN),
    ("TIME_WAIT 144 (focal)", ACC),
])

out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "02-01.dt-idle-cap-2-vs-50.svg"))
d.save(out_path)

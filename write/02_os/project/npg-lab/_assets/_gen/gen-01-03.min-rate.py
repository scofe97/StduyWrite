# 01-03-min-rate — 느린 손님의 전송 추세와 최소 속도 하한선 미달에 의한 408 CT 차단
# 본문 요구: 가로 시간, 세로 누적 바이트. 2초에 1바이트 손님 선과 최소 속도 하한 선. 틈 시계(틈 2초 < 기한)는 못 끊고 하한 선 아래로 떨어지는 지점에서 408 CT 로 끊긴다. 값은 리허설 J1·ADR 0014 의 값만.
# 타입 스펙: type-line
# 사실 출처: 01-03.리버스 프록시 다운스트림 층 — 틈 시계·최소 속도·드레인.md:51-64, ADR 0014:11-13,38-42,59-60, ch09-slow-post-body.md:13,20-22,33-39,43-45
import sys
from pathlib import Path

ASSETS_DIR = Path(__file__).resolve().parent.parent
GEN_DIR = Path(__file__).resolve().parent
if str(ASSETS_DIR) not in sys.path:
    sys.path.insert(0, str(ASSETS_DIR))
if str(GEN_DIR) not in sys.path:
    sys.path.insert(0, str(GEN_DIR))

from dd import D, INK, MUTED, SOFT, RULE, PAPER, PAPER2, ACC, OK, BAD, WARN, INFO, KR, MONO

W = 960
H = 492

d = D(
    W,
    H,
    "LINE CHART · CH09 J1 MIN-RATE & 408 CT",
    "느린 손님 전송과 최소 속도 하한선의 408 CT 차단",
    "2초에 1바이트씩 흘리는 느린 손님은 틈 시계로 끊지 못하고, 10초 시점에 최소 속도 1KB/s 하한선에 미달하여 408 CT 로 차단되는 추세",
    lead="틈 시계는 2초 간격마다 갱신되어 차단하지 못하지만, 10초 뒤 최소 속도 미달로 408 CT 가 발동합니다.",
)

# 상단 구분선
d.line(24, 92, 936, 92, RULE, 0.8)

# 차트 영역: X 100 ~ 760 (폭 660px), Y 124 ~ 380 (높이 256px)
X0, X1 = 100, 760
Y_TOP, Y_BOT = 124, 380

def px(sec):
    return round(X0 + (X1 - X0) * sec / 12.0, 1)

def py(kb):
    return round(Y_BOT - (Y_BOT - Y_TOP) * kb / 10.0, 1)

# Y축 격자선 및 라벨 (0, 2, 4, 6, 8, 10 KB)
for kb in (0, 2, 4, 6, 8, 10):
    y = py(kb)
    d.line(X0, y, X1, y, RULE, 0.5, "3 4")
    d.t(X0 - 12, y + 4, f"{kb} KB", 11, MUTED, MONO, "end")

d.t(X0 - 12, Y_TOP - 12, "누적 바이트", 12, MUTED, KR, "end", 600)

# X축 기준선 및 눈금 라벨 (0, 2, 4, 6, 8, 10, 12초)
d.line(X0, Y_BOT, X1, Y_BOT, RULE, 1.0)
for sec in (0, 2, 4, 6, 8, 10, 12):
    x = px(sec)
    d.line(x, Y_BOT, x, Y_BOT + 6, RULE, 1.0)
    d.t(x, Y_BOT + 22, f"{sec}s", 12, MUTED, MONO, "middle")

# 1. 최소 속도 하한 선 (1KB/s, 10s 에 10KB 도달)
d.line(px(0), py(0), px(10), py(10), WARN, 1.6, "6 4")
d.t(px(7.5), 156, "최소 속도 하한 선 (1KB/s)", 13, WARN, KR, "middle", 600)

# 10s 최소 속도 판정 기준선
d.line(px(10), Y_TOP, px(10), Y_BOT, INFO, 0.9, "3 3")
d.t(px(10), Y_TOP - 12, "10s: 최소 속도 평가 시작", 13, INFO, KR, "middle", 600)

# 2. 틈 시계 10s 설명 상자 (좌측 상단 여백)
d.box(120, 140, 220, 52, fill=PAPER2, stroke=INFO, sw=0.9, r=6)
d.t(230, 162, "읽기 틈 시계 10s (ADR 0014)", 13, INFO, KR, "middle", 600)
d.t(230, 180, "전송 틈 2s < 10s 로 매번 갱신 · 미차단", 12, MUTED, KR, "middle")

# 3. 느린 손님 전송선 (2초에 1B, 10s에 누적 5B)
pts = [(0, 0), (2, 0.001), (4, 0.002), (6, 0.003), (8, 0.004), (10, 0.005)]
pts_str = " ".join(f"{px(s):.1f},{py(kb):.1f}" for s, kb in pts)
d.o.append(f'<polyline points="{pts_str}" fill="none" stroke="{ACC}" stroke-width="2.0"/>')

for s, kb in pts:
    d.o.append(f'<circle cx="{px(s):.1f}" cy="{py(kb):.1f}" r="4" fill="{ACC}"/>')

d.t(px(5), Y_BOT - 16, "느린 손님 전송선 (2초에 1B)", 13, ACC, KR, "middle", 600)

# 4. 10.0s 시점 하한선 미달 및 408 CT 차단
# 하한선 미달 간격 표시 (수직 화살표)
d.arrow([(px(10) + 16, py(10) + 16), (px(10) + 16, Y_BOT - 16)], c=BAD, m="bad", sw=1.4)
d.t(px(10) + 26, (py(10) + Y_BOT) / 2, "하한선 미달 (5B << 10KB)", 12, BAD, KR, "start", 600)

# 10.0s 차단 원
d.o.append(f'<circle cx="{px(10):.1f}" cy="{py(0.005):.1f}" r="6" fill="{BAD}"/>')

# 차단 결과 상자 (x=666..862)
d.tone(px(10) + 16, Y_BOT - 52, 196, 52, BAD, r=6, op="18", sw=1.4)
d.t(px(10) + 114, Y_BOT - 32, "10.0s 에 408 CT 차단", 13, BAD, KR, "middle", 600)
d.t(px(10) + 114, Y_BOT - 14, "75건 차단 · 조회 p99 12ms", 12, OK, KR, "middle", 600)

# 범례
d.legend(
    428,
    [
        ("느린 손님", ACC),
        ("최소 속도 하한", WARN),
        ("읽기 틈 10s", INFO),
        ("408 CT 차단", BAD),
        ("다른 요청 정상", OK),
    ],
)

d.save("01-03-min-rate.svg")

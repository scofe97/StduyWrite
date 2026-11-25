# 05-01 §3 Flagger 가 옮긴 카나리 가중치의 시간 추이 — 원문 5.3.1 의 kubectl get canary -w 출력 11행을 그대로.
# 본문 근거: 05-01 §3 Flagger 기반 카나리 자동화.
# 값 근거: ch05.txt §5.3.1 (lines 1094-1105) kubectl get canary catalog-release -w 출력 11행 (22:50:16 ~ 23:04:41, 0→10→20→30→40→50→0).
# 타입 스펙: type-line — 시간에 따른 연속 추세. 점 11개(≤12), 시간축은 실제 타임스탬프 간격 그대로, y 축은 0 포함.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 960, 600
d = D(W, H, "ISTIO IN ACTION · 05-01 §3",
      "Flagger가 옮긴 카나리 가중치의 시간 추이",
      "2021-01-20 22:50:16 부터 23:04:41 까지 kubectl get canary catalog-release -w 가 찍은 11개 행. 가중치는 canary 로 가는 트래픽 비율(%).",
      "출력의 타임스탬프를 x 축에 놓았습니다. Progressing 에서 Promoting 까지 45초 구간 여섯 번이 걸립니다. 가운데 빈 구간은 축을 줄였습니다")

rows = [("22:50:16", "Initializing", 0), ("22:51:11", "Initialized", 0), ("22:58:41", "Progressing", 0),
        ("22:59:26", "Progressing", 10), ("23:00:11", "Progressing", 20), ("23:00:56", "Progressing", 30),
        ("23:01:41", "Progressing", 40), ("23:02:26", "Progressing", 50), ("23:03:11", "Promoting", 0),
        ("23:03:56", "Finalising", 0), ("23:04:41", "Succeeded", 0)]
def sec(t):
    h, m, s = map(int, t.split(":")); return h * 3600 + m * 60 + s
t0, t1 = sec(rows[0][0]), sec(rows[-1][0])
PL, PR, PT, PB = 80, W - 40, 112, 476
# 축 생략 — Initialized(22:51:11) 와 첫 Progressing(22:58:41) 사이 450초는 70px 로 줄인다
GAP_W = 70
ga, gb = sec(rows[1][0]), sec(rows[2][0])
K = (PR - PL - GAP_W) / ((t1 - t0) - (gb - ga))
def X(t):
    s = sec(t)
    if s <= ga: return PL + (s - t0) * K
    if s >= gb: return PL + (ga - t0) * K + GAP_W + (s - gb) * K
    return PL + (ga - t0) * K + (s - ga) / (gb - ga) * GAP_W
def Yv(v): return PB - v / 60 * (PB - PT)
# 그리드 0..60 step 10
for v in range(0, 61, 10):
    d.line(PL, Yv(v), PR, Yv(v), RULE, 0.8 if v else 1.0)
    d.t(PL - 10, Yv(v) + 4, f"{v}%", 10, SOFT, MONO, "end")
d.t(12, PT - 16, "canary 가중치 (%)", 13, SOFT, KR, "start")
# 시간 눈금 — 점마다
for t, st, v in rows:
    d.line(X(t), PB, X(t), PB + 6, RULE, 0.8)
for i, (t, st, v) in enumerate(rows):
    d.t(X(t), PB + 20 if i % 2 == 0 else PB + 36, t, 9, MUTED, MONO)
# 폴리라인(초점) + 점
pts = " ".join(f"{X(t):.1f},{Yv(v):.1f}" for t, st, v in rows)
d.o.append(f'<polygon points="{pts} {X(rows[-1][0]):.1f},{PB} {X(rows[0][0]):.1f},{PB}" fill="{ACC}" opacity="0.08"/>')
d.o.append(f'<polyline points="{pts}" fill="none" stroke="{ACC}" stroke-width="1.8" stroke-linejoin="round"/>')
for t, st, v in rows:
    d.o.append(f'<circle cx="{X(t):.1f}" cy="{Yv(v):.1f}" r="4" fill="{ACC}"/>')
# 상태 라벨 — 오렌지 꺾은선과 겹치지 않도록 좌우 여백 쪽으로 정렬
d.t(X(rows[0][0]), Yv(0) - 14, "Initializing", 10, MUTED, MONO, "start", 600)
d.t(X(rows[1][0]), Yv(0) - 30, "Initialized", 10, MUTED, MONO, "start", 600)
d.t(X(rows[2][0]) - 6, Yv(0) - 14, "Progressing", 10, INK, MONO, "end", 600)
d.t(X(rows[8][0]) + 6, Yv(0) - 14, "Promoting", 10, MUTED, MONO, "start", 600)
d.t(X(rows[9][0]) + 6, Yv(0) - 30, "Finalising", 10, MUTED, MONO, "start", 600)
d.t(X(rows[10][0]) - 6, Yv(0) - 46, "Succeeded", 10, INK, MONO, "end", 600)
# 인출선 — 라벨이 가리키는 점을 잇는다
for r, hgt in ((8, 18), (9, 34), (10, 50)):
    d.line(X(rows[r][0]), Yv(0) - 7, X(rows[r][0]), Yv(0) - hgt - 2, SOFT, 0.8)
# 주석 — 빈 구간과 승격
gx = (X(rows[1][0]) + X(rows[2][0])) / 2
d.t(gx, Yv(35), "v2 배포를 기다림 · 7분 30초 (축 생략)", 13, SOFT, KR)
d.line(gx - 7, PB + 7, gx - 1, PB - 7, INK, 1.2)
d.line(gx + 1, PB + 7, gx + 7, PB - 7, INK, 1.2)
d.t(X(rows[7][0]) + 10, Yv(54), "maxWeight 50 → 승격", 13, ACC, KR, "start")
d.t(X(rows[9][0]), Yv(26), "승격 뒤 표시는 0 —", 13, MUTED, KR)
d.t(X(rows[9][0]), Yv(22.5), "전체가 새 버전", 13, MUTED, KR)
d.legend(552, [("canary 로 가는 트래픽 비율", ACC)])
d.save("05-01.flagger-weight.svg")

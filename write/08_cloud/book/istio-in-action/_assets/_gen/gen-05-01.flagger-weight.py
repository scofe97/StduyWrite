# 05-01 §3 Flagger 가 옮긴 카나리 가중치의 시간 추이 — 원문 5.3.1 의 kubectl get canary -w 출력 11행을 그대로.
# 본문: "Initialized 뒤 7분 남짓 비어 있는 구간은 v2 배포 전. Progressing 에 들어가면 45초마다 10%씩 올라 50%.
# Promoting·Finalising·Succeeded 로 넘어가며 표시 가중치는 0 으로 돌아온다 — canary 가 primary 로 승격."
# 타입 스펙: type-line — 시간에 따른 연속 추세. 점 11개(≤12), 시간축은 실제 타임스탬프 간격 그대로(등간격 금지),
#           y 축은 0 을 포함, 초점 시리즈 하나에만 점. 여백은 스펙(좌 80 · 하 60 · 상 40 · 우 40)을 제목 블록만큼 내려 적용.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 600
d = D(W, H, "ISTIO IN ACTION · 05-01 §3",
      "Flagger가 옮긴 카나리 가중치의 시간 추이",
      "2021-01-20 22:50:16 부터 23:04:41 까지 kubectl get canary catalog-release -w 가 찍은 11개 행. 가중치는 canary 로 가는 트래픽 비율(%).",
      "원문 출력의 타임스탬프를 그대로 x 축에 놓았습니다. 45초 구간 여섯 번(가중치 다섯 걸음) 뒤 승격")

rows = [("22:50:16", "Initializing", 0), ("22:51:11", "Initialized", 0), ("22:58:41", "Progressing", 0),
        ("22:59:26", "Progressing", 10), ("23:00:11", "Progressing", 20), ("23:00:56", "Progressing", 30),
        ("23:01:41", "Progressing", 40), ("23:02:26", "Progressing", 50), ("23:03:11", "Promoting", 0),
        ("23:03:56", "Finalising", 0), ("23:04:41", "Succeeded", 0)]
def sec(t):
    h, m, s = map(int, t.split(":")); return h * 3600 + m * 60 + s
t0, t1 = sec(rows[0][0]), sec(rows[-1][0])
PL, PR, PT, PB = 80, W - 40, 100, 480          # plot 영역 — 제목 블록 60px 만큼 내린 스펙 여백
def X(t): return PL + (sec(t) - t0) / (t1 - t0) * (PR - PL)
def Yv(v): return PB - v / 60 * (PB - PT)
# 그리드 0..60 step 10
for v in range(0, 61, 10):
    d.line(PL, Yv(v), PR, Yv(v), RULE, 0.8 if v else 1.0)
    d.t(PL - 10, Yv(v) + 4, f"{v}%", 9, SOFT, MONO, "end")
d.t(8, PT - 12, "canary 가중치 (%)", 9, SOFT, KR, "start")
# 시간 눈금 — 점마다
for t, st, v in rows:
    d.line(X(t), PB, X(t), PB + 6, RULE, 0.8)
# 라벨은 겹치지 않게 45초 걸음은 격줄로 위아래 교대
for i, (t, st, v) in enumerate(rows):
    d.t(X(t), PB + 20 if i % 2 == 0 else PB + 34, t, 8, MUTED, MONO)
# 폴리라인(초점) + 점
pts = " ".join(f"{X(t):.1f},{Yv(v):.1f}" for t, st, v in rows)
d.o.append(f'<polygon points="{pts} {X(rows[-1][0]):.1f},{PB} {X(rows[0][0]):.1f},{PB}" fill="{ACC}" opacity="0.08"/>')
d.o.append(f'<polyline points="{pts}" fill="none" stroke="{ACC}" stroke-width="1.8" stroke-linejoin="round"/>')
for t, st, v in rows:
    d.o.append(f'<circle cx="{X(t):.1f}" cy="{Yv(v):.1f}" r="4" fill="{ACC}"/>')
# 상태 라벨 — 같은 상태가 이어지는 구간은 한 번만
# 55초·45초 간격이라 이웃 라벨이 겹친다 — 세 단으로 엇갈려 올린다
lift = {"Initializing": 14, "Initialized": 28, "Progressing": 14, "Promoting": 14, "Finalising": 28, "Succeeded": 42}
last = None
for i, (t, st, v) in enumerate(rows):
    if st != last:
        base = Yv(v) if st != "Progressing" else Yv(0)
        anchor = "start" if i == 0 else ("end" if i == len(rows) - 1 else "middle")
        d.t(X(t), base - lift[st], st, 9, INK if st in ("Progressing", "Succeeded") else MUTED, MONO, anchor, 600)
        last = st
# 주석 — 빈 구간과 승격
d.t((X(rows[1][0]) + X(rows[2][0])) / 2, Yv(35), "v2 배포 전 · 7분 30초", 12, SOFT, KR)
d.t(X(rows[7][0]) + 8, Yv(55), "maxWeight 50 → 승격", 12, ACC, KR, "start")
d.t(X(rows[9][0]), Yv(25), "승격 뒤 표시는 0 —", 12, MUTED, KR)
d.t(X(rows[9][0]), Yv(15), "전체가 새 버전", 12, MUTED, KR)
d.legend(556, [("canary 로 가는 트래픽 비율", ACC)])
d.save("05-01.flagger-weight.svg")

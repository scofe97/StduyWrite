# 06-01 §4 중첩된 타임아웃과 실습의 0.5초.
# 본문: "위는 저자의 A·B·C 예시. 막대 길이가 곧 타임아웃 예산이고, 색이 붙은 A→B 의 1초가 먼저 끊긴다.
# 아래는 실습 — simple-backend 가 절반의 호출에 1초 지연을 넣는 상태에서 0.5초 타임아웃을 건다."
# 타입 스펙: type-gantt — 막대 길이가 곧 구간. 왼쪽 라벨 열 + 시간축, 국면(phase) 두 묶음, 초점 막대 하나.
#           축약: 시간축 단위가 주(week)가 아니라 초라서 눈금 라벨만 바꿨다. 부라벨은 라벨 열이 좁아
#           막대 오른쪽에 두었고, 의존 화살표는 v1 관례대로 그리지 않는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, BAD, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 540
d = D(W, H, "ISTIO IN ACTION · 06-01 §4",
      "중첩된 타임아웃과 실습의 0.5초",
      "위 묶음은 저자의 A·B·C 예시로, A→B 의 1초가 먼저 끊겨 B→C 의 2초는 발동하지 못한다. "
      "아래 묶음은 실습으로, 1초 지연을 넣은 백엔드에 0.5초 타임아웃을 걸어 응답이 HTTP 500 으로 끊긴다.",
      "가장 제한적인 타임아웃이 이깁니다. 그래서 엣지는 크게, 깊은 곳은 짧게 둡니다")

LX, TX, TW = 24, 200, 600     # 오른쪽에 부라벨 자리를 남기고 1s = 300px 로 통일
TMAX, AXIS_Y, ROWH = 2.0, 124, 40
P1_TOP, P2_TOP = 140, 320
def X(sec): return TX + sec / TMAX * TW
def row_y(top, i): return top + 28 + i * ROWH

for tick in [0, 0.5, 1.0, 1.5, 2.0]:
    d.line(X(tick), AXIS_Y - 6, X(tick), P2_TOP + 28 + 2 * ROWH, RULE, 0.8)
    d.t(X(tick), AXIS_Y - 12, f"{tick:g}s", 8, SOFT, MONO)
d.line(TX, AXIS_Y, TX + TW, AXIS_Y, RULE, 1.0)

def phase(top, rows, label):
    h = 28 + rows * ROWH + 12
    d.o.append(f'<rect x="{LX - 12}" y="{top}" width="{W - LX - 20}" height="{h}" rx="8" fill="rgba(245,245,245,0.02)" stroke="rgba(245,245,245,0.10)" stroke-width="0.8"/>')
    d.t(LX, top + 18, label, 11, SOFT, MONO, "start")

def bar(top, i, name, sub, start, end, focal=False, dashed=False):
    y = row_y(top, i)
    d.t(LX, y + 21, name, 11, ACC if focal else INK, KR, "start", 600)
    x0, w = X(start), X(end) - X(start)
    if focal:
        d.o.append(f'<rect x="{x0}" y="{y + 4}" width="{w}" height="24" rx="4" fill="{ACC}1F" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        dash = ' stroke-dasharray="4 3"' if dashed else ''
        d.o.append(f'<rect x="{x0}" y="{y + 4}" width="{w}" height="24" rx="4" fill="rgba(139,152,169,0.15)" stroke="{MUTED}" stroke-width="1"{dash}/>')
    d.t(x0 + w + 10, y + 21, sub, 11, ACC if focal else MUTED, MONO, "start")

phase(P1_TOP, 3, "저자의 예 — 중첩된 타임아웃")
bar(P1_TOP, 0, "A → B", "timeout 1s", 0, 1.0, focal=True)
bar(P1_TOP, 1, "B → C", "timeout 2s", 0, 2.0)
bar(P1_TOP, 2, "C 의 실제 처리", "얼마가 걸리든", 0, 2.0, dashed=True)
phase(P2_TOP, 2, "실습 — 1초 지연에 0.5초 타임아웃")
bar(P2_TOP, 0, "백엔드 처리", "50% 에 1s 지연", 0, 1.0)
bar(P2_TOP, 1, "요청 타임아웃", "0.5s → HTTP 500", 0, 0.5)

d.line(X(1.0), row_y(P1_TOP, 0) + 2, X(1.0), row_y(P1_TOP, 2) + 34, ACC, 1.2, "4 3")
d.t(X(1.0) + 10, row_y(P1_TOP, 2) + 48, "여기서 끊긴다 — B→C 의 2초는 발동하지 못한다", 11, ACC, KR, "start")
d.line(X(0.5), row_y(P2_TOP, 0) + 2, X(0.5), row_y(P2_TOP, 1) + 34, BAD, 1.2, "4 3")
d.t(X(0.5) + 10, row_y(P2_TOP, 1) + 48, "0.5s 에 HTTP 500 — 느린 응답이 빠른 실패가 된다", 11, BAD, KR, "start")

d.legend(P2_TOP + 28 + 2 * ROWH + 56, [("먼저 끊기는 타임아웃", ACC), ("타임아웃이 만든 실패", BAD)])
d.save("06-01.timeout-budget.svg")

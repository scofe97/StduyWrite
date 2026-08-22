# 06-02 §3 — 재시작 사이의 지연은 두 배씩 늘다가 5분에서 멈춘다
# 본문: "첫 종료 때는 즉시 재시작되지만, 다음번에는 10초를 기다린 뒤 재시작합니다. 이 지연은
#        이후 종료마다 20초·40초·80초·160초로 두 배씩 늘어나고, 그 뒤로는 5분으로 유지됩니다."
#       "10분 동안 정상적으로 돌면 0 으로 리셋된다"
# 타입 스펙: type-bar.md — 회차별 '한 값'을 비교하는 것이 요점이므로 세로 막대. 옛 판은
#           컨테이너 그림을 늘어놓아 지연이 두 배가 되는 것을 눈으로 못 재게 했다.
#           막대 길이가 곧 초라서 두 배와 상한이 눈금으로 읽힌다.
#           관례: 막대 폭은 pitch 의 50% 이상 · y 눈금선 4~6개 · focal 막대 1개.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO
import ddx

W, H = 1000, 556
d = D(W, H, "KUBERNETES IN ACTION · 06-02",
      "재시작 지연은 두 배씩 늘다가 5분에서 멈춘다",
      "첫 종료는 즉시 재시작되고 그다음부터 10초에서 시작해 매번 두 배가 된다. 300초에서 상한에 "
      "닿고, 컨테이너가 10분 동안 정상으로 돌면 지연은 0 으로 리셋된다.",
      lead="이 대기 상태가 CrashLoopBackOff 다 — state 는 Waiting, reason 이 그 이름이다")

BASE, TOP = 400, 176            # y — 0초와 300초
X0, PITCH, BARW = 128, 104, 72
DELAYS = [0, 10, 20, 40, 80, 160, 300, 300]
CAP = 300
FOCAL = 6                        # 상한에 처음 닿는 회차

ddx.band(d, 104, 500, "지연이 두 배가 되는 것과 5분에서 멈추는 것, 둘 다 막대 길이로 읽힌다")

def y_of(sec):
    return BASE - round(sec / CAP * (BASE - TOP))

for sec in (0, 60, 120, 180, 240, 300):
    y = y_of(sec)
    d.line(120, y, 960, y, RULE, 0.8)
    d.t(112, y + 4, f"{sec}s", 9, SOFT, MONO, "end")
d.line(120, TOP, 120, BASE, RULE, 1.0)
d.line(120, BASE, 960, BASE, RULE, 1.0)

for i, sec in enumerate(DELAYS):
    cx = X0 + BARW // 2 + i * PITCH
    focal = i == FOCAL
    c = ACC if focal else INFO
    if sec == 0:
        d.chip(cx, BASE - 16, "즉시", c, 11)
    else:
        y = y_of(sec)
        d.o.append(f'<rect x="{cx-BARW//2}" y="{y}" width="{BARW}" height="{BASE-y}" rx="4" '
                   f'fill="{c}{"22" if focal else "18"}" stroke="{c}" '
                   f'stroke-width="{1.4 if focal else 1.0}"/>')
        d.t(cx, y - 8, f"{sec}s", 9, c, MONO)
    d.t(cx, 424, f"{i+1}회차", 11, ACC if focal else MUTED, KR, "middle", 600)

d.line(120, TOP, 960, TOP, MUTED, 1.2, "6 5")
# 상한선 라벨을 오른쪽 끝에 두면 상한에 닿은 두 막대의 값 라벨(908·804)과 같은 행에서 겹친다.
# 왼쪽 끝은 첫 회차가 '즉시' 칩이라 위가 비어 있다 — 거기에 둔다.
d.t(128, TOP - 8, "300s · 5분 상한", 10, MUTED, MONO, "start")

# 리셋 — 마지막 회차에서 첫 회차로 되돌아간다
RY = 448
LAST = X0 + BARW // 2 + (len(DELAYS) - 1) * PITCH
FIRST = X0 + BARW // 2
d.path(f"M {LAST} 434 L {LAST} {RY} L {FIRST} {RY} L {FIRST} 434", MUTED, 1.3, m="ar", dash="6 5")
d.chip((FIRST + LAST) // 2, RY, "10분 정상 동작 → 지연 0 으로 리셋", MUTED, 11)

d.t(36, 478, "최악의 경우 컨테이너는 5분 동안 시작하지 못한다 — 이미지 pull 실패의 재시도에도 "
             "같은 백오프가 적용된다", 12, MUTED, KR, "start")
d.legend(516, [("재시작 전 대기", INFO), ("상한에 처음 닿는 회차", ACC)])
d.save("06-02-exponential-backoff.svg")
print("ok exponential-backoff")

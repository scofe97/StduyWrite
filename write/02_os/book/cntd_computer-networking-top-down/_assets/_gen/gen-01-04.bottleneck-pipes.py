# 01-04 §4 — 처리량은 경로 위 가장 좁은 링크의 폭이고, 그 링크를 다른 흐름과 나누면 병목이 옮겨 간다.
# 값 출처: 원문 1.4.4 — Rs 2 Mbps · Rc 1 Mbps → min 1 Mbps, 코어 공유 링크 5 Mbps 를 열이 나눠 500 kbps.
# 두 경우를 위아래 두 장의 연결된 Sankey 로 둔다. 띠 굵기가 초당 흐르는 양이고, k = 24px / Mbps 로 한 장 안에서 같다.
# 타입 스펙: type-sankey — 3열, 막대 폭 12, 채운 리본(양쪽 제어점이 열 중간 x), 화살촉 없음, 강조 경로 하나.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, RULE, KR, MONO

W, H = 1000, 640
K = 24                              # px per Mbps
X = [220, 500, 780]                 # 열의 막대 x
BW = 12

d = D(W, H, "COMPUTER NETWORKING TOP-DOWN · 01-04 §4",
      "처리량은 가장 좁은 곳의 폭입니다",
      "원문 1.4.4 의 두 예. 링크 둘이면 좁은 쪽 1 Mbps 가 처리량이고, 코어 링크 5 Mbps 를 열이 나누면 내 몫 0.5 Mbps 가 접속 링크 1 Mbps 보다 좁아져 병목이 코어로 옮겨 간다.",
      "띠의 굵기가 초당 흐르는 양입니다. 위아래 그림의 눈금은 같습니다")

def ribbon(x0, y0, h0, x1, y1, h1, c, op):
    mx = (x0 + x1) / 2
    d.o.append(f'<path d="M {x0} {y0} C {mx} {y0} {mx} {y1} {x1} {y1} L {x1} {y1 + h1} C {mx} {y1 + h1} {mx} {y0 + h0} {x0} {y0 + h0} Z" fill="{c}" opacity="{op}"/>')

def bar(col, y, h):
    d.o.append(f'<rect x="{X[col]}" y="{y}" width="{BW}" height="{h}" fill="{INK}"/>')

def _q(t): return (11, KR) if any("가" <= c <= "힣" for c in t) else (9, MONO)
def label(col, y, h, name, qty, above=None):
    qs, qf = _q(qty)
    if col == 0:
        d.t(X[0] - 10, y + h / 2 + 4, name, 12, INK, KR, "end", 600)
        d.t(X[0] - 10, y + h / 2 + 19, qty, qs, MUTED, qf, "end")
    elif col == 2:
        d.t(X[2] + BW + 10, y + h / 2 + 4, name, 12, INK, KR, "start", 600)
        d.t(X[2] + BW + 10, y + h / 2 + 19, qty, qs, MUTED, qf, "start")
    else:
        cy = above if above is not None else y - 20
        d.t(X[1] + BW / 2, cy, name, 12, INK, KR, "middle", 600)
        d.t(X[1] + BW / 2, cy + 14, qty, qs, MUTED, qf)

def headers(y):
    for i, h in enumerate(("보내는 쪽 링크", "가운데 링크", "받는 쪽")):
        d.t(X[i] + BW / 2, y, h, 11, SOFT, KR, "middle")

# ── 위: 링크 둘, 다른 흐름 없음 ──
yA = 186
d.t(24, 132, "링크 둘만 있을 때 — 처리량은 좁은 쪽", 12, INK, KR, "start", 600)
headers(150)
rs, rc, spare = 2 * K, 1 * K, 1 * K
y_rc, y_sp = yA, yA + rc + 16
ribbon(X[0] + BW, yA + rc, spare, X[1], y_sp, spare, MUTED, "0.18")      # Rs 의 남는 폭
ribbon(X[1] + BW, y_sp, spare, X[2], y_sp, spare, MUTED, "0.18")
ribbon(X[0] + BW, yA, rc, X[1], y_rc, rc, ACC, "0.28")                    # 실제 흐름
ribbon(X[1] + BW, y_rc, rc, X[2], y_rc, rc, ACC, "0.28")
bar(0, yA, rs); bar(1, y_rc, rc); bar(1, y_sp, spare); bar(2, y_rc, rc); bar(2, y_sp, spare)
label(0, yA, rs, "서버 링크 Rs", "2 Mbps")
label(1, y_rc, rc, "접속 링크 Rc", "1 Mbps", above=y_rc - 18)
label(1, y_sp, spare, "Rs 의 남는 폭", "1 Mbps 놀림", above=y_sp + spare + 20)
label(2, y_rc, rc, "클라이언트 처리량", "min{2, 1} = 1 Mbps")
label(2, y_sp, spare, "쓰이지 않음", "1 Mbps")

# ── 아래: 코어 공유 링크를 열이 나눔 ──
yB = 362
d.t(24, 306, "코어 링크를 열이 나눌 때 — 병목이 코어로 옮겨 감", 12, INK, KR, "start", 600)
headers(324)
R, mine, others = 5 * K, int(0.5 * K), int(4.5 * K)
y_me, y_ot = yB, yB + mine + 16
ribbon(X[0] + BW, yB + mine, others, X[1], y_ot, others, MUTED, "0.18")
ribbon(X[1] + BW, y_ot, others, X[2], y_ot, others, MUTED, "0.18")
ribbon(X[0] + BW, yB, mine, X[1], y_me, mine, ACC, "0.28")
ribbon(X[1] + BW, y_me, mine, X[2], y_me, mine, ACC, "0.28")
bar(0, yB, R); bar(1, y_me, mine); bar(1, y_ot, others); bar(2, y_me, mine); bar(2, y_ot, others)
label(0, yB, R, "코어 공유 링크 R", "5 Mbps · 다운로드 열이 지남")
label(1, y_me, mine, "내 다운로드 몫", "5 ÷ 10 = 0.5 Mbps", above=y_me - 18)
label(1, y_ot, others, "다른 아홉의 몫", "4.5 Mbps", above=y_ot + others + 20)
label(2, y_me, mine, "내 접속 링크 Rc 에 0.5 만 흐름", "Rc 1 Mbps 의 절반")
label(2, y_ot, others, "다른 클라이언트 아홉", "각 0.5 Mbps")

d.legend(H - 44, [("실제 흐름 — 병목의 폭", ACC), ("놀거나 남에게 간 폭", MUTED)])
d.save("01-04.bottleneck-pipes.svg")
print("ok bottleneck-pipes")

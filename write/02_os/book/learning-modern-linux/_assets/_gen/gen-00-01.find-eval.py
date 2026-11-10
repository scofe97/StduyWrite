# 00-01 §3 — find 가 파일 하나를 놓고 조건을 왼쪽부터 평가하다가 거짓에서 멈추는 모습.
# 근거(find(1), GNU findutils 4.9.0): "Two expressions in a row are taken to be joined with an
#       implied -a; expr2 is not evaluated if expr1 is false." · "If no expression is given, the
#       expression -print is used."
# 실행(debian:12): find logs -type f -name '*.log' -mtime +30 -print  →  logs/app.log
#       logs/app.gz 는 같은 40일 전 파일인데 -name 에서 거짓이 되어 뒤 조건에 닿지 않는다.
# 타입 스펙: type-flowchart — 같은 규칙 줄을 두 입력이 지나가는 평가 추적 두 줄. 칸마다 PASS · FAIL ·
#           NOT REACHED 를 글자로 적고, accent 는 두 줄이 처음 갈리는 조건 하나(-name).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, BAD, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 452
d = D(W, H, "LEARNING MODERN LINUX · 00-01 §3",
      "find 는 조건을 왼쪽부터 평가하다 거짓에서 멈춘다",
      "find logs -type f -name '*.log' -mtime +30 -print 를 두 파일에 적용한 평가 추적. "
      "logs/app.log 는 네 조건을 모두 지나 출력되고, logs/app.gz 는 -name 에서 거짓이 되어 "
      "-mtime 과 -print 에 닿지 않는다.",
      "find logs -type f -name '*.log' -mtime +30 -print")

LX, LW = 24, 172
CX = [216, 372, 528, 684]
CW = 136
HY, HH = 104, 44
rules = [("-type f", "조건 1"), ("-name '*.log'", "조건 2"), ("-mtime +30", "조건 3"), ("-print", "동작")]

d.t(LX, HY + 26, "평가 순서", 12, MUTED, KR, "start")
for i, (r, sub) in enumerate(rules):
    x = CX[i]
    d.box(x, HY, CW, HH, PAPER2, RULE, 1.0, 6)
    d.t(x + CW / 2, HY + 20, r, 13, INK, MONO, "middle", 600)
    d.t(x + CW / 2, HY + 36, sub, 12, MUTED)
    if i < 3:
        d.arrow([(x + CW + 2, HY + 22), (CX[i + 1] - 4, HY + 22)], MUTED, "ar", 1.4)

RY = [176, 264]
RH = 64
traces = [
    ("logs/app.log", "일반 파일 · 40일 전",
     [("PASS", "일반 파일", OK), ("PASS", "이름 끝 .log", OK), ("PASS", "40일 > 30일", OK),
      ("출력", "logs/app.log", OK)]),
    ("logs/app.gz", "일반 파일 · 40일 전",
     [("PASS", "일반 파일", OK), ("FAIL", "이름 끝 .gz", BAD), ("NOT REACHED", "평가 안 함", SOFT),
      ("NOT REACHED", "출력 없음", SOFT)]),
]

# 첫 갈림(-name 열)을 두 줄에 걸쳐 감싼다
d.o.append(f'<rect x="{CX[1] - 8}" y="{RY[0] - 8}" width="{CW + 16}" height="{RY[1] + RH - RY[0] + 16}" '
           f'rx="8" fill="{ACC}0D" stroke="{ACC}" stroke-width="1.4"/>')

for (name, attr, cells), y in zip(traces, RY):
    d.box(LX, y, LW, RH, PAPER2, RULE, 1.0, 6)
    d.t(LX + LW / 2, y + 28, name, 13, INK, MONO, "middle", 600)
    d.t(LX + LW / 2, y + 48, attr, 12, MUTED)
    for i, (st, why, c) in enumerate(cells):
        x = CX[i]
        if c is SOFT:
            d.o.append(f'<rect x="{x}" y="{y}" width="{CW}" height="{RH}" rx="6" fill="{PAPER}" '
                       f'stroke="{SOFT}" stroke-width="1" stroke-dasharray="4 4"/>')
        else:
            d.tone(x, y, CW, RH, c)
        d.t(x + CW / 2, y + 28, st, 12, c if c is not SOFT else MUTED, MONO, "middle", 600)
        d.t(x + CW / 2, y + 48, why, 12, INK if c is not SOFT else MUTED,
            MONO if "logs/" in why or ".log" in why or ".gz" in why else KR)
        if i < 3 and c is OK:
            m = "ok"
            d.arrow([(x + CW + 2, y + RH / 2), (CX[i + 1] - 4, y + RH / 2)], OK, m, 1.4)

d.t(CX[1] + CW / 2, RY[1] + RH + 28, "두 파일이 처음 갈리는 조건", 12, ACC, KR, "middle", 600)
d.t(LX, 388, "거짓이 나온 뒤의 조건은 평가하지 않음 · -print 도 같은 줄에 선 식의 하나", 12, MUTED, KR, "start")

d.legend(408, [("참", OK), ("거짓", BAD), ("닿지 않음", SOFT), ("첫 갈림", ACC)])
d.save("00-01.find-eval.svg")
print("ok 00-01.find-eval.svg")

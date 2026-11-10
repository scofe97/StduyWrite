# 03-02 §4 「정렬로 같은 줄을 붙여 세기」 — IP 일곱 줄이 정렬되고 세어져 순위가 되는 파이프라인.
# 근거(책 밖 보강): GNU coreutils "uniq invocation" — "repeated input lines are detected only if they are
#       adjacent". <https://www.gnu.org/software/coreutils/manual/coreutils.html#uniq-invocation>
# 실측(Debian 12, coreutils 9.1): access.log 첫 칸 순서 .7 .9 .7 .3 .7 .9 .7
#       sort | uniq -c → 1 10.0.0.3 · 4 10.0.0.7 · 2 10.0.0.9
#       sort | uniq -c | sort -rn → 4 10.0.0.7 · 2 10.0.0.9 · 1 10.0.0.3
#       uniq -c (sort 없이) → 일곱 줄 모두 1
# 타입 스펙: type-data-flow — 열마다 파이프를 지난 실제 값이 놓이고, 열 사이 화살표 위 칩이 그 값을 바꾼
#           명령이다. 축약: 역할 lane 없이 단계 열 넷만 쓰고, 아래 띠에 sort 를 뺀 경로의 값을 둔다.
#           coral 은 같은 줄을 합치는 uniq -c 열 하나.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, BAD, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 500
d = D(W, H, "LEARNING MODERN LINUX · 03-02 §4",
      "IP 일곱 줄이 정렬되고 세어져 순위가 된다",
      "grep -oE '^[0-9.]+' access.log | sort | uniq -c | sort -rn 의 각 단계를 지난 값. sort 가 같은 IP 를 "
      "이웃에 모아야 uniq -c 가 한 덩이로 센다.",
      "uniq 는 이웃한 같은 줄만 합칩니다")

CXL = [32, 252, 472, 692]
CWD = 156
HEAD = ["입력 순서", "sort 뒤", "uniq -c 뒤", "sort -rn 뒤"]
CMDS = ["sort", "uniq -c", "sort -rn"]
RY0, RH = 148, 28

inp = ["10.0.0.7", "10.0.0.9", "10.0.0.7", "10.0.0.3", "10.0.0.7", "10.0.0.9", "10.0.0.7"]
srt = sorted(inp, key=lambda s: int(s.split(".")[-1]))
groups = [("1", "10.0.0.3", 0, 1), ("4", "10.0.0.7", 1, 4), ("2", "10.0.0.9", 5, 2)]
ranked = [("4", "10.0.0.7"), ("2", "10.0.0.9"), ("1", "10.0.0.3")]
TONE = {"10.0.0.3": SOFT, "10.0.0.7": ACC, "10.0.0.9": INFO}

for i, h in enumerate(HEAD):
    d.t(CXL[i] + CWD / 2, 132, h, 12, ACC if i == 2 else MUTED, KR, "middle", 600)

# 열 사이 화살표와 명령 칩
AY = RY0 + RH * 3.5
for i, c in enumerate(CMDS):
    x1 = CXL[i] + CWD + 4
    x2 = CXL[i + 1] - 6
    d.arrow([(x1, AY), (x2, AY)], ACC if i == 1 else MUTED, "acc" if i == 1 else "ar", 1.4)
    d.t((x1 + x2) / 2, AY - 10, c, 11, ACC if i == 1 else MUTED, MONO, "middle", 600)

# 1열·2열: 일곱 줄
for col, vals in ((0, inp), (1, srt)):
    for r, v in enumerate(vals):
        y = RY0 + r * RH
        d.box(CXL[col], y + 2, CWD, RH - 4, PAPER2, RULE, 0.8, 4)
        d.t(CXL[col] + CWD / 2, y + 19, v, 12, TONE[v] if col == 1 else INK, MONO)

# 3열: 이웃 덩이마다 한 칸 (높이 = 덩이 줄 수)
for cnt, ip, start, n in groups:
    y = RY0 + start * RH
    h = n * RH
    d.o.append(f'<rect x="{CXL[2]}" y="{y + 2}" width="{CWD}" height="{h - 4}" rx="5" '
               f'fill="{TONE[ip]}12" stroke="{TONE[ip]}" stroke-width="1.2"/>')
    d.t(CXL[2] + 20, y + h / 2 + 5, cnt, 14, TONE[ip], MONO, "start", 600)
    d.t(CXL[2] + CWD - 16, y + h / 2 + 5, ip, 12, INK, MONO, "end")

# 4열: 개수순
for r, (cnt, ip) in enumerate(ranked):
    y = RY0 + r * RH
    d.box(CXL[3], y + 2, CWD, RH - 4, PAPER2, RULE, 0.8, 4)
    d.t(CXL[3] + 20, y + 19, cnt, 13, TONE[ip], MONO, "start", 600)
    d.t(CXL[3] + CWD - 16, y + 19, ip, 12, INK, MONO, "end")

# sort 를 뺀 경로
SY = 368
d.tone(24, SY, W - 48, 64, BAD, op="0c")
d.t(40, SY + 26, "sort 없이 uniq -c", 12, BAD, KR, "start", 600)
d.t(40, SY + 46, "일곱 줄 모두 1", 11, MUTED, KR, "start")
x = 196
for v in inp:
    d.chip(x + 41, SY + 32, "1 " + v, SOFT, 11, 5)
    x += 92

d.legend(452, [("10.0.0.7 · 4줄", ACC), ("10.0.0.9 · 2줄", INFO), ("10.0.0.3 · 1줄", SOFT),
               ("놓치는 경로", BAD)])
d.save("03-02.count-pipeline.svg")
print("ok 03-02.count-pipeline")

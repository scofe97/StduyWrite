# 03-02 §3 「cut 과 awk 로 열 뽑기」·「awk 비교가 문자열로 떨어질 때」 — df 한 줄을 칸으로 나눠 견주기.
# 근거(책 밖 보강): GNU awk 매뉴얼
#       "Fields are separated by runs of whitespace" (Field-Separators),
#       숫자 꼴인 입력 칸만 strnum 이고 한쪽이 STRING 이면 문자열 비교 (Variable-Typing),
#       "A string is converted to a number by interpreting any numeric prefix" (Strings-And-Numbers).
# 실측(Debian 12, mawk 1.3.4 · gawk 5.2.1 동일):
#       awk 'NR>1 && $5 >= 90 {print $6, $5}' df.txt   → /var/log 95%
#       awk 'NR>1 && $5+0 >= 90 {print $6, $5}' df.txt → /data 100% · /var/log 95%
# 타입 스펙: type-swimlane — 레인 둘(문자열 비교 · 숫자 비교)이 같은 단계 열(비교식 → 견주는 값 → 결과)을
#           지나며, 위쪽 띠는 두 레인이 함께 쓰는 입력 한 줄을 칸으로 나눈 것. coral 은 고친 레인의 결과 하나.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, BAD, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 460
d = D(W, H, "LEARNING MODERN LINUX · 03-02 §3",
      "awk 가 df 한 줄을 칸으로 나눠 견주는 두 방식",
      "df.txt 3행을 공백 묶음마다 끊어 $1~$6 으로 나눈 뒤, 다섯째 칸을 90 과 견주는 두 식을 나란히 놓은 것. "
      "% 가 붙은 칸은 문자열이라 그대로 견주면 앞 글자끼리 비교한다.",
      "같은 칸도 +0 을 붙이면 숫자로 견줍니다")

# 입력 한 줄 → 칸
d.t(32, 108, "df.txt 3행 · NR=3 · NF=6", 12, MUTED, KR, "start", 600)
fields = [("$1", "/dev/sdb1", 136), ("$2", "103081248", 128), ("$3", "97927188", 120),
          ("$4", "0", 64), ("$5", "100%", 104), ("$6", "/data", 104)]
x = 32
FY = 140
for name, val, w in fields:
    focal = (name == "$5")
    if focal:
        d.tone(x, FY, w, 40, INFO, op="14")
    else:
        d.box(x, FY, w, 40, PAPER2, RULE, 0.9, 4)
    d.t(x + w / 2, FY - 8, name, 11, INFO if focal else SOFT, MONO, "middle", 600)
    d.t(x + w / 2, FY + 25, val, 13, INK, MONO, "middle", 600 if focal else 400)
    x += w + 8
d.t(x + 8, FY + 25, "공백 묶음 = 구분자 하나", 11, MUTED, KR, "start")

# 레인
LX, LW = 24, 152
COLS = [(192, 208), (416, 216), (648, 208)]
HEAD = ["비교식", "견주는 두 값", "결과"]
for (cx, cw), h in zip(COLS, HEAD):
    d.t(cx + cw / 2, 220, h, 12, MUTED, KR, "middle", 600)
d.line(LX, 228, W - 24, 228, RULE, 1)

lanes = [
    ("문자열 비교", "칸 그대로", "$5 >= 90", ("\"100%\" 대 \"90\"", "첫 글자 1 < 9"),
     ("거짓", "출력 없음"), BAD, False),
    ("숫자 비교", "+0 으로 변환", "$5+0 >= 90", ("100 대 90", "앞머리 숫자만 읽음"),
     ("참", "/data 100%"), ACC, True),
]
LY = [240, 328]
for (lname, lsub, expr, cmp_, res, col, focal), y in zip(lanes, LY):
    d.t(LX + 8, y + 32, lname, 13, INK, KR, "start", 600)
    d.t(LX + 8, y + 52, lsub, 11, MUTED, KR, "start")
    # 연결선 먼저
    for i in range(2):
        x1 = COLS[i][0] + COLS[i][1]
        x2 = COLS[i + 1][0]
        d.arrow([(x1, y + 40), (x2 - 2, y + 40)], MUTED, "ar", 1.2)
    c0, c1, c2 = COLS
    d.box(c0[0], y + 12, c0[1], 56, PAPER2, MUTED, 1.0, 6)
    d.t(c0[0] + c0[1] / 2, y + 45, expr, 14, INK, MONO, "middle", 600)
    d.box(c1[0], y + 12, c1[1], 56, PAPER2, RULE, 0.9, 6)
    d.t(c1[0] + c1[1] / 2, y + 36, cmp_[0], 13, INK, MONO, "middle")
    d.t(c1[0] + c1[1] / 2, y + 56, cmp_[1], 11, MUTED, KR)
    if focal:
        d.o.append(f'<rect x="{c2[0]}" y="{y + 12}" width="{c2[1]}" height="56" rx="6" '
                   f'fill="{ACC}14" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.tone(c2[0], y + 12, c2[1], 56, col, op="10")
    d.t(c2[0] + 20, y + 45, res[0], 13, ACC if focal else col, KR, "start", 600)
    d.t(c2[0] + c2[1] - 20, y + 45, res[1], 13, INK if focal else SOFT,
        MONO if res[1].isascii() else KR, "end", 600 if focal else 400)
d.line(LX, 320, W - 24, 320, RULE, 0.8)

d.legend(412, [("견주는 칸", INFO), ("놓치는 결과", BAD), ("고친 식의 결과", ACC)])
d.save("03-02.awk-record.svg")
print("ok 03-02.awk-record")

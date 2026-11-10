# 00-01 §3 — find 가 내보낸 바이트를 xargs 가 어디서 끊어 인자로 만드는가.
# 근거(xargs(1), findutils 4.9.0): 입력 항목은 "delimited by blanks ... or newlines". "-0 ... Input
#       items are terminated by a null character instead of by whitespace". find(1) -print0: "print the
#       full file name on the standard output, followed by a null character".
# 실행(debian:12, 파일 'old report.gz' · 'plain.gz'):
#       find . -name '*.gz' | od -c            → ./old report.gz\n./plain.gz\n
#       find . -name '*.gz' | xargs ls -l      → ls: cannot access './old' / 'report.gz'
#       find . -name '*.gz' -print0 | xargs -0 ls -l → 두 파일 모두 나열
# 타입 스펙: type-data-flow — 바이트 열이 구분자에서 끊겨 인자 목록이 되고 명령에 닿는 두 갈래.
#           accent 는 이름 하나를 둘로 쪼개는 공백 한 바이트.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, BAD, PAPER, PAPER2, RULE, KR, MONO

W, H = 960, 396
d = D(W, H, "LEARNING MODERN LINUX · 00-01 §3",
      "xargs 는 구분자에서 이름을 끊는다",
      "find 의 출력 바이트가 xargs 를 지나 ls 의 인자가 되는 두 갈래. 줄바꿈으로 끝낸 출력은 공백에서도 "
      "끊겨 old report.gz 가 ./old 와 report.gz 두 인자로 갈라지고, 널 바이트로 끝낸 출력은 널에서만 "
      "끊겨 이름이 온전히 넘어간다.",
      "파일 둘: 'old report.gz' · 'plain.gz'")

d.t(32, 108, "find 출력 바이트", 13, MUTED, KR, "start")
d.t(432, 108, "xargs 가 만든 인자", 13, MUTED, KR, "start")
d.t(736, 108, "ls 결과", 13, MUTED, KR, "start")


def strip(x, y, cells):
    for txt, w, kind in cells:
        if kind == "cut":
            d.tone(x, y, w, 32, ACC, 4, "33", 1.4)
            d.t(x + w / 2, y + 21, txt, 13, ACC, KR, "middle", 600)
        elif kind == "sep":
            d.tone(x, y, w, 32, MUTED, 4, "22", 1.0)
            d.t(x + w / 2, y + 21, txt, 12, MUTED, MONO, "middle", 600)
        elif kind == "nul":
            d.tone(x, y, w, 32, OK, 4, "22", 1.2)
            d.t(x + w / 2, y + 21, txt, 12, OK, MONO, "middle", 600)
        else:
            d.box(x, y, w, 32, PAPER2, RULE, 1.0, 4)
            d.t(x + w / 2, y + 21, txt, 12, INK, MONO)
        x += w
    return x


def args(x, y, items, c):
    for txt, w in items:
        d.tone(x, y, w, 32, c, 4, "14", 1.1)
        d.t(x + w / 2, y + 21, txt, 12, INK, MONO)
        x += w + 8
    return x - 8


# 갈래 1: -print | xargs
Y1 = 152
d.t(32, Y1 - 12, "find . -name '*.gz' | xargs ls -l", 12, INFO, MONO, "start", 600)
e = strip(32, Y1, [("./old", 56, ""), ("공백", 40, "cut"), ("report.gz", 84, ""), ("\\n", 32, "sep"),
                   ("./plain.gz", 92, ""), ("\\n", 32, "sep")])
d.arrow([(e + 8, Y1 + 16), (424, Y1 + 16)], MUTED, "ar", 1.4)
a = args(432, Y1, [("./old", 56), ("report.gz", 84), ("./plain.gz", 92)], BAD)
d.arrow([(a + 8, Y1 + 16), (728, Y1 + 16)], MUTED, "ar", 1.4)
d.tone(736, Y1 - 8, 200, 48, BAD, 6)
d.t(836, Y1 + 12, "cannot access './old'", 12, BAD, MONO)
d.t(836, Y1 + 30, "cannot access 'report.gz'", 12, BAD, MONO)
d.t(32, Y1 + 56, "공백 · 줄바꿈 모두 경계", 13, MUTED, KR, "start")
d.t(432, Y1 + 56, "인자 3개 · 없는 이름 둘", 13, MUTED, KR, "start")

d.line(24, 232, W - 24, 232, RULE, 0.8)

# 갈래 2: -print0 | xargs -0
Y2 = 276
d.t(32, Y2 - 12, "find . -name '*.gz' -print0 | xargs -0 ls -l", 12, INFO, MONO, "start", 600)
e = strip(32, Y2, [("./old report.gz", 128, ""), ("\\0", 32, "nul"), ("./plain.gz", 92, ""), ("\\0", 32, "nul")])
d.arrow([(e + 8, Y2 + 16), (424, Y2 + 16)], MUTED, "ar", 1.4)
a = args(432, Y2, [("./old report.gz", 128), ("./plain.gz", 92)], OK)
d.arrow([(a + 8, Y2 + 16), (728, Y2 + 16)], MUTED, "ar", 1.4)
d.tone(736, Y2 - 8, 200, 48, OK, 6)
d.t(836, Y2 + 12, "./old report.gz", 12, OK, MONO)
d.t(836, Y2 + 30, "./plain.gz", 12, OK, MONO)
d.t(32, Y2 + 56, "널 바이트만 경계", 13, MUTED, KR, "start")
d.t(432, Y2 + 56, "인자 2개 · 이름 그대로", 13, MUTED, KR, "start")

d.legend(352, [("이름을 쪼개는 공백", ACC), ("줄바꿈", MUTED), ("널 바이트", OK), ("실패", BAD), ("명령", INFO)])
d.save("00-01.find-handoff.svg")
print("ok 00-01.find-handoff.svg")

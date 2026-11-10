# 03-02 §4 「xargs 로 입력을 인자로 바꾸기」 — 입력 다섯 줄이 인자 둘씩 묶여 echo 세 번이 된다.
# 근거(책 밖 보강): xargs(1) — "-n max-args: Use at most max-args arguments per command line",
#       "-t: Print the command line on the standard error output before executing it",
#       기본 명령은 echo. <https://man7.org/linux/man-pages/man1/xargs.1.html>
# 실측(Debian 12, findutils 4.9.0):
#       printf 'a\nb\nc\nd\ne\n' | xargs -t -n 2 echo → echo a b / a b / echo c d / c d / echo e / e
#       printf 'a\nb\nc\nd\ne\n' | xargs echo → a b c d e (한 번)
# 타입 스펙: type-tree — 뿌리(xargs) 아래로 실행 회차가 갈리고 회차마다 출력 잎이 하나씩 달린다.
#           연결선은 직각 버스, coral 은 뿌리 하나.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 552
d = D(W, H, "LEARNING MODERN LINUX · 03-02 §4",
      "xargs 가 입력 다섯 줄을 두 개씩 묶어 echo 를 세 번 실행",
      "표준 입력의 a~e 다섯 줄을 xargs -t -n 2 echo 가 인자로 바꾸는 모양. 한 번 실행에 인자를 둘까지 붙이고, "
      "-t 가 실행할 명령 줄을 먼저 찍는다.",
      "인자 묶음 하나가 실행 한 번입니다")

CX = 440
# 입력
d.box(CX - 160, 100, 320, 44, PAPER2, RULE, 0.9, 6)
d.t(CX - 144, 127, "stdin", 11, SOFT, MONO, "start", 600)
d.t(CX + 144, 127, "a · b · c · d · e", 13, INK, MONO, "end")
d.arrow([(CX, 144), (CX, 174)], MUTED, "ar", 1.3)

# 뿌리
RY, RHt = 176, 52
d.o.append(f'<rect x="{CX - 120}" y="{RY}" width="240" height="{RHt}" rx="6" '
           f'fill="{ACC}14" stroke="{ACC}" stroke-width="1.4"/>')
d.t(CX, RY + 24, "xargs -t -n 2 echo", 13, ACC, MONO, "middle", 600)
d.t(CX, RY + 42, "인자 2개씩 끊기", 12, MUTED, KR)

KX = [200, 440, 680]
KW, KY, KH = 176, 276, 52
BUS = 252
# 연결선 먼저 (직각 버스)
d.line(CX, RY + RHt, CX, BUS, MUTED, 1.0)
d.line(KX[0], BUS, KX[2], BUS, MUTED, 1.0)
for kx in KX:
    d.arrow([(kx, BUS), (kx, KY - 2)], MUTED, "ar", 1.0)
    d.arrow([(kx, KY + KH), (kx, 370)], OK, "ok", 1.1)

runs = [("1회", "echo a b", "a b"), ("2회", "echo c d", "c d"), ("3회", "echo e", "e")]
for kx, (n, cmd, out) in zip(KX, runs):
    d.box(kx - KW / 2, KY, KW, KH, PAPER2, MUTED, 1.0, 6)
    d.t(kx - KW / 2 + 14, KY + 31, n, 12, SOFT, KR, "start", 600)
    d.t(kx + KW / 2 - 14, KY + 31, cmd, 13, INK, MONO, "end", 600)
    d.box(kx - KW / 2, 372, KW, 44, PAPER, OK, 1.0, 6)
    d.t(kx - KW / 2 + 14, 399, "stdout", 11, SOFT, MONO, "start")
    d.t(kx + KW / 2 - 14, 399, out, 13, OK, MONO, "end", 600)
d.t(32, BUS - 8, "-t 가 stderr 에 먼저 찍는 줄", 12, MUTED, KR, "start")

# -n 없이
d.tone(24, 440, W - 48, 48, MUTED, op="0c", sw=0.9)
d.t(40, 469, "-n 없이", 12, MUTED, KR, "start", 600)
d.t(120, 469, "xargs echo", 13, INK, MONO, "start")
d.t(W - 40, 469, "echo a b c d e · 1회", 13, INK, MONO, "end")

d.legend(504, [("인자를 묶는 자리", ACC), ("실행 회차", MUTED), ("출력", OK)])
d.save("03-02.xargs-argv.svg")
print("ok 03-02.xargs-argv")

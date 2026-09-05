# 03-01 §2 — 셸이 모든 프로세스에 쥐여 주는 세 갈래와 그 방향을 바꾸는 법.
# 원문("Streams"): "the shell equips every process with three default file descriptors (FDs) for input
#       and output: stdin (FD 0) / stdout (FD 1) / stderr (FD 2)". 기본 연결은 키보드와 화면이다 —
#       "unless you specify something else, a command you enter in the shell will take its input (stdin)
#       from your keyboard, and it will deliver its output (stdout) to your screen."
#       방향 바꾸기는 "$FD> and <$FD ... for example, 2> means redirect the stderr stream. Note that 1>
#       and > are the same since stdout is the default. If you want to redirect both stdout and stderr,
#       use &>, and when you want to get rid of a stream, you can use /dev/null."
#       파이프는 "Connects stdout of one process with the stdin of the next process".
# 타입 스펙: type-data-flow — 존 셋(입력 · 프로세스 · 출력) 사이로 바이트가 건너간다.
#           accent 는 기본값을 벗어나게 만드는 자리 하나(리다이렉션 연산자).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, BAD, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 604
d = D(W, H, "LEARNING MODERN LINUX · 03-01 §2",
      "세 갈래는 기본으로 어디에 붙어 있는가",
      "셸은 모든 프로세스에 파일 서술자 셋을 쥐여 준다. 기본 연결은 키보드와 화면이고, "
      "리다이렉션 연산자가 그 끝을 파일이나 다른 프로세스로 옮긴다.",
      "2> 가 stderr 만 옮기고, &> 가 둘 다 옮깁니다")


def zone(x, y, w, h, label):
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{INK}05" '
               f'stroke="{INK}33" stroke-width="1" stroke-dasharray="4 4"/>')
    tw = len(label) * 6 + 12
    d.o.append(f'<rect x="{x + 12}" y="{y - 7}" width="{tw}" height="14" fill="{PAPER}"/>')
    d.t(x + 18, y + 3, label, 8, SOFT, MONO, "start", 600)


AX, AW = 24, 188
BX, BW = 292, 244
CX_, CW = 620, 236
TOP, ROW = 152, 76

zone(AX - 8, TOP - 20, AW + 16, 3 * ROW + 8, "DEFAULT SOURCE")
zone(BX - 8, TOP - 20, BW + 16, 3 * ROW + 8, "PROCESS")
zone(CX_ - 8, TOP - 20, CW + 16, 3 * ROW + 8, "DEFAULT SINK")

d.box(BX, TOP + 4, BW, 3 * ROW - 32, PAPER2, RULE, 1.0, 6)
d.t(BX + BW / 2, TOP + 84, "명령 하나", 15, INK, KR, "middle", 600)
d.t(BX + BW / 2, TOP + 108, "cat · curl · wc", 12, INFO, MONO)

rows = [("stdin", "FD 0", "키보드", INFO, "in"),
        ("stdout", "FD 1", "화면", OK, "out"),
        ("stderr", "FD 2", "화면", BAD, "out")]
for i, (name, fd, endp, c, direction) in enumerate(rows):
    y = TOP + i * ROW + 24
    if direction == "in":
        d.t(AX + AW / 2, y - 6, endp, 14, INK, KR, "middle", 600)
        d.t(AX + AW / 2, y + 14, name, 12, c, MONO)
        d.t(AX + AW / 2, y + 32, fd, 12, SOFT, MONO)
        d.path(f"M {AX + AW + 6} {y + 4} L {BX - 10} {y + 4}", c, 1.5, m="info")
    else:
        d.path(f"M {BX + BW + 6} {y + 4} L {CX_ - 10} {y + 4}", c, 1.5,
               m="ok" if c is OK else "bad")
        d.t(CX_ + CW / 2, y - 6, endp, 14, INK, KR, "middle", 600)
        d.t(CX_ + CW / 2, y + 14, name, 12, c, MONO)
        d.t(CX_ + CW / 2, y + 32, fd, 12, SOFT, MONO)

d.t(AX + AW / 2, TOP + 190, "출력 두 갈래는", 12, SOFT, KR)
d.t(AX + AW / 2, TOP + 208, "반대편으로 나갑니다", 12, SOFT, KR)

d.tone(24, 400, W - 32 - 16, 100, ACC)
d.t(44, 428, "기본값을 벗어나게 하는 연산자", 14, ACC, KR, "start", 600)
for k, line in enumerate([
        "2> 는 stderr 만 파일로 · 1> 과 > 는 같다(stdout 이 기본) · &> 는 둘 다",
        "/dev/null 로 보내면 버린다 · | 는 앞 프로세스의 stdout 을 뒤 프로세스의 stdin 에 잇는다"]):
    d.t(44, 452 + k * 22, line, 12, MUTED, KR, "start")

d.t(24, 528, "저자는 stderr 를 화면에서 치우고 파일에 담고 싶을 때를 예로 들며 이 연산자들을 소개합니다.",
    12, SOFT, KR, "start")
d.legend(548, [("입력", INFO), ("정상 출력", OK), ("오류 출력", BAD), ("기본값을 바꾸는 자리", ACC)])
d.save("03-01.streams.svg")
print("ok 03-01.streams")

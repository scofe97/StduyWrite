# 03-02 §2 「sed 로 줄을 바꾸고 골라내기」 — sed 가 한 줄을 읽어 바꾸고 내보내는 한 바퀴.
# 근거(책 밖 보강): GNU sed 매뉴얼 "How sed Works" —
#       "sed operates by performing the following cycle on each line of input: first, sed reads one line
#        from the input stream ... and places it in the pattern space. Then commands are executed; ...
#        When the end of the script is reached, unless the -n option is in use, the contents of pattern
#        space are printed out to the output stream". <https://www.gnu.org/software/sed/manual/sed.html#Execution-Cycle>
# 실측(Debian 12, sed 4.9): printf 'name=app\nversion=1.4.2\n' 에
#       sed -n 's/^version=//p' → 1.4.2 / sed 's/^version=//p' → name=app · 1.4.2 · 1.4.2
# 타입 스펙: type-flowchart — 단계는 사각형, 판단은 마름모(출구 둘, 모두 라벨), 흐름은 왼쪽→오른쪽.
#           coral 은 결과를 가르는 판단 하나(치환됨?)에만. 아래 표는 두 입력 줄이 각 칸에서 갖는 실제 값.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 496
d = D(W, H, "LEARNING MODERN LINUX · 03-02 §2",
      "sed 가 한 줄을 읽어 바꾸고 내보내는 한 바퀴",
      "sed -n 's/^version=//p' 가 두 줄짜리 파일을 처리하는 순서. 한 줄을 패턴 스페이스에 올려 s 명령을 적용하고, "
      "치환이 일어난 줄만 p 플래그로 찍는다. -n 이 끝의 자동 출력을 끈다.",
      "치환이 일어난 줄만 출력에 닿습니다")

CX = [104, 272, 440, 608, 776]
BW, BY, BH = 144, 124, 56
MID = BY + BH / 2


def step(i, name, sub, mono=True):
    x = CX[i] - BW / 2
    d.box(x, BY, BW, BH, PAPER2, MUTED, 1.0, 6)
    d.t(CX[i], BY + 24, name, 13, INK, MONO if mono else KR, "middle", 600)
    d.t(CX[i], BY + 44, sub, 11, MUTED, KR)


# 연결선 먼저
d.arrow([(CX[0] + BW / 2, MID), (CX[1] - BW / 2 - 2, MID)], MUTED, "ar", 1.3)
d.arrow([(CX[1] + BW / 2, MID), (CX[2] - 64 - 2, MID)], MUTED, "ar", 1.3)
d.arrow([(CX[2] + 64, MID), (CX[3] - BW / 2 - 2, MID)], OK, "ok", 1.4)
d.t((CX[2] + 64 + CX[3] - BW / 2) / 2, MID - 8, "예", 11, OK, KR, "middle", 600)
d.arrow([(CX[3] + BW / 2, MID), (CX[4] - BW / 2 - 2, MID)], MUTED, "ar", 1.3)
# 아니오: 마름모 아래로 내려 p 칸 밑을 지나 끝 칸 아래로 들어간다
d.path(f"M {CX[2]} {MID + 36} L {CX[2]} 204 L {CX[4]} 204 L {CX[4]} {BY + BH + 2}", SOFT, 1.3, m="soft")
d.t(CX[2] + 10, 198, "아니오", 11, SOFT, KR, "start", 600)
# 다음 줄로 되돌아가는 선
d.path(f"M {CX[4]} {BY} L {CX[4]} 104 L {CX[0]} 104 L {CX[0]} {BY - 2}", SOFT, 1.1, m="soft", dash="4 3")
d.t(CX[2], 96, "다음 줄", 11, SOFT, KR)

step(0, "줄 읽기", "패턴 스페이스에 올림", False)
step(1, "s/^version=//", "s 명령 적용")
# 판단 마름모
cx, cy = CX[2], MID
d.o.append(f'<path d="M {cx} {cy - 36} L {cx + 64} {cy} L {cx} {cy + 36} L {cx - 64} {cy} Z" '
           f'fill="{ACC}14" stroke="{ACC}" stroke-width="1.4"/>')
d.t(cx, cy + 5, "치환됨?", 13, ACC, KR, "middle", 600)
step(3, "p 플래그", "패턴 스페이스 출력", False)
step(4, "스크립트 끝", "-n 이라 자동 출력 꺼짐", False)

# 두 입력 줄의 실제 값
TY = [256, 316]
d.t(32, 240, "입력 줄마다 각 칸의 값", 12, MUTED, KR, "start", 600)
rows = [
    ("name=app", "name=app", "아니오", "건너뜀", "없음"),
    ("version=1.4.2", "1.4.2", "예", "1.4.2", "없음"),
]
for r, vals in enumerate(rows):
    y = TY[r]
    d.box(24, y, W - 48, 48, PAPER2 if r == 0 else PAPER, RULE, 0.8, 4)
    for i, v in enumerate(vals):
        if i == 3 and r == 1:
            col, w = OK, 600
        elif i == 2:
            col, w = (OK if v == "예" else SOFT), 600
        elif v in ("건너뜀", "없음"):
            col, w = SOFT, 400
        else:
            col, w = INK, 400
        fam = MONO if all(ord(c) < 128 for c in v) else KR
        d.t(CX[i], y + 29, v, 13, col, fam, "middle", w)

d.tone(24, 380, W - 48, 44, OK, op="0e")
d.t(40, 407, "stdout", 12, OK, MONO, "start", 600)
d.t(112, 407, "1.4.2", 13, INK, MONO, "start", 600)
d.t(W - 40, 407, "-n 없이 돌리면 · name=app · 1.4.2 · 1.4.2", 12, MUTED, KR, "end")

d.legend(444, [("결과를 가르는 판단", ACC), ("출력에 닿는 값", OK), ("건너뛰는 값", SOFT)])
d.save("03-02.sed-cycle.svg")
print("ok 03-02.sed-cycle")

# 03-02.string-bytes — 문자열 인덱스와 len 은 코드 포인트가 아니라 바이트를 센다
# 본문 요구(03-02 §1 「인덱스와 slice 식은 바이트를 셉니다」): "Hello 🌞" 는 코드 포인트 7개지만 바이트 10개이고,
#           s[4:7] 은 해 이모지의 첫 바이트만 잘라 온다 — 문자열 ⊃ 룬 ⊃ 바이트의 포함 관계와 그 경계를 가로지르는 구간.
# 타입 스펙: type-nested — 바깥 상자(문자열) 안에 룬 묶음, 룬 묶음 안에 바이트 칸. 포함은 괄호 선으로,
#           잘린 구간 하나에만 coral 대신 bad 를 쓰고 focal 은 이모지 룬 묶음 하나.
#           stride: 바이트 칸 폭 76, 칸 사이 0, 행 간격 44. 모든 좌표 4 의 배수.
# 사실 출처: Learning Go 2판 3장 「Strings and Runes and Bytes」·예제 3-9, go1.25.1 실행(2026-09-27) —
#           []byte("Hello, 🌞") 끝 네 바이트 240 159 140 158, s[4:7] == "o \xf0", len(s) == 10, 룬 수 7.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, BAD, INFO, PAPER2, KR, MONO

W, H = 984, 476
CW, CH = 76, 40
X0 = (W - 10 * CW) // 2          # 112
ROW_B = 196                        # 바이트 칸 y
BYTES = ["72", "101", "108", "108", "111", "32", "240", "159", "140", "158"]
RUNES = ["H", "e", "l", "l", "o", "공백", "🌞"]
RUNE_SPAN = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 10)]


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def bx(i):
    return X0 + i * CW


d = D(W, H, "NESTED · 03-02 §1",
      "문자열 인덱스는 바이트를 센다",
      "문자열 \"Hello 🌞\" 을 바이트 열 칸으로 펼치고 그 위에 코드 포인트(룬) 일곱 개의 경계를 괄호로 묶은 그림. "
      "해 이모지 하나가 UTF-8 로 네 바이트라서 len 은 10 이다. s[4:7] 은 4·5·6번 바이트를 잘라 이모지의 첫 바이트만 가져오고, "
      "s[6:] 은 네 바이트를 모두 가져와 이모지 하나가 된다.",
      lead="위 괄호는 룬 경계, 가운데 칸은 바이트 값, 아래 선은 slice 식이 잘라 오는 구간입니다.")

# 바깥 상자 — 문자열
d.o.append(f'<rect x="{X0 - 24}" y="112" width="{10 * CW + 48}" height="264" rx="8" fill="none" stroke="rgba(191,192,192,0.22)" stroke-width="0.9"/>')
d.t(X0 - 12, 132, "string · len 10", 12, MUTED, MONO, "start")

# 룬 괄호 — 바이트 칸 위
for k, (a, b) in enumerate(RUNE_SPAN):
    x1, x2 = bx(a) + 6, bx(b) - 6
    c = ACC if k == 6 else INFO
    d.line(x1, 176, x2, 176, c, 1.6 if k == 6 else 1.2)
    d.line(x1, 176, x1, 184, c, 1.2)
    d.line(x2, 176, x2, 184, c, 1.2)
    d.t((x1 + x2) / 2, 166, RUNES[k], 14 if k != 5 else 12, c, kr(RUNES[k]), "middle", 600)

# 바이트 칸
for i, v in enumerate(BYTES):
    if i >= 6:
        d.tone(bx(i), ROW_B, CW, CH, ACC, 2, "12", 1.0)
        col = ACC
    else:
        d.box(bx(i), ROW_B, CW, CH)
        col = INK
    d.t(bx(i) + CW // 2, ROW_B + 26, v, 14, col, MONO, "middle", 600)
    d.t(bx(i) + CW // 2, ROW_B + 60, str(i), 12, SOFT, MONO, "middle")

# slice 식 구간 — 아래
def span(a, b, y, label, c, left=False):
    x1, x2 = bx(a) + 4, bx(b) - 4
    d.line(x1, y, x2, y, c, 1.6)
    d.line(x1, y - 8, x1, y, c, 1.6)
    d.line(x2, y - 8, x2, y, c, 1.6)
    if left:
        d.t(x1 - 12, y + 5, label, 13, c, kr(label), "end")
    else:
        d.t(x2 + 12, y + 5, label, 13, c, kr(label), "start")

span(0, 5, 292, 's[:5] → "Hello"', OK)
span(4, 7, 324, 's[4:7] → "o \\xf0"', BAD)
span(6, 10, 356, 's[6:] → "🌞"', OK, left=True)

d.legend(412, [("한 바이트 룬", INFO), ("네 바이트 룬", ACC), ("룬 경계 안의 구간", OK), ("룬 경계를 자름", BAD)])
d.save("03-02.string-bytes.svg")
print("ok 03-02 string-bytes")

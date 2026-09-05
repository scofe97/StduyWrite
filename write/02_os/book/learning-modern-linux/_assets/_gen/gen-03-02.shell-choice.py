# 03-02 §5 — 셸을 고를 때 저자가 세우는 두 물음과, 정작 그가 답하지 않은 칸.
# 원문("Other Modern Shells"): "In addition to fish and zsh, there are a number of other interesting—
#       but not necessarily always bash-compatible—shells available out there. When you have a look at
#       those, ask yourself what the focus of the respective shell is (interactive usage vs. scripting)
#       and how active the community around it is."
#       Oil shell: "Targets Python and JavaScript users. Put in other words, the focus is less on
#                   interactive use but more on scripting."
#       murex: "A POSIX shell that sports interesting features such as an integrated testing framework,
#               typed pipelines, and event-driven programming."
#       Nushell: "An experimental new shell paradigm, featuring tabular output with a powerful query
#                 language."
#       PowerShell: "A cross-platform shell that started off as a fork of the Windows PowerShell and
#                    offers a different set of semantics and interactions than POSIX shells."
#       zsh: "a Bourne-like shell with a powerful completion system and rich theming support ... while
#             retaining wide backward compatibility with bash."
#       fish("Basic usage"): "For many daily tasks, you won't notice a big difference from bash in terms
#             of input; most of the commands provided in Table 3-2 are valid."
#       "I personally use the Fish shell, but many of my peers are super happy with the Z-shell."
#       bash 호환은 항목별 판정이 아니라 그룹에 붙은 일괄 단서뿐이므로 셸마다 O/X 로 나눌 근거가 없다.
# 타입 스펙: type-dp-security-matrix — 행(셸) × 열(저자가 밝힌 것)의 격자에 값과 미기재를 함께 놓아
#           "무엇을 안 적었는가" 가 보이게 한다. 초점은 저자가 자기 물음에 답한 단 하나의 칸.
#           축약: 커뮤니티 활발함은 원문이 어느 셸에도 답하지 않아 열로 세우지 않았다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 696
d = D(W, H, "LEARNING MODERN LINUX · 03-02 §5",
      "저자는 두 가지를 물으라 하고 자기 목록에는 답하지 않는다",
      "저자가 셸을 볼 때 던지라고 한 물음을 열로 세우고, 그가 실제로 적은 것만 칸에 넣은 격자. "
      "빈 칸이 아니라 미기재라고 적어 두면 무엇을 직접 확인해야 하는지가 보인다.",
      "저자는 자기가 Fish 를 쓰고 동료들은 zsh 에 만족한다고 밝힙니다")

LX, LW = 36, 156
CW, RH = 216, 54
HY = 172
RY = 200
COLS = ["저자가 밝힌 초점", "bash 호환 서술", "저자가 붙인 특징"]

for i, c in enumerate(COLS):
    d.t(LX + LW + CW * i + CW / 2, HY, c, 12, MUTED, KR, "middle", 600)
d.line(LX, HY + 12, LX + LW + CW * 3, HY + 12, RULE, 1)

# (셸, 초점, 호환, 특징) — 값 뒤 코드: 1 기재 · 2 단서만 · 0 미기재 · 9 초점
ROWS = [
    ("fish",       ("원문 미기재", 0), ("일상 입력은 큰 차이 없다", 2), ("저자 본인이 쓰는 셸", 1)),
    ("zsh",        ("원문 미기재", 0), ("넓은 하위 호환 유지", 1),      ("자동완성과 테마", 1)),
    ("Oil",        ("스크립팅 쪽", 9), ("원문 미기재", 0),             ("Python·JS 사용자 대상", 1)),
    ("murex",      ("원문 미기재", 0), ("POSIX 셸이라고만", 2),        ("테스트 틀·타입 파이프라인", 1)),
    ("Nushell",    ("원문 미기재", 0), ("원문 미기재", 0),             ("표 형태 출력과 질의 언어", 1)),
    ("PowerShell", ("원문 미기재", 0), ("POSIX 와 다른 의미론", 2),    ("크로스 플랫폼", 1)),
]
TONE = {0: SOFT, 1: OK, 2: WARN, 9: ACC}

for r, (name, *cells) in enumerate(ROWS):
    y = RY + RH * r
    if r % 2 == 0:
        d.box(LX, y, LW + CW * 3, RH, PAPER2, "none", 0, 4)
    d.t(LX + 14, y + RH / 2 + 5, name, 14, INK, MONO, "start", 600)
    for c, (val, code) in enumerate(cells):
        cx = LX + LW + CW * c
        col = TONE[code]
        if code == 9:
            d.box(cx + 6, y + 5, CW - 12, RH - 10, PAPER, ACC, 1.4, 6)
            d.t(cx + CW / 2, y + 24, val, 12.5, ACC, KR, "middle", 600)
            d.t(cx + CW / 2, y + 42, "자기 물음에 답한 유일한 칸", 11, ACC, KR)
        else:
            d.t(cx + CW / 2, y + RH / 2 + 5, val, 12.5, col, KR)

d.line(LX, RY + RH * len(ROWS) + 4, LX + LW + CW * 3, RY + RH * len(ROWS) + 4, RULE, 1)

d.tone(LX, 548, LW + CW * 3, 62, WARN)
d.t(LX + 20, 574, "bash 호환은 셸마다 판정된 적이 없습니다", 13, INK, KR, "start", 600)
d.t(LX + 20, 594, "원문은 목록 전체에 \"항상 bash 호환은 아니다\" 라는 단서 한 줄만 붙입니다.",
    12, MUTED, KR, "start")

d.legend(632, [("원문이 밝힌 것", OK), ("단서만 붙인 것", WARN),
               ("원문 미기재", SOFT), ("저자의 물음에 대한 답", ACC)])
d.save("03-02.shell-choice.svg")
print("ok 03-02.shell-choice")

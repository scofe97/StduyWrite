# 03-02 학습 목표 뒤 전체 지도 — 3장 가운데 구간(도구를 갈아 끼우는 축)을 읽는 순서로 잇는다.
# 원문 3장 "Common Tasks" · "Human-Friendly Shells" · "Terminal Multiplexer" 구간.
#       저자의 출발 문장은 "One fundamental insight with interfaces is that commands that you are using
#       very often should take the least effort—they should be quick to enter." 이고,
#       셸 절은 "While the bash shell is likely still the most widely used shell, it is not necessarily
#       the most human-friendly one", 멀티플렉서 절은 "multiplexing the terminal I/O" 로 연다.
#       명령 사용법(grep·awk·head·tail·date 등)은 docs/cmd/ 시트로 옮겨 이 지도에서 뺐다.
# 타입 스펙: type-process — 절마다 같은 의미 슬롯(번호 · 층 · 이름 · 다루는 것)이 반복되고
#           화살표가 읽는 순서를 나른다. 축약: 주체(lane)가 없는 단계 지도라 카드 격자 stride 로 놓는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 880, 424
d = D(W, H, "LEARNING MODERN LINUX · 03-02",
      "자주 치는 것일수록 짧아야 한다",
      "3장 가운데 구간 노트의 절 여섯을 읽는 순서로 이은 지도. 1~2절이 지금 쓰는 셸에서 손을 덜 쓰는 법이고, "
      "3~4절이 셸 자체를 갈아 끼우는 판단, 5~6절이 터미널을 쪼개 쓰는 법이다.",
      "4절에서 저자가 셸 선택을 밝힙니다")

CW, CH, GAP, X0 = 264, 104, 20, 20
ROWS = [104, 232]
L1, L2, L3 = "셸 안에서 줄이기", "셸 바꾸기", "터미널 쪼개기"
cards = [
    ("§1", L1, "명령 줄이기", "별칭 · 축약 · 함수 · 단축키"),
    ("§2", L1, "편집기 없이 다루기", "리다이렉션 · 히어 도큐먼트 · diff"),
    ("§3", L2, "bash 의 나이", "Fish 가 다른 두 자리"),
    ("§4", L2, "어느 셸을 고르나", "초점 · 커뮤니티 · bash 호환"),
    ("§5", L3, "창 하나를 쪼개기", "세션 · 윈도 · 페인 · 끊김"),
    ("§6", L3, "한 벌로 묶기", "Alacritty · fish · tmux"),
]


def pos(i):
    return X0 + (i % 3) * (CW + GAP), ROWS[i // 3]


for i in range(len(cards) - 1):
    x1, y1 = pos(i); x2, y2 = pos(i + 1)
    if y1 == y2:
        d.arrow([(x1 + CW, y1 + CH / 2), (x2 - 2, y2 + CH / 2)], MUTED, "ar", 1.4)
    else:
        bus = y1 + CH + 12
        d.path(f"M {x1 + CW / 2} {y1 + CH} L {x1 + CW / 2} {bus} "
               f"L {x2 + CW / 2} {bus} L {x2 + CW / 2} {y2 - 2}", MUTED, 1.4, m="ar")

for i, (n, layer, title, q) in enumerate(cards):
    x, y = pos(i)
    focal = (i == 3)
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{CW}" height="{CH}" rx="8" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, y, CW, CH, PAPER2, RULE, 1.0, 8)
    d.t(x + 18, y + 26, n, 12, ACC if focal else SOFT, MONO, "start", 600)
    d.t(x + CW - 18, y + 26, layer, 12, SOFT, KR, "end")
    d.t(x + 18, y + 56, title, 16, ACC if focal else INK, KR, "start", 600)
    d.t(x + 18, y + 84, q, 13, MUTED, KR, "start")

d.legend(364, [("저자가 셸 선택을 밝히는 자리", ACC)])
d.save("03-02.chapter-overview.svg")
print("ok 03-02.chapter-overview")

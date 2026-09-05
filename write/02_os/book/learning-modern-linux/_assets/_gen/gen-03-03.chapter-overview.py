# 03-03 학습 목표 뒤 전체 지도 — 3장 뒷부분(자동화 축)을 읽는 순서로 잇는다.
# 원문 3장 "Scripting" 이후 구간. 저자의 출발 문장은 "Once you've done a certain task over and over
#       again manually on the prompt, it's likely time to automate the task. This is where scripts come in."
#       이고, 좋은 관례의 첫 항목이 "Fail fast and loud ... Since bash tends to fail silently by default,
#       failing fast is almost always a good idea." 다.
# 타입 스펙: type-process — 절마다 같은 의미 슬롯(번호 · 이름 · 그 절이 답하는 물음)이 반복되고
#           화살표가 읽는 순서를 나른다. 축약: 주체(lane)가 없는 단계 지도라 카드 격자 stride 로 놓는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 880, 600
d = D(W, H, "LEARNING MODERN LINUX · 03-03",
      "bash 는 조용히 실패하므로 시끄럽게 만들어야 한다",
      "3장 뒷부분 노트의 절 일곱을 읽는 순서로 이은 지도. 1~3절이 스크립트를 쓸 수 있게 만드는 조건이고, "
      "4~6절이 그 스크립트를 믿을 수 있게 만드는 장치, 7절이 그것을 다 적용한 예제다.",
      "4절의 세 줄이 이 구간에서 가장 값이 큰 부분입니다")

CW, CH, GAP, X0 = 400, 88, 20, 20
ROWS = [104, 212, 320, 428]
cards = [
    ("§1", "언제 스크립트로 넘어가나", "그리고 언제 파이썬으로 넘어가나"),
    ("§2", "텍스트 파일이 스크립트가 되려면", "해시뱅 한 줄과 실행 권한"),
    ("§3", "스크립트가 쓰는 문법", "배열 · 분기 · 반복 · 함수 · 입출력"),
    ("§4", "조용한 실패를 시끄럽게", "errexit · nounset · pipefail"),
    ("§5", "저자가 세는 좋은 관례 여덟", "시크릿부터 문서화와 버전 관리까지"),
    ("§6", "린트하고 포맷하고 테스트한다", "shellcheck · shfmt · bats"),
    ("§7", "끝까지 만들어 본 예제", "그리고 저자가 남긴 네 가지 숙제"),
]


def pos(i):
    return X0 + (i % 2) * (CW + GAP), ROWS[i // 2]


for i in range(6):
    x1, y1 = pos(i); x2, y2 = pos(i + 1)
    if y1 == y2:
        d.arrow([(x1 + CW, y1 + CH / 2), (x2 - 2, y2 + CH / 2)], MUTED, "ar", 1.4)
    else:
        bus = y1 + CH + 10
        d.path(f"M {x1 + CW / 2} {y1 + CH} L {x1 + CW / 2} {bus} "
               f"L {x2 + CW / 2} {bus} L {x2 + CW / 2} {y2 - 2}", MUTED, 1.4, m="ar")

for i, (n, title, q) in enumerate(cards):
    x, y = pos(i)
    focal = (i == 3)
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{CW}" height="{CH}" rx="8" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, y, CW, CH, PAPER2, RULE, 1.0, 8)
    d.t(x + 18, y + 24, n, 12, ACC if focal else SOFT, MONO, "start", 600)
    d.t(x + 18, y + 50, title, 15, ACC if focal else INK, KR, "start", 600)
    d.t(x + 18, y + 74, q, 12, MUTED, KR, "start")

d.legend(540, [("조용한 실패를 막는 세 줄", ACC)])
d.save("03-03.chapter-overview.svg")
print("ok 03-03.chapter-overview")

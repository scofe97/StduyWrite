# 07-03 학습 목표 뒤 전체 지도 — 512
# 원문 7장 서두: "We'll first have a look at common network terms, from the hardware level all the way up
#       to user-facing components such as HTTP and SSH. We'll also discuss the network stack, protocols,
#       and interfaces."
# 타입 스펙: type-process — 절마다 같은 의미 슬롯(번호 · 이름 · 그 절이 답하는 물음)이 반복되고
#           읽는 순서가 화살표로 흐른다. 축약: 주체 lane 이 없어 카드 격자 stride 로 놓는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 880, 588
d = D(W, H, "LEARNING MODERN LINUX · 07-03",
      "주고받는 일은 결국 몇 개의 명령으로 줄어든다",
      "7장 마지막 구간의 절 일곱을 읽는 순서로 이은 지도. 1~3절이 웹, 4~6절이 원격 접속과 파일, 7절이 고급 도구다.",
      "3절이 이 노트의 제목이 가리키는 자리입니다")

CW, CH, GAPX, GAPY, X0, Y0 = 272, 96, 12, 20, 20, 116
cards = [
    ("§1", "웹은 셋으로", "URL · HTTP · HTML"),
    ("§2", "URI 뜯어보기", "다섯 부분과 그 순서"),
    ("§3", "서버와 curl", "옵션 일곱이 곧 쓰임새"),
    ("§4", "SSH", "안전하지 않은 망 위에서"),
    ("§5", "파일을 옮기는 길", "scp · rsync · aws s3"),
    ("§6", "중앙 저장소 붙이기", "NFS 와 SMB"),
    ("§7", "고급 도구", "층마다 하나씩"),
]


def pos(i):
    return X0 + (i % 3) * (CW + GAPX), Y0 + (i // 3) * (CH + GAPY)


for i in range(len(cards) - 1):
    x1, y1 = pos(i); x2, y2 = pos(i + 1)
    if y1 == y2:
        d.arrow([(x1 + CW, y1 + CH / 2), (x2 - 2, y2 + CH / 2)], MUTED, "ar", 1.3)
    else:
        bus = y1 + CH + 10
        d.path(f"M {x1 + CW / 2} {y1 + CH} L {x1 + CW / 2} {bus} "
               f"L {x2 + CW / 2} {bus} L {x2 + CW / 2} {y2 - 2}", MUTED, 1.3, m="ar")

for i, (n, title, q) in enumerate(cards):
    x, y = pos(i)
    focal = (i == 2)
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{CW}" height="{CH}" rx="8" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, y, CW, CH, PAPER2, RULE, 1.0, 8)
    d.t(x + 16, y + 26, n, 12, ACC if focal else SOFT, MONO, "start", 600)
    d.t(x + 16, y + 54, title, 14, ACC if focal else INK, KR, "start", 600)
    d.t(x + 16, y + 78, q, 11.5, MUTED, KR, "start")

d.legend(524, [("명령 한 줄로 줄어드는 자리", ACC)])
d.save("07-03.chapter-overview.svg")
print("ok 07-03.chapter-overview")

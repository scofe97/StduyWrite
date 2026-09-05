# 04-01 학습 목표 뒤 전체 지도 — 4장 노트의 절 일곱을 읽는 순서로 잇는다.
# 원문 4장 서두: "we'll first take a look at the fundamental relationship between users, processes, and
#       files, from an access perspective. We'll also review sandboxing and access control types. Next,
#       we'll focus on the definition of a Linux user ... Then, we'll move on to the topic of permissions
#       ... We'll wrap up this chapter covering a range of advanced Linux features in the access control
#       space, including capabilities, seccomp profiles, and ACLs. To round things off, we'll provide
#       some security good practices around permissions and access control."
# 타입 스펙: type-process — 절마다 같은 의미 슬롯(번호 · 이름 · 그 절이 답하는 물음)이 반복되고
#           화살표가 읽는 순서를 나른다. 축약: 주체(lane)가 없는 단계 지도라 카드 격자 stride 로 놓는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 880, 600
d = D(W, H, "LEARNING MODERN LINUX · 04-01",
      "전부 아니면 전무에서 잘게 쪼개는 쪽으로",
      "4장 노트의 절 일곱을 읽는 순서로 이은 지도. 1~3절이 누가 무엇을 갖는가이고, "
      "4~5절이 그 권한을 파일과 프로세스에서 읽는 법, 6~7절이 이분법을 쪼개는 장치와 관례다.",
      "6절이 이 장의 제목이 가리키는 자리입니다")

CW, CH, GAP, X0 = 400, 88, 20, 20
ROWS = [104, 212, 320, 428]
cards = [
    ("§1", "사용자와 프로세스와 파일", "셋이 서로 무엇을 하는가"),
    ("§2", "권한을 누가 정하는가", "재량적 통제와 강제적 통제"),
    ("§3", "사용자를 만드는 파일 넷", "UID 범위와 /etc/passwd 한 줄"),
    ("§4", "파일 모드 한 줄 읽기", "파일과 디렉토리에서 뜻이 다르다"),
    ("§5", "프로세스가 갖는 네 개의 UID", "실제 · 유효 · 저장된 · 파일시스템"),
    ("§6", "이분법을 쪼개는 세 장치", "capability · seccomp · ACL"),
    ("§7", "저자가 세는 좋은 관례 셋", "최소 권한 · setuid 피하기 · 감사"),
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
    focal = (i == 5)
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{CW}" height="{CH}" rx="8" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, y, CW, CH, PAPER2, RULE, 1.0, 8)
    d.t(x + 18, y + 24, n, 12, ACC if focal else SOFT, MONO, "start", 600)
    d.t(x + 18, y + 50, title, 15, ACC if focal else INK, KR, "start", 600)
    d.t(x + 18, y + 74, q, 12, MUTED, KR, "start")

d.legend(540, [("이분법이 깨지는 자리", ACC)])
d.save("04-01.chapter-overview.svg")
print("ok 04-01.chapter-overview")

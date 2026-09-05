# 05-01 학습 목표 뒤 전체 지도 — 5장 노트의 절 아홉을 읽는 순서로 잇는다.
# 원문 5장 서두: "In this chapter, we first define some relevant terms. Then, we look at how Linux
#       implements the 'everything is a file' abstraction. Next, we review special-purpose filesystems
#       the kernel uses to expose information about processes or devices. We then move on to regular
#       files and filesystems, something you would typically associate with documents, data, and
#       programs. We compare filesystem options and discuss common operations."
# 타입 스펙: type-process — 절마다 같은 의미 슬롯(번호 · 이름 · 그 절이 답하는 물음)이 반복되고
#           읽는 순서가 화살표로 흐른다. 축약: 주체 lane 이 없어 카드 격자 stride 로 놓는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 880, 588
d = D(W, H, "LEARNING MODERN LINUX · 05-01",
      "모든 것이 파일이라는 말은 손잡이가 하나라는 뜻이다",
      "5장 노트의 절 아홉을 읽는 순서로 이은 지도. 1~3절이 용어와 구조, 4~7절이 그 위에 놓인 층과 "
      "연산, 8~9절이 블록 장치가 아닌 것과 겹쳐 쌓는 방법이다.",
      "8절이 이 장의 제목이 가리키는 자리입니다")

CW, CH, GAPX, GAPY, X0, Y0 = 272, 96, 12, 20, 20, 116
cards = [
    ("§1", "전제 다섯", "정의 전에 무엇을 깔고 가는가"),
    ("§2", "드라이브에서 아이노드까지", "다섯 이름이 어떻게 포개지는가"),
    ("§3", "이름과 데이터를 갈라 두면", "링크 둘이 왜 다르게 도는가"),
    ("§4", "VFS", "손잡이를 하나로 만드는 층"),
    ("§5", "LVM", "파티션이 못 하는 것은 무엇인가"),
    ("§6", "만들고 붙이고 되살리기", "mkfs · mount · fstab"),
    ("§7", "어디에 무엇을 두는가", "FHS 와 배포판의 거리"),
    ("§8", "블록 장치가 아닌 것에", "procfs · sysfs · devfs"),
    ("§9", "복사하지 않는 복사", "CoW 와 유니온 마운트"),
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
    focal = (i == 7)
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{CW}" height="{CH}" rx="8" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, y, CW, CH, PAPER2, RULE, 1.0, 8)
    d.t(x + 16, y + 26, n, 12, ACC if focal else SOFT, MONO, "start", 600)
    d.t(x + 16, y + 54, title, 14, ACC if focal else INK, KR, "start", 600)
    d.t(x + 16, y + 78, q, 11.5, MUTED, KR, "start")

d.legend(524, [("같은 손잡이가 블록 장치 밖으로 뻗는 자리", ACC)])
d.save("05-01.chapter-overview.svg")
print("ok 05-01.chapter-overview")

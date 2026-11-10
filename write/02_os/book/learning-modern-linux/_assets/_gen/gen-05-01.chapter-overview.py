# 05-01 학습 목표 뒤 전체 지도 — 5장 개념 편의 절 여덟과 05-02 연계를 잇는다.
# 타입 스펙: type-process — 절마다 같은 의미 슬롯(번호 · 이름 · 그 절이 답하는 물음)이 반복되고
#           읽는 순서가 화살표로 흐른다. 축약: 주체 lane 이 없어 카드 격자 stride 로 놓는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO, INFO

W, H = 880, 588
d = D(W, H, "LEARNING MODERN LINUX · 05-01",
      "모든 것이 파일이라는 말은 손잡이가 하나라는 뜻이다",
      "5장 개념 편의 절 여덟을 읽는 순서로 이은 지도. 1~3절이 용어와 링크, 4~5절이 VFS 와 LVM 간접 층, "
      "6~8절이 디렉터리 배치와 가짜 파일시스템 및 CoW · 유니온 마운트다.",
      "7절 가짜 파일시스템이 이 장의 제목이 가리키는 핵심 자리")

CW, CH, GAPX, GAPY, X0, Y0 = 272, 96, 12, 20, 20, 116
cards = [
    ("§1", "전제 다섯", "계층형 트리와 파일 추상 전제"),
    ("§2", "드라이브에서 아이노드까지", "다섯 이름이 어떻게 포개지는가"),
    ("§3", "하드 링크와 심볼릭 링크", "아이노드와 경로 분기"),
    ("§4", "VFS 추상 층", "손잡이를 하나로 만드는 간접 층"),
    ("§5", "LVM", "파티션이 못 하는 것 · PV · VG · LV"),
    ("§6", "디렉터리 배치", "FHS 표준과 배포판 현실"),
    ("§7", "가짜 파일시스템", "procfs · sysfs · devtmpfs"),
    ("§8", "보통 파일과 CoW", "유니온 마운트와 컨테이너 이미지 층"),
    ("05-02 연계", "키울 때는 아래 층부터", "mkfs · mount · fstab 운영 절차"),
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
    focal = (i == 6)
    is_next = (i == 8)
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{CW}" height="{CH}" rx="8" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    elif is_next:
        d.o.append(f'<rect x="{x}" y="{y}" width="{CW}" height="{CH}" rx="8" '
                   f'fill="{INFO}08" stroke="{INFO}" stroke-width="1.2" stroke-dasharray="6 4"/>')
    else:
        d.box(x, y, CW, CH, PAPER2, RULE, 1.0, 8)

    col = ACC if focal else (INFO if is_next else SOFT)
    tcol = ACC if focal else (INK if not is_next else INFO)
    d.t(x + 16, y + 26, n, 12, col, MONO if not is_next else KR, "start", 600)
    d.t(x + 16, y + 54, title, 14, tcol, KR, "start", 600)
    d.t(x + 16, y + 78, q, 11.5, MUTED, KR, "start")

d.legend(524, [("균일한 손잡이가 블록 장치 밖으로 뻗는 자리", ACC), ("운영 절차를 다루는 다음 편", INFO)])
d.save("05-01.chapter-overview.svg")
print("ok 05-01.chapter-overview")

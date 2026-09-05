# 02-01 학습 목표 뒤 전체 지도 — 2장 노트의 절 여덟을 읽는 순서로 잇는다.
# 원문: 2장은 조감(아키텍처) → CPU 계열 → 커널 구성요소 → syscall → 커널 확장 순으로 흐르고,
#       저자가 "One main takeaway of this chapter is that while the kernel provides all the core
#       functionality, on its own it is not the operating system but only a very central part of it" 라고
#       미리 못 박는다. 가장 중요한 인터페이스는 syscall 이라고 결론에서 다시 적는다.
# 타입 스펙: type-process — 절마다 같은 의미 슬롯(번호 · 이름 · 그 절이 답하는 물음)이 반복되고
#           화살표가 읽는 순서를 나른다. 축약: 주체(lane)가 없는 단계 지도라 카드 격자 stride 로 놓는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 880, 600
d = D(W, H, "LEARNING MODERN LINUX · 02-01",
      "커널은 전부를 하지만 운영체제는 아니다",
      "2장 노트의 절 여덟을 읽는 순서로 이은 지도. 1~2절이 커널의 자리와 하드웨어 쪽 경계, "
      "3~5절이 커널이 맡는 일, 6~7절이 유저 랜드와 갈리는 인터페이스, 8절이 그 커널을 늘리는 두 길이다.",
      "6절의 시스템 콜이 저자가 가장 중요하다고 못 박은 인터페이스입니다")

CW, CH, GAP, X0 = 400, 88, 20, 20
ROWS = [104, 212, 320, 428]
cards = [
    ("§1", "셸도 ps 도 커널이 아니다", "세 층과 그 사이의 인터페이스"),
    ("§2", "CPU 계열을 왜 아나", "x86 · ARM · RISC-V 가 갈리는 자리"),
    ("§3", "다섯 이름이 한 구조체로", "세션 · 그룹 · 프로세스 · 스레드 · 태스크"),
    ("§4", "없는 방을 있는 것처럼", "페이지 · 페이지 테이블 · TLB"),
    ("§5", "커널이 맡는 나머지", "네트워크 · 파일시스템 · 드라이버"),
    ("§6", "명령이 커널로 내려가는 길", "래퍼 라이브러리와 세 걸음"),
    ("§7", "그 경계를 실제로 센다", "strace 가 보여 주는 비용"),
    ("§8", "커널을 늘리는 두 길", "모듈과 eBPF 가 갈리는 지점"),
]


def pos(i):
    return X0 + (i % 2) * (CW + GAP), ROWS[i // 2]


for i in range(7):
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

d.legend(540, [("저자가 가장 중요하다고 적은 인터페이스", ACC)])
d.save("02-01.chapter-overview.svg")
print("ok 02-01.chapter-overview")

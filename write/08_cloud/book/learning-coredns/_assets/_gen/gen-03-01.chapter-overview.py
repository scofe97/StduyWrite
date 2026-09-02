# 03-01 학습 목표 뒤 전체 지도 — 절 여섯을 읽는 순서로 잇는다.
# 타입 스펙: type-process — 절마다 같은 의미 슬롯(번호 · 이름 · 질문)이 반복되고 화살표가 읽는 순서를 나른다.
#           축약: 주체(lane)가 없는 단계 지도라 카드 격자 stride 로 놓는다(같은 폴더 관례).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 880, 680
d = D(W, H, "LEARNING COREDNS · 03-01",
      "Corefile 은 라벨과 블록으로 서버를 가른다",
      "3장 전반부의 절 여섯을 읽는 순서로 이은 지도. 1~2절이 실행 파일과 명령줄, "
      "3~4절이 Corefile 문법, 5~6절이 서버 블록과 질의가 그 블록에 붙는 규칙이다.",
      "6절의 최장 일치 규칙이 앞의 문법을 실제 동작으로 잇습니다")

CW, CH, GAP, X0 = 400, 104, 20, 20
ROWS = [104, 232, 360, 488]
cards = [
    ("§1", "실행 파일부터 받는다", "체크섬을 맞추고 버전을 찍는다"),
    ("§2", "명령줄 옵션 여덟", "로그 옵션이 없는 것이 설계다"),
    ("§3", "엔트리는 라벨과 블록", "중괄호가 경계를 그린다"),
    ("§4", "환경 변수와 스니펫", "import 가 둘 다 끌어온다"),
    ("§5", "서버 블록이 서버 하나다", "프로토콜·도메인·포트로 고른다"),
    ("§6", "가장 긴 라벨이 이긴다", "질의가 어느 블록에 붙는가"),
]
def pos(i):
    return X0 + (i % 2) * (CW + GAP), ROWS[i // 2]

for i in range(len(cards) - 1):
    x1, y1 = pos(i); x2, y2 = pos(i + 1)
    if y1 == y2:
        d.arrow([(x1 + CW, y1 + CH / 2), (x2 - 2, y2 + CH / 2)], MUTED, "ar", 1.4)
    else:
        bus = y1 + CH + 12
        d.path(f"M {x1 + CW / 2} {y1 + CH} L {x1 + CW / 2} {bus} L {x2 + CW / 2} {bus} L {x2 + CW / 2} {y2 - 2}",
               MUTED, 1.4, m="ar")

for i, (n, title, q) in enumerate(cards):
    x, y = pos(i); focal = (i == 5)
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{CW}" height="{CH}" rx="8" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, y, CW, CH, PAPER2, RULE, 1.0, 8)
    d.t(x + 18, y + 26, n, 12, ACC if focal else SOFT, MONO, "start", 600)
    d.t(x + 18, y + 56, title, 16, ACC if focal else INK, KR, "start", 600)
    d.t(x + 18, y + 84, q, 13, MUTED, KR, "start")

d.legend(620, [("문법을 동작으로 잇는 자리", ACC)])
d.save("03-01.chapter-overview.svg")

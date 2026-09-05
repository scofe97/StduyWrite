# 09-02 학습 목표 뒤 전체 지도 — 절 일곱을 읽는 순서로 잇는다.
# 타입 스펙: type-process — 절마다 같은 의미 슬롯(번호 · 이름 · 한 줄)이 반복되고 화살표가 읽는 순서를 나른다.
#           축약: 주체(lane)가 없는 단계 지도라 카드 격자 stride 로 놓는다(같은 폴더 관례).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 880, 734
d = D(W, H, "LEARNING COREDNS · 09-02",
      "네 함수를 구현하면 체인의 한 칸이 된다",
      "9장 후반부의 절 일곱을 읽는 순서로 이은 지도. 1~3절이 뼈대, 4~6절이 예제 플러그인, "
      "7절이 운영에 붙이는 일이다.",
      "주황이 원서가 규약을 뒤집어 적은 자리입니다")

CW, CH, GAP, X0 = 400, 104, 20, 20
ROWS = [104, 232, 360, 488]
cards = [
    ("§1", "세 갈래로 나눈다", "백엔드 · 뮤테이터 · 설정자"),
    ("§2", "네 함수와 그 시점", "프로세스 · 블록 · 요청마다"),
    ("§3", "훅 여섯", "재시작에 두 인스턴스가 겹친다"),
    ("§4", "가짜 소켓을 넘긴다", "nonwriter 로 응답을 가로챈다"),
    ("§5", "참·거짓 하나가 뒤집힌다", "원서가 ClientWrite 를 반대로 적었다"),
    ("§6", "파싱 루프와 ErrOnce", "체인을 알려면 OnStartup"),
    ("§7", "운영에 붙이면", "지표 · 추적 · metadata"),
]


def pos(i):
    return X0 + (i % 2) * (CW + GAP), ROWS[i // 2]


for i in range(len(cards) - 1):
    x1, y1 = pos(i)
    x2, y2 = pos(i + 1)
    if y1 == y2:
        d.arrow([(x1 + CW, y1 + CH / 2), (x2 - 2, y2 + CH / 2)], MUTED, "ar", 1.4)
    else:
        bus = y1 + CH + 12
        d.path(f"M {x1 + CW / 2} {y1 + CH} L {x1 + CW / 2} {bus} L {x2 + CW / 2} {bus} L {x2 + CW / 2} {y2 - 2}",
               MUTED, 1.4, m="ar")

for i, (n, title, q) in enumerate(cards):
    x, y = pos(i)
    focal = (i == 4)
    if focal:
        d.tone(x, y, CW, CH, ACC, 8, "12", 1.4)
    else:
        d.box(x, y, CW, CH, PAPER2, RULE, 1.0, 8)
    d.t(x + 18, y + 26, n, 12, ACC if focal else SOFT, MONO, "start", 600)
    d.t(x + 18, y + 56, title, 16, ACC if focal else INK, KR, "start", 600)
    d.t(x + 18, y + 84, q, 13, MUTED, KR, "start")

d.t(20, 620, "무엇을 어느 함수에 두느냐가 곧 그것이 몇 번 실행될지를 정한다", 13, MUTED, KR, "start")
d.t(20, 644, "반환값 int 하나가 규약이라 컴파일러가 잡아 주지 않는다", 13, MUTED, KR, "start")

d.legend(672, [("규약이 뒤집힌 자리", ACC)])
d.save("09-02.chapter-overview.svg")

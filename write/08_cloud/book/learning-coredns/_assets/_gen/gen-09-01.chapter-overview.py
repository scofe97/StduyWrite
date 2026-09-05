# 09-01 학습 목표 뒤 전체 지도 — 절 일곱을 읽는 순서로 잇는다.
# 타입 스펙: type-process — 절마다 같은 의미 슬롯(번호 · 이름 · 한 줄)이 반복되고 화살표가 읽는 순서를 나른다.
#           축약: 주체(lane)가 없는 단계 지도라 카드 격자 stride 로 놓는다(같은 폴더 관례).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 880, 734
d = D(W, H, "LEARNING COREDNS · 09-01",
      "한 줄을 옮기면 그 플러그인이 쓸모없어진다",
      "9장 전반부의 절 일곱을 읽는 순서로 이은 지도. 1~5절이 plugin.cfg 를 고치는 길이고, "
      "6~7절이 main 을 갈아 끼우는 길이다.",
      "주황이 이 편의 논지가 실증되는 자리입니다")

CW, CH, GAP, X0 = 400, 104, 20, 20
ROWS = [104, 232, 360, 488]
cards = [
    ("§1", "빌드 때와 실행 때", "플러그인은 동적으로 안 붙는다"),
    ("§2", "Docker 하나로 짓기", "-u 를 붙이는 자리와 떼는 자리"),
    ("§3", "워크스테이션에 Go", "go modules 로 GOPATH 해방"),
    ("§4", "두 파일이 나눠 정한다", "순서는 plugin.cfg 가 정한다"),
    ("§5", "한 줄을 옮겨 확인한다", "같은 질의에 다른 답이 온다"),
    ("§6", "main 을 갈아 끼우면", "CoreDNS 가 라이브러리가 된다"),
    ("§7", "코드가 Corefile 을 짓는다", "문자열로 만들어 Caddy 에 먹인다"),
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

d.t(20, 620, "Corefile 에 어떤 순서로 적든 체인은 plugin.cfg 의 순서대로 선다", 13, MUTED, KR, "start")
d.t(20, 644, "그래서 순서를 고치는 일이 배포를 동반한다", 13, MUTED, KR, "start")

d.legend(672, [("논지가 실증되는 절", ACC)])
d.save("09-01.chapter-overview.svg")

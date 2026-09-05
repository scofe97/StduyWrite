# 08-02 학습 목표 뒤 전체 지도 — 절 여덟을 읽는 순서로.
# 원문 8장 서두: "Then, we'll cover monitoring for different resource types, such as CPU cycles, memory,
#       or I/O traffic. We'll review different tools that you can use and show certain end-to-end setup
#       you may wish to adopt."
# 타입 스펙: type-process — 절마다 같은 의미 슬롯(번호 · 이름 · 그 절이 답하는 물음)이 반복되고
#           읽는 순서가 화살표로 흐른다. 축약: 주체 lane 이 없어 카드 격자 stride 로 놓는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 880, 588
d = D(W, H, "LEARNING MODERN LINUX · 08-02",
      "자원마다 창이 따로 나 있어 어느 창을 여느냐가 곧 진단이다",
      "8장 둘째 구간의 절 여덟을 읽는 순서로 이은 지도. 2~5절이 리눅스 기본 도구이고 7~8절이 그 위에 "
      "얹히는 층이다.",
      "저자는 기본 도구만으로도 꽤 멀리 간다고 적습니다")

CW, CH, GAPX, GAPY, X0, Y0 = 272, 96, 12, 20, 20, 116
cards = [
    ("§1", "원인의 범주", "느리다는 증상을 어디로 나누나"),
    ("§2", "처음 치는 세 명령", "uptime · free · vmstat 를 어떻게 읽나"),
    ("§3", "얼마나 걸렸나", "real 과 user 와 sys 는 뭐가 다른가"),
    ("§4", "장치와 소켓", "iostat · ss · lsof 는 무엇을 보나"),
    ("§5", "통합 모니터", "top 화면의 네 구역은 무엇인가"),
    ("§6", "내 코드의 계측", "메트릭을 어떻게 내보내나"),
    ("§7", "추적과 프로파일링", "어디에 훅을 걸어 실행을 보나"),
    ("§8", "Prometheus 와 Grafana", "언제 이 무게를 감당할 만한가"),
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
    focal = (i == 0)
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{CW}" height="{CH}" rx="8" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, y, CW, CH, PAPER2, RULE, 1.0, 8)
    d.t(x + 16, y + 26, n, 12, ACC if focal else SOFT, MONO, "start", 600)
    d.t(x + 16, y + 54, title, 14, ACC if focal else INK, KR, "start", 600)
    d.t(x + 16, y + 78, q, 11.5, MUTED, KR, "start")

d.legend(524, [("증상을 자원 범주로 나누는 자리", ACC)])
d.save("08-02.chapter-overview.svg")
print("ok 08-02.chapter-overview")

# 05-01 §6 — 원서가 적은 etcd 옵션 일곱과 현재 master 문법의 차이를 버전 축 위에 놓는다.
# 원문 근거(왼쪽 세 칸): stubzones 는 "only valid in versions of CoreDNS before 1.4.0",
#            upstream 은 "obsolete in CoreDNS 1.3.0 and later", credentials 는 "available starting in
#            CoreDNS 1.4.0", 나머지 넷(fallthrough·path·endpoint·tls)에는 버전 단서가 없다.
# 공식 근거(오른쪽 칸): master 의 plugin/etcd/README.md 문법 블록에 stubzones·upstream 이 없고
#            no_apex_fallback 이 있으며, 블록 밖에 min-lease-ttl(기본 30초)·max-lease-ttl(기본 24시간)이 있다.
# 타입 스펙: type-gantt — 막대의 시작점과 길이가 곧 그 옵션이 유효한 구간이다.
#           축약: 가로축이 날짜가 아니라 CoreDNS 버전 구간이다(같은 폴더 02-01 캐시 사다리와 같은 축약).
#           원서 이후 붙은 셋은 도입 버전을 확인하지 못해 막대를 마지막 칸에만 두고 점선으로 표시한다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, RULE, OK, BAD, INFO, KR, MONO

W, H = 1000, 748
d = D(W, H, "LEARNING COREDNS · 05-01 §6",
      "원서의 일곱 항목이 지금 어디까지 유효한가",
      "가로축은 날짜가 아니라 CoreDNS 버전 구간이다. 막대가 끊긴 자리가 그 옵션이 문법에서 사라진 지점이고, "
      "막대가 늦게 시작하는 자리가 새로 생긴 지점이다.",
      "1.4.0 경계에서 하나가 끝나고 하나가 시작합니다")

LX, TX, TW = 20, 220, 720
COLS = ["1.2 이전", "1.3", "1.4", "현재 (master)"]
PITCH = TW / len(COLS)

for i, nm in enumerate(COLS):
    d.t(TX + PITCH * i + PITCH / 2, 116, nm, 12, SOFT, MONO)
d.line(TX, 128, TX + TW, 128, RULE, 1.0)

rows = [
    ("stubzones", 0, 2, BAD, None),
    ("upstream", 0, 1, BAD, None),
    ("fallthrough", 0, 4, OK, None),
    ("path", 0, 4, OK, None),
    ("endpoint", 0, 4, OK, None),
    ("tls", 0, 4, OK, None),
    ("credentials", 2, 2, OK, None),
    ("no_apex_fallback", 3, 1, INFO, "5 4"),
    ("min-lease-ttl", 3, 1, INFO, "5 4"),
    ("max-lease-ttl", 3, 1, INFO, "5 4"),
]


def row_y(k):
    return 168 + k * 40 + (36 if k >= 7 else 0)


d.box(204, 136, 752, 304, PAPER, RULE, 0.8, 6)
d.t(212, 156, "원서가 적은 일곱", 11, SOFT, MONO, "start", 600)
d.box(204, 452, 752, 144, PAPER, RULE, 0.8, 6)
d.t(212, 472, "원서 이후 붙은 셋", 11, SOFT, MONO, "start", 600)

for k, (nm, start, span, color, dash) in enumerate(rows):
    ry = row_y(k)
    d.t(LX, ry + 22, nm, 13, INK, MONO, "start", 600)
    for s in range(1, len(COLS)):
        c = ACC if s == 2 else RULE
        d.line(TX + PITCH * s, ry + 2, TX + PITCH * s, ry + 34, c, 0.8 if s != 2 else 1.2, "3 5")
    x = TX + PITCH * start
    w = PITCH * span
    if dash:
        d.o.append(f'<rect x="{x + 8}" y="{ry + 6}" width="{w - 16}" height="24" rx="4" '
                   f'fill="{color}16" stroke="{color}" stroke-width="1.2" stroke-dasharray="{dash}"/>')
    else:
        d.tone(x + 8, ry + 6, w - 16, 24, color, 4, "16", 1.2)

d.t(TX + PITCH * 2, 628, "1.4.0 — stubzones 가 끝나고 credentials 가 시작한다", 13, ACC, KR)
d.t(LX, 660, "원서 이후 붙은 셋은 master 문법에 있다는 것만 확인했고 도입 버전은 확인하지 못했다", 13, MUTED, KR, "start")

d.legend(684, [("지금 문법에 없다", BAD), ("그대로 남았다", OK), ("원서 이후 추가", INFO), ("원서가 적은 경계", ACC)])
d.save("05-01.option-lifespan.svg")

# 06-04 §1 — 원서가 싣는 kubernetes 플러그인 문법 항목이 어느 릴리스까지 살았는가.
# 원문 근거: resyncperiod 는 "The default is 5 minutes in versions before 1.5.0, and never in 1.5.0
#            and later. This option will be eliminated in later versions." / upstream 은 "obsolete in
#            CoreDNS 1.3.0 and later" (같은 장 다른 자리는 1.4).
# 릴리스 노트 근거(2026-10-03 확인): 1.5.0 "The resyncperiod option ... is deprecated", 1.6.0 "removes the
#            resyncperiod option", 1.3.1 upstream 이 1.4.0 부터 CoreDNS 자신을 기본으로, 1.7.0 "Remove
#            already-deprecated options resyncperiod and upstream", 1.8.0 transfer 플러그인. 현재 setup.go 는
#            세 항목을 모르는 속성으로 거부한다.
# 타입 스펙: type-gantt — 막대의 시작·끝이 곧 그 항목이 살아 있던 버전 구간이다.
#           축약: 가로축이 날짜가 아니라 CoreDNS 버전 구간이다(같은 폴더 05-01 과 같은 축약).
#           원서 이후 붙은 항목은 도입 버전을 확인하지 못해 마지막 칸에만 점선으로 둔다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, RULE, OK, WARN, BAD, INFO, KR, MONO

W, H = 1000, 600
d = D(W, H, "LEARNING COREDNS · 06-04 §1",
      "원서의 문법 항목이 어느 릴리스까지 살았나",
      "가로축은 CoreDNS 버전 구간이다. 초록은 뜻대로 동작하던 구간, 노랑은 남아 있지만 효과가 없거나 폐기 예고를 받은 구간이고, "
      "막대가 끝나는 자리가 릴리스 노트가 적은 제거 시점이다.",
      "주황 점선이 원서가 적은 1.5.0 경계입니다")

LX, TX, TW = 20, 250, 700
COLS = ["1.2 이전", "1.3", "1.4", "1.5", "1.6", "1.7", "1.8 이후"]
PITCH = TW / len(COLS)

for i, nm in enumerate(COLS):
    d.t(TX + PITCH * i + PITCH / 2, 116, nm, 12, SOFT, MONO)
d.line(TX, 128, TX + TW, 128, RULE, 1.0)

# (이름, 메모, [(시작칸, 칸수, 색, 점선)], 제거 라벨 칸)
rows = [
    ("resyncperiod", "1.5.0 폐기 예고 · 1.6.0 제거", [(0, 3, OK, None), (3, 1, WARN, None)], (4, "1.6.0 제거")),
    ("upstream", "1.4 부터 기본 동작 · 1.7.0 제거", [(0, 1, OK, None), (1, 4, WARN, None)], (5, "1.7.0 제거")),
    ("transfer to", "transfer 플러그인으로 이사", [(0, 6, OK, None)], (6, "1.8.0 이사")),
    ("나머지 열하나", "endpoint · tls · pods · ttl …", [(0, 7, OK, None)], None),
    ("원서 이후 붙은 것들", "apiserver_qps 계열 · zonal …", [(6, 1, INFO, "5 4")], None),
]


def row_y(k):
    return 168 + k * 56


for k, (nm, note, segs, cut) in enumerate(rows):
    ry = row_y(k)
    d.t(LX, ry + 18, nm, 13, INK, MONO if k < 3 else KR, "start", 600)
    d.t(LX, ry + 38, note, 12, MUTED, KR, "start")
    for s in range(1, len(COLS)):
        c = ACC if s == 3 else RULE
        d.line(TX + PITCH * s, ry - 2, TX + PITCH * s, ry + 44, c, 0.8 if s != 3 else 1.2, "3 5")
    for start, span, color, dash in segs:
        x = TX + PITCH * start
        w = PITCH * span
        if dash:
            d.o.append(f'<rect x="{x + 6}" y="{ry + 6}" width="{w - 12}" height="30" rx="4" '
                       f'fill="{color}16" stroke="{color}" stroke-width="1.2" stroke-dasharray="{dash}"/>')
            d.t(x + w / 2, ry + 26, "master", 12, INFO, MONO)
        else:
            d.tone(x + 6, ry + 6, w - 12, 30, color, 4, "16", 1.2)
    if cut:
        cx = TX + PITCH * cut[0]
        d.t(cx + 8, ry + 26, cut[1], 12, BAD, KR, "start", 600)

d.t(TX + PITCH * 3, 468, "1.5.0 · resyncperiod 기본 5분 → 하지 않음", 13, ACC, KR)
d.t(LX, 500, "제거 시점 · 릴리스 노트 1.5.0 · 1.6.0 · 1.7.0 · 1.8.0 · 지금 쓰면 모르는 속성으로 거부", 13, MUTED, KR, "start")
d.t(LX, 522, "원서 이후 붙은 항목 · 도입 버전 미확인 · master 문법에서 확인", 12, SOFT, KR, "start")

d.legend(540, [("뜻대로 동작", OK), ("효과 없음 · 폐기 예고", WARN), ("원서 이후 추가", INFO), ("원서가 적은 경계", ACC)])
d.save("06-04.option-lifespan.svg")

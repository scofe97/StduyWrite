# 06-04 §1 — 원서가 싣는 kubernetes 플러그인 문법 항목이 지금 어디까지 유효한가.
# 원문 근거: resyncperiod 는 "The default is 5 minutes in versions before 1.5.0, and never in 1.5.0
#            and later. This option will be eliminated in later versions." / upstream 은 "obsolete in
#            CoreDNS 1.3.0 and later" / transfer to 는 존 전송 기능을 켠다.
# 공식 근거: master 의 plugin/kubernetes/README.md 문법 블록에 resyncperiod·upstream·transfer to 가
#            없고, apiserver_qps 계열·namespace_labels·multicluster·zonal·startup_timeout 이 있다.
#            정확히 어느 릴리스에서 걷혔는지는 확인하지 못해 오른쪽 끝을 "현재" 로만 둔다.
# 타입 스펙: type-gantt — 막대의 시작점과 길이가 곧 그 항목이 유효한 구간이다.
#           축약: 가로축이 날짜가 아니라 CoreDNS 버전 구간이다(같은 폴더 05-01 과 같은 축약).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, RULE, OK, BAD, INFO, KR, MONO

W, H = 1000, 560
d = D(W, H, "LEARNING COREDNS · 06-04 §1",
      "원서의 문법 항목이 지금 어디까지 유효한가",
      "가로축은 날짜가 아니라 CoreDNS 버전 구간이다. 막대가 끊긴 자리가 그 항목이 문법에서 사라진 지점이고, "
      "제거를 예고한 것은 resyncperiod 하나뿐이다.",
      "1.5.0 경계에서 resyncperiod 의 성격이 바뀝니다")

LX, TX, TW = 20, 250, 690
COLS = ["1.2 이전", "1.3", "1.4", "1.5", "현재"]
PITCH = TW / len(COLS)

for i, nm in enumerate(COLS):
    d.t(TX + PITCH * i + PITCH / 2, 116, nm, 12, SOFT, MONO)
d.line(TX, 128, TX + TW, 128, RULE, 1.0)

rows = [
    ("resyncperiod", 0, 4, BAD, None, "1.5.0 부터 아예 안 한다"),
    ("upstream", 0, 1, BAD, None, "1.3.0 부터 무의미"),
    ("transfer to", 0, 4, BAD, None, "transfer 플러그인으로 옮겨 갔다"),
    ("나머지 열하나", 0, 5, OK, None, "endpoint · tls · pods · ttl …"),
    ("원서 이후 붙은 것들", 4, 1, INFO, "5 4", "apiserver_qps 계열 · multicluster · zonal"),
]


def row_y(k):
    return 168 + k * 48


for k, (nm, start, span, color, dash, note) in enumerate(rows):
    ry = row_y(k)
    d.t(LX, ry + 18, nm, 13, INK, MONO, "start", 600)
    d.t(LX, ry + 38, note, 11, MUTED, KR, "start")
    for s in range(1, len(COLS)):
        c = ACC if s == 3 else RULE
        d.line(TX + PITCH * s, ry - 2, TX + PITCH * s, ry + 40, c, 0.8 if s != 3 else 1.2, "3 5")
    x = TX + PITCH * start
    w = PITCH * span
    if dash:
        d.o.append(f'<rect x="{x + 8}" y="{ry + 6}" width="{w - 16}" height="28" rx="4" '
                   f'fill="{color}16" stroke="{color}" stroke-width="1.2" stroke-dasharray="{dash}"/>')
    else:
        d.tone(x + 8, ry + 6, w - 16, 28, color, 4, "16", 1.2)

d.t(TX + PITCH * 3, 428, "1.5.0 — resyncperiod 가 \"기본 5분\" 에서 \"하지 않음\" 으로 바뀐다", 13, ACC, KR)
d.t(LX, 460, "셋이 사라진 정확한 릴리스는 확인하지 못했고, master 문법 블록에 없다는 것만 확인했다", 13, MUTED, KR, "start")

d.legend(488, [("지금 문법에 없다", BAD), ("그대로 남았다", OK), ("원서 이후 추가", INFO), ("원서가 적은 경계", ACC)])
d.save("06-04.option-lifespan.svg")

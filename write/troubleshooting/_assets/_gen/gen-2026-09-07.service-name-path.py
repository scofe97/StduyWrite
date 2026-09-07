# 2026-09-07 D2 — 이름 하나가 Pod 에 닿기까지 지나는 두 관문과, 각 관문이 실패할 때
# 클라이언트가 보는 서로 다른 증상. 학습자가 "타임아웃이니 DNS 는 성공"까지 추론했으므로
# 그 추론이 어디서 갈리는지를 형태로 남긴다.
# 타입 스펙: type-flowchart — 조건에 따라 갈라지는 판단 논리. 도형이 종류를 나른다
#           (타원=시작·끝, 사각형=조치·결과, 마름모=판단). focal 은 이 문항의 답이 된 판단.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, BAD, WARN, PAPER2, RULE, KR, MONO

W, H = 900, 728
CX, RX = 296, 686

d = D(W, H, "TROUBLESHOOTING DRILL · 2026-09-07 D2",
      "이름이 Pod 에 닿기까지",
      "Service 이름으로 부를 때만 지나는 두 관문. 첫째는 이름을 주소로 바꾸는 일이고 둘째는 그 주소가 "
      "어느 Pod 로 갈지 아는 일이다. 어느 쪽이 막혔느냐에 따라 클라이언트가 보는 증상이 다르다.",
      lead="이름 해석이 실패하면 즉시 오류가, 대상 목록이 비면 타임아웃이 돌아옵니다")

def oval(cx, y, w, h, txt, c=INK):
    d.o.append(f'<rect x="{cx - w / 2}" y="{y}" width="{w}" height="{h}" rx="20" '
               f'fill="{PAPER2}" stroke="{c}" stroke-width="1.1"/>')
    d.t(cx, y + h / 2 + 5, txt, 13, c, KR, "middle", 600)

def step(cx, y, w, h, title, sub, c=None):
    if c: d.tone(cx - w / 2, y, w, h, c, 6)
    else: d.box(cx - w / 2, y, w, h, PAPER2, RULE, 1.0, 6)
    d.t(cx, y + 26, title, 13, c if c else INK, KR, "middle", 600)
    d.t(cx, y + 46, sub, 11, MUTED, KR)

def diamond(cx, y, hw, hh, txt, focal=False):
    cy, c = y + hh, (ACC if focal else INK)
    d.o.append(f'<polygon points="{cx},{y} {cx + hw},{cy} {cx},{y + 2 * hh} {cx - hw},{cy}" '
               f'fill="{ACC + "12" if focal else PAPER2}" stroke="{c}" stroke-width="{1.4 if focal else 1.1}"/>')
    d.t(cx, cy + 5, txt, 12, c, KR, "middle", 600)

Y_S, Y_D1, Y_D2, Y_A, Y_END = 100, 176, 312, 448, 556

d.arrow([(CX, Y_S + 40), (CX, Y_D1 - 4)], MUTED, "ar", 1.4)
d.arrow([(CX, Y_D1 + 84), (CX, Y_D2 - 4)], MUTED, "ar", 1.4)
d.arrow([(CX, Y_D2 + 84), (CX, Y_A - 4)], MUTED, "ar", 1.4)
d.arrow([(CX, Y_A + 68), (CX, Y_END - 4)], MUTED, "ar", 1.4)
d.arrow([(CX + 152, Y_D1 + 42), (RX - 164, Y_D1 + 42)], SOFT, "ar", 1.4)
d.arrow([(CX + 152, Y_D2 + 42), (RX - 164, Y_D2 + 42)], BAD, "ar", 1.4)

oval(CX, Y_S, 268, 40, "curl http://payment:8080")
diamond(CX, Y_D1, 150, 42, "이름이 주소로 풀리는가?")
diamond(CX, Y_D2, 150, 42, "EndpointSlice 에 대상이 있는가?", focal=True)
step(CX, Y_A, 320, 68, "노드 규칙이 주소를 바꿔칩니다",
     "ClusterIP 10.96.140.22 → Pod IP 10.244.2.17")
oval(CX, Y_END, 268, 40, "Pod 도착 · ok", OK)

step(RX, Y_D1, 320, 68, "Could not resolve host",
     "즉시 실패 · exit 6", c=WARN)
step(RX, Y_D2, 320, 68, "Operation timed out",
     "갈 곳이 없어 조용히 사라짐 · exit 28", c=BAD)

d.t(CX + 12, Y_D1 + 104, "풀린다", 11, MUTED, KR, "start", 600)
d.t(CX + 12, Y_D2 + 104, "있다", 11, MUTED, KR, "start", 600)
d.t(CX + 168, Y_D1 + 30, "못 푼다", 11, SOFT, KR, "start")
d.t(CX + 168, Y_D2 + 30, "비었다", 11, BAD, KR, "start", 600)

d.t(24, Y_D2 + 24, "Pod IP 직접", 11, SOFT, KR, "start")
d.t(24, Y_D2 + 42, "호출이 성공한", 11, SOFT, KR, "start")
d.t(24, Y_D2 + 60, "것이 앱·포트·", 11, SOFT, KR, "start")
d.t(24, Y_D2 + 78, "정책을 한꺼번에", 11, SOFT, KR, "start")
d.t(24, Y_D2 + 96, "배제합니다", 11, SOFT, KR, "start")

d.t(CX - 160, Y_END + 60, "목록이 비는 원인은 둘입니다. selector 와 Pod 라벨이 어긋났거나, targetPort 가 컨테이너 포트와 다릅니다.",
    12, MUTED, KR, "start")

d.legend(H - 56, [("이 문항의 답이 된 판단", ACC), ("타임아웃이 되는 경로", BAD), ("즉시 실패", WARN), ("정상 도착", OK)])
d.save("2026-09-07.service-name-path.svg")
print("ok service-name-path")

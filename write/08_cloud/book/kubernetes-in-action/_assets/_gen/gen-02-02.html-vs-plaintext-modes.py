# 02-02 §1 — 같은 두 서비스를 어디서 부르는가
# 본문 근거(02-02.Kiada 애플리케이션 빌드와 배포.md §1):
#   요약: "두 모드는 Quote·Quiz 서비스를 클러스터 안팎 어디서 호출하는지가 갈립니다."
#   HTML: "클라이언트 쪽 자바스크립트가 Quote·Quiz 라는 두 개의 RESTful 서비스에서 …가져옵니다."
#         "브라우저는 세 서비스와 직접 통신합니다. API 게이트웨이가 따로 없는데 … 일부러 넣지 않았습니다."
#   평문: "Node.js 애플리케이션이 그 서비스들을 클러스터 안에서 대신 호출하고, 그 결과를 하나로 합쳐 응답합니다."
#   결론: "두 서비스는 내부·외부 양쪽으로 노출돼야 합니다."
# 타입 스펙: 절 요약이 '두 모드가 …갈립니다' 라고 형태를 지정한다 → 비교(두 레인).
#   기존 Mermaid 두 장(구성도 + 시퀀스)은 한 절에 도식 둘을 두면서도 '어디서 부르는가' 라는
#   갈림 자체는 그리지 못했다. 한 장으로 합치면서 그 대비를 그림의 축으로 올린다.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO
import ddx

BA0, BA1 = 104, 344          # HTML 모드 띠
BB0, BB1 = 360, 600          # 평문 모드 띠
CONC_Y, CONC_H = 616, 56     # 결론 — 두 모드가 함께 요구하는 것
LEG_Y = CONC_Y + CONC_H + 16
W, H = 1000, LEG_Y + 44

d = D(W, H, "KUBERNETES IN ACTION · 02-02",
      "같은 서비스를 어디서 부르는가",
      "Kiada 는 HTML 모드와 평문 모드를 함께 제공한다. 두 모드가 부르는 서비스는 같지만 "
      "부르는 자리가 클러스터 바깥과 안으로 갈리고, 그 갈림이 노출 요구사항을 만든다.",
      lead="브라우저가 직접 부르느냐, Node.js 앱이 대신 부르느냐 — 갈리는 것은 호출 주체와 자리다")


def node(cx, cy, t, s, c, w=232, h=52):
    d.box(cx - w // 2, cy - h // 2, w, h, PAPER2, c, 1.1, 6)
    d.t(cx, cy - 4, ddx.fit(t, 13, w - 20, t), 13, c,
        MONO if all(ord(ch) < 128 for ch in t) else KR, "middle", 600)
    d.t(cx, cy + 16, ddx.fit(s, 10, w - 16, s), 10, SOFT, KR)


# ── HTML 모드 — 브라우저가 클러스터 바깥에서 세 서비스를 직접 부른다
ddx.band(d, BA0, BA1, "HTML 모드 — 브라우저가 바깥에서 직접 부른다", bar=INFO, focal=False)
d.box(40, 148, 176, 168, PAPER2, INFO, 1.1, 6)
d.t(128, 224, "웹 브라우저", 13, INFO, KR, "middle", 600)
d.t(128, 244, "클러스터 바깥", 10, SOFT, KR)
for cy, (t, s) in zip((176, 240, 304), (
        ("Web", "Node.js 가 HTML 을 서빙한다"),
        ("Quote service", "REST — 인용문을 준다"),
        ("Quiz service", "REST — 퀴즈 문제를 준다"))):
    node(452, cy, t, s, INFO)
    d.path(f"M 222 {cy} L 326 {cy}", INFO, 1.5, m="info")
d.t(600, 216, "브라우저가 세 서비스와 직접 통신한다", 11, MUTED, KR, "start")
d.t(600, 240, "API 게이트웨이는 일부러 두지 않았다 — 게이트웨이 뒤에", 10, SOFT, KR, "start")
d.t(600, 258, "묶이지 않은 서비스들의 문제를 보이려는 의도다", 10, SOFT, KR, "start")

# ── 평문 모드 — Node.js 앱이 클러스터 안에서 대신 부르고 합친다
ddx.band(d, BB0, BB1, "평문 모드 — Node.js 앱이 안에서 대신 부른다", bar=OK, focal=False)
node(128, 480, "curl", "터미널 클라이언트", OK, w=176)
node(452, 480, "Node.js Web App", "받아서 하나로 합친다", OK)
node(800, 440, "Quote service", "클러스터 안에서 호출", OK, w=200)
node(800, 524, "Quiz service", "클러스터 안에서 호출", OK, w=200)
d.path("M 222 480 L 326 480", OK, 1.5, m="ok")
d.t(274, 468, "GET /text", 10, OK, MONO)
d.path("M 574 480 L 640 480 L 640 440 L 690 440", OK, 1.5, m="ok")
d.path("M 574 480 L 640 480 L 640 524 L 690 524", OK, 1.5, m="ok")
d.path("M 452 506 L 452 566 L 128 566 L 128 510", MUTED, 1.4, m="ar", dash="6 5")
d.t(290, 556, "합쳐진 평문 응답 하나", 10, MUTED, KR)

# ── 결론 — 두 모드가 함께 요구하는 것. 도식의 focal 은 여기 하나.
d.o.append(f'<rect x="24" y="{CONC_Y}" width="952" height="{CONC_H}" rx="8" '
           f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t(44, CONC_Y + 24, "그래서 Quote·Quiz 는 내부·외부 양쪽으로 노출돼야 한다", 12, ACC, KR, "start", 600)
d.t(44, CONC_Y + 44, "평문 모드는 클러스터 안에서, HTML 모드는 바깥에서 같은 서비스에 닿는다. "
                     "노출을 한쪽만 열면 다른 모드가 끊긴다.", 10, SOFT, KR, "start")

d.legend(LEG_Y, [("바깥에서 직접 부르는 길", INFO), ("안에서 대신 부르는 길", OK),
                 ("두 모드가 함께 요구하는 것", ACC)])
d.save("02-02-html-vs-plaintext-modes.svg")
print("ok html-vs-plaintext-modes")

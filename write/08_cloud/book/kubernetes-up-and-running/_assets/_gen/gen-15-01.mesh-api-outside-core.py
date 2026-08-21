# 15-01 §코어 네트워킹은 왜 부족한가
# 이 절은 토폴로지가 아니라 API 설계 논증이다. 제목의 "밀어냈다" 가 형태를 정한다 —
# 호환해야 하는 폭이 능력을 눌렀다는 인과. 그래서 두 API 를 같은 축(호환 폭 · 그 결과 능력)에
# 나란히 놓고, 폭을 나타내는 막대 길이 자체가 논증이 되게 한다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, MUTED, SOFT, INK, PAPER2, PAPER, RULE, KR, MONO
import ddx

W, H = 1240, 622
d = D(W, H, "KUBERNETES UP AND RUNNING · 15-01",
      "아울러야 할 폭이 능력을 눌렀다",
      "코어의 네트워킹은 애플리케이션을 오직 목적지로만 안다. Ingress 가 조금 더 나아가지만, "
      "기존 구현체를 폭넓게 아우르는 공통 API 여야 한다는 과제가 그 능력을 제한했다.",
      "메시 API 가 코어 밖에서 자란 것은 그 과제의 결과다")

PY0, PY1 = 118, 430

def panel(px, title, where, span_w, span_note, caps, focal=False):
    d.box(px, PY0, 600, PY1 - PY0, PAPER2, RULE, 1.0, 8)
    d.t(px + 24, 148, title, 14, INK, KR, "start", 600)
    d.t(px + 576, 148, where, 10, SOFT, KR, "end")
    d.line(px + 24, 162, px + 576, 162, RULE, 0.8)

    d.t(px + 24, 190, "호환해야 하는 것", 10, SOFT, KR, "start")
    bx0, by = px + 24, 214
    c = ACC if focal else OK
    d.line(bx0, by, bx0 + span_w, by, c, 2.0)
    for x in (bx0, bx0 + span_w):
        d.line(x, by - 7, x, by + 7, c, 2.0)
    for i, n in enumerate(n for n in span_note if n):
        d.t(bx0, by + 26 + i * 19, n, 10, SOFT, KR, "start")
    if focal:   # 막대가 길면 그 위에 얹고, 짧으면 옆에 붙인다 — 가운데 정렬하면 왼쪽으로 넘친다
        d.t(bx0 + span_w / 2, by - 14, "이 폭을 공통 API 하나가 전부 아울러야 한다", 11, c, KR)
    else:
        d.t(bx0 + span_w + 18, by + 4, "여기까지다 — 기존 인프라와의 호환 의무가 없다", 11, c, KR, "start")

    d.t(px + 24, 306, "그래서 가능한 능력", 10, SOFT, KR, "start")
    for i, cap in enumerate(caps):
        yy = 324 + i * 28
        d.o.append(f'<rect x="{px+24}" y="{yy}" width="552" height="22" rx="4" '
                   f'fill="{PAPER}" stroke="{RULE}" stroke-width="0.8"/>')
        d.t(px + 36, yy + 15, cap, 10, MUTED, KR, "start")

panel(12, "Ingress API", "코어 안", 552,
      ["왼쪽 끝 — 베어메탈 네트워크 장비",
       "오른쪽 끝 — 클라우드 네이티브를 염두에 두지 않고 만들어진 퍼블릭 클라우드 API"],
      ["목적지로 보낸다 — label selector 로 고른 파드 집합",
       "HTTP 로드밸런서로서 조금 더 나아간다",
       "그 너머로 더 해 주는 일은 비교적 적다"], focal=True)
panel(628, "메시 API", "코어 밖 · CRD 로 더한다", 150,
      ["클러스터 안쪽 파드 사이만 본다", ""],
      ["암호화와 신원 — mTLS 로 모든 파드 사이에 자동으로",
       "트래픽 셰이핑 — 10% 는 Y, 90% 는 X 를 선언으로",
       "내부 관찰 — 흩어진 요청을 하나로 되맞춘다"])

CY = 498
for x, lab, sub in ((140, "바깥세상", "HTTP(S) 트래픽"),
                    (500, "클러스터 안", "클라우드 네이티브 애플리케이션"),
                    (860, "파드 사이", "서로 부르는 마이크로서비스")):
    ddx.node(d, x + 120, CY, lab, sub, w=240, h=68)
d.path("M 380 498 L 496 498", MUTED, 1.5, m="ar")
d.path("M 740 498 L 856 498", MUTED, 1.5, m="ar")
d.t(438, 478, "Ingress API 가 들여온다", 10, SOFT, KR)
d.t(798, 478, "메시 API 가 능력을 더한다", 10, SOFT, KR)

d.legend(566, [("호환 폭이 능력을 누른 자리", ACC), ("호환 의무가 없는 자리", OK)])
d.save("15-01.mesh-api-outside-core.svg")
print("h 필요:", 566 + 48, " 실제:", H)

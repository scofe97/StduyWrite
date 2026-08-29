# 21-01 §배치 모델 셋
# 본문이 "나란한 선택지가 아니라 성장에 따라 밀려나는 단계" 라고 못 박는다. 그러니 셋을
# 카드로 늘어놓기만 하면 논지가 죽는다 — 방향이 있어야 하고, 각 칸이 *앞 칸의 무엇이
# 아파서* 다음으로 밀려나는지를 적어야 한다.
# 16-01 storage-three-paths 와 같은 형태를 쓰되, 거기서 "포기하는 것" 이던 칸을
# "다음으로 밀리는 이유" 로 바꾼다. 마지막 칸에는 밀려날 곳이 없으므로 대가를 적는다.
# 타입 스펙: type-process.md — 세 모델이 같은 의미 슬롯(이름 · 얻는 것 · 다음으로 밀리는 이유)으로
#           반복되고 칸 사이를 화살표가 잇는다. 본문이 "나란한 선택지가 아니라 성장에 따라
#           밀려나는 단계" 라고 못 박으므로 방향이 반드시 있어야 한다.
#           어긋나는 지점: 정본의 lane=주체가 없고 열이 단계다. 마지막 칸은 밀려날 곳이 없어
#           같은 슬롯에 "치러야 할 것" 을 적는다 — 라벨이 하나만 다르다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, MUTED, SOFT, INK, PAPER2, PAPER, RULE, INFO, KR, MONO
import ddx

W, H = 1240, 588
d = D(W, H, "KUBERNETES UP AND RUNNING · 21-01",
      "셋은 선택지가 아니라 밀려나는 단계다",
      "가장 단순한 것에서 시작해, 그것이 아파지는 지점에서 다음으로 넘어간다. "
      "어디에 설지는 애플리케이션마다 다르고 자라면서 바뀐다.",
      "원서 21장 — 바뀔 것을 전제로 설계해 두면 대규모 리팩터링을 피한다")

CW, GAP = 386, 18
Y0, CH = 138, 308
CARDS = [
    ("01 · 복제 사일로", "모든 리전에 그대로 복사",
     ["요청이 들어온 리전 안에서 끝까지 처리", "애플리케이션을 크게 바꾸지 않아도 된다"],
     "가장 큰 지역에 맞춰 사이징한다", "작은 지역의 복제본이 크게 남는다", WARN, "가장 쉬운 시작"),
    ("02 · 리전 샤딩", "데이터를 나눠 일부 리전에만",
     ["전역 복제 비용이 준다", "데이터 위치 규제를 지킬 수 있다"],
     "라우팅 계층이 필요해진다", "라이브러리 말고 별도 마이크로서비스로", ACC, "저자의 강한 권고"),
    ("03 · 마이크로서비스 라우팅", "서비스마다 자체 LB 와 복제",
     ["팀마다 독립적으로 확장·배포한다", "사일로라는 더 큰 모놀리스를 깬다"],
     "서비스 수만큼 비용이 붙는다", "LB 유지 비용과 리전 간 트래픽", BAD, "가장 유연하고 가장 비싸다"),
]
for i, (title, sub, gains, cost, costsub, c, tag) in enumerate(CARDS):
    x = 24 + i * (CW + GAP)
    focal = c is ACC
    if focal:
        d.tone(x, Y0, CW, CH, c, 8, "0C", 1.5)
    else:
        d.box(x, Y0, CW, CH, PAPER2, RULE, 1.0, 8)
    d.t(x + 20, Y0 + 30, title, 13, c, KR, "start", 600)
    d.t(x + CW - 20, Y0 + 30, tag, 9, SOFT, KR, "end")
    d.t(x + 20, Y0 + 54, ddx.fit(sub, 11, CW - 40, sub), 11, MUTED, KR, "start")
    d.line(x + 20, Y0 + 70, x + CW - 20, Y0 + 70, RULE, 0.8)

    d.t(x + 20, Y0 + 94, "얻는 것", 9, OK, KR, "start")
    for j, g in enumerate(gains):
        yy = Y0 + 106 + j * 32
        d.o.append(f'<rect x="{x+20}" y="{yy}" width="{CW-40}" height="26" rx="4" '
                   f'fill="{PAPER}" stroke="{RULE}" stroke-width="0.8"/>')
        d.t(x + 32, yy + 17, ddx.fit(g, 10, CW - 64, g), 10, MUTED, KR, "start")

    d.t(x + 20, Y0 + 190, "다음으로 밀리는 이유" if i < 2 else "치러야 할 것", 9, SOFT, KR, "start")
    d.o.append(f'<rect x="{x+20}" y="{Y0+200}" width="{CW-40}" height="56" rx="5" '
               f'fill="{c}12" stroke="{c}" stroke-width="1.2"/>')
    d.t(x + CW / 2, Y0 + 224, ddx.fit(cost, 12, CW - 60, cost), 12, c, KR, "middle", 600)
    d.t(x + CW / 2, Y0 + 244, ddx.fit(costsub, 10, CW - 60, costsub), 10, c, KR)
    if i < 2:
        d.arrow([(x + CW + 2, Y0 + CH / 2), (x + CW + GAP - 2, Y0 + CH / 2)], SOFT, "soft", 1.3)

BY = Y0 + CH + 26
d.line(24, BY, W - 48, BY, RULE, 0.8)
d.t(24, BY + 24, "가운데 칸의 권고가 이 장에서 가장 실무적이다 — 데이터 라우팅을 모든 서비스가 "
                 "각자 걱정하는 대신 한 서비스가 캡슐화한다. 서비스를 더하는 것이 오히려 단순화다.",
    11, ACC, KR, "start")
d.legend(BY + 40, [("저자가 못 박는 자리", ACC), ("감당되는 비용", WARN), ("가장 큰 대가", BAD)])
d.save("21-01.three-models.svg")
print("필요 h:", BY + 40 + 48, "· 실제:", H)

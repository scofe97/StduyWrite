# 20-01 §설치 — 웹훅은 셋인데, 원서가 안 보여 준 것과 없던 것은 다르다
# 본문이 표로 셋을 나열하므로 도식은 표를 되풀이하면 안 된다. 표가 못 보이는 것은
# *failurePolicy 가 왜 갈리는가* 다 — 검증은 열고 실패하는데 레이블 검사만 닫고 실패한다.
# 그러니 세 웹훅을 나란히 놓되 "실패하면 어떻게 되는가" 를 같은 자리에 붙여, 하나만
# 색이 다른 것이 형태로 보이게 한다.
# ⚠ 초판 도식은 아래 칸을 "원서에 없음" 으로 적었다가 적대적 검증에서 반증됐다. 원서는
# 웹훅 출력을 `...` 로 생략했을 뿐이고, 두 번째 웹훅은 원서보다 앞선 차트에도 있었다.
# 생략을 부재로 읽은 것이므로, 아래 칸은 "원서가 무엇을 보여 줬는가" 만 적는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, MUTED, SOFT, INK, PAPER2, PAPER, RULE, INFO, KR, MONO
import ddx

W, H = 1240, 592
d = D(W, H, "KUBERNETES UP AND RUNNING · 20-01",
      "정책 엔진이 죽어도 클러스터는 멈추지 않는다",
      "세 웹훅 중 둘은 열고 실패한다. 닫고 실패하는 것은 우회를 막는 하나뿐이다.",
      "kind 로컬 클러스터 실측 — Gatekeeper v3.23.0 · 원서는 출력을 … 로 생략한다")

CW, GAP = 386, 18
Y0, CH = 132, 306
CARDS = [
    ("validation.gatekeeper.sh", "ValidatingWebhookConfiguration", "Ignore", "열고 실패한다",
     "3초 안에 답이 없으면 요청을 그냥 통과시킨다", "원서가 본문에 싣는 것", MUTED, False),
    ("check-ignore-label.gatekeeper.sh", "같은 리소스 · namespaces 만", "Fail", "닫고 실패한다",
     "우회용 레이블을 붙이는 행위 자체를 막는다", "원서는 … 로 생략", ACC, True),
    ("mutation.gatekeeper.sh", "MutatingWebhookConfiguration", "Ignore", "열고 실패한다",
     "원서는 이 설치로는 안 켜진다고 적는다", "그 명령으로는 안 보인다", WARN, False),
]
for i, (name, target, fp, fpk, why, orig, c, focal) in enumerate(CARDS):
    x = 24 + i * (CW + GAP)
    if focal:
        d.tone(x, Y0, CW, CH, c, 8, "0C", 1.5)
    else:
        d.box(x, Y0, CW, CH, PAPER2, RULE, 1.0, 8)
    d.t(x + 20, Y0 + 30, ddx.fit(name, 12, CW - 40, name), 12, c, MONO, "start", 600)
    d.t(x + 20, Y0 + 52, ddx.fit(target, 10, CW - 40, target), 10, SOFT, KR, "start")
    d.line(x + 20, Y0 + 68, x + CW - 20, Y0 + 68, RULE, 0.8)

    d.t(x + 20, Y0 + 92, "failurePolicy", 9, SOFT, KR, "start")
    fc = BAD if fp == "Fail" else OK
    d.o.append(f'<rect x="{x+20}" y="{Y0+102}" width="{CW-40}" height="58" rx="6" '
               f'fill="{fc}12" stroke="{fc}" stroke-width="1.3"/>')
    d.t(x + CW / 2, Y0 + 126, fp, 15, fc, MONO, "middle", 600)
    d.t(x + CW / 2, Y0 + 148, fpk, 11, fc, KR)

    d.t(x + 20, Y0 + 186, "왜", 9, SOFT, KR, "start")
    d.t(x + 20, Y0 + 206, ddx.fit(why, 10, CW - 40, why), 10, MUTED, KR, "start")

    d.o.append(f'<rect x="{x+20}" y="{Y0+232}" width="{CW-40}" height="50" rx="5" '
               f'fill="{PAPER}" stroke="{c if focal else RULE}" stroke-width="{1.2 if focal else 0.8}"/>')
    d.t(x + CW / 2, Y0 + 254, orig, 12, c if focal else SOFT, KR, "middle", 600 if focal else 400)
    d.t(x + CW / 2, Y0 + 272, "설치 명령은 원서와 같다", 9, SOFT, KR)

BY = Y0 + CH + 26
d.line(24, BY, W - 48, BY, RULE, 0.8)
d.t(24, BY + 24, "검증 웹훅은 admission.gatekeeper.sh/ignore 레이블이 붙은 네임스페이스를 건너뛴다. "
                 "그 레이블을 아무나 붙일 수 있으면 정책 전체가 우회된다.", 11, MUTED, KR, "start")
d.t(24, BY + 46, "그래서 레이블을 붙이는 길만 닫고 지킨다 — 가운데 카드가 유일하게 Fail 인 이유다. "
                 "원서가 안 보여 준 것이지 없던 것이 아니다.", 11, ACC, KR, "start")
d.legend(BY + 62, [("원서가 생략한 자리", ACC), ("열고 실패", OK), ("닫고 실패", BAD), ("원서가 안 켜진다고 한 것", WARN)])
d.save("../20-01.webhook-topology.svg")
print("필요 h:", BY + 62 + 48, "· 실제:", H)

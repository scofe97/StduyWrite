# 19-01 §NetworkPolicy — kindnet 에서도 강제됩니다
# 이 랩은 "이렇게 하면 된다" 가 아니라 "걸었더니 이렇게 되더라" 의 3 연속이다. 그래서 단계
# 사슬이 아니라 *시도와 응답을 짝지은 사다리* 로 그린다(17-01 랩 도식과 같은 형태).
# 응답은 지어내지 않고 본문이 실측해 적어 둔 문자열을 그대로 옮긴다.
# 가운데 줄이 초점이다 — 여기서 막히는 것이 kindnet 이 정책을 집행한다는 증거이고,
# 로컬 kind 에서는 안 될 거라고 넘겨짚기 쉬운 자리다.
# 타입 스펙: type-process.md — 세 단계가 같은 의미 슬롯(무엇을 걸었나 · 응답 · 무엇을 뜻하나)으로
#           반복되고 순서가 있다. 앞 단계의 결과가 다음 단계를 부르므로 절차다(17-01 랩과 같은 형태).
#           어긋나는 지점: 행이 단계이고 열이 시도/응답이라 정본의 축과 뒤집혀 있다.
#           응답은 지어내지 않고 본문이 실측한 문자열을 그대로 옮긴다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, MUTED, SOFT, INK, PAPER2, PAPER, RULE, INFO, KR, MONO
import ddx

W, H = 1240, 608
d = D(W, H, "KUBERNETES UP AND RUNNING · 19-01",
      "선택되지 않으면 열려 있고 선택되면 닫힌다",
      "어떤 정책에도 걸리지 않은 파드는 전부 허용된다. 하나라도 걸리는 순간 명시하지 않은 "
      "통신은 차단된다. 그래서 default deny 를 먼저 깔고 필요한 경로만 연다.",
      "kind 로컬 클러스터 실측 — CNI 는 kindnet · 응답은 실제로 받은 문자열")

LX, LW = 24, 452
RX, RW = 494, 448
CX, CW = 958, 258
Y0, RH, GAP = 148, 96, 14

d.t(LX, 128, "무엇을 걸었나", 9, SOFT, KR, "start")
d.t(RX, 128, "test 파드에서 wget http://web", 9, SOFT, KR, "start")
d.t(CX, 128, "무엇을 뜻하나", 9, SOFT, KR, "start")

ROWS = [
    ("01", "정책 없음", "podSelector 에 걸리는 정책이 하나도 없다",
     "<!DOCTYPE html>\n<title>Welcome to nginx!</title>", True,
     "선택되지 않은 파드는 전부 허용", MUTED, False),
    ("02", "default deny", "podSelector: {} · policyTypes: [Ingress]",
     "wget: download timed out", False,
     "kindnet 이 정책을 집행한다", ACC, True),
    ("03", "allow 규칙 추가", "podSelector app=web · from run=src3",
     "<!DOCTYPE html>\n<title>Welcome to nginx!</title>", True,
     "명시한 경로만 다시 열린다", OK, False),
]

for i, (no, title, spec, resp, ok, meaning, c, focal) in enumerate(ROWS):
    y = Y0 + i * (RH + GAP)
    if focal:
        d.tone(LX, y, LW, RH, c, 8, "0C", 1.4)
    else:
        d.box(LX, y, LW, RH, PAPER2, RULE, 1.0, 8)
    d.t(LX + 18, y + 30, no, 11, c, MONO, "start", 600)
    d.t(LX + 48, y + 30, title, 13, c if focal else INK, KR, "start", 600)
    d.t(LX + 18, y + 58, ddx.fit(spec, 10, LW - 36, spec), 10, MUTED, MONO, "start")

    rc = BAD if not ok else OK
    d.o.append(f'<rect x="{RX}" y="{y}" width="{RW}" height="{RH}" rx="8" '
               f'fill="{rc}0C" stroke="{rc}" stroke-width="{1.4 if focal else 1.0}"/>')
    for j, ln in enumerate(resp.split("\n")):
        d.t(RX + 18, y + 34 + j * 20, ddx.fit(ln, 11, RW - 36, ln), 11, rc, MONO, "start")
    d.t(RX + RW - 18, y + RH - 16, "붙는다" if ok else "막힌다", 10, rc, KR, "end")
    d.arrow([(LX + LW + 4, y + RH / 2), (RX - 6, y + RH / 2)], SOFT, "soft", 1.2)

    d.t(CX, y + RH / 2 + 5, ddx.fit(meaning, 11, CW, meaning), 11, c, KR, "start",
        600 if focal else 400)

BY = Y0 + 3 * (RH + GAP) + 8
d.line(24, BY, W - 48, BY, RULE, 0.8)
d.t(24, BY + 24, "NetworkPolicy 는 컨트롤러가 함께 오지 않는다. 집행하는 네트워크 플러그인이 "
                 "없으면 리소스는 만들어지지만 아무도 읽지 않는다.", 11, MUTED, KR, "start")
d.t(24, BY + 46, "정책을 만들었는데 아무것도 막히지 않으면 플러그인부터 확인한다. "
                 "Calico · Cilium · Weave Net · kindnet 이 그 역할을 한다.", 11, MUTED, KR, "start")
d.legend(BY + 62, [("집행이 확인되는 자리", ACC), ("통신이 붙음", OK), ("차단됨", BAD)])
d.save("19-01.networkpolicy-lab.svg")
print("필요 h:", BY + 62 + 48, "· 실제:", H)

# 타입 스펙: type-architecture — 카드 결제의 네 당사자(소지자·발급사·매입사·가맹점)와 둘 사이를 잇는 카드 네트워크 규칙, 계약 선과 수수료 두 흐름(인터체인지·가맹점 수수료).
# 사실 출처: EU 규정 2015/751(OJ L 123, 2015-05-19) 제2조 (1) acquirer · (2) issuer · (10) interchange fee · (12) merchant service charge · (17) four party payment card scheme,
#   제3조 1항 직불 0,2 % · 제4조 신용 0,3 %, 제5조(발급사가 받는 보수는 인터체인지로 본다), 전문 (10)(주된 부분)·(30)(매입의 일부만 하는 중개자도 매입사에 든다).
# Layout conventions: 노드 폭 152·높이 68, 가로 stride 196(x=24+196k), 노드 y=108, 계약 선은 노드 중앙 높이, 수수료 화살표는 ㄷ자(수직→수평→수직) y=276·340. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 1000, 436
d = D(W, H, "BYTEBYTEGO · 07-01 §1",
      "카드 한 장 뒤의 계약은 발급사 쪽과 매입사 쪽으로 갈린다",
      "발급사는 카드 소지자와, 매입사는 가맹점과 계약하고 둘 사이를 카드 네트워크의 규칙이 잇습니다.",
      "수수료 상한은 EU 규정 2015/751 의 소비자 카드 기준입니다")


def _kr(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO


NW, NH, STR, X0, Y = 152, 68, 196, 24, 108
nodes = [("카드 소지자", "payer"), ("발급사", "issuer"), ("카드 네트워크", "scheme"), ("매입사", "acquirer · PSP"), ("가맹점", "payee")]
for i, (a, b) in enumerate(nodes):
    x = X0 + i * STR
    d.box(x, Y, NW, NH, PAPER2, RULE, 1.0, 6)
    d.t(x + NW / 2, Y + 30, a, 13, INK, _kr(a), "middle", 600)
    d.t(x + NW / 2, Y + 52, b, 12, MUTED, MONO)

YM = Y + NH // 2
links = ["카드 발급 계약", "규칙 · 라이선스", "규칙 · 라이선스", "가맹 계약"]
for i, lab in enumerate(links):
    x1 = X0 + i * STR + NW
    x2 = X0 + (i + 1) * STR
    d.line(x1, YM, x2, YM, MUTED, 1.4)
    d.t((x1 + x2) / 2, Y + NH + 28, lab, 12, MUTED, _kr(lab), "middle")

# 인터체인지: 매입사 → 발급사 (제5조 — 발급사가 받는 보수)
XI = X0 + 1 * STR + NW // 2 + 20     # 발급사 중앙 +20
XA = X0 + 3 * STR + NW // 2 - 20     # 매입사 중앙 -20
d.arrow([(XA, Y + NH + 4), (XA, 276), (XI, 276), (XI, Y + NH + 8)], ACC, "acc", 1.6)
d.t((XA + XI) / 2, 262, "인터체인지", 13, ACC, KR, "middle", 600)
d.t((XA + XI) / 2, 300, "직불 ≤ 0.2% · 신용 ≤ 0.3%", 12, MUTED, KR, "middle")

# 가맹점 수수료: 가맹점 → 매입사 (제2조 (12))
XM = X0 + 4 * STR + NW // 2          # 가맹점 중앙
XB = X0 + 3 * STR + NW // 2 + 20     # 매입사 중앙 +20
d.arrow([(XM, Y + NH + 4), (XM, 340), (XB, 340), (XB, Y + NH + 8)], WARN, "warn", 1.6)
d.t((XM + XB) / 2, 326, "가맹점 수수료", 13, WARN, KR, "middle", 600)
d.t((XM + XB) / 2, 364, "인터체인지가 주된 몫", 12, MUTED, KR, "middle")

d.legend(H - 44, [("계약·규칙 관계", MUTED), ("인터체인지", ACC), ("가맹점 수수료", WARN)])
d.save("07-01.four-party.svg")

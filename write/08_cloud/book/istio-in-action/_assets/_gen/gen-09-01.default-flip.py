# 09-01 §4 정책이 붙는 순서에 따라 워크로드의 기본값이 바뀐다.
# 본문(저자 9.3.3 "gotcha"): ALLOW 인가 정책이 하나 이상 적용되면 그 워크로드로 가는 접근은 기본 거부가 된다.
#       저자는 이걸 모르면 디버깅에 몇 시간을 날린다고 경고하고, catch-all DENY 를 먼저 깔라고 처방한다.
# 가운데 상태가 사고를 흐리는 자리다 — 허용도 거부도 적지 않은 요청이 막힌다.
# 두 결과는 저자가 적용하지 않고 "mentally examine" 한 예측이라 응답값을 적지 않는다(적대적 검증 2026-08-31).
# 타입 스펙: type-state — 주체 하나(워크로드의 인가 기본값)의 상태 전이. 시작점 · 상태 3 · 종료점,
#           전이 라벨은 event [guard] 형태, coral 은 사고가 뒤집히는 상태 하나에.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 1000, 560
d = D(W, H, "ISTIO IN ACTION · 09-01 §4",
      "허용을 하나 적으면 나머지가 닫힌다",
      "정책이 없을 때는 전부 허용이다. ALLOW 정책을 하나 붙이는 순간 그 워크로드의 기본값이 거부로 "
      "뒤집힌다. 색이 붙은 상태가 저자가 gotcha 라 부른 자리이고, 오른쪽이 그 처방이다.",
      "저자는 이 뒤집힘을 세부 설명보다 먼저 꺼내 놓습니다")

CY, SW, SH = 236, 280, 72
XS = [36, 360, 684]

def state(x, name, sub, focal=False):
    y = CY - SH / 2
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{SW}" height="{SH}" rx="8" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, y, SW, SH, PAPER2, RULE, 1.0, 8)
    d.t(x + SW / 2, y + 30, name, 13, ACC if focal else INK, KR, "middle", 600)
    d.t(x + SW / 2, y + 52, sub, 11, MUTED, MONO)

d.o.append(f'<circle cx="60" cy="{CY}" r="6" fill="{INK}"/>')
d.o.append(f'<circle cx="1206" cy="{CY}" r="8" fill="none" stroke="{INK}" stroke-width="1.2"/>')
d.o.append(f'<circle cx="1206" cy="{CY}" r="5" fill="{INK}"/>')

d.arrow([(68, CY), (XS[0] - 2, CY)], MUTED, "ar", 1.4)
d.arrow([(XS[0] + SW, CY), (XS[1] - 2, CY)], ACC, "acc", 1.5)
d.arrow([(XS[1] + SW, CY), (XS[2] - 2, CY)], MUTED, "ar", 1.4)
d.arrow([(XS[2] + SW, CY), (1196, CY)], MUTED, "ar", 1.4)

state(XS[0], "정책 없음", "전부 허용")
state(XS[1], "기본 거부", "ALLOW 에 맞아야 통과", focal=True)
state(XS[2], "명시한 것만 허용", "catch-all DENY 가 나머지")

d.t((XS[0] + SW + XS[1]) / 2, CY - 70, "ALLOW 정책 하나 추가", 11, ACC, MONO, "middle", 600)
d.t((XS[0] + SW + XS[1]) / 2, CY - 52, "[그 워크로드에 적용될 때]", 11, MUTED, MONO)
d.t((XS[1] + SW + XS[2]) / 2, CY - 70, "catch-all DENY 추가", 11, MUTED, MONO, "middle", 600)
d.t((XS[1] + SW + XS[2]) / 2, CY - 52, "[spec: {} · 루트 네임스페이스]", 11, MUTED, MONO)

OY = CY + SH / 2 + 40
d.box(XS[1] - 60, OY, 420, 108, PAPER2, RULE, 1.0, 6)
d.t(XS[1] - 44, OY + 26, "가운데 상태에서 벌어지는 일", 11, ACC, KR, "start", 600)
d.t(XS[1] - 44, OY + 50, "/api/catalog   ->  허용  (경로가 맞는다)", 11, MUTED, MONO, "start")
d.t(XS[1] - 44, OY + 72, "/hello/world   ->  거부  (맞는 정책 없음)", 11, MUTED, MONO, "start")
d.t(XS[1] - 44, OY + 94, "허용도 거부도 적지 않은 요청이 막힌다", 11, SOFT, KR, "start")
d.line(XS[1] + 110, CY + SH / 2, XS[1] + 110, OY, MUTED, 1.0, "3 5")

d.t(32, 480, "catch-all 을 먼저 깔면 생각할 것이 하나로 준다 — 무엇을 들일지만 적는다", 11, SOFT, KR, "start")
d.legend(504, [("사고가 뒤집히는 상태", ACC)])
d.save("09-01.default-flip.svg")

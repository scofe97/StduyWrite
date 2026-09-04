# a0-01 §2 검증이 어디에 서 있는가.
# 본문(부록 A.1): Helm 은 "lack of user-input validation" 이라 오류가 많았고 최악의 경우
#       "an indentation error would cause production outages". IstioOperator API 의 이득 둘 —
#       user-input validation 과 "consult the docs and discover all the configuration possibilities".
# 타입 스펙: type-layers — 같은 흐름 위에 층이 하나 끼어드는 것이 논점이다. 층은 위에서 아래로
#           쌓고 각 층에 무엇이 걸러지는지를 오른쪽에 적는다.
#           축약: 두 경로를 나란히 두어 끼어든 층의 유무를 대조한다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, BAD, OK, PAPER2, RULE, KR, MONO

W, H = 960, 588
d = D(W, H, "ISTIO IN ACTION · A0-01 §2",
      "층 하나가 끼어들면 실수가 설치 전에 걸린다",
      "왼쪽은 Helm 단독 경로이고 오른쪽은 IstioOperator API 를 거치는 경로다. 층 하나가 더 있고 없고에 "
      "따라 오타와 들여쓰기가 어디서 드러나는지가 달라진다. 색이 붙은 층이 저자가 이득으로 꼽은 자리다.",
      "저자는 이 검증에 \"이게 큽니다\" 라고 덧붙입니다")

LW, LH = 380, 64
LX, RX = 40, 540
def layer(x, y, title, sub, c=None, focal=False, faint=False):
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{LW}" height="{LH}" rx="6" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    elif faint:
        d.o.append(f'<rect x="{x}" y="{y}" width="{LW}" height="{LH}" rx="6" '
                   f'fill="{INK}04" stroke="{MUTED}" stroke-width="1" stroke-dasharray="5 5"/>')
    elif c:
        d.o.append(f'<rect x="{x}" y="{y}" width="{LW}" height="{LH}" rx="6" '
                   f'fill="{c}12" stroke="{c}" stroke-width="1.2"/>')
    else:
        d.box(x, y, LW, LH, PAPER2, RULE, 1.0, 6)
    d.t(x + 20, y + 26, title, 13, ACC if focal else INK, KR, "start", 600)
    d.t(x + 20, y + 46, sub, 11, MUTED, MONO, "start")

d.t(LX + LW / 2, 116, "HELM 단독", 11, SOFT, MONO, "middle", 600)
d.t(RX + LW / 2, 116, "ISTIOOPERATOR 경유", 11, SOFT, MONO, "middle", 600)

Y0, STEP = 136, 88
layer(LX, Y0, "사람이 값을 적는다", "values.yaml")
layer(RX, Y0, "사람이 값을 적는다", "IstioOperator CR")

layer(LX, Y0 + STEP, "검증하는 층이 없다", "통과", faint=True)
layer(RX, Y0 + STEP, "스키마가 값을 검사한다", "user-input validation", focal=True)

layer(LX, Y0 + 2 * STEP, "Helm 템플릿", "리소스 생성")
layer(RX, Y0 + 2 * STEP, "Helm 템플릿", "리소스 생성")

layer(LX, Y0 + 3 * STEP, "운영에서 드러난다", "indentation error -> outage", BAD)
layer(RX, Y0 + 3 * STEP, "설치 전에 드러난다", "적용이 거부된다", OK)

for x in (LX, RX):
    for k in range(3):
        cx = x + LW / 2
        d.arrow([(cx, Y0 + k * STEP + LH), (cx, Y0 + (k + 1) * STEP - 2)], MUTED, "ar", 1.3)

d.t(452, Y0 + STEP + 20, "여기가", 11, ACC, KR, "middle", 600)
d.t(452, Y0 + STEP + 40, "빈 자리", 11, ACC, KR, "middle", 600)

d.t(28, 496, "저자가 적은 또 하나의 이득 — 잘 정의된 API 가 있으면 문서를 보고 설정 가능성을 발견할 수 있다", 11, SOFT, KR, "start")
d.t(28, 518, "앞의 것은 틀린 설정을 막고 뒤의 것은 맞는 설정을 찾게 한다. 둘은 같은 스키마의 다른 얼굴이다", 11, MUTED, KR, "start")
d.legend(540, [("저자가 이득으로 꼽은 층", ACC), ("운영에서 터지는 자리", BAD), ("설치 전에 걸리는 자리", OK)])
d.save("a0-01.validation-layer.svg")

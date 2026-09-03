# 08-01 §7 부트스트랩을 갈아 끼웠다가 되돌리기까지.
# 본문: 저자는 커스텀 부트스트랩을 적용해 보이고, 곧바로 그 설정이 webapp 의 추적을 깨뜨린다고 밝히며
#       원상 복구 명령까지 붙인다. 그래서 이 절의 상태 전이는 되돌아오는 것으로 끝난다.
# 가운데 상태에서 sharedSpanContext 가 사라지는 것이 이 절의 관찰이다 — 병합이 아니라 대체라는 근거.
# 타입 스펙: type-state — 주체 하나(워크로드의 추적 설정)의 상태 전이. 시작점 · 상태 3 · 종료점,
#           전이 라벨은 event [guard] 형태, coral 은 추적이 끊긴 상태 하나에.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 1000, 560
d = D(W, H, "ISTIO IN ACTION · 08-01 §7",
      "갈아 끼운 뒤 되돌아오는 것까지가 저자의 절차",
      "저자는 커스텀 부트스트랩을 적용해 보인 다음 그 설정이 추적을 깨뜨린다고 밝히고 복구 명령을 붙인다. "
      "가운데 상태에서 손대지 않은 필드 하나가 사라지는 것이 이 절의 관찰이다.",
      "typedConfig 는 Any 로 감싼 블록이라 병합이 필드 단위로 내려가지 않습니다")

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

# 시작점 · 종료점
d.o.append(f'<circle cx="60" cy="{CY}" r="6" fill="{INK}"/>')
d.o.append(f'<circle cx="1206" cy="{CY}" r="8" fill="none" stroke="{INK}" stroke-width="1.2"/>')
d.o.append(f'<circle cx="1206" cy="{CY}" r="5" fill="{INK}"/>')

d.arrow([(68, CY), (XS[0] - 2, CY)], MUTED, "ar", 1.4)
d.arrow([(XS[0] + SW, CY), (XS[1] - 2, CY)], ACC, "acc", 1.5)
d.arrow([(XS[1] + SW, CY), (XS[2] - 2, CY)], MUTED, "ar", 1.4)
d.arrow([(XS[2] + SW, CY), (1196, CY)], MUTED, "ar", 1.4)

state(XS[0], "기본 부트스트랩", "collectorEndpoint /api/v2/spans")
state(XS[1], "커스텀 부트스트랩", "collectorEndpoint /zipkin/api/v1/spans", focal=True)
state(XS[2], "기본으로 되돌림", "webapp.yaml 재적용")

d.t((XS[0] + SW + XS[1]) / 2, CY - 70, "bootstrapOverride", 10, ACC, MONO, "middle", 600)
d.t((XS[0] + SW + XS[1]) / 2, CY - 52, "[configmap 이 같은 ns 에 있을 때]", 11, MUTED, MONO)
d.t((XS[1] + SW + XS[2]) / 2, CY - 70, "kubectl apply", 10, MUTED, MONO, "middle", 600)
d.t((XS[1] + SW + XS[2]) / 2, CY - 52, "[원본 Deployment]", 11, MUTED, MONO)

# 관찰 — 가운데 상태 아래
OY = CY + SH / 2 + 40
d.box(XS[1] - 40, OY, 380, 108, PAPER2, RULE, 1.0, 6)
d.t(XS[1] - 24, OY + 26, "적용 후 출력에서 사라진 것", 11, ACC, KR, "start", 600)
d.t(XS[1] - 24, OY + 50, '- "sharedSpanContext": false', 10, MUTED, MONO, "start")
d.t(XS[1] - 24, OY + 72, '"traceId128bit": "true" -> true', 10, MUTED, MONO, "start")
d.t(XS[1] - 24, OY + 94, "저자는 둘 다 언급하지 않는다", 11, SOFT, KR, "start")
d.line(XS[1] + 110, CY + SH / 2, XS[1] + 110, OY, MUTED, 1.0, "3 5")

d.t(32, 480, "Jaeger 의 Zipkin 수신구는 9411 에서 /api/v1/spans 와 /api/v2/spans 를 받는다 — /zipkin 접두 경로는 없다", 11, SOFT, KR, "start")
d.legend(504, [("추적이 끊긴 상태", ACC)])
d.save("08-01.bootstrap-states.svg")

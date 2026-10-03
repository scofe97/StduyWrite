# 08-01 §6 「전체 문법과 엔드포인트」 — Corefile 의 trace 줄이 실제로 어느 주소로 스팬을 보내는가.
# 소스 근거: plugin/trace/setup.go — 인자 0개면 zipkin 기본, 1개면 ENDPOINT(유형은 zipkin), 2개면 유형·ENDPOINT.
#            normalizeEndpoint: zipkin 이고 `!strings.Contains(ep, "http")` 일 때만 "http://" + ep + "/api/v2/spans".
#            supportedProviders: zipkin "localhost:9411", datadog "localhost:8126".
# 타입 스펙: type-dp-security-matrix — 입력 줄(행) × 유형·실제 엔드포인트(열) 격자이고, 마지막 행의 함정이 논지다.
#           tracing:9411 은 설명용 예시 호스트다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 880, 524
d = D(W, H, "LEARNING COREDNS · 08-01 §6",
      "trace 줄이 실제로 보내는 곳",
      "인자를 하나만 주면 그것은 유형이 아니라 엔드포인트로 읽히고 유형은 zipkin 이 된다. 엔드포인트 변환은 zipkin 에서 "
      "주소에 http 가 없을 때만 일어나 /api/v2/spans 가 붙는다.",
      "주황 행이 의도와 다르게 읽히는 줄입니다")

COLS = [(20, 330, "Corefile 줄"), (360, 110, "유형"), (480, 380, "실제 엔드포인트")]
rows = [
    ("trace", "zipkin", "http://localhost:9411/api/v2/spans", "기본 주소에 경로가 붙음", False),
    ("trace tracing:9411", "zipkin", "http://tracing:9411/api/v2/spans", "http 가 없어 변환", False),
    ("trace zipkin http://tracing:9411", "zipkin", "http://tracing:9411", "http 가 있어 그대로 · 경로 없음", False),
    ("trace datadog localhost:8126", "datadog", "localhost:8126", "datadog 은 변환 없음", False),
    ("trace datadog", "zipkin", "http://datadog/api/v2/spans", "인자 하나는 엔드포인트", True),
]
for x, w, head in COLS:
    d.t(x + 12, 118, head, 12, SOFT, KR, "start", 600)

Y0, PITCH, RH = 132, 62, 54
for i, (line, typ, ep, note, focal) in enumerate(rows):
    y = Y0 + i * PITCH
    for k, (x, w, _) in enumerate(COLS):
        if focal:
            d.tone(x, y, w, RH, ACC, 6, "12", 1.4)
        else:
            d.box(x, y, w, RH, PAPER2, RULE, 1.0, 6)
    c = ACC if focal else INK
    d.t(COLS[0][0] + 12, y + 33, line, 12, c, MONO, "start", 600)
    d.t(COLS[1][0] + 12, y + 33, typ, 12, c, MONO, "start", 600)
    d.t(COLS[2][0] + 12, y + 23, ep, 12, c, MONO, "start", 600)
    d.t(COLS[2][0] + 12, y + 43, note, 12, MUTED, KR, "start")

d.t(20, 460, "every · service · client_server 는 블록 안 · 엔드포인트 규칙과 무관", 13, MUTED, KR, "start")

d.legend(484, [("의도와 다르게 읽히는 줄", ACC)])
d.save("08-01.trace-endpoint.svg")

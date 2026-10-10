# 타입 스펙: type-dp-security-matrix — 행 = 필드, 열 = 가리기 전·후의 비교 행렬. 배정된 비교 타입 이름이 스펙 목록에 없어 비교 행렬 문법을 가진 이 타입으로 바꿨다. 셀 1개만 focal.
# 사실 출처: Cilium Up and Running 15장 cil15.txt 줄 691-705(Bearer MY_TOKEN), 716-722(deny: Authorization), 759-769(HUBBLE_REDACTED), 655-656(User-Agent curl/8.7.1) / cilium v1.20.2 pkg/hubble/parser/seven/http.go filterHeader(deny 에 없는 헤더는 그대로)
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, BAD, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 424
LP, COMP_W, GAP, ROLE_W, ROLE_GAP = 12, 240, 12, 316, 16
HDR_Y, HDR_H = 96, 48
ROW_Y0, ROW_H, STRIDE = 160, 52, 62
RX = [LP + COMP_W + GAP + j * (ROLE_W + ROLE_GAP) for j in range(2)]

d = D(W, H, "CILIUM UP AND RUNNING · 15-01 §5", "가리기 전과 후의 필드",
      "deny 목록에 든 헤더 값만 HUBBLE_REDACTED 로 바뀐다", "deny 목록에 든 헤더 값만 HUBBLE_REDACTED 로 바뀐다")

d.box(LP, HDR_Y, COMP_W, HDR_H, PAPER2, RULE, 0.9)
d.t(LP + COMP_W / 2, HDR_Y + 30, "필드", 13, INK, KR, "middle", 600)
for j, nm in enumerate(["가리기 전", "가리기 후"]):
    d.box(RX[j], HDR_Y, ROLE_W, HDR_H, PAPER2, SOFT, 1.0)
    d.t(RX[j] + ROLE_W / 2, HDR_Y + 30, nm, 13, INK, KR, "middle", 600)

rows = [
    ("Authorization 헤더", "l7.http.headers", "Bearer MY_TOKEN", "HUBBLE_REDACTED", "focal"),
    ("User-Agent 헤더", "deny 목록에 없음", "curl/8.7.1", "curl/8.7.1", None),
    ("hubble.redact", "Helm 값", "enabled: false", "enabled: true · deny: Authorization", None),
]
for i, (name, hint, a, b, tone) in enumerate(rows):
    y = ROW_Y0 + i * STRIDE
    d.box(LP, y, COMP_W, ROW_H, PAPER2, RULE, 0.9, r=4)
    d.t(LP + 12, y + 22, name, 12, INK, KR, "start", 600)
    d.t(LP + 12, y + 41, hint, 11, MUTED, KR if any("가" <= c <= "힣" for c in hint) else MONO, "start")
    for j, val in enumerate([a, b]):
        x = RX[j]
        if tone == "focal" and j == 1:
            d.tone(x, y, ROLE_W, ROW_H, OK, r=4, op="14", sw=1.4)
            col = OK
        elif tone == "focal":
            d.tone(x, y, ROLE_W, ROW_H, BAD, r=4, op="12", sw=1.0)
            col = BAD
        else:
            d.box(x, y, ROLE_W, ROW_H, PAPER2, RULE, 0.7, r=4)
            col = INK
        d.t(x + ROLE_W / 2, y + 31, val, 12, col, MONO, "middle", 600)

d.legend(ROW_Y0 + 3 * STRIDE + 16, [("토큰이 보임", BAD), ("값이 가려짐", OK)])
d.save("15-01.redaction-comparison.svg")

# 00-03-device-flow — 같은 프레임을 넣어도 장비마다 나가는 모습이 다르다
# 본문 요구: "왼쪽에 같은 프레임을 넣었다. 가운데가 그 장비가 읽는 깊이이고, 오른쪽이 그 결과다."
#           겉봉을 새로 쓰는 것은 라우터뿐이라 거기에 focal.
# 타입 스펙: type-dp-security-matrix.md 의 행 대조 — 행이 장비 셋, 열이 (같은 입력 · 읽는 깊이 ·
#           그 결과). 세 줄을 세로로 맞춰 읽는 것이 논지라 격자가 배치 문법이다.
# 이력: 2026-08-28 신설. 생성기 없이 손으로 만들어진 SVG 였다. 값·좌표를 그대로 옮겼다.
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, BAD, PAPER2, KR, MONO

W, H = 1000, 620
IN_X, IN_W, DEV_X, DEV_W, OUT_X, OUT_W = 60, 140, 260, 180, 560, 380
ROWS = [(164, "L1", "허브", "아무것도 안 읽는다", BAD, False,
         [(OK, "포트 2 · 받을 대상"), (BAD, "포트 3 · 남의 것이라 버림"), (BAD, "포트 4 · 남의 것이라 버림")]),
        (324, "L2", "스위치", "겉봉 MAC 만 읽는다", MUTED, False,
         [(OK, "포트 2 에게만 · MAC 표에서 찾았다")]),
        (464, "L3", "라우터", "속의 IP 까지 읽는다", ACC, True,
         [(ACC, "다른 망으로 · 겉봉 MAC 을 새로 쓴다")])]

d = D(W, H, "FLOW COMPARISON · WHAT EACH DEVICE READS",
      "같은 프레임이 들어와도 나가는 모습이 다르다",
      "허브·스위치·라우터에 같은 프레임을 넣었을 때 각각 무엇을 읽고 어떻게 내보내는지를 세 줄로 "
      "나란히 놓은 흐름 비교. 허브는 모든 포트로 복사하고, 스위치는 한 포트로만 보내며, "
      "라우터만 겉봉을 새로 쓴다.",
      lead="왼쪽에 같은 프레임을 넣었습니다. 가운데가 그 장비가 읽는 깊이이고, 오른쪽이 그 결과입니다.")

for y, layer, name, depth, dc, focal, outs in ROWS:
    d.box(IN_X, y, IN_W, 56, PAPER2, RULE, 1.0, 6)
    d.t(IN_X + IN_W // 2, y + 26, "프레임 도착", 12, INK, KR)
    d.t(IN_X + IN_W // 2, y + 44, "dst AA:..:02", 11, MUTED, MONO)
    dy = y - 12
    if focal:
        d.tone(DEV_X, dy, DEV_W, 80, ACC, 6, "12", 1.2)
    else:
        d.box(DEV_X, dy, DEV_W, 80, PAPER2, RULE, 1.0, 6)
    d.t(DEV_X + 16, dy + 24, layer, 8, SOFT, MONO, "start")
    d.t(DEV_X + DEV_W // 2, dy + 46, name, 15, INK, KR, "middle", 600)
    d.t(DEV_X + DEV_W // 2, dy + 68, depth, 12, dc, KR)
    d.path(f"M {IN_X + IN_W + 6} {y + 28} L {DEV_X - 10} {y + 28}", MUTED, 1.4, m="ar")
    oy = y - 16 if len(outs) > 1 else y + 6
    for i, (c, text) in enumerate(outs):
        h = 28 if len(outs) > 1 else 44
        by = oy + i * 40
        d.box(OUT_X, by, OUT_W, h, PAPER2, RULE, 1.0, 6)
        d.t(OUT_X + 16, by + (19 if h == 28 else 28), text, 12, c, KR, "start")
    d.path(f"M {DEV_X + DEV_W + 6} {y + 28} L {OUT_X - 10} {y + 28}",
           ACC if focal else MUTED, 1.4, m="acc" if focal else "ar")

d.t(IN_X, 556, "세 줄의 차이는 성능이 아니라 여는 깊이입니다. 겉봉을 고쳐 쓰는 것은 라우터뿐입니다.",
    12, MUTED, KR, "start")
d.legend(572, [("받을 대상", OK), ("버린다", BAD), ("겉봉을 새로 쓴다", ACC)])
d.save("00-03-device-flow.svg")
print("ok device-flow")

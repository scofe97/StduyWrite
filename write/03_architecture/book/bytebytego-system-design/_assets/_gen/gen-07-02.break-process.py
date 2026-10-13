# 타입 스펙: type-process — 같은 두 불일치 건(ORD-1002·ORD-1004)을 대사 회차마다 다시 그려 임시 불일치가 해소되거나 확정되는 상태 변화를 값으로 보인다.
# 사실 출처: 추출본 v1.txt 3310~3318행(컷오프 때문에 생긴 불일치는 임시 불일치로 분류하고 다음 날 PSP 기록과 다시 대조, 찾으면 해소되어 더는 조치가 없다).
#   ORD-1004 의 세 번째 대사에서 확정은 이 도식의 설계 가정이며 확정 시점은 계약·정산 주기에 따라 정한다. 날짜·번호는 문서용 예시.
# Layout conventions: 라벨 열 x=24 폭 200, 회차 열 stride 232(x=232+232k, 셀 폭 208), 행 stride 80(y=140 부터 2행), 머리 행 y=92. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, BAD, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 960, 380
d = D(W, H, "BYTEBYTEGO · 07-02 §4",
      "임시 불일치는 다음 파일에서 해소되거나 확정된다",
      "두 건 모두 01-01 대사에서는 PSP 파일에 없었고, 이후 파일에서 갈립니다.",
      "확정을 세 번째 대사로 둔 것은 설계 가정입니다")


def _kr(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO


LX, LW, CX0, CSTR, CWID = 24, 200, 232, 232, 208
Y_H, Y0, RS = 92, 140, 80
steps = ["대사 1 · 01-01 파일", "대사 2 · 01-02 파일", "대사 3 · 01-03 파일"]
rows = [
    ("ORD-1002", "10.00 USD · 내부 01-01 23:59:55", [
        ("임시 불일치", "01-01 파일에 없음", WARN),
        ("해소", "00:00:30 행 발견", OK),
        ("종결", "", None),
    ]),
    ("ORD-1004", "10.00 USD · 내부 01-01", [
        ("임시 불일치", "01-01 파일에 없음", WARN),
        ("임시 유지", "01-02 파일에도 없음", WARN),
        ("확정 불일치", "조사 대상", BAD),
    ]),
]

for k, s in enumerate(steps):
    x = CX0 + k * CSTR
    if k == 1:
        d.tone(x, Y_H - 4, CWID, 36, ACC, 4, "14", 1.4)
    else:
        d.box(x, Y_H - 4, CWID, 36, PAPER2, RULE, 0.9, 4)
    d.t(x + CWID / 2, Y_H + 19, s, 13, ACC if k == 1 else INK, _kr(s), "middle", 600)

for r, (name, sub, cells) in enumerate(rows):
    y = Y0 + r * RS
    d.line(LX, y - 4, W - 24, y - 4, RULE, 0.5)
    d.t(LX, y + 28, name, 13, INK, MONO, "start", 600)
    d.t(LX, y + 52, sub, 11, MUTED, _kr(sub), "start")
    for k, (a, b, c) in enumerate(cells):
        x = CX0 + k * CSTR
        if c is None:
            d.t(x + CWID / 2, y + 40, a, 13, MUTED, _kr(a), "middle")
            continue
        d.tone(x, y + 4, CWID, 60, c, 4, "18", 1.0)
        d.t(x + CWID / 2, y + 30, a, 13, c, _kr(a), "middle", 600)
        d.t(x + CWID / 2, y + 52, b, 13, MUTED, _kr(b), "middle")
        if k < 2 and cells[k + 1][2] is not None:
            d.arrow([(x + CWID + 2, y + 34), (x + CSTR - 4, y + 34)], MUTED, "ar", 1.4)

d.line(LX, Y0 + 2 * RS - 4, W - 24, Y0 + 2 * RS - 4, RULE, 0.5)
d.legend(H - 56, [("임시", WARN), ("해소", OK), ("확정", BAD), ("갈리는 회차", ACC)])
d.save("07-02.break-process.svg")

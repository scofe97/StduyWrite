# 07-01 §5 — rewrite edns0 의 액션 넷이 같은 코드의 옵션이 이미 있느냐에 따라 어떻게 갈리는가.
# 소스 근거: plugin/rewrite/edns0.go — 일치하는 옵션을 찾으면 Replace·Set 만 덮어쓰고 끝내며, Append 는 "add option if not found"
#            블록까지 내려가 하나 더 붙인다. Unset 은 unsetEdns0Option 으로 지운다. README: "append will add the option only if no matching option exists".
# 타입 스펙: type-dp-security-matrix — 액션(행) × 옵션 유무(열)에서 칸마다 결과가 다르고, append 칸에서 문서와 코드가 갈린다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 880, 476
d = D(W, H, "LEARNING COREDNS · 07-01 §5",
      "같은 코드의 옵션이 이미 있느냐가 액션을 가른다",
      "set 은 있든 없든 그 값으로 맞추고, replace 는 있을 때만 고친다. unset 은 지운다. "
      "append 는 옵션이 이미 있을 때 README 와 코드가 다르게 말한다.",
      "주황 칸이 문서와 코드가 갈리는 자리입니다")

COLS = [(20, 150, "액션"), (180, 300, "같은 코드 옵션이 없을 때"), (490, 370, "같은 코드 옵션이 있을 때")]
rows = [
    ("set", ("새로 붙인다", ""), ("값을 덮어쓴다", "")),
    ("replace", ("아무것도 안 한다", ""), ("값을 덮어쓴다", "")),
    ("append", ("새로 붙인다", ""), ("README · 붙이지 않는다", "코드 · 하나 더 붙인다")),
    ("unset", ("아무것도 안 한다", ""), ("지운다", "")),
]

for x, w, head in COLS:
    d.t(x + 10, 118, head, 12, SOFT, KR, "start", 600)

for i, (act, *cells) in enumerate(rows):
    y = 132 + i * 66
    x, w, _ = COLS[0]
    d.box(x, y, w, 58, PAPER2, RULE, 1.0, 6)
    d.t(x + 12, y + 35, act, 14, INK, MONO, "start", 600)
    for k, (a, b) in enumerate(cells, start=1):
        x, w, _ = COLS[k]
        foc = (act == "append" and k == 2)
        if foc:
            d.tone(x, y, w, 58, ACC, 6, "12", 1.4)
        else:
            d.box(x, y, w, 58, PAPER2, RULE, 1.0, 6)
        if b:
            d.t(x + 12, y + 25, a, 13, ACC if foc else INK, KR, "start", 600)
            d.t(x + 12, y + 45, b, 12, ACC if foc else MUTED, KR, "start")
        else:
            d.t(x + 12, y + 35, a, 13, INK, KR, "start", 600)

d.t(20, 412, "원서의 append 설명 \"항상 하나 더\" 는 코드 쪽과 같다 · unset 은 원서 이후 추가", 13, MUTED, KR, "start")

d.legend(428, [("README 와 코드가 갈리는 칸", ACC)])
d.save("07-01.edns0-actions.svg")

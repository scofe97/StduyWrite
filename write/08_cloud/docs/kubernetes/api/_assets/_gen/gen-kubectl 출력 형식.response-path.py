# -*- coding: utf-8 -*-
# 타입 스펙: type-data-flow
"""kubectl 출력 형식 §1 도식 — 출력 형식에 따라 갈리는 요청·응답·가공 경로.

선언이 SSOT다. 생성된 SVG 를 손으로 고치지 않는다.
위 행은 서버가 표를 만드는 경로, 아래 행은 서버가 객체를 주고 kubectl 이 가공하는 경로다.
_assets/ 에서 실행한다: python3 "_gen/gen-kubectl 출력 형식.response-path.py"
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from dd import D, INK, MUTED, SOFT, ACC, PAPER2, RULE, MONO, KR

W = 1000
COL_W, COL_GAP, COL_X0 = 210, 36, 24
cols = [COL_X0 + i * (COL_W + COL_GAP) for i in range(4)]
HEAD_Y = 116
ROW_Y0, ROW_H, ROW_GAP = 128, 60, 28
FOCAL = (0, 2)   # 위 행의 priority 거르기

ROWS = [
    # 열마다 (이름, 보조)
    [("as=Table", "기본 · -o wide"),
     ("Table", "columnDefinitions · rows"),
     ("priority 거르기", "기본은 0 만 · wide 는 전부"),
     ("평문 표", "Pod 기본 5열 · wide 9열")],
    [("application/json", "yaml · json · name 등"),
     ("API 객체 전체", "PodList JSON"),
     ("클라이언트 printer", "직렬화 · 경로 추출"),
     ("객체 형식", "yaml · json · name · 지정 열")],
]
row_y = lambda r: ROW_Y0 + r * (ROW_H + ROW_GAP)
H = row_y(len(ROWS) - 1) + ROW_H + 28

def is_ascii(s):
    return all(ord(ch) < 128 for ch in s)

d = D(W, H,
      "ACCEPT HEADER -> RESPONSE -> KUBECTL -> OUTPUT",
      "출력 형식이 가르는 두 응답 경로",
      "kubectl get 이 보내는 Accept 헤더에 따라 응답이 둘로 갈리는 흐름도입니다. "
      "기본 출력과 -o wide 는 서버가 만든 Table 을 받아 kubectl 이 priority 로 열을 거르고, "
      "그 밖의 형식은 API 객체 전체를 받아 kubectl 이 직렬화하거나 필드를 뽑습니다.",
      lead="표는 서버가 만들고, 객체 형식은 kubectl 이 만든다")

for x, head in zip(cols, ("요청 Accept", "서버 응답", "kubectl 가공", "출력")):
    d.t(x, HEAD_Y, head, 11, SOFT, KR, "start")

for r, row in enumerate(ROWS):
    y = row_y(r)
    cy = y + ROW_H / 2
    for c, (name, sub) in enumerate(row):
        x = cols[c]
        focal = (r, c) == FOCAL
        if focal:
            d.tone(x, y, COL_W, ROW_H, ACC)
        else:
            d.box(x, y, COL_W, ROW_H, PAPER2, RULE, 0.9)
        d.t(x + 14, y + 25, name, 13, ACC if focal else INK, MONO if is_ascii(name) else KR, "start", 600)
        d.t(x + 14, y + 45, sub, 11, MUTED, MONO if is_ascii(sub) else KR, "start")
        if c < 3:
            d.arrow([(x + COL_W + 4, cy), (cols[c + 1] - 6, cy)])

out = pathlib.Path(__file__).resolve().parents[1] / "kubectl 출력 형식.response-path.svg"
d.save(str(out))
print(f"wrote {out.name}  viewBox={W}x{H}")

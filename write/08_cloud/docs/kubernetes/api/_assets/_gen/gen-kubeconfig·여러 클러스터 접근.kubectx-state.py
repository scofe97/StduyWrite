# -*- coding: utf-8 -*-
# 타입 스펙: type-data-flow
"""kubeconfig·여러 클러스터 접근 §5 도식 — 전환 명령이 바꾸는 필드와 직전 값을 남기는 곳.

선언이 SSOT다. 생성된 SVG 를 손으로 고치지 않는다.
행마다 명령 → kubeconfig 필드 → 직전 값 저장소로 가는 가로 흐름이다. 연결선은 모두 수평이다.
_assets/ 에서 실행한다: python3 "_gen/gen-kubeconfig·여러 클러스터 접근.kubectx-state.py"
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from dd import D, INK, MUTED, SOFT, ACC, PAPER2, RULE, MONO, KR

W = 1000
COLS = [(24, 280), (372, 280), (720, 256)]   # (x, w)
HEAD_Y = 116
ROW_Y0, ROW_H, ROW_GAP = 128, 52, 16
ROWS = [
    # (명령, 명령 보조, 필드, 직전 값 저장소, kubectx 계열인가)
    ("kubectl config use-context", "<컨텍스트>", "current-context", "남기지 않음", False),
    ("kubectx", "<컨텍스트>", "current-context", "~/.kube/kubectx", True),
    ("kubectl config set-context", "--current --namespace=<ns>", "contexts[현재].namespace", "남기지 않음", False),
    ("kubens", "<네임스페이스>", "contexts[현재].namespace", "~/.kube/kubens/<컨텍스트>", True),
]
row_y = lambda k: ROW_Y0 + k * (ROW_H + ROW_GAP)
BOTTOM = row_y(len(ROWS) - 1) + ROW_H
H = BOTTOM + 28

d = D(W, H,
      "COMMAND -> KUBECONFIG FIELD -> PREVIOUS VALUE",
      "전환 명령이 고치는 필드와 직전 값의 자리",
      "네 명령이 kubeconfig 에서 바꾸는 필드와, 되돌아가기용 직전 값을 남기는 파일을 행마다 보인 흐름도입니다. "
      "kubectx 와 kubens 는 kubectl config 명령과 같은 필드를 고치고, 직전 값만 kubeconfig 밖의 상태 파일에 따로 남깁니다.",
      lead="같은 필드를 고치고, 직전 값은 kubeconfig 밖 상태 파일에")

for (x, w), head in zip(COLS, ("명령", "kubeconfig 에서 바뀌는 필드", "직전 값을 남기는 곳")):
    d.t(x, HEAD_Y, head, 11, SOFT, KR, "start")

for k, (cmd, sub, field, store, kx) in enumerate(ROWS):
    y = row_y(k)
    cy = y + ROW_H / 2
    (x1, w1), (x2, w2), (x3, w3) = COLS
    # 명령
    d.box(x1, y, w1, ROW_H, PAPER2, RULE, 0.9)
    d.t(x1 + 16, y + 22, cmd, 13, INK, MONO, "start", 600)
    d.t(x1 + 16, y + 40, sub, 11, MUTED, MONO, "start")
    # 필드
    d.box(x2, y, w2, ROW_H, PAPER2, RULE, 0.9)
    d.t(x2 + w2 / 2, cy + 5, field, 13, INK, MONO, "middle")
    # 직전 값
    if kx:
        d.tone(x3, y, w3, ROW_H, ACC)
        d.t(x3 + w3 / 2, cy + 5, store, 12, ACC, MONO, "middle", 600)
    else:
        d.box(x3, y, w3, ROW_H, "none", RULE, 0.8)
        d.t(x3 + w3 / 2, cy + 5, store, 12, SOFT, KR, "middle")
    d.arrow([(x1 + w1 + 4, cy), (x2 - 6, cy)])
    d.arrow([(x2 + w2 + 4, cy), (x3 - 6, cy)], ACC if kx else SOFT, "acc" if kx else "soft",
            1.4, None if kx else "3 4")

out = pathlib.Path(__file__).resolve().parents[1] / "kubeconfig·여러 클러스터 접근.kubectx-state.svg"
d.save(str(out))
print(f"wrote {out.name}  viewBox={W}x{H}")

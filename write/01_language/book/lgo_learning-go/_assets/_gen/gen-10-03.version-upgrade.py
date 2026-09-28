# 10-03.version-upgrade — -u=patch 는 같은 마이너의 패치로, -u 는 가장 최신으로 올리고, 메이저가 바뀐 v2 는 다른 import 경로다
# 본문 요구(10-03 §3 「호환되는 버전과 호환되지 않는 버전으로 올리기」): simpletax 는 v1.0.0 · v1.1.0 · v1.1.1 · v1.2.0 · v1.2.1 이 있다.
#           v1.0.0 에서 -u=patch 는 같은 마이너의 패치가 없어 그대로다. v1.1.0 에서 -u=patch 는 v1.1.1, -u 는 v1.2.1 로 올린다.
#           v2.0.0 은 모듈 경로가 simpletax/v2 로 끝나는 다른 패키지라 v1 과 따로 import 할 수 있다.
# 타입 스펙: type-state — 상태 = 버전(둥근 사각 rx 8), 전이 = go get 옵션(mono 라벨). 버전 다섯을 한 줄에, 전이는 아래로 꺾는 직교 경로.
#           노드 폭 136, stride 176, 줄 y 184. v2 는 따로 떨어진 아랫줄. focal 은 -u 가 닿는 v1.2.1 하나.
# 사실 출처: Learning Go 2판 10장 「Updating to Compatible Versions」·「Updating to Incompatible Versions」, go1.25.1 로컬 실행(2026-09-27).
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, PAPER2, KR, MONO

W, H = 984, 540
X0, NW, NS, NY, NH = 60, 136, 176, 184, 56
vers = [("v1.0.0", "내려 둔 판"), ("v1.1.0", "버그 있음"), ("v1.1.1", "v1.1.0 패치"), ("v1.2.0", "함수 추가"), ("v1.2.1", "v1.2.0 패치")]


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def cx(k):
    return X0 + k * NS + NW // 2


d = D(W, H, "STATE · 10-03 §3",
      "-u=patch 와 -u 는 올리는 거리가 다릅니다",
      "simpletax 의 v1 판 다섯을 한 줄에 두었다. v1.1.0 에서 go get -u=patch 는 같은 마이너의 패치인 v1.1.1 로, go get -u 는 가장 최신인 v1.2.1 로 올린다. "
      "v1.0.0 에서는 같은 마이너의 패치가 없어 -u=patch 로는 그대로다. 아래 v2.0.0 은 모듈 경로가 /v2 로 끝나는 다른 패키지라 v1 과 따로 import 된다.",
      lead="v1.1.1·v1.2.0·v1.2.1 은 원문이 가정한 판입니다(실제 목록은 v1.0.0·v1.1.0).")

for k in range(4):
    d.line(X0 + k * NS + NW, NY + NH // 2, X0 + (k + 1) * NS, NY + NH // 2, RULE, 1.0)
for k, (v, sub) in enumerate(vers):
    x = X0 + k * NS
    if k == 4:
        d.tone(x, NY, NW, NH, OK, 8, "18", 1.4)
    else:
        d.box(x, NY, NW, NH, r=8)
    d.t(x + NW // 2, NY + 26, v, 14, OK if k == 4 else INK, MONO, "middle", 600)
    d.t(x + NW // 2, NY + 46, sub, 11, MUTED, KR, "middle")

# v1.0.0 -u=patch → 그대로
d.tone(cx(0) - 64, NY + NH + 28, 128, 28, WARN, 4, "14", 1.0)
d.t(cx(0), NY + NH + 47, "-u=patch · 그대로", 11, WARN, kr("그대로"), "middle", 600)

# v1.1.0 → v1.1.1 : -u=patch
y1 = NY + NH + 44
d.arrow([(cx(1) + 16, NY + NH + 2), (cx(1) + 16, y1), (cx(2), y1), (cx(2), NY + NH + 4)], INFO, "info", 1.3)
d.t((cx(1) + cx(2)) // 2, y1 + 18, "go get -u=patch", 11, INFO, MONO, "middle", 600)

# v1.1.0 → v1.2.1 : -u
y2 = NY + NH + 92
d.arrow([(cx(1) - 16, NY + NH + 2), (cx(1) - 16, y2), (cx(4), y2), (cx(4), NY + NH + 4)], OK, "ok", 1.3)
d.t((cx(2) + cx(3)) // 2, y2 + 18, "go get -u", 11, OK, MONO, "middle", 600)

# v2
VY = 424
d.tone(X0, VY, 320, NH, ACC, 8, "14", 1.1)
d.t(X0 + 160, VY + 26, ".../simpletax/v2 · v2.0.0", 13, ACC, MONO, "middle", 600)
d.t(X0 + 160, VY + 46, "API 가 바뀐 판", 11, MUTED, KR, "middle")
d.t(X0 + 344, VY + 26, "메이저가 바뀌면 import 경로 끝에 /v2", 12, MUTED, KR, "start", 600)
d.t(X0 + 344, VY + 46, "다른 패키지라 v1 과 함께 import 할 수 있음", 12, MUTED, KR, "start")
d.line(X0, VY - 20, 948, VY - 20, RULE, 0.8, "3 5")

d.legend(496, [("같은 마이너의 패치", INFO), ("가장 최신", OK), ("올라가지 않음", WARN), ("다른 import 경로", ACC)])
d.save("10-03.version-upgrade.svg")
print("ok 10-03 version-upgrade")

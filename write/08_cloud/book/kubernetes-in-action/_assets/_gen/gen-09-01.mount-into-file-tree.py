# 09-01 §1 — 마운트는 트리의 한 가지를 갈아 끼우는 일이다
# 볼륨을 상자로 그리면 "어디에 붙는가"가 안 보인다. 파일 트리를 실제로 그리고 그 한 지점이
# 다른 파일시스템으로 바뀌는 장면이어야 마운트라는 말이 몸에 붙는다.
# 타입 스펙: type-tree.md — 파일 트리 자체를 그린다 — 뿌리 / 아래로 자식이 들여쓰기로 뻗고, 그중 한 가지가 마운트로
#           갈아 끼워지는 것이 논지다. 마운트 전후 두 벌을 나란히 두어 그 한 지점만 달라진다.
#           type-dependency 정본은 트리로 표현 못 하는 두 가지(팬인·순환)를 위한 타입이고
#           '둘 다 없으면 Tree 를 쓰고 그렇다고 밝히라'고 명시한다. 여기엔 둘 다 없다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO
import ddx

d = D(1180, 620, "KUBERNETES IN ACTION · 09-01",
      "트리의 한 가지를 갈아 끼운다",
      "마운트는 파일시스템을 파일 트리의 어느 지점에 붙이는 일이다. 그 지점 아래에 원래 무엇이 "
      "있었든, 마운트한 뒤에는 붙인 쪽이 보인다.",
      "volumeMounts.mountPath 가 그 지점을 정한다")

def tree(x0, label, mounted):
    d.box(x0, 168, 420, 300, PAPER, RULE, 0.9, 8)
    d.t(x0 + 210, 196, label, 11, SOFT, KR)
    ROWS = [("/", 0, None), ("etc", 1, None), ("usr", 1, None),
            ("var", 1, None), ("data", 2, "mount"), ("tmp", 1, None)]
    for i, (nm, depth, kind) in enumerate(ROWS):
        y = 232 + i * 38
        x = x0 + 40 + depth * 34
        if kind == "mount" and mounted:
            d.o.append(f'<rect x="{x-8}" y="{y-20}" width="300" height="30" rx="5" '
                       f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
            d.t(x + 4, y, nm, 12, ACC, MONO, "start", 600)
            d.t(x + 70, y, "← 여기에 볼륨이 붙었다", 10, ACC, KR, "start")
        elif kind == "mount":
            d.t(x + 4, y, nm, 12, SOFT, MONO, "start")
            d.t(x + 70, y, "이미지가 담고 있던 빈 디렉터리", 10, SOFT, KR, "start")
        else:
            d.t(x + 4, y, nm, 12, MUTED, MONO, "start")

tree(60, "마운트 전 — 이미지의 파일 트리", False)
tree(700, "마운트 후 — 같은 경로, 다른 파일시스템", True)
d.path("M 490 318 L 670 318", MUTED, 1.5, m="ar")
d.t(580, 300, "mount", 11, SOFT, MONO)

d.t(24, 512, "그래서 마운트 지점 아래에 원래 있던 것은 가려진다. 이미지에 파일이 있었더라도 "
             "볼륨을 그 자리에 붙이면 볼륨 쪽이 보인다.", 11, MUTED, KR, "start")
d.t(24, 534, "볼륨은 파드의 spec.volumes 에 정의하고, 컨테이너마다 volumeMounts 로 어느 경로에 붙일지 따로 정한다 — "
             "같은 볼륨을 두 컨테이너가 다른 경로에 붙일 수도 있다.", 11, MUTED, KR, "start")
d.legend(560, [("붙는 자리", ACC)])
d.save("09-01-mount-into-file-tree.svg")
print("ok")

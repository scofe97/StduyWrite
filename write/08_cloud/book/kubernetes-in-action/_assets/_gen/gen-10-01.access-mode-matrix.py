# 10-01 §5 — Once 의 '하나'가 무엇인지가 갈린다
# 본문이 축 둘(제한 단위 · 동시 사용)을 직접 준다. 그러니 네 모드를 나열하지 말고 그 두 축의
# 교차로 놓아야 "RWOP 와 RWO 가 비슷해 보이지만 다르다"가 좌표로 드러난다.
# 타입 스펙: type-dp-security-matrix.md — 가로축이 제한 단위(파드·노드), 세로축이 동시 사용(하나만·여럿)인 2 차원 격자이고 네 모드가
#           그 교차에 놓인다. 축 둘이 다 의미를 지는 정본 그대로의 격자다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, MUTED, SOFT, PAPER2, KR, MONO
import ddx

d = D(920, 540, "KUBERNETES IN ACTION · 10-01",
      "Once 의 '하나'는 파드인가 노드인가",
      "Once 계열은 하나가 파드냐 노드냐로 갈리고, Many 계열은 read-write 를 허용하느냐로 갈린다. "
      "이름만 보면 RWOP 와 RWO 가 비슷해 보이지만 제한 단위가 다르다.",
      "제한 단위 × 동시 사용")

CX = (320, 680)
CY = (236, 368)
d.t(CX[0], 148, "파드 단위", 13, SOFT, KR)
d.t(CX[1], 148, "노드 단위", 13, SOFT, KR)
d.t(80, CY[0], "하나만", 13, SOFT, KR)
d.t(80, CY[1], "여럿", 13, SOFT, KR)

CELLS = [(0, 0, "ReadWriteOncePod", "RWOP", "파드 하나만 마운트", ACC),
         (1, 0, "ReadWriteOnce", "RWO", "노드 하나가 붙임 · 같은 노드의 파드는 함께 씀", INFO),
         (0, 1, "ReadWriteMany", "RWX", "여러 노드가 동시에 읽고 씀", OK),
         (1, 1, "ReadOnlyMany", "ROX", "여러 노드가 동시에 읽기 전용", OK)]
for ci, ri, nm, ab, s, c in CELLS:
    cx, cy = CX[ci], CY[ri]
    if c is ACC:
        d.o.append(f'<rect x="{cx-170}" y="{cy-52}" width="340" height="104" rx="6" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(cx - 170, cy - 52, 340, 104, PAPER2, c, 1.1, 6)
    d.t(cx, cy - 20, nm, 14, c, MONO, "middle", 600)
    d.t(cx, cy + 4, ab, 12, MUTED, MONO)
    d.t(cx, cy + 28, ddx.fit(s, 12, 320, s), 12, MUTED, KR)

d.t(24, 444, "RWO: 다른 노드의 파드는 Multi-Attach 에러로 ContainerCreating · 같은 노드의 파드는 함께 씀", 12, MUTED, KR, "start")
d.t(24, 468, "RWOP: 단일 파드 제한 · 같은 노드라도 둘째 파드는 Pending", 12, MUTED, KR, "start")
d.legend(494, [("파드로 좁힌다", ACC), ("노드가 단위", INFO), ("여럿이 함께", OK)])
d.save("10-01-access-mode-matrix.svg")
print("ok")

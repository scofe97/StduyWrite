# 10-01 §5 — Once 의 '하나'가 무엇인지가 갈린다
# 본문이 축 둘(제한 단위 · 동시 사용)을 직접 준다. 그러니 네 모드를 나열하지 말고 그 두 축의
# 교차로 놓아야 "RWOP 와 RWO 가 비슷해 보이지만 다르다"가 좌표로 드러난다.
# 타입 스펙: type-dp-security-matrix.md — 가로축이 제한 단위(파드·노드), 세로축이 동시 사용(하나만·여럿)인 2 차원 격자이고 네 모드가
#           그 교차에 놓인다. 축 둘이 다 의미를 지는 정본 그대로의 격자다. type-quadrant 는 뺐다 —
#           그 정본은 축선 십자와 점 배치가 문법인데 여기는 칸이 값을 담는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, WARN, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO
import ddx

d = D(1200, 660, "KUBERNETES IN ACTION · 10-01",
      "Once 의 '하나'는 파드인가 노드인가",
      "Once 계열은 하나가 파드냐 노드냐로 갈리고, Many 계열은 read-write 를 허용하느냐로 갈린다. "
      "이름만 보면 RWOP 와 RWO 가 비슷해 보이지만 제한 단위가 다르다.",
      "제한 단위 × 동시 사용")

CX = (420, 800)
CY = (280, 440)
d.t(CX[0], 190, "파드 단위", 12, SOFT, KR)
d.t(CX[1], 190, "노드 단위", 12, SOFT, KR)
d.t(180, CY[0], "하나만", 12, SOFT, KR)
d.t(180, CY[1], "여럿", 12, SOFT, KR)

CELLS = [(0, 0, "ReadWriteOncePod", "RWOP", "파드 하나만 쓴다", ACC),
         (1, 0, "ReadWriteOnce", "RWO", "노드 하나가 붙인다 — 그 노드의 여러 파드는 쓴다", INFO),
         (0, 1, "ReadWriteMany", "RWX", "여러 노드가 동시에 읽고 쓴다", OK),
         (1, 1, "ReadOnlyMany", "ROX", "여러 노드가 동시에 읽기만", OK)]
for ci, ri, nm, ab, s, c in CELLS:
    cx, cy = CX[ci], CY[ri]
    if c is ACC:
        d.o.append(f'<rect x="{cx-180}" y="{cy-56}" width="360" height="112" rx="6" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(cx - 180, cy - 56, 360, 112, PAPER2, c, 1.1, 6)
    d.t(cx, cy - 20, nm, 13, c, MONO, "middle", 600)
    d.t(cx, cy + 2, ab, 11, MUTED, MONO)
    d.t(cx, cy + 30, ddx.fit(s, 10, 330, s), 10, MUTED, KR)

d.t(24, 540, "RWO 에서 다른 노드의 파드가 같은 볼륨을 붙이려 하면 Multi-Attach 에러로 Pending 에 걸린다. "
             "같은 노드의 파드끼리는 문제없이 함께 쓴다.", 11, MUTED, KR, "start")
d.t(24, 562, "RWOP 는 그 하나마저 파드 단위로 좁힌다 — 같은 노드라도 둘째 파드는 Pending 이다.",
     11, MUTED, KR, "start")
d.legend(588, [("파드로 좁힌다", ACC), ("노드가 단위", INFO), ("여럿이 함께", OK)])
d.save("10-01-access-mode-matrix.svg")
print("ok")

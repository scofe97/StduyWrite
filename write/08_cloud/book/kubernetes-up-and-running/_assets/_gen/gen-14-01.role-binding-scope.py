# 14-01 §Role 과 Binding — 네 리소스의 범위 조합
# 본문이 "위 도식의 점선, 즉 ClusterRole 을 RoleBinding 으로 묶어 범위를 한 네임스페이스로
# 좁히는 조합" 이라고 도식을 직접 가리킨다. 그러니 점선은 반드시 그 조합이어야 하고,
# 읽는 사람이 "점선" 을 찾아 짚을 수 있게 아래에 이름을 붙여 둔다.
# 네 칸 격자로 그리면 "범위는 바인딩이 정한다" 가 안 보이므로, 바인딩을 범위 띠 안에 넣는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, PAPER, RULE, KR, MONO
import ddx

W, H = 1240, 542
d = D(W, H, "KUBERNETES UP AND RUNNING · 14-01",
      "범위를 정하는 것은 바인딩이다",
      "역할은 추상적인 능력의 묶음이고, 바인딩은 그 묶음을 신원에 붙이는 행위다. 각각 "
      "네임스페이스판과 클러스터판이 있어 네 리소스가 된다.",
      "역할은 무엇을 할 수 있는지만 정하고, 어디까지 미치는지는 바인딩이 정한다")

LX, LW = 40, 260
BX, BW = 560, 656
BOX_X, BOX_W = 590, 250

def scope_band(y0, y1, binding, bsub, scope, ssub):
    d.box(BX, y0, BW, y1 - y0, PAPER, RULE, 1.0, 8)
    cy = (y0 + y1) / 2
    ddx.node(d, BOX_X + BOX_W / 2, cy, binding, bsub, w=BOX_W, h=70)
    d.t(BX + BW - 20, cy - 12, "범위", 8, SOFT, MONO, "end")
    d.t(BX + BW - 20, cy + 8, scope, 12, INK, KR, "end", 600)
    d.t(BX + BW - 20, cy + 28, ssub, 10, SOFT, KR, "end")

scope_band(160, 262, "RoleBinding", "네임스페이스 리소스",
           "그 네임스페이스 안에서만", "역할과 바인딩이 함께 든 그 네임스페이스다")
scope_band(282, 384, "ClusterRoleBinding", "클러스터 리소스",
           "클러스터 전체", "네임스페이스를 가리지 않는다")

ddx.node(d, LX + LW / 2, 211, "Role", "네임스페이스 안의 능력", w=LW, h=70)
ddx.node(d, LX + LW / 2, 333, "ClusterRole", "클러스터 범위의 능력", w=LW, h=70)

d.path("M 300 211 L 586 211", MUTED, 1.5, m="ar")
d.path("M 300 333 L 586 333", MUTED, 1.5, m="ar")
d.path("M 300 312 L 450 312 L 450 232 L 586 232", ACC, 1.5, m="acc", dash="6 5")

d.t(LX, 412, "Role 의 제약 둘 — 그 네임스페이스 안의 능력만 나타내고, "
              "CustomResourceDefinition 처럼 네임스페이스에 속하지 않는 리소스에는 쓸 수 없다.",
     11, MUTED, KR, "start")
d.t(LX, 434, "그래서 Role 은 ClusterRoleBinding 과 짝지어지지 않는다 — 위 도식에 그 선이 없는 이유다.",
     11, MUTED, KR, "start")
d.t(LX, 462, "점선 — ClusterRole 을 RoleBinding 으로 묶으면 클러스터 범위의 능력 묶음을 한 네임스페이스로 좁혀 쓴다. "
              "같은 묶음을 여러 네임스페이스에서 재사용할 때 실제로 가장 많이 쓰는 형태이나, 이 책은 다루지 않는다.",
     11, ACC, KR, "start")

d.legend(488, [("책 밖 보강 — 이 책이 다루지 않는 조합", ACC)])
d.save("14-01.role-binding-scope.svg")
print("h 필요:", 488 + 48, " 실제:", H)

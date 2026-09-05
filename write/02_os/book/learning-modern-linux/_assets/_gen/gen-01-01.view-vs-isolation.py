# 01-01 §5 — 가시성과 격리가 서로 다른 축이라는 것.
# 원문("Resource Visibility"): "The way to provide a local view on (certain supported) resources in Linux
#       is via namespaces." 그리고 "A second, independent dimension is that of isolation. When I use the
#       term isolation here, I don't necessarily qualify it—that is, I make no assumptions about how well
#       things are isolated." 메모리 소비를 제한해 다른 프로세스를 굶기지 않게 하는 것이 격리의 한 예이고
#       "In Linux we use a kernel feature called cgroups to provide this kind of isolation" 이다.
#       완전히 격리된 환경의 예로는 가상 머신을 든다. 기본값은 "a by-default global view on resources" 다.
# 타입 스펙: type-quadrant — 2x2. 축 라벨은 팁마다 한 단어, 항목은 r=4 점 + 라벨, 초점 하나.
#           항목이 축선을 걸치지 않게 놓는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, RULE, KR, MONO

W, H = 880, 572
d = D(W, H, "LEARNING MODERN LINUX · 01-01 §5",
      "무엇이 보이는가와 얼마나 갇혔는가는 다른 축이다",
      "가로축은 자원 뷰가 전역인가 로컬인가, 세로축은 격리가 약한가 강한가. 원서가 둘을 독립된 두 차원이라 "
      "적은 대목을 격자로 편 것이다. 색이 붙은 자리가 두 축이 갈린다는 증거다.",
      "namespace 는 뷰를 바꾸고 cgroups 는 뷰를 그대로 둔 채 몫을 자릅니다")

CX, CY = 440, 292
AX0, AX1 = 152, 764
AY0, AY1 = 152, 432

d.path(f"M {CX} {AY1} L {CX} {AY0}", INK, 1.2, m="ar")
d.path(f"M {AX0} {CY} L {AX1} {CY}", INK, 1.2, m="ar")
d.line(CX, AY1, CX, CY, INK, 1.2)
d.line(AX0, CY, CX, CY, INK, 1.2)

d.t(CX, AY0 - 14, "강함", 12, INK, KR, "middle")
d.t(CX, AY1 + 24, "약함", 12, INK, KR, "middle")
d.t(AX0 - 14, CY + 4, "전역", 12, INK, KR, "end")
d.t(AX1 + 14, CY + 4, "로컬", 12, INK, KR, "start")
d.t(CX + 12, AY0 - 32, "격리", 12, SOFT, KR, "start")
d.t(AX1 + 14, CY + 22, "자원 뷰", 12, SOFT, KR, "start")


def item(x, y, name, sub, focal=False, anchor="start"):
    c = ACC if focal else MUTED
    dx = 14 if anchor == "start" else -14
    d.o.append(f'<circle cx="{x}" cy="{y}" r="{5 if focal else 4}" fill="{c}"/>')
    d.t(x + dx, y - 4, name, 14, ACC if focal else INK, KR, anchor, 600)
    d.t(x + dx, y + 15, sub, 12, MUTED, KR, anchor)


item(268, 216, "cgroups", "몫을 자르되 목록은 그대로", focal=True)
item(612, 216, "가상 머신", "혼자 있는 것처럼 보이게", anchor="end")
item(268, 376, "보통의 프로세스", "리눅스의 기본값")
item(612, 376, "namespace", "보이는 것만 바꾼다", anchor="end")

d.t(164, 184, "몫은 잘렸는데 남의 것이 다 보인다", 12, SOFT, KR, "start")
d.t(752, 184, "자기만의 세계가 통째로 주어진다", 12, SOFT, KR, "end")
d.t(164, 410, "전부 보이고 아무것도 막지 않는다", 12, SOFT, KR, "start")
d.t(752, 410, "안 보이게는 했지만 굶기는 것은 못 막는다", 12, SOFT, KR, "end")

d.t(20, 484, "원서는 격리라는 말을 쓰면서 얼마나 잘 격리되는지는 따지지 않겠다고 미리 못 박습니다. "
             "그래서 이 두 축은 서로를 대신하지 못합니다.", 12, MUTED, KR, "start")

d.legend(508, [("두 축이 갈린다는 증거", ACC), ("원서가 든 나머지 예", MUTED)])
d.save("01-01.view-vs-isolation.svg")
print("ok 01-01.view-vs-isolation")

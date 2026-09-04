# a0-02 §4 특권을 파드에서 노드로 옮긴다.
# 본문(부록 B.2): istio-init 은 elevated permissions 를 요구하고 멀티테넌트 기준("a tenant must
#       not be able to harm another tenant")과 부딪힌다. CNI 플러그인은 "moves the istio-init
#       container functionality into centralized Pods that run on every node".
# 타입 스펙: type-architecture — 무엇이 어느 경계에 배치되고 무엇이 사라지는지가 논점이다.
#           존과 컴포넌트로 두 배치를 나란히 두고 관계선을 긋는다.
#           축약: accent 는 특권 요구가 사라지는 자리 하나에.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, BAD, OK, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 600
d = D(W, H, "ISTIO IN ACTION · A0-02 §4",
      "같은 일을 어디서 하느냐가 권한 요구를 바꾼다",
      "왼쪽은 파드마다 init 컨테이너가 규칙을 세우는 배치이고 오른쪽은 노드마다 도는 파드가 "
      "대신하는 배치다. 색이 붙은 자리에서 특권 요구가 사라진다.",
      "OpenShift 프로파일이 이 플러그인을 켜 두는 이유입니다")

def zone(x, y, w, h, label):
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{INK}05" '
               f'stroke="{INK}33" stroke-width="1" stroke-dasharray="4 4"/>')
    tw = len(label) * 6 + 14
    d.o.append(f'<rect x="{x + 12}" y="{y - 7}" width="{tw}" height="14" fill="{PAPER}"/>')
    d.t(x + 18, y + 3, label, 8, SOFT, MONO, "start", 600)

def comp(x, y, w, h, name, sub, c=None, focal=False):
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    elif c:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" '
                   f'fill="{c}12" stroke="{c}" stroke-width="1.2"/>')
    else:
        d.box(x, y, w, h, PAPER2, RULE, 1.0, 6)
    d.t(x + w / 2, y + 26, name, 12, ACC if focal else (c or INK), KR, "middle", 600)
    d.t(x + w / 2, y + 46, sub, 11, MUTED, KR, "middle")

d.t(248, 122, "ISTIO-INIT 배치", 11, SOFT, MONO, "middle", 600)
d.t(752, 122, "CNI 플러그인 배치", 11, SOFT, MONO, "middle", 600)

zone(28, 148, 440, 240, "NODE")
zone(532, 148, 440, 240, "NODE")

comp(48, 180, 196, 64, "파드 A", "init 이 붙는다", BAD)
comp(272, 180, 176, 64, "파드 B", "init 이 붙는다", BAD)
comp(48, 288, 400, 64, "팀마다 특권을 받아야 한다", "테넌트 기준과 부딪힌다", BAD)

comp(552, 180, 196, 64, "파드 A", "init 이 없다", OK)
comp(776, 180, 176, 64, "파드 B", "init 이 없다", OK)
comp(552, 288, 400, 64, "CNI 파드 하나가 노드에 뜬다", "모든 파드의 규칙을 대신 세운다", focal=True)

for x in (146, 360):
    d.arrow([(x, 244), (x, 284)], BAD, "bad", 1.3)
for x in (650, 864):
    d.arrow([(x, 352), (x, 248)], ACC, "acc", 1.4)

d.path("M 468 268 L 528 268", MUTED, 1.4, m="ar")
d.t(498, 250, "옮긴다", 11, MUTED, KR, "middle", 600)

d.t(28, 424, "멀티테넌트 기준 — 한 테넌트가 다른 테넌트를 해칠 수 없어야 한다", 11, SOFT, KR, "start")
d.t(28, 448, "권한을 안 주면 워크로드를 못 돌리고 주면 남용될 수 있다. 어느 쪽으로 가도 기준이 깨진다", 11, MUTED, KR, "start")
d.t(28, 472, "일을 노드로 옮기면 istio-init 자체가 필요 없어지고 그 특권 요구도 함께 사라진다", 11, SOFT, KR, "start")
d.legend(500, [("특권 요구가 사라지는 자리", ACC), ("기준과 부딪히는 자리", BAD), ("특권이 필요 없는 파드", OK)])
d.save("a0-02.init-vs-cni.svg")

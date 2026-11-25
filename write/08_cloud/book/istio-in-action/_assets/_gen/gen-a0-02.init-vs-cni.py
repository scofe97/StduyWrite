# a0-02 §4 특권을 파드에서 노드로 옮긴다.
# 값 근거(본문 §4 · 부록 B.2 · Istio 1.32 CNI 문서):
#   - istio-init 은 NET_ADMIN · NET_RAW 권한이 필요해 멀티테넌트 기준(한 테넌트가 다른 테넌트를 해칠 수 없음)과 충돌.
#   - Istio CNI 노드 에이전트는 노드마다 데몬셋으로 돌아 기존 CNI 플러그인 뒤에 이어 실행되는(chained) 플러그인을 설치해 리디렉션을 대신 수행.
#   - 파드의 istio-init 과 팀별 RBAC 특권 요구가 사라진다.
# 타입 스펙: type-architecture — 두 배치를 존과 컴포넌트로 나란히 두고 관계선을 긋는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, BAD, OK, PAPER2, RULE, KR, MONO

W, H = 960, 480
d = D(W, H, "ISTIO IN ACTION · A0-02 §4",
      "리디렉션 주체를 노드로 옮겨 파드 특권을 없앤다",
      "왼쪽은 파드마다 istio-init 컨테이너가 NET_ADMIN·NET_RAW 권한으로 규칙을 세우는 배치이고, "
      "오른쪽은 노드마다 도는 Istio CNI 데몬셋 파드가 대신 세우는 배치다.",
      lead="멀티테넌트 보안 기준(다른 테넌트를 해칠 수 없음)을 지키면서 리디렉션을 수행하는 구조 변화입니다.")


def zone(x, y, w, h, label):
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{INK}05" '
               f'stroke="{INK}33" stroke-width="1" stroke-dasharray="4 4"/>')
    d.t(x + 16, y + 22, label, 12, SOFT, MONO, "start", 600)


def comp(x, y, w, h, name, sub, c=None, focal=False):
    if focal:
        d.tone(x, y, w, h, ACC, 6, "14", 1.4)
    elif c:
        d.tone(x, y, w, h, c, 6, "12", 1.2)
    else:
        d.box(x, y, w, h, PAPER2, RULE, 1.0, 6)
    fam = KR if any("가" <= ch <= "힣" for ch in name) else MONO
    d.t(x + w / 2, y + 28, name, 13, ACC if focal else (c or INK), fam, "middle", 600)
    d.t(x + w / 2, y + 50, sub, 13, MUTED, KR, "middle")


d.t(236, 114, "ISTIO-INIT 배치", 12, SOFT, MONO, "middle", 600)
d.t(724, 114, "ISTIO CNI 배치", 12, SOFT, MONO, "middle", 600)

zone(24, 132, 424, 256, "NODE")
zone(512, 132, 424, 256, "NODE")

comp(44, 172, 180, 68, "파드 A", "istio-init 포함", BAD)
comp(248, 172, 180, 68, "파드 B", "istio-init 포함", BAD)
comp(44, 296, 384, 68, "팀마다 NET_ADMIN·NET_RAW 권한 필요", "남용 시 다른 테넌트 침해 위험", BAD)

comp(532, 172, 180, 68, "파드 A", "init 컨테이너 없음", OK)
comp(736, 172, 180, 68, "파드 B", "init 컨테이너 없음", OK)
comp(532, 296, 384, 68, "Istio CNI 데몬셋 (chained CNI)", "모든 파드의 리디렉션 대신 설정", focal=True)

for x in (134, 338):
    d.arrow([(x, 240), (x, 294)], BAD, "bad", 1.3)
for x in (622, 826):
    d.arrow([(x, 296), (x, 242)], ACC, "acc", 1.4)

d.path("M 448 260 L 508 260", MUTED, 1.4, m="ar")
d.t(478, 246, "대체", 13, MUTED, KR, "middle", 600)
d.t(142, 268, "특권 요구", 12, BAD, KR, "start", 600)
d.t(630, 268, "리디렉션 설정", 12, ACC, KR, "start", 600)

d.legend(416, [("특권을 모은 노드 에이전트", ACC), ("보안 기준과 부딪히는 자리", BAD), ("특권이 필요 없는 파드", OK)])
d.save("a0-02.init-vs-cni.svg")
print("ok init-vs-cni")

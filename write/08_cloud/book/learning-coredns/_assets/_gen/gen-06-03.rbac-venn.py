# 06-03 §2 — ClusterRole 이 준 자원 다섯과 기본 설정이 실제로 쓰는 셋.
# 원문 근거: ClusterRole 은 endpoints·services·pods·namespaces 에 list·watch 를, nodes 에 get 을 준다 /
#            "the ability to watch and list Endpoints and Services makes sense" / 네임스페이스는
#            NXDOMAIN 판단과 와일드카드 질의에 필요하다 / "The answer for whether it needs pods and
#            nodes is 'probably not.'" / "CoreDNS needs to watch pods only if you enable the pods
#            verified option ... If this is not enabled, there is no need to keep the privilege".
# 타입 스펙: type-venn — 두 집합의 포함 관계가 논지이고, 바깥 고리가 지울 수 있는 권한이다.
#           반지름은 원소 수에 비례하게 잡는다(5:3 → sqrt 비 1.29). 눈대중으로 같게 만들지 않는다.
import sys, math; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, OK, KR, MONO

W, H = 880, 740
d = D(W, H, "LEARNING COREDNS · 06-03 §2",
      "부여된 권한과 실제로 쓰는 권한",
      "바깥 원이 ClusterRole 이 준 자원 다섯, 안쪽 원이 기본 Corefile 이 실제로 쓰는 셋이다. "
      "두 원 사이의 고리가 배포 편의로 미리 준 권한이다.",
      "주황 고리가 지워도 되는 자리입니다")

CAX, CAY, RA = 440, 340, 236
CBX, CBY, RB = 440, 396, 156

d.o.append(f'<circle cx="{CAX}" cy="{CAY}" r="{RA}" fill="{MUTED}0A" stroke="{MUTED}" stroke-width="1.2"/>')
d.o.append(f'<circle cx="{CBX}" cy="{CBY}" r="{RB}" fill="{OK}12" stroke="{OK}" stroke-width="1.4"/>')

d.t(24, 128, "ClusterRole 이 준 다섯", 14, MUTED, KR, "start", 600)
d.t(24, 148, "system:coredns", 12, SOFT, MONO, "start")
d.t(856, 128, "기본 Corefile 이 쓰는 셋", 14, OK, KR, "end", 600)
d.t(856, 148, "endpoints · services · namespaces", 12, SOFT, MONO, "end")

d.tone(300, 152, 280, 76, ACC, 8, "12", 1.4)
d.t(440, 180, "pods · nodes", 15, ACC, MONO, "middle", 600)
d.t(440, 204, "배포 편의로 미리 준 것", 12, ACC, KR)

d.t(440, 356, "endpoints · services", 15, OK, MONO, "middle", 600)
d.t(440, 380, "namespaces", 15, OK, MONO, "middle", 600)
d.t(440, 408, "레코드를 만드는 데 실제로 쓴다", 12, MUTED, KR)

# 설명 줄은 두 원 바깥에 둔다. 원 안에 두면 그 집합의 속성으로 읽힌다.
d.t(20, 604, "nodes 만 동사가 get 이고 나머지 넷은 list · watch 다 — 다섯 어디에도 쓰기 동사가 없다", 13, MUTED, KR, "start")
d.t(20, 628, "네임스페이스는 NXDOMAIN 을 줄지 정하는 데 쓰이고 와일드카드 질의에도 필요하다", 13, MUTED, KR, "start")
d.t(20, 652, "파드는 pods verified 를 켤 때만 감시가 필요하고, 안 켜면 그 권한을 남길 이유가 없다", 13, MUTED, KR, "start")

d.legend(680, [("지워도 되는 고리", ACC), ("기본 설정이 쓰는 집합", OK)])
d.save("06-03.rbac-venn.svg")

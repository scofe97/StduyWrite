# 11-01 §1 유령 워크로드 — 원문 그림 11.1.
# 본문(원문 11.1): 성능이 나빠질 때 나타나는 흔한 현상이 phantom workloads 다. 서비스가 이미 사라진
#       엔드포인트로 트래픽을 보내도록 설정돼 있어 요청이 실패한다. 순서는 셋이다 —
#       (1) 불건강해지는 워크로드가 이벤트를 낸다 (2) 갱신이 늦어 서비스가 낡은 설정을 갖는다
#       (3) 그 낡은 설정 때문에 존재하지 않는 워크로드로 트래픽을 보낸다.
#       짧은 지연은 기본 재시도 두 번과 이상값 감지가 덮어 주지만, 몇 초를 넘기면 최종 사용자에 닿는다.
# 원문 그림 11.1 은 개념도라 주소를 적지 않는다 — 노트도 지어내지 않고 파드 이름으로만 가리킨다.
# 타입 스펙: type-deployment — 무엇이 어디에 있고 무엇이 없는지가 논점이다. 존 2 · 노드 5 · 경로 2,
#           accent 는 설정에는 남아 있지만 실제로는 없는 자리 하나.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, BAD, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 616
d = D(W, H, "ISTIO IN ACTION · 11-01 §1",
      "설정에는 남아 있고 클러스터에는 없다",
      "왼쪽은 실제 클러스터, 오른쪽은 프록시가 들고 있는 엔드포인트 목록이다. 색이 붙은 줄이 이미 "
      "사라졌는데도 목록에 남아 있는 항목이고, 그리로 간 요청이 실패한다.",
      "짧은 지연은 재시도와 이상값 감지가 덮지만 몇 초를 넘기면 최종 사용자에 닿습니다")

def zone(x, y, w, h, label):
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="rgba(245,245,245,0.02)" stroke="rgba(245,245,245,0.10)" stroke-width="0.8"/>')
    lw = len(label) * 12 + 16
    d.o.append(f'<rect x="{x + 12}" y="{y + 4}" width="{lw}" height="18" rx="2" fill="{PAPER}"/>')
    d.t(x + 12 + lw / 2, y + 17, label, 12, SOFT, KR)

def node(x, y, w, h, tag, name, sub, c=None, focal=False, gone=False):
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    elif gone:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{INK}04" '
                   f'stroke="{MUTED}" stroke-width="1" stroke-dasharray="5 5"/>')
    elif c:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{c}12" stroke="{c}" stroke-width="1.2"/>')
    else:
        d.box(x, y, w, h, PAPER2, RULE, 1.0, 6)
    d.o.append(f'<rect x="{x + 12}" y="{y + 12}" width="44" height="14" rx="2" fill="{INK}14"/>')
    d.t(x + 34, y + 23, tag, 8, INK, MONO, "middle", 600)
    d.t(x + 66, y + 24, name, 13, ACC if focal else (SOFT if gone else INK), KR, "start", 600)
    d.t(x + 66, y + 42, sub, 11, MUTED, MONO, "start")

zone(20, 128, 432, 200, "실제 클러스터")
zone(552, 128, 432, 300, "프록시가 들고 있는 엔드포인트 목록")

node(40, 160, 392, 60, "POD", "catalog-1", "Running", OK)
node(40, 236, 392, 60, "POD", "catalog-2", "terminated", gone=True)
node(568, 160, 392, 60, "EP", "catalog-1 의 주소", "HEALTHY")
node(568, 236, 392, 60, "EP", "catalog-2 의 주소", "가리키는 파드가 없다", focal=True)
node(568, 336, 392, 60, "REQ", "그리로 간 요청", "실패한다", BAD)

d.path("M 432 190 H 516 V 190 H 568", MUTED, 1.2, m="ar")
d.path("M 432 266 H 516 V 266 H 568", ACC, 1.5, m="acc", dash="5 4")
d.t(500, 250, "갱신이 늦다", 11, ACC, KR, "middle", 600)
d.path("M 764 296 V 332", BAD, 1.4, m="bad")

d.t(28, 476, "저자가 든 순서 — 워크로드가 불건강해져 이벤트가 나고, 갱신이 늦어 설정이 낡고, 낡은 설정이 없는 곳으로 보낸다", 11, SOFT, KR, "start")
d.t(28, 500, "기본 재시도 두 번과 이상값 감지가 짧은 지연을 덮어 준다 — 그래서 몇 초까지는 견딜 만하다", 11, MUTED, KR, "start")
d.legend(528, [("설정에만 남은 항목", ACC), ("살아 있는 것", OK), ("실패로 끝나는 요청", BAD)])
d.save("11-01.phantom-workload.svg")

# 12-01 §2 멀티 클러스터 배포 모델 셋 — 원문 그림 12.2 · 12.3 · 12.4.
# 본문(원문 12.2.1): 주 클러스터는 Istio 컨트롤 플레인이 설치된 클러스터이고 원격 클러스터는 그 설치에서
#       멀리 있는 클러스터다. primary-remote 는 컨트롤 플레인 하나가 메시를 관리해 자원을 덜 쓰지만 주
#       클러스터의 장애가 메시 전체에 미쳐 가용성이 낮다. primary-primary 는 컨트롤 플레인이 여럿이라 자원을
#       더 쓰는 대신 장애가 그 클러스터 안으로 갇혀 가용성이 높다. external control plane 은 모든 클러스터가
#       컨트롤 플레인에 대해 원격이며, 클라우드 사업자가 Istio 를 관리형 서비스로 제공할 수 있게 한다.
# 저자는 실습에서 primary-primary 를 고른다 — ACME 의 요구가 고가용성이기 때문이다.
# 타입 스펙: type-deployment — 무엇이 어느 클러스터에 놓이는지가 논점이다. 존 3 · 노드 7 · 경로 4,
#           accent 는 저자가 실습에서 고른 모델 하나.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 560
d = D(W, H, "ISTIO IN ACTION · 12-01 §2",
      "컨트롤 플레인을 어디에 몇 개 둘까",
      "세 모델은 컨트롤 플레인의 자리와 개수만 다르다. 저자가 자원과 가용성을 맞대어 비교하는 것은 앞의 둘뿐이고, "
      "세 번째는 누가 운영하느냐가 다른 모델이다. 색이 붙은 모델이 저자가 실습에서 고른 쪽이다.",
      "고를 근거는 기술이 아니라 몇 분의 다운타임을 견딜 수 있느냐입니다")

def zone(x, y, w, h, label, focal=False):
    c = ACC if focal else "rgba(245,245,245,0.10)"
    f = f"{ACC}08" if focal else "rgba(245,245,245,0.02)"
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{f}" stroke="{c}" stroke-width="{1.4 if focal else 0.8}"/>')
    lw = len(label) * 12 + 16
    d.o.append(f'<rect x="{x + 12}" y="{y + 4}" width="{lw}" height="18" rx="2" fill="{PAPER}"/>')
    d.t(x + 12 + lw / 2, y + 17, label, 12, ACC if focal else SOFT, KR)

def node(x, y, w, h, tag, name, sub, c=None):
    if c:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{c}12" stroke="{c}" stroke-width="1.2"/>')
    else:
        d.box(x, y, w, h, PAPER2, RULE, 1.0, 6)
    d.o.append(f'<rect x="{x + 10}" y="{y + 10}" width="34" height="14" rx="2" fill="{INK}14"/>')
    d.t(x + 27, y + 21, tag, 8, INK, MONO, "middle", 600)
    d.t(x + 54, y + 22, name, 12, c or INK, KR, "start", 600)
    d.t(x + 54, y + 40, sub, 11, MUTED, MONO, "start")

CW, GAP, X0, ZY, ZH = 308, 20, 20, 128, 216
def zx(i): return X0 + i * (CW + GAP)

zone(zx(0), ZY, CW, ZH, "primary-remote")
zone(zx(1), ZY, CW, ZH, "primary-primary", focal=True)
zone(zx(2), ZY, CW, ZH, "external control plane")

node(zx(0) + 20, ZY + 44, CW - 40, 60, "CP", "istiod", "주 클러스터에만", INFO)
node(zx(0) + 20, ZY + 132, CW - 40, 60, "REM", "원격 클러스터", "컨트롤 플레인 없음")
node(zx(1) + 20, ZY + 44, CW - 40, 60, "CP", "istiod", "클러스터마다 하나", INFO)
node(zx(1) + 20, ZY + 132, CW - 40, 60, "CP", "istiod", "클러스터마다 하나", INFO)
node(zx(2) + 20, ZY + 44, CW - 40, 60, "EXT", "istiod", "메시 밖에 산다", INFO)
node(zx(2) + 20, ZY + 132, CW - 40, 60, "REM", "모든 클러스터", "전부 원격이다")

# primary-remote 와 external 은 위가 아래로 설정을 내리는 관계라 화살표가 맞다.
# primary-primary 는 컨트롤 플레인 둘이 각자 자기 클러스터를 맡는 peer 이므로
# 화살표를 그리면 없는 방향이 생긴다. 그 열만 방향 없는 점선으로 잇는다.
for i in range(3):
    if i == 1:
        d.path(f"M {zx(i) + CW / 2} {ZY + 104} V {ZY + 130}", ACC, 1.4, dash="5 4")
        d.t(zx(i) + CW / 2 + 14, ZY + 122, "서로 독립", 11, ACC, KR, "start", 600)
        continue
    d.path(f"M {zx(i) + CW / 2} {ZY + 104} V {ZY + 130}", MUTED, 1.2, m="ar")

BY = 388
# 저자는 자원·가용성을 primary-remote 와 primary-primary 둘 사이에서만 비교한다.
# external control plane 의 두 축은 원문에 없으므로 값을 지어내지 않고 비워 둔다.
rows = [("자원", "적게 쓴다", "많이 쓴다", "저자가 비교하지 않음"),
        ("가용성", "주 클러스터가 죽으면 전부", "장애가 그 클러스터에 갇힌다", "저자가 비교하지 않음")]
for k, (label, *vals) in enumerate(rows):
    y = BY + k * 28
    d.t(X0, y, label, 11, SOFT, KR, "start", 600)
    for i, v in enumerate(vals):
        d.t(zx(i) + CW / 2, y, v, 11, ACC if i == 1 else MUTED, KR, "middle")

d.t(24, 464, "저자가 고른 근거 — ACME 는 1분의 다운타임이 수백만 달러라 고가용성이 최우선이다", 11, SOFT, KR, "start")
d.legend(492, [("저자가 실습에서 고른 모델", ACC), ("컨트롤 플레인", INFO)])
d.save("12-01.deployment-models.svg")

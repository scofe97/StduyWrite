# 타입 스펙: type-architecture — 빌드 · 저장 · 배포 세 존을 가로로 놓고 빌드 머신 → push → 레지스트리 → pull → 클러스터로 이미지가 흐른다. 존마다 약한 고리 두 개와 짝지은 대응 두 개를 쌓는다. focal 은 빌드 존의 RUN 편집 = 원격 코드 실행.
# 사실 출처: 노트 L21~L23(무결성 · RUN 경고), L55~L60 · L80~L82(Dockerfile 접근 통제 · RUN), L96~L105(빌드 머신), L109~L135(레지스트리 · 서명 · in-toto), L147~L157(태그 · URL 한 글자), L161~L171(어드미션)
# Layout conventions: 존 폭 288 · 간격 40(x=20·348·676), 존 y=100, 흐름 노드 y=140 h=64, 약한 고리/대응 쌍 stride 96(h=36 · 간격 8), 모든 좌표 4의 배수.
import sys, pathlib
ASSETS = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ASSETS))
from dd import D, INK, MUTED, SOFT, ACC, OK, WARN, BAD, INFO, KR, MONO, RULE

W, H = 984, 500
ZX = [20, 348, 676]
ZW = 288
NW = 256


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def fit(t, size, limit):
    w = sum(size if "가" <= c <= "힣" else size * 0.62 for c in t)
    assert w <= limit, (t, w, limit)


d = D(W, H, "CONTAINER SECURITY · 06-02 OVERVIEW",
      "빌드 · 저장 · 배포 세 고리마다 약한 고리와 대응이 있습니다",
      "이미지는 빌드 머신에서 레지스트리를 거쳐 클러스터로 흐르고, 세 단계 모두에 약한 고리가 있으며 단계마다 짝지은 대응이 붙는다.",
      "이미지 무결성은 세 단계가 모두 지켜질 때만 성립합니다.")

ZONES = [
    ("빌드", "빌드 머신", "Dockerfile → 이미지",
     [("`RUN` 편집 = 원격 코드 실행", "편집 권한 제한 + 코드 리뷰", True),
      ("빌드 머신 침해 → 백도어", "프로덕션과 분리된 빌드 머신", False)]),
    ("저장", "레지스트리", "이미지 저장",
     [("이미지 교체 · 수정", "이미지 서명 · in-toto", False),
      ("레지스트리 주소 DNS 스푸핑", "자체 · 관리형 레지스트리 (VPC 안)", False)]),
    ("배포", "클러스터", "배포 YAML → 컨테이너 실행",
     [("태그는 불변이 아님", "태그 대신 다이제스트 참조", False),
      ("레지스트리 URL 한 글자 변형", "어드미션 컨트롤", False)]),
]

ZY, ZH = 100, 328
NY, NH = 140, 64
PY0, PSTRIDE, BH = 228, 96, 36

for i, (zname, nname, nsub, pairs) in enumerate(ZONES):
    zx = ZX[i]
    d.o.append(f'<rect x="{zx}" y="{ZY}" width="{ZW}" height="{ZH}" rx="8" fill="#F5F5F308" stroke="{RULE}" stroke-width="0.9" stroke-dasharray="6 5"/>')
    d.t(zx + 16, ZY + 22, zname, 12, MUTED, KR, "start", 600)
    nx = zx + 16
    fit(nname, 14, NW - 16)
    fit(nsub, 12, NW - 16)
    d.box(nx, NY, NW, NH, "#161B22", RULE, 1.0)
    d.t(nx + NW / 2, NY + 26, nname, 14, INK, kr(nname), "middle", 600)
    d.t(nx + NW / 2, NY + 48, nsub, 12, MUTED, kr(nsub), "middle")
    d.line(nx + NW / 2, NY + NH, nx + NW / 2, PY0, SOFT, 1.0)
    for k, (weak, defense, focal) in enumerate(pairs):
        wy = PY0 + k * PSTRIDE
        dy = wy + BH + 8
        wl = weak.replace("`", "")
        fit(wl, 13, NW - 24)
        fit(defense, 13, NW - 24)
        c = ACC if focal else BAD
        d.tone(nx, wy, NW, BH, c, 6, "1F" if focal else "14", 1.4 if focal else 1.1)
        d.t(nx + NW / 2, wy + 23, wl, 13, c if not focal else INK, kr(wl), "middle", 600)
        d.tone(nx, dy, NW, BH, OK, 6, "14", 1.1)
        d.t(nx + NW / 2, dy + 23, defense, 13, OK, kr(defense), "middle", 400)

# 존 사이 이미지 흐름
cy = NY + NH // 2
for j, lab in enumerate(["push", "pull"]):
    x1 = ZX[j] + 16 + NW + 2
    x2 = ZX[j + 1] + 16 - 4
    d.arrow([(x1, cy), (x2, cy)], MUTED, "ar", 1.5)
    d.t((x1 + x2) / 2, cy - 9, lab, 12, MUTED, MONO, "middle", 600)

d.legend(ZY + ZH + 24, [("약한 고리", BAD), ("대응", OK), ("가장 날카로운 경고", ACC)])
d.save(str(ASSETS / "06-02.supply-chain.svg"))
print("ok 06-02 supply-chain")

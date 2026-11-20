# 01-01.chapter-overview — 키워드를 노드로, 앞 키워드에서 뒤 키워드로 넘어가는 관계를 화살표 라벨로 이은 편 전체 지도
# 행 하나가 본문 `##` 하나다. 왼쪽 칩은 절 번호, 노드는 그 절의 핵심 키워드와 실제 값, 화살표 라벨은 두 키워드 사이의 관계다.
# 노드 근거: §1 = 1절 `>` 요약과 Target state·Live state·Sync status 문단, §2 = 2절 `>` 요약과 네 원칙 표(셋째 Pulled Automatically,
#            넷째 Continuously Reconciled)와 `timeout.reconciliation` 기본 120초, §3 = 3절 `>` 요약과 Helm 비교 문단(HelmRelease, helm template).
#            편의 한 줄은 핵심 요약의 "주기적인 조정 루프" 이므로 §2 의 세 번째 노드에 건다.
# 타입 스펙: type-process — 행마다 같은 의미 슬롯(문제 · 중간 · 대응)이 같은 자리에 반복된다("Stage framework with semantic slots").
#           화살표는 읽는 순서이고 라벨은 관계다. 형제 편 gen-45-02.chapter-overview.py 와 같은 열 간격을 쓴다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INK, MUTED, SOFT, OK, INFO, KR, MONO

W = 1000
COL_X, STRIDE, NW, NH = 64, 344, 216, 64
ROW_Y, ROW_STRIDE = 104, 92
ROWS = 3
H = ROW_Y + (ROWS - 1) * ROW_STRIDE + NH + 24 + 48

d = D(W, H, "CHAPTER MAP · 01-01",
      "Argo CD 는 Git 과 클러스터를 주기마다 비교해 어긋남을 막는다",
      "01-01 편의 전체 지도. 첫 행은 손으로 고친 클러스터의 구성 드리프트를 Application 의 Target state 와 Live state 비교로 가려 "
      "Synced 와 OutOfSync 로 판정하는 흐름, "
      "둘째 행은 이벤트 기반 CD 를 GitOps 의 셋째·넷째 원칙이 가르고 그 결과가 기본 간격 약 3분(120초에 jitter 를 더함)의 조정 루프로 나타나는 흐름, "
      "셋째 행은 Argo 프로젝트 도구 넷 중 하나인 Argo CD 가 Flux 와 Helm 을 다루는 방식에서 갈려 helm template 으로 차트를 펼치는 흐름을 보인다.",
      lead="행은 본문 절, 화살표 라벨은 앞 키워드에서 뒤 키워드로 넘어가는 관계")


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def nx(j):
    return COL_X + j * STRIDE


def ny(i):
    return ROW_Y + i * ROW_STRIDE


def node(i, j, title, sub, c=None):
    x, y = nx(j), ny(i)
    if c:
        d.tone(x, y, NW, NH, c, 6, "14", 1.4 if c == ACC else 1.1)
    else:
        d.box(x, y, NW, NH)
    d.t(x + NW / 2, y + 27, title, 14, c or INK, kr(title), "middle", 600)
    d.t(x + NW / 2, y + 49, sub, 12, MUTED, kr(sub), "middle")


def harrow(i, j, label):
    y = ny(i) + NH / 2
    x1, x2 = nx(j) + NW, nx(j + 1)
    d.arrow([(x1 + 2, y), (x2 - 4, y)], MUTED, "ar", 1.4)
    d.t((x1 + x2) / 2, y - 10, label, 12, MUTED, kr(label), "middle", 600)


for i in range(ROWS):
    d.chip(34, ny(i) + NH / 2 - 4, f"§{i + 1}", MUTED, 11, 4)

# §1 구성 드리프트를 Application 단위로 막기
node(0, 0, "구성 드리프트", "손으로 고친 클러스터", INFO)
node(0, 1, "Application", "Target · Live state 비교", None)
node(0, 2, "Sync status", "Synced · OutOfSync", OK)
harrow(0, 0, "단위로 묶음")
harrow(0, 1, "차이를 판정")

# §2 GitOps 네 원칙과 pull 방식
node(1, 0, "이벤트 기반 CD", "파이프라인을 한 번 실행", INFO)
node(1, 1, "셋째·넷째 원칙", "Pulled · Reconciled", None)
node(1, 2, "조정 루프", "120초 + jitter, 약 3분", ACC)
harrow(1, 0, "GitOps 와 가름")
harrow(1, 1, "주기마다 반복")

# §3 Flux 와 Argo 프로젝트 속의 Argo CD
node(2, 0, "Argo CD", "Argo 도구 넷 중 하나", INFO)
node(2, 1, "Helm 처리", "Flux 는 HelmRelease", None)
node(2, 2, "helm template", "Live state 와 비교 가능", OK)
harrow(2, 0, "Flux 와 갈림")
harrow(2, 1, "펼치기만 함")

d.legend(ny(ROWS - 1) + NH + 24, [("문제", INFO), ("이 편의 한 줄", ACC), ("대응", OK)])
d.save("01-01.chapter-overview.svg")

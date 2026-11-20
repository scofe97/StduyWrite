# 04-01.chapter-overview — 키워드를 노드로, 앞 키워드에서 뒤 키워드로 넘어가는 관계를 화살표 라벨로 이은 편 전체 지도
# 행 하나가 본문 `##` 하나다. 왼쪽 칩은 절 번호, 노드는 그 절의 핵심 키워드와 실제 값, 화살표 라벨은 두 키워드 사이의 관계다.
# 노드 근거: §1 = 1절 `>` 요약과 Application 선언의 필드 구조·source 와 destination 문단,
#            §2 = 2절 `>` 요약과 렌더링 도구를 고르는 규칙 문단(Chart.yaml · kustomization.yaml), 핵심 요약의 "Repository Server 가 렌더링",
#            §3 = 3절 `>` 요약과 수동 동기화 문단(sync 전 OutOfSync), finalizer 와 연쇄 삭제 문단(`metadata.finalizers`).
#            편의 한 줄은 핵심 요약 첫 문장이 말하는 Application 이 배포를 관리하는 가장 작은 단위라는 점이므로
#            §1 의 가운데 노드에 건다. §3 의 finalizer 는 삭제 방식을 고르는 대응이라 초록, 남거나 지워지는 결과는 색을 두지 않는다.
# 타입 스펙: type-process — 행마다 같은 의미 슬롯(문제 · 중간 · 대응)이 같은 자리에 반복된다("Stage framework with semantic slots").
#           화살표는 읽는 순서이고 라벨은 관계다. 형제 편 gen-01-01.chapter-overview.py 와 같은 열 간격을 쓴다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INK, MUTED, SOFT, OK, INFO, KR, MONO

W = 1000
COL_X, STRIDE, NW, NH = 64, 344, 216, 64
ROW_Y, ROW_STRIDE = 104, 92
ROWS = 3
H = ROW_Y + (ROWS - 1) * ROW_STRIDE + NH + 24 + 48

d = D(W, H, "CHAPTER MAP · 04-01",
      "Application 은 소스를 대상에 맞추는 선언이고 삭제는 finalizer 가 정한다",
      "04-01 편의 전체 지도. 첫 행은 매니페스트가 있는 곳인 source 를 Application 이 담아 클러스터와 네임스페이스인 destination 에 맞추는 선언, "
      "둘째 행은 소스 폴더의 파일을 보고 Helm 이나 Kustomize 를 골라 렌더링한 매니페스트가 클러스터에 닿는 흐름, "
      "셋째 행은 sync 를 해야 배포되는 새 Application 을 지울 때 finalizer 유무가 리소스를 남기거나 지우는 흐름을 보인다.",
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

# §1 Application 구조 — 소스와 대상
node(0, 0, "source", "매니페스트가 있는 곳", INFO)
node(0, 1, "Application", "가장 작은 배포 단위", ACC)
node(0, 2, "destination", "클러스터와 네임스페이스", OK)
harrow(0, 0, "위치를 적음")
harrow(0, 1, "대상에 맞춤")

# §2 템플릿 도구 — Helm 과 Kustomize
node(1, 0, "소스 폴더", "Chart.yaml 이 있으면 Helm", INFO)
node(1, 1, "Helm · Kustomize", "Repository Server 가 렌더", None)
node(1, 2, "렌더가 끝난 매니페스트", "Helm 릴리스는 안 생김", OK)
harrow(1, 0, "폴더로 고름")
harrow(1, 1, "렌더링한 결과")

# §3 수명 주기 — 배포·상태·삭제
node(2, 0, "수동 동기화", "sync 전에는 OutOfSync", INFO)
node(2, 1, "finalizer", "metadata.finalizers 목록", OK)
node(2, 2, "남거나 지워짐", "리소스는 finalizer 가 정함")
harrow(2, 0, "만든 뒤 지울 때")
harrow(2, 1, "유무가 가름")

d.legend(ny(ROWS - 1) + NH + 24, [("문제", INFO), ("이 편의 한 줄", ACC), ("대응", OK)])
d.save("04-01.chapter-overview.svg")

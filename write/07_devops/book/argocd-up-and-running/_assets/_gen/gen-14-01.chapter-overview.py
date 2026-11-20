# 14-01.chapter-overview — 키워드를 노드로, 앞 키워드에서 뒤 키워드로 넘어가는 관계를 화살표 라벨로 이은 편 전체 지도
# 행 하나가 본문 `##` 하나다. 왼쪽 칩은 절 번호, 노드는 그 절의 핵심 키워드와 실제 값, 화살표 라벨은 두 키워드 사이의 관계다.
# 노드 근거: 1행은 §1 요약(DRY, 본체 하나와 변경분, overlay 와 매개변수), 2행은 §2 요약과 분리 이유 다섯 가지(빌드 트리거 무한 반복), monorepo · polyrepo 와 Conway 법칙,
#           3행은 §3 요약과 핵심 요약(배포 때 렌더, rendered manifests 패턴, Source Hydrator 의 drySource · syncSource), 4행은 §4 요약과 병합 전략 절(환경 브랜치, trunk 하나, 릴리스 산출물),
#           5행은 §5 요약과 핵심 요약(Argo CD 는 점진 배포와 승격을 직접 하지 않음, Argo Rollouts · Image Updater, write-back 의 argocd · git). 값은 모두 본문에 적힌 것이다.
# 타입 스펙: type-process — 행마다 같은 의미 슬롯(문제 · 중간 · 대응)이 같은 자리에 반복된다("Stage framework with semantic slots").
#           화살표는 읽는 순서이고 라벨은 관계다. 형제 편 gen-45-02.chapter-overview.py 와 같은 열 간격을 쓴다.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, OK, INFO, KR, MONO

W, H = 1000, 608
COL_X, STRIDE, NW, NH = 64, 344, 200, 64
ROW_Y, ROW_STRIDE = 104, 92

d = D(W, H, "CHAPTER MAP · 14-01",
      "구조는 조직이 정하고 렌더 결과는 따로 쌓으며 승격은 옆 도구가 맡는다",
      "14-01 편의 전체 지도. 첫 행은 같은 YAML 의 반복을 DRY 로 줄이는 방법, "
      "둘째 행은 설정 저장소를 앱 소스에서 떼고 개수를 조직 구조에 맞추는 결정, "
      "셋째 행은 배포 때 렌더하는 방식의 한계를 rendered manifests 패턴과 Source Hydrator 로 푸는 것, "
      "넷째 행은 환경 브랜치 대신 trunk 하나를 쓰고 렌더 결과 브랜치를 병합하지 않는 릴리스 산출물로 두는 것, "
      "다섯째 행은 점진 배포와 승격을 옆 도구에 맡기고 Image Updater 의 write-back 두 방식으로 반영하는 길을 보인다.",
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
        d.tone(x, y, NW, NH, c, 6, "14", 1.1)
    else:
        d.box(x, y, NW, NH)
    d.t(x + NW / 2, y + 27, title, 14, c or INK, kr(title), "middle", 600)
    d.t(x + NW / 2, y + 49, sub, 12, MUTED, kr(sub), "middle")


def harrow(i, j, label):
    y = ny(i) + NH / 2
    x1, x2 = nx(j) + NW, nx(j + 1)
    d.arrow([(x1 + 2, y), (x2 - 4, y)], MUTED, "ar", 1.4)
    d.t((x1 + x2) / 2, y - 10, label, 12, MUTED, kr(label), "middle", 600)


for i in range(5):
    d.chip(34, ny(i) + NH / 2 - 4, f"§{i + 1}", MUTED, 11, 4)

# §1 DRY 와 매개변수화
node(0, 0, "같은 YAML 의 반복", "환경마다 되풀이", INFO)
node(0, 1, "DRY", "본체 하나 + 변경분", None)
node(0, 2, "overlay · 매개변수", "Kustomize · Helm", OK)
harrow(0, 0, "한 번만 적음")
harrow(0, 1, "도구로 담음")

# §2 저장소 분리와 구조 선택
node(1, 0, "앱 소스와 한 저장소", "빌드 트리거 무한 반복", INFO)
node(1, 1, "설정 저장소 분리", "이유 다섯 가지", None)
node(1, 2, "monorepo · polyrepo", "Conway 법칙이 가름", OK)
harrow(1, 0, "저장소를 떼어")
harrow(1, 1, "조직 구조를 따라")

# §3 Rendered Manifests 패턴
node(2, 0, "배포 때 렌더", "diff 에 실제 효과 안 보임", INFO)
node(2, 1, "Rendered Manifests", "렌더 결과를 Git 에 커밋", None)
node(2, 2, "Source Hydrator", "drySource · syncSource", OK)
harrow(2, 0, "렌더를 앞으로")
harrow(2, 1, "기능으로 맡김")

# §4 trunk 기반 GitOps 작업 흐름
node(3, 0, "환경 브랜치", "Git Flow 식 병합", INFO)
node(3, 1, "trunk 하나", "main 이 단일 진실 공급원", None)
node(3, 2, "릴리스 산출물", "브랜치끼리 병합 안 함", OK)
harrow(3, 0, "병합 대신")
harrow(3, 1, "main 에서 생성")

# §5 점진 배포와 승격 도구
node(4, 0, "Argo CD 는 직접 안 함", "점진 배포 · 승격", INFO)
node(4, 1, "옆 도구", "Rollouts · Image Updater", None)
node(4, 2, "write-back 두 방식", "argocd · git", OK)
harrow(4, 0, "옆 도구에 맡김")
harrow(4, 1, "Image Updater 가 반영")

d.legend(ny(4) + NH + 24, [("문제", INFO), ("대응", OK)])
d.save("14-01.chapter-overview.svg")

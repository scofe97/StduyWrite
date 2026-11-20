# 07-01.chapter-overview — 키워드를 노드로, 앞 키워드에서 뒤 키워드로 넘어가는 관계를 화살표 라벨로 이은 편 전체 지도
# 행 하나가 본문 `##` 하나다. 왼쪽 칩은 절 번호, 노드는 그 절의 핵심 키워드와 실제 값, 화살표 라벨은 두 키워드 사이의 관계다.
# 노드와 관계는 본문 각 절의 `>` 요약과 핵심 요약에서 가져왔다.
#   §1 in-cluster(Secret 없이 기본 등록)·허브 앤 스포크(연결은 허브에서만)·cluster Secret(원격 클러스터 하나에 하나) — `## 1.` 요약과 핵심 요약 첫 문단
#   §2 argocd cluster add(허브 Secret 과 원격 계정)·인증서로 접속하면 토큰 대신 certData·cluster rm 의 같은 이름 컨텍스트 — `## 2.` 요약과 「접속 방식별 Secret 내용」·「argocd cluster rm 과 정리」
#   §3 Application 하나는 클러스터 하나·App-of-Apps(부모 Application)·ApplicationSet(클러스터 목록) — `## 3.` 요약과 핵심 요약 마지막 문장
# 타입 스펙: type-process — 행마다 같은 의미 슬롯(문제 · 중간 · 대응)이 같은 자리에 반복된다("Stage framework with semantic slots").
#           화살표는 읽는 순서이고 라벨은 관계다. 2행은 등록에서 삭제까지 이어지는 절차를 따라 읽는다.
#           ACC 는 핵심 요약 첫 문단이 말하는 원격 클러스터 하나당 cluster Secret 하나 한 곳이다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INK, MUTED, SOFT, OK, INFO, KR, MONO

W, H = 1000, 424
COL_X, STRIDE, NW, NH = 64, 344, 200, 64
ROW_Y, ROW_STRIDE = 104, 92

d = D(W, H, "CHAPTER MAP · 07-01",
      "원격 클러스터 하나는 허브의 cluster Secret 하나로 정의된다",
      "07-01 편의 전체 지도. 첫 행은 Secret 없이 기본 등록된 in-cluster 에서 허브 앤 스포크로 원격을 늘리고 cluster Secret 이 접속 정보를 담는 것, "
      "둘째 행은 argocd cluster add 가 만드는 Secret 이 접속 방식에 따라 인증서를 담고 cluster rm 이 같은 이름의 컨텍스트를 찾는 것, "
      "셋째 행은 Application 하나가 클러스터 하나에만 배포되어 App-of-Apps 와 ApplicationSet 으로 늘리는 것을 보인다.",
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


for i in range(3):
    d.chip(34, ny(i) + NH / 2 - 4, f"§{i + 1}", MUTED, 11, 4)

# §1 클러스터 정의와 허브 앤 스포크
node(0, 0, "in-cluster", "Secret 없이 기본 등록", None)
node(0, 1, "허브 앤 스포크", "연결은 허브에서만 나감", None)
node(0, 2, "cluster Secret", "원격 클러스터 하나에 하나", ACC)
harrow(0, 0, "원격으로 확장")
harrow(0, 1, "접속 정보")

# §2 원격 클러스터 등록과 삭제
node(1, 0, "cluster add", "허브 Secret + 원격 계정", None)
node(1, 1, "인증서로 접속", "토큰 대신 certData", INFO)
node(1, 2, "같은 이름 컨텍스트", "cluster rm 의 원격 정리")
harrow(1, 0, "접속 방식별")
harrow(1, 1, "삭제할 때")

# §3 멀티 클러스터 배포
node(2, 0, "Application 하나", "클러스터 하나에만 배포", INFO)
node(2, 1, "App-of-Apps", "부모 Application", OK)
node(2, 2, "ApplicationSet", "클러스터 목록", OK)
harrow(2, 0, "부모로 늘림")
harrow(2, 1, "또는 목록으로 늘림")

d.legend(ny(2) + NH + 24, [("문제", INFO), ("이 편의 한 줄", ACC), ("대응", OK)])
d.save("07-01.chapter-overview.svg")

# 05-01.chapter-overview — 키워드를 노드로, 앞 키워드에서 뒤 키워드로 넘어가는 관계를 화살표 라벨로 이은 편 전체 지도
# 행 하나가 본문 `##` 하나다. 왼쪽 칩은 절 번호, 노드는 그 절의 핵심 키워드와 실제 값, 화살표 라벨은 두 키워드 사이의 관계다.
# 노드와 관계는 본문 각 절의 `>` 요약과 핵심 요약에서 가져왔다.
#   §1 수동 기본·automated·prune/selfHeal·조회 주기 약 3분(120초 + 최대 60초 jitter) — `## 1.` 요약과 「자동 동기화 켜기와 확인 주기」·「prune 과 selfHeal 스위치」
#   §2 Sync Option·IgnoreExtraneous·ignoreDifferences — `## 2.` 요약과 「리소스를 비교에서 빼는 compare-options」·「필드 차이를 무시하는 ignoreDifferences」
#   §3 순서 있는 배포·Hook·Sync Wave·readiness probe — `## 3.` 요약과 「wave 전환 조건과 prune 순서」·「데이터베이스 스키마 배포 사례」, 핵심 요약의 마지막 문단
# 타입 스펙: type-process — 행마다 같은 의미 슬롯(문제 · 중간 · 대응)이 같은 자리에 반복된다("Stage framework with semantic slots").
#           화살표는 읽는 순서이고 라벨은 관계다. 2행은 세 방법을 나란히 견주는 줄이라 문제·대응 색을 쓰지 않는다.
#           1행 첫 노드의 수동 동기화 기본은 그 절이 푸는 문제가 아니라 출발 상태라 색을 두지 않는다.
#           ACC 는 핵심 요약이 끝에 짚는 readiness probe 한 곳이다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INK, MUTED, SOFT, OK, INFO, KR, MONO

W, H = 1000, 424
COL_X, STRIDE, NW, NH = 64, 344, 200, 64
ROW_Y, ROW_STRIDE = 104, 92

d = D(W, H, "CHAPTER MAP · 05-01",
      "동기화 시점과 방식과 순서는 syncPolicy 와 어노테이션이 정한다",
      "05-01 편의 전체 지도. 첫 행은 수동 동기화가 기본이고 automated 를 적어야 자동으로 돌며 prune 과 selfHeal 은 따로 켠다는 것, "
      "둘째 행은 Sync Option 과 IgnoreExtraneous 와 ignoreDifferences 가 적용 방식과 비교 대상을 조절하는 것, "
      "셋째 행은 순서가 있는 배포를 Hook 과 Sync Wave 로 나누고 readiness probe 가 다음 wave 로 넘어가는 신호가 되는 것을 보인다.",
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

# §1 시작 시점
node(0, 0, "수동 동기화 기본", "syncPolicy 를 안 적음")
node(0, 1, "automated", "조회 주기 약 3분", None)
node(0, 2, "prune · selfHeal", "기본은 둘 다 꺼짐", OK)
harrow(0, 0, "정책 추가")
harrow(0, 1, "스위치 추가")

# §2 적용 방식과 차이 무시
# 세 방법을 나란히 견주는 절이라 문제·대응 색을 쓰지 않는다
node(1, 0, "Sync Option", "syncOptions · 어노테이션", None)
node(1, 1, "IgnoreExtraneous", "리소스를 통째로 뺌", None)
node(1, 2, "ignoreDifferences", "필드 차이만 뺌", None)
harrow(1, 0, "적용에서 비교로")
harrow(1, 1, "리소스에서 필드로")

# §3 순서
node(2, 0, "순서가 있는 배포", "데이터베이스 뒤 스키마", INFO)
node(2, 1, "Hook · Sync Wave", "단계 안은 wave 숫자순", OK)
node(2, 2, "readiness probe", "다음 wave 로 넘는 신호", ACC)
harrow(2, 0, "단계와 숫자")
harrow(2, 1, "Healthy 판정")

d.legend(ny(2) + NH + 24, [("문제", INFO), ("핵심 요약의 끝", ACC), ("대응", OK)])
d.save("05-01.chapter-overview.svg")

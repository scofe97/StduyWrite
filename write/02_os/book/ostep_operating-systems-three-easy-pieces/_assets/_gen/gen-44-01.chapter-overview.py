# 44-01 개념도 — 이 편의 세 절이 각각 어떤 문제에서 출발해 어떤 도구로 가는지.
# 한 행이 한 절이다. 노드는 키워드, 가로 화살표 라벨은 노드 사이의 관계다.
# 본문 근거: 이 노트 「1. 알고리즘은 공개하고 키만 숨기는 대칭 암호」·「2. 개인 키로 서명하고 공개 키로 암호화한다」·「3. 해시만 서명해 무결성을 싸게 확인한다」.
# 공식 근거: NIST FIPS 197(AES), SP 800-38D(GCM), SP 800-131A Rev. 2(SHA-1·RSA), NIST 해시 함수 정책.
# 타입 스펙: type-process — 절마다 한 행, 행마다 노드 셋과 라벨 있는 가로 화살표 둘.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, ACC, OK, INFO, KR, MONO

COL_X, STRIDE, NW, NH = 60, 340, 216, 64
ROW_Y, ROW_STRIDE = 112, 116
W, H = 984, 480


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def nx(j):
    return COL_X + j * STRIDE


def ny(i):
    return ROW_Y + i * ROW_STRIDE


d = D(W, H, "OSTEP · 44-01 OVERVIEW",
      "암호는 키 하나에 비밀을 걸고, 해시는 그 비용을 줄인다",
      "한 행이 한 절이다. 첫 행은 OS 의 통제가 닿지 않는 데이터를 대칭 암호로 감싸고 변조 검출을 덧붙이는 흐름이다. "
      "둘째 행은 대칭 키 배포 문제를 공개 키와 개인 키로 푸는 흐름이고 공개 키의 출처 확인이 새 문제로 남는다. "
      "셋째 행은 느린 서명의 비용을 해시만 서명해서 줄이는 흐름이다.",
      lead="가로 화살표의 라벨이 노드 사이의 관계이고, 왼쪽 칩이 절 번호이다.")


def node(i, j, title, sub, c):
    x, y = nx(j), ny(i)
    d.tone(x, y, NW, NH, c, 6, "14", 1.1)
    d.t(x + NW / 2, y + 27, title, 14, INK, kr(title), "middle", 600)
    d.t(x + NW / 2, y + 48, sub, 13, MUTED, kr(sub), "middle")


def harrow(i, j, label, c=SOFT, m="soft"):
    y = ny(i) + NH / 2
    x1, x2 = nx(j) + NW, nx(j + 1)
    d.arrow([(x1 + 2, y), (x2 - 4, y)], c, m, 1.3)
    d.t((x1 + x2) / 2, y - 9, label, 13, c if c != SOFT else MUTED, kr(label), "middle", 600)


for i, sec in enumerate(("1", "2", "3")):
    d.chip(34, ny(i) + NH / 2 - 4, sec, MUTED, 12, 6)

# 1. 대칭 암호
node(0, 0, "OS 밖의 데이터", "디스크·네트워크로 나간 값", INFO)
node(0, 1, "대칭 암호", "같은 키 K 로 잠그고 연다", OK)
node(0, 2, "변조 검출", "MAC · AES-GCM 태그", ACC)
harrow(0, 0, "키로 변환")
harrow(0, 1, "비트 반전 가능", ACC, "acc")

# 2. 공개 키 암호
node(1, 0, "키 배포", "수억 명에게 같은 키", INFO)
node(1, 1, "공개 키 암호", "공개 키 + 개인 키", OK)
node(1, 2, "키 주인 확인", "공개 키 배포가 약한 고리", ACC)
harrow(1, 0, "키를 둘로 나눔")
harrow(1, 1, "배포가 약점", ACC, "acc")

# 3. 암호 해시
node(2, 0, "느린 서명", "공개 키 연산은 수백 배 느림", INFO)
node(2, 1, "암호 해시", "키 없는 고정 길이 지문", OK)
node(2, 2, "무결성 확인", "해시만 서명 · MAC", ACC)
harrow(2, 0, "입력을 압축")
harrow(2, 1, "지문만 서명", ACC, "acc")

d.legend(440, [("출발하는 문제", INFO), ("쓰는 도구", OK), ("남는 과제 · 얻는 결과", ACC)])
d.save("44-01.chapter-overview.svg")

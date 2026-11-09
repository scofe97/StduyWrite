# 08-01.chapter-overview — 키워드를 노드로, 앞 키워드에서 뒤 키워드로 넘어가는 관계를 화살표 라벨로 이은 편 전체 지도
# 행 하나가 본문 `##` 하나다. 왼쪽 칩은 절 번호, 노드는 그 절의 핵심 키워드와 실제 값, 화살표 라벨은 두 키워드 사이의 관계다.
# 노드 근거: §1 은 「클러스터 범위 설치」(ClusterRole 3개·CRD 3개)·「네임스페이스 범위 설치」(Role 6개·CRD 없음)·
#            「네임스페이스 범위 인스턴스 실습」(RoleBinding 을 대상 네임스페이스에 따로 더함),
#            §2 는 절 도입의 default 프로젝트 설명과 「저장소·대상 검사 시점」 표(생성·갱신, refresh, 동기화),
#            §3 은 절 도입(CI 파이프라인에 한 앱의 동기화만 허용)과 「JWT 토큰 발급과 삭제」(기본 만료 없음)·
#            「역할 정책 형식과 검증」(applications get·sync)이다. 값은 모두 본문에 있는 것이다.
# 타입 스펙: type-process — 행마다 같은 의미 슬롯(문제 · 중간 · 대응)이 같은 자리에 반복된다("Stage framework with semantic slots").
#           화살표는 읽는 순서이고 라벨은 관계다. 색은 문제 INFO, 대응 OK, 이 편의 한 줄 ACC 다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INK, MUTED, SOFT, OK, INFO, KR, MONO

W, H = 1000, 424
COL_X, STRIDE, NW, NH = 64, 344, 200, 64
ROW_Y, ROW_STRIDE = 104, 92

d = D(W, H, "CHAPTER MAP · 08-01",
      "설치 모드가 권한 크기를 정하고 AppProject 가 팀의 배포 범위를 좁힌다",
      "08-01 편의 전체 지도. 첫 행은 클러스터 범위 설치에서 네임스페이스 범위 설치로 권한을 좁히고 "
      "대상 네임스페이스에 RoleBinding 을 더하는 흐름, "
      "둘째 행은 default 프로젝트의 넓은 허용 범위를 AppProject 가 제한하고 필드마다 검사 시점이 다른 흐름, "
      "셋째 행은 사람 없는 인증을 프로젝트 역할의 JWT 토큰이 맡고 정책에 적힌 get 과 sync 까지만 통과하는 흐름을 보인다.",
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

# §1 설치 모드 — 클러스터·네임스페이스 범위
node(0, 0, "클러스터 범위", "ClusterRole 3개 · CRD 3개", INFO)
node(0, 1, "네임스페이스 범위", "Role 6개 · CRD 없음", None)
node(0, 2, "RoleBinding 추가", "컨트롤러 계정 연결", OK)
harrow(0, 0, "권한을 좁힘")
harrow(0, 1, "배포하려면")

# §2 AppProject 의 배포 범위 제한
node(1, 0, "default 프로젝트", "모든 저장소·대상 허용", INFO)
node(1, 1, "AppProject", "저장소·대상·종류 제한", ACC)
node(1, 2, "시점별 검사", "생성·갱신·refresh·동기화", OK)
harrow(1, 0, "범위를 제한")
harrow(1, 1, "필드별 시점")

# §3 프로젝트 역할과 JWT 토큰
node(2, 0, "사람 없는 인증", "CI 의 한 앱 동기화", INFO)
node(2, 1, "프로젝트 역할 토큰", "JWT · 기본 만료 없음", None)
node(2, 2, "정책 줄까지만", "get · sync 허용", OK)
harrow(2, 0, "토큰 발급")
harrow(2, 1, "정책 대조")

d.legend(ny(2) + NH + 24, [("문제", INFO), ("이 편의 한 줄", ACC), ("대응", OK)])
d.save("08-01.chapter-overview.svg")

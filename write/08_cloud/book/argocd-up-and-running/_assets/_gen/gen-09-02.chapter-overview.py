# 09-02.chapter-overview — 키워드를 노드로, 앞 키워드에서 뒤 키워드로 넘어가는 관계를 화살표 라벨로 이은 편 전체 지도
# 행 하나가 본문 `##` 하나다. 왼쪽 칩은 절 번호, 노드는 그 절의 핵심 키워드와 실제 값, 화살표 라벨은 두 키워드 사이의 관계다.
# 노드 근거: §1 은 「개인 키와 호스트 키 등록」(개인 키는 저장소 Secret, 호스트 키는 known hosts ConfigMap)과
#            「자격 증명 템플릿으로 키 재사용」(repo-creds 라벨 Secret, CREDS 열의 inherited, 가장 긴 접두사 우선),
#            §2 는 「검증 흐름과 키링 준비」(키링과 프로젝트 정책의 믿는 키 목록 둘 다 필요)·「sourceIntegrity 정책과 mode」·
#            「거부 문구로 원인 가리기」(서명 없음·키링에 없는 키·허용되지 않은 키가 서로 다른 문구),
#            §3 은 「스위치 두 개와 enforced」(sync 가 컨트롤러와 같은 권한이 되는 것을 막는 기능, 기본 꺼짐, enabled 기본값 false)·
#            「프로젝트의 서비스 계정 매핑」(defaultServiceAccount)·「dry run 에서 드러나는 실패」다. 값은 모두 본문에 있는 것이다.
#            핵심 요약은 세 곳을 같은 무게로 들어 코랄 노드를 두지 않는다.
# 타입 스펙: type-process — 행마다 같은 의미 슬롯(문제 · 중간 · 대응)이 같은 자리에 반복된다("Stage framework with semantic slots").
#           화살표는 읽는 순서이고 라벨은 관계다. 색은 문제 INFO, 대응 OK 다.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, OK, INFO, KR, MONO

W, H = 1000, 424
COL_X, STRIDE, NW, NH = 64, 344, 200, 64
ROW_Y, ROW_STRIDE = 104, 92

d = D(W, H, "CHAPTER MAP · 09-02",
      "Argo CD 는 열쇠·서명·sync 계정 세 곳에서 Git 에 대한 믿음을 좁힌다",
      "09-02 편의 전체 지도. 첫 행은 SSH 저장소에 개인 키와 호스트 키를 둘 다 등록하고 저장소가 많으면 "
      "자격 증명 템플릿의 가장 긴 접두사가 적용되어 CREDS 열에 inherited 가 찍히는 흐름, "
      "둘째 행은 서명 없는 커밋과 낯선 키의 커밋을 sourceIntegrity 정책이 키링과 믿는 키로 거르고 거부 문구로 원인을 가리는 흐름, "
      "셋째 행은 sync 가 컨트롤러 계정 권한을 갖는 문제를 프로젝트의 서비스 계정 매핑과 dry run 검사로 풀어 컨트롤러와 테넌트의 권한을 분리하는 흐름을 보인다.",
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


for i in range(3):
    d.chip(34, ny(i) + NH / 2 - 4, f"§{i + 1}", MUTED, 11, 4)

# §1 SSH 인증과 자격 증명 템플릿
node(0, 0, "개인 키 · 호스트 키", "Secret · ConfigMap", INFO)
node(0, 1, "자격 증명 템플릿", "repo-creds Secret", None)
node(0, 2, "CREDS inherited", "가장 긴 접두사 우선", OK)
harrow(0, 0, "저장소가 많으면")
harrow(0, 1, "접두사 일치")

# §2 GPG 서명 검증과 소스 무결성 정책
node(1, 0, "서명 없는 커밋", "낯선 키의 커밋도", INFO)
node(1, 1, "sourceIntegrity", "키링 · 믿는 키 둘 다 필요", None)
node(1, 2, "거부 문구 3종", "원인이 문구로 갈림", OK)
harrow(1, 0, "프로젝트 정책")
harrow(1, 1, "검증에 걸리면")

# §3 Sync Impersonation 과 권한 분리
node(2, 0, "컨트롤러 계정 권한", "sync 와 같은 권한", INFO)
node(2, 1, "서비스 계정 매핑", "defaultServiceAccount", None)
node(2, 2, "테넌트 권한 분리", "enabled 를 켜야 동작", OK)
harrow(2, 0, "계정을 지정")
harrow(2, 1, "dry run 검사")

d.legend(ny(2) + NH + 24, [("문제", INFO), ("대응", OK)])
d.save("09-02.chapter-overview.svg")

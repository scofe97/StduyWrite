# 06-02.chapter-overview — 키워드를 노드로, 앞 키워드에서 뒤 키워드로 넘어가는 관계를 화살표 라벨로 이은 편 전체 지도
# 행 하나가 본문 `##` 하나다. 왼쪽 칩은 절 번호, 노드는 그 절의 핵심 키워드와 실제 값, 화살표 라벨은 두 키워드 사이의 관계다.
# 노드와 관계는 본문 각 절의 `>` 요약과 핵심 요약에서 가져왔다.
#   §1 dex.config(범용 oidc 커넥터)·Dex 기본 요청 범위 profile · email·insecureEnableGroups 와 scopes 의 groups — `## 1.` 요약과 본문 「그룹은 따로 켜야 나옵니다」
#   §2 oidc.config(Dex 없이 IdP 직접)·CLI 의 localhost:8085 콜백과 비밀 보관 불가·PKCE(S256, public 클라이언트) — `## 2.` 요약과 「CLI SSO 로그인과 PKCE」
#   §3 PermissionDenied·p 줄과 g 줄의 주체(사용자 이름·그룹 이름 문자열)·deny 우선 — `## 3.` 요약과 핵심 요약 첫 문장·「줄이 적힌 순서는 결과에 영향을 주지 않습니다」
#   §4 내장 역할 admin · readonly·개발자 역할(p 다섯 줄 · g 한 줄)·rbac validate · rbac can·policy.default — `## 4.` 요약과 각 소절
# 타입 스펙: type-process — 행마다 같은 의미 슬롯(문제 · 중간 · 대응)이 같은 자리에 반복된다("Stage framework with semantic slots").
#           화살표는 읽는 순서이고 라벨은 관계다. ACC 는 핵심 요약 첫 문장의 "사용자 이름과 그룹 이름이라는 문자열" 한 곳이다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INK, MUTED, SOFT, OK, INFO, KR, MONO

W, H = 1000, 516
COL_X, STRIDE, NW, NH = 64, 344, 200, 64
ROW_Y, ROW_STRIDE = 104, 92

d = D(W, H, "CHAPTER MAP · 06-02",
      "SSO 는 누구인지를, RBAC 정책은 할 수 있는 일을 정한다",
      "06-02 편의 전체 지도. 첫 행은 Dex 설정에서 그룹이 기본으로 나오지 않아 따로 켜는 것, "
      "둘째 행은 직접 OIDC 의 CLI 로그인이 비밀 없이 PKCE 로 동작하는 것, "
      "셋째 행은 인증을 통과해도 권한이 없다가 이름과 그룹 문자열로 p 줄과 g 줄에 일치하고 deny 가 우선하는 것, "
      "넷째 행은 내장 역할로 부족할 때 개발자 역할을 만들고 적용 전에 검증하는 것을 보인다.",
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


for i in range(4):
    d.chip(34, ny(i) + NH / 2 - 4, f"§{i + 1}", MUTED, 11, 4)

# §1 Dex 로 SSO 켜기
node(0, 0, "dex.config", "범용 oidc 커넥터", None)
node(0, 1, "그룹은 기본 미요청", "범위는 profile · email", INFO)
node(0, 2, "insecureEnableGroups", "groups 를 넘기는 스위치", OK)
harrow(0, 0, "기본 범위")
harrow(0, 1, "그룹을 따로 켬")

# §2 직접 OIDC 와 CLI 로그인
node(1, 0, "oidc.config", "Dex 없이 IdP 직접", None)
node(1, 1, "CLI 는 비밀 보관 불가", "localhost:8085 콜백", INFO)
node(1, 2, "PKCE", "비밀 없는 public 클라이언트", OK)
harrow(1, 0, "CLI 로그인")
harrow(1, 1, "비밀 대신")

# §3 RBAC 정책의 p·g 줄
node(2, 0, "인증 통과, 권한 없음", "PermissionDenied", INFO)
node(2, 1, "이름 · 그룹 문자열", "p 줄 · g 줄의 주체", ACC)
node(2, 2, "deny 가 우선", "줄 순서와 무관", OK)
harrow(2, 0, "권한은 따로")
harrow(2, 1, "일치 줄 모음")

# §4 개발자 역할과 기본 권한
node(3, 0, "내장 역할로 부족", "admin · readonly 둘뿐", INFO)
node(3, 1, "개발자 역할", "p 다섯 줄 · g 한 줄", None)
node(3, 2, "validate · can", "적용 전 문법·결과 확인", OK)
harrow(3, 0, "p 줄로 정의")
harrow(3, 1, "적용 전에")

d.legend(ny(3) + NH + 24, [("문제", INFO), ("이 편의 한 줄", ACC), ("대응", OK)])
d.save("06-02.chapter-overview.svg")

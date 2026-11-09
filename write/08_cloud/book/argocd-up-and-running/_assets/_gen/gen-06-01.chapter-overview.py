# 06-01.chapter-overview — 키워드를 노드로, 앞 키워드에서 뒤 키워드로 넘어가는 관계를 화살표 라벨로 이은 편 전체 지도
# 행 하나가 본문 `##` 하나다. 왼쪽 칩은 절 번호, 노드는 그 절의 핵심 키워드와 실제 값, 화살표 라벨은 두 키워드 사이의 관계다.
# 노드와 관계는 본문 각 절의 `>` 요약과 핵심 요약에서 가져왔다.
#   §1 admin 초기 계정·로컬 사용자(login · apiKey)·argocd-secret 의 비밀번호 해시 — `## 1.` 요약과 「admin 초기 비밀번호 교체」·「로컬 사용자 정의와 비밀번호」
#   §2 apiKey 계정·--expires-in 을 생략한 만료 없는 토큰·90d 와 delete-token — `## 2.` 요약과 본문 명령 `generate-token --expires-in 90d --id ci-bot`
#   §3 Dex · 직접 OIDC(dex.config · oidc.config)·준비물 넷(url · 콜백 · 그룹 클레임 · 비밀 참조)·토큰의 발급자·사용자 이름·그룹 — `## 3.` 요약과 핵심 요약 첫 문단
# 타입 스펙: type-process — 행마다 같은 의미 슬롯(문제 · 중간 · 대응)이 같은 자리에 반복된다("Stage framework with semantic slots").
#           화살표는 읽는 순서이고 라벨은 관계다. ACC 는 핵심 요약 첫 문장이 말하는 토큰의 발급자·사용자 이름·그룹 한 곳이다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INK, MUTED, SOFT, OK, INFO, KR, MONO

W, H = 1000, 424
COL_X, STRIDE, NW, NH = 64, 344, 200, 64
ROW_Y, ROW_STRIDE = 104, 92

d = D(W, H, "CHAPTER MAP · 06-01",
      "누구인지는 토큰의 발급자와 사용자 이름과 그룹으로 정해진다",
      "06-01 편의 전체 지도. 첫 행은 제한 없는 admin 초기 계정에서 로컬 사용자로 옮기고 비밀번호 해시를 argocd-secret 에 두는 것, "
      "둘째 행은 apiKey 계정이 만료 없는 토큰 대신 만료 시간을 붙여 발급하고 폐기하는 것, "
      "셋째 행은 Dex 와 직접 OIDC 의 준비물 넷을 거쳐 토큰의 발급자와 사용자 이름과 그룹이 사용자를 정하는 것을 보인다.",
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

# §1 admin 과 로컬 사용자
node(0, 0, "admin 초기 계정", "제한 없는 권한", INFO)
node(0, 1, "로컬 사용자", "login · apiKey 능력", None)
node(0, 2, "비밀번호 해시", "argocd-secret 에 저장", OK)
harrow(0, 0, "사용자로 이전")
harrow(0, 1, "비밀번호는 별도")

# §2 CI 용 토큰
node(1, 0, "apiKey 계정", "login 없이 apiKey 만", None)
node(1, 1, "만료 없는 토큰", "--expires-in 생략 시", INFO)
node(1, 2, "만료와 폐기", "90d · delete-token", OK)
harrow(1, 0, "토큰 발급")
harrow(1, 1, "만료 시간 부여")

# §3 SSO 준비물
node(2, 0, "Dex · 직접 OIDC", "dex.config · oidc.config", None)
node(2, 1, "준비물 넷", "url · 콜백 · 그룹 · 비밀", None)
node(2, 2, "발급자 · 이름 · 그룹", "사용자 목록은 Argo CD 밖", ACC)
harrow(2, 0, "켜기 전에")
harrow(2, 1, "로그인 뒤 토큰")

d.legend(ny(2) + NH + 24, [("문제", INFO), ("이 편의 한 줄", ACC), ("대응", OK)])
d.save("06-01.chapter-overview.svg")

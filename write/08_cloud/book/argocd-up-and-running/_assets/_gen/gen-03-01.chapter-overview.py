# 03-01.chapter-overview — 키워드를 노드로, 앞 키워드에서 뒤 키워드로 넘어가는 관계를 화살표 라벨로 이은 편 전체 지도
# 행 하나가 본문 `##` 하나다. 왼쪽 칩은 절 번호, 노드는 그 절의 핵심 키워드와 실제 값, 화살표 라벨은 두 키워드 사이의 관계다.
# 노드 근거: §1 = 1절 `>` 요약과 port-forward 한계·TLS 종료 위치 문단(`server.insecure`, 기본값 "false"),
#            §2 = 2절 `>` 요약과 세 입구가 닿는 같은 API server 문단, REST API 세션 토큰 문단(`/api/v1/session`, Bearer),
#            §3 = 3절 `>` 요약과 설정 리소스 여섯 문단, ConfigMap 별 반영 시점 문단.
#            편의 한 줄은 핵심 요약의 "UI 와 CLI 와 REST API 는 모두 같은 API server 로 들어가는 입구" 이므로 §2 의 가운데 노드에 건다.
# 타입 스펙: type-process — 행마다 같은 의미 슬롯(문제 · 중간 · 대응)이 같은 자리에 반복된다("Stage framework with semantic slots").
#           화살표는 읽는 순서이고 라벨은 관계다. 형제 편 gen-01-01.chapter-overview.py 와 같은 열 간격을 쓴다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INK, MUTED, SOFT, OK, INFO, KR, MONO

W = 1000
COL_X, STRIDE, NW, NH = 64, 344, 216, 64
ROW_Y, ROW_STRIDE = 104, 92
ROWS = 3
H = ROW_Y + (ROWS - 1) * ROW_STRIDE + NH + 24 + 48

d = D(W, H, "CHAPTER MAP · 03-01",
      "UI 와 CLI 와 REST API 는 같은 API server 로 들어간다",
      "03-01 편의 전체 지도. 첫 행은 임시 통로인 port-forward 를 Ingress 컨트롤러로 바꾸면 컨트롤러가 TLS 를 풀어 평문으로 넘기므로 "
      "API server 의 server.insecure 를 켜는 흐름, "
      "둘째 행은 CLI 와 REST API 가 UI 와 같은 API server 에 닿고 로그인에서 받은 세션 토큰을 Bearer 로 보내는 흐름, "
      "셋째 행은 설정을 ConfigMap 과 Secret 리소스로 선언하면 CLI 없이 구성이 끝나고 ConfigMap 마다 반영 시점이 다른 흐름을 보인다.",
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

# §1 UI 심화 — Ingress 로 노출하기
node(0, 0, "port-forward", "명령이 도는 동안만 열림", INFO)
node(0, 1, "Ingress 컨트롤러", "kind 위의 Traefik", None)
node(0, 2, "server.insecure", "false 에서 true 로", OK)
harrow(0, 0, "대신 노출")
harrow(0, 1, "평문으로 넘김")

# §2 CLI 와 REST API — 로그인과 세션 토큰
node(1, 0, "CLI 와 REST API", "UI 밖의 두 입구", INFO)
node(1, 1, "API server", "세 입구가 닿는 한 곳", ACC)
node(1, 2, "세션 토큰", "Authorization: Bearer", OK)
harrow(1, 0, "같은 서버로")
harrow(1, 1, "로그인해서 받음")

# §3 선언적 구성 — ConfigMap 과 Secret
node(2, 0, "CLI 없이 구성", "kubectl apply 로 선언", OK)
node(2, 1, "ConfigMap · Secret", "이름이 정해진 리소스 여섯", None)
node(2, 2, "반영 시점", "ConfigMap 마다 다름")
harrow(2, 0, "리소스를 apply")
harrow(2, 1, "값을 고친 뒤")

d.legend(ny(ROWS - 1) + NH + 24, [("문제", INFO), ("이 편의 한 줄", ACC), ("대응", OK)])
d.save("03-01.chapter-overview.svg")

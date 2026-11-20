# 11-01.chapter-overview — 키워드를 노드로, 앞 키워드에서 뒤 키워드로 넘어가는 관계를 화살표 라벨로 이은 편 전체 지도
# 행 하나가 본문 `##` 하나다. 왼쪽 칩은 절 번호, 노드는 그 절의 핵심 키워드와 실제 값, 화살표 라벨은 두 키워드 사이의 관계다.
# 노드 근거: 1행은 §1 요약과 핵심 요약(내장 도구로 못 만드는 소스, 사이드카, generate 의 stdout), 2행은 §2 요약과 핵심 요약(plugin.env · parameters 의 접두사, 시간 제한 60초와 set -o pipefail),
#           3행은 §3 요약과 핵심 요약(배너 · CSS · 확장 세 층, /tmp/extensions 아래 extension*.js). 값은 모두 본문에 적힌 것이다.
# 타입 스펙: type-process — 행마다 같은 의미 슬롯(문제 · 중간 · 대응)이 같은 자리에 반복된다("Stage framework with semantic slots").
#           화살표는 읽는 순서이고 라벨은 관계다. 형제 편 gen-45-02.chapter-overview.py 와 같은 열 간격을 쓴다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INK, MUTED, SOFT, OK, INFO, KR, MONO

W, H = 1000, 424
COL_X, STRIDE, NW, NH = 64, 344, 200, 64
ROW_Y, ROW_STRIDE = 104, 92

d = D(W, H, "CHAPTER MAP · 11-01",
      "플러그인은 사이드카가 매니페스트를 만들고 UI 는 설정과 파일이 맞춘다",
      "11-01 편의 전체 지도. 첫 행은 내장 도구로 렌더할 수 없는 소스를 사이드카의 플러그인이 받아 "
      "generate 가 stdout 에 찍은 YAML 을 매니페스트로 쓰는 구조, "
      "둘째 행은 plugin.env 와 parameters 가 접두사를 달고 도착하는 통로와 운영에서 부딪히는 함정, "
      "셋째 행은 배너와 CSS 와 확장의 세 층과 extension 파일이 놓이는 자리를 보인다.",
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

# §1 플러그인이 필요한 때와 CMP 의 구조
node(0, 0, "내장 도구로 못 만드는 소스", "Helm·Kustomize·Directory", INFO)
node(0, 1, "사이드카 CMP", "유닉스 소켓 · gRPC", None)
node(0, 2, "generate 의 stdout", "YAML 이 매니페스트", ACC)
harrow(0, 0, "사이드카로 분리")
harrow(0, 1, "소스에서 실행")

# §2 값 넘기기와 운영
node(1, 0, "Application 별 입력", "같은 플러그인 재사용", INFO)
node(1, 1, "env · parameters", "ARGOCD_ENV_ · PARAM_", None)
node(1, 2, "운영 함정 다섯", "60초 제한 · pipefail")
harrow(1, 0, "접두사를 달아")
harrow(1, 1, "돌려 보면")

# §3 UI 맞춤
node(2, 0, "UI 를 맞추고 싶음", "코드는 안 고침", INFO)
node(2, 1, "세 층", "배너 · CSS · 확장", None)
node(2, 2, "extension*.js", "/tmp/extensions", OK)
harrow(2, 0, "층으로 나눔")
harrow(2, 1, "새 화면은")

d.legend(ny(2) + NH + 24, [("문제", INFO), ("이 편의 한 줄", ACC), ("대응", OK)])
d.save("11-01.chapter-overview.svg")

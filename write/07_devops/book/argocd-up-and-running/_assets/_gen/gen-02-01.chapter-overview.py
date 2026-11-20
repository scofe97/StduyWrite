# 02-01.chapter-overview — 키워드를 노드로, 앞 키워드에서 뒤 키워드로 넘어가는 관계를 화살표 라벨로 이은 편 전체 지도
# 행 하나가 본문 `##` 하나다. 왼쪽 칩은 절 번호, 노드는 그 절의 핵심 키워드와 실제 값, 화살표 라벨은 두 키워드 사이의 관계다.
# 노드 근거: §1 = 1절 `>` 요약과 컨트롤러·커스텀 리소스 문단, `kubectl get crd` 로 보이는 세 CRD(argoproj.io 그룹),
#            §2 = 2절 `>` 요약과 선언의 길·사용자의 길 문단, §3 = 3절 `>` 요약과 설치 유형 문단(두 질문, core·multi-tenant, ha/ 매니페스트),
#            §4 = 4절 `>` 요약과 `--server-side` 이유(어노테이션 262KB 한도)·port-forward·초기 비밀번호 문단,
#            §5 = 5절 `>` 요약과 Helm 차트(argo-cd 10.14.0)·릴리스 이름 문단.
#            편의 한 줄은 핵심 요약의 "설치는 필요한 기능과 설치 범위를 정해 매니페스트 하나를 고르는 일" 이므로 §3 의 세 번째 노드에 건다.
#            §2 는 두 길이 한 컨트롤러에서 만나는 구조를 보이는 줄이라 문제·대응 색을 쓰지 않는다.
# 타입 스펙: type-process — 행마다 같은 의미 슬롯(문제 · 중간 · 대응)이 같은 자리에 반복된다("Stage framework with semantic slots").
#           화살표는 읽는 순서이고 라벨은 관계다. 형제 편 gen-01-01.chapter-overview.py 와 같은 열 간격을 쓴다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INK, MUTED, SOFT, OK, INFO, KR, MONO

W = 1000
COL_X, STRIDE, NW, NH = 64, 344, 216, 64
ROW_Y, ROW_STRIDE = 104, 92
ROWS = 5
H = ROW_Y + (ROWS - 1) * ROW_STRIDE + NH + 24 + 48

d = D(W, H, "CHAPTER MAP · 02-01",
      "Argo CD 설치는 필요한 기능과 범위로 매니페스트 하나를 고르는 일이다",
      "02-01 편의 전체 지도. 첫 행은 컨트롤러가 커스텀 리소스를 감시해 세 CRD 를 제공하는 바탕, "
      "둘째 행은 선언의 길이 Repository Server 에서 Application Controller 로 가고 사용자의 길이 API server 에서 같은 컨트롤러로 이어지는 구성, "
      "셋째 행은 기능과 권한 범위 두 질문이 core 와 multi-tenant 를 거쳐 매니페스트 하나로 좁혀지는 선택, "
      "넷째 행은 CRD 크기 한도를 server-side apply 로 피해 설치하고 초기 admin 비밀번호로 로그인하는 순서, "
      "다섯째 행은 같은 설치를 Helm 차트로 반복할 때 릴리스 이름이 리소스 이름 앞에 붙는 변화를 보인다.",
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


def larrow(i, j, label):
    # 오른쪽 노드(j+1)에서 왼쪽 노드(j)로 가는 화살표
    y = ny(i) + NH / 2
    x1, x2 = nx(j) + NW, nx(j + 1)
    d.arrow([(x2 - 2, y), (x1 + 4, y)], MUTED, "ar", 1.4)
    d.t((x1 + x2) / 2, y - 10, label, 12, MUTED, kr(label), "middle", 600)


for i in range(ROWS):
    d.chip(34, ny(i) + NH / 2 - 4, f"§{i + 1}", MUTED, 11, 4)

# §1 컨트롤러와 커스텀 리소스
node(0, 0, "컨트롤러", "끝없는 비교 루프", INFO)
node(0, 1, "커스텀 리소스", "CRD 로 종류를 더함", None)
node(0, 2, "CRD 세 개", "argoproj.io 그룹", OK)
harrow(0, 0, "리소스를 감시")
harrow(0, 1, "세 종류 제공")

# §2 구성 요소와 요청 흐름 — 두 길이 한 컨트롤러에서 만나는 구조라 중립색
node(1, 0, "Repository Server", "매니페스트를 만듦", None)
node(1, 1, "Application Controller", "실제 상태와 비교", None)
node(1, 2, "API server", "UI · CLI · CI/CD 요청", None)
harrow(1, 0, "선언의 길")
larrow(1, 1, "사용자의 길")

# §3 설치 유형 고르기
node(2, 0, "두 질문", "기능 · 권한 범위", INFO)
node(2, 1, "core · multi-tenant", "기능으로 가름", None)
node(2, 2, "매니페스트 하나", "운영은 ha/ 매니페스트", ACC)
harrow(2, 0, "기능을 정함")
harrow(2, 1, "범위로 좁힘")

# §4 매니페스트로 설치하기
node(3, 0, "CRD 크기", "어노테이션 262KB 한도", INFO)
node(3, 1, "server-side apply", "한도에 걸리지 않음", None)
node(3, 2, "초기 admin 로그인", "port-forward 8080:443", OK)
harrow(3, 0, "한도를 피함")
harrow(3, 1, "설치가 끝나면")

# §5 Helm 과 Operator
node(4, 0, "같은 설치 반복", "값만 바꿔 되풀이", INFO)
node(4, 1, "Helm 차트", "argo-cd 10.14.0", None)
node(4, 2, "릴리스 이름 접두", "svc/argo-cd-argocd-server", OK)
harrow(4, 0, "값으로 반복")
harrow(4, 1, "이름 앞에 붙음")

d.legend(ny(ROWS - 1) + NH + 24, [("문제", INFO), ("이 편의 한 줄", ACC), ("대응", OK)])
d.save("02-01.chapter-overview.svg")

# 10-03.chapter-overview — go get 이 go.mod·go.sum 을 채우고, 모듈 경로를 넘기면 indirect 가 붙어 tidy 로 고치며, 최소 버전 선택이 가장 낮은 만족 버전을 고르고, -u 로 올리며, 메이저가 바뀌면 경로가 바뀐다
# 본문 요구(10-03 「학습 목표」 개념도 문단): 첫 줄 go get ./...(§1), 둘째 줄 모듈 경로 go get 과 tidy(§1), 셋째 줄 최소 버전 선택(§2), 넷째 줄 -u=patch·-u(§3), 다섯째 줄 /v2 경로(§3).
# 타입 스펙: type-architecture — 키워드 개념도. 5행 × 3열 노드 격자(11-01 개념도와 같은 공식: 열 x = 60 + j·340,
#           노드 216×64, 행 y = 112 + i·128), 행 안은 가로 화살표, 행 사이는 필요할 때만 세로 화살표.
# 사실 출처: Learning Go 2판 10장 「Working with Modules」·「Minimal Version Selection」·「Updating to Compatible Versions」·「Updating to Incompatible Versions」, go1.25.1 로컬 실행(2026-09-27).
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, KR, MONO

COL_X, STRIDE, NW, NH = 60, 340, 216, 64
ROW_Y, ROW_STRIDE = 112, 128
W, H = 984, 808


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def nx(j):
    return COL_X + j * STRIDE


def ny(i):
    return ROW_Y + i * ROW_STRIDE


d = D(W, H, 'ARCHITECTURE · 10-03 OVERVIEW',
      'Go 는 요구를 만족하는 가장 낮은 버전을 고릅니다',
      '10-03 의 키워드 개념도. 첫 줄은 소스의 import 를 go get ./... 이 훑어 go.mod 와 go.sum 을 채우고, 의존성 소스까지 함께 컴파일해 바이너리 하나를 만든다는 것이다. 둘째 줄은 모듈 경로를 넘긴 go get 은 모두 indirect 로 적고 go mod tidy 가 소스와 맞춘다는 것이다. 셋째 줄은 여러 요구 가운데 모두를 만족하는 가장 낮은 버전 하나를 고르는 최소 버전 선택이다. 넷째 줄은 -u=patch 가 같은 마이너의 패치로, -u 가 가장 최신으로 올린다는 것이다. 다섯째 줄은 메이저 버전이 바뀌면 import 경로 끝에 /v2 가 붙어 다른 패키지가 된다는 것이다.',
      lead='화살표 위 글자는 두 키워드의 관계, 왼쪽 칩은 그 줄을 다루는 절입니다.')


def node(i, j, title, sub, c=None):
    x, y = nx(j), ny(i)
    if c:
        d.tone(x, y, NW, NH, c, 6, "14", 1.1)
    else:
        d.box(x, y, NW, NH)
    d.t(x + NW / 2, y + 27, title, 14, c or INK, kr(title), "middle", 600)
    d.t(x + NW / 2, y + 48, sub, 11, MUTED, kr(sub), "middle")


def harrow(i, j, label, c=SOFT, m="soft"):
    y = ny(i) + NH / 2
    x1, x2 = nx(j) + NW, nx(j + 1)
    d.arrow([(x1 + 2, y), (x2 - 4, y)], c, m, 1.3)
    d.t((x1 + x2) / 2, y - 9, label, 11, c if c != SOFT else MUTED, kr(label), "middle", 600)


def varrow(i, j, label):
    x = nx(j) + NW / 2
    y1, y2 = ny(i) + NH, ny(i + 1)
    d.arrow([(x, y1 + 2), (x, y2 - 4)], SOFT, "soft", 1.3)
    d.t(x + 10, (y1 + y2) / 2 + 4, label, 11, MUTED, kr(label), "start", 600)




for i, sec in enumerate(('§1', '§1', '§2', '§3', '§3')):
    d.chip(34, ny(i) + NH / 2 - 4, sec, MUTED, 11, 4)

node(0, 0, 'import ".../decimal"', '저장소 위치를 담은 경로')
node(0, 1, 'go.mod · go.sum', 'require 와 해시', INFO)
node(0, 2, '바이너리 하나', '의존성 소스까지 컴파일', OK)
harrow(0, 0, 'go get ./...')
harrow(0, 1, '빌드하면')

node(1, 0, 'go get 모듈 경로', '버전을 바꿀 때')
node(1, 1, '모두 // indirect', '소스를 확인하지 않음', WARN)
node(1, 2, '소스와 맞춘 go.mod', 'indirect 바로잡음', OK)
harrow(1, 0, '더하면')
harrow(1, 1, 'go mod tidy')

node(2, 0, 'A · B · C 가 요구', 'D v1.1.0 · v1.2.0 · v1.2.3')
node(2, 1, 'D v1.2.3', '모두를 만족하는 최소', INFO)
node(2, 2, 'go-isatty v0.0.14', '최신 v0.0.24 대신', OK)
harrow(2, 0, '최소 버전 선택')
harrow(2, 1, 'money 에서도')

node(3, 0, 'simpletax v1.1.0', '현재 버전')
node(3, 1, 'v1.1.1', '같은 마이너의 패치 · 가정한 판', INFO)
node(3, 2, 'v1.2.1', '가장 최신 · 가정한 판', OK)
harrow(3, 0, '-u=patch')
harrow(3, 1, '-u')

node(4, 0, '".../simpletax/v2"', '메이저가 바뀐 판의 import')
node(4, 1, 'v1 · v2 함께 적힘', '다른 패키지', INFO)
node(4, 2, 'v2.0.0 만 남음', '옛 버전 정리', OK)
harrow(4, 0, 'go get ./...')
harrow(4, 1, 'go mod tidy')


d.legend(712, [("go.mod 상태", INFO), ("결과", OK), ("고칠 표시", WARN)])
d.save('10-03.chapter-overview.svg')
print('ok', '10-03')

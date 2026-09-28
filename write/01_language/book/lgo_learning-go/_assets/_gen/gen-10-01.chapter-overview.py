# 10-01.chapter-overview — 저장소가 모듈을, 모듈이 패키지를 담고, go.mod 가 모듈을 선언하며, go 줄이 빌드할 Go 를 정하고, require 가 의존성을 적는다
# 본문 요구(10-01 「학습 목표」 개념도 문단): 첫 줄 저장소·모듈·패키지(§1), 둘째 줄 go mod init 과 go.mod(§2), 셋째 줄 go 줄과 GOTOOLCHAIN(§3), 넷째 줄 require 와 indirect(§3).
# 타입 스펙: type-architecture — 키워드 개념도. 4행 × 3열 노드 격자(11-01 개념도와 같은 공식: 열 x = 60 + j·340,
#           노드 216×64, 행 y = 112 + i·128), 행 안은 가로 화살표, 행 사이는 필요할 때만 세로 화살표.
# 사실 출처: Learning Go 2판 10장 「Repositories, Modules, and Packages」·「Using go.mod」·「Use the go Directive to Manage Go Build Versions」·「The require Directive」, go1.25.1 로컬 실행(2026-09-27).
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, KR, MONO

COL_X, STRIDE, NW, NH = 60, 340, 216, 64
ROW_Y, ROW_STRIDE = 112, 128
W, H = 984, 680


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def nx(j):
    return COL_X + j * STRIDE


def ny(i):
    return ROW_Y + i * ROW_STRIDE


d = D(W, H, 'ARCHITECTURE · 10-01 OVERVIEW',
      '모듈이 배포의 단위이고 go.mod 가 그 약속입니다',
      '10-01 의 키워드 개념도. 첫 줄은 저장소가 모듈을 담고 모듈이 디렉터리 단위의 패키지를 담는 세 단계다. 둘째 줄은 go mod init 이 전역으로 유일한 모듈 경로로 go.mod 를 만들고, 그 안의 go 줄이 최소 Go 버전이자 언어 수준이라는 것이다. 셋째 줄은 go 줄이 설치된 Go 보다 새로우면 기본 auto 는 그 버전을 내려받아 빌드하고, GOTOOLCHAIN=local 은 오류로 멈춘다는 것이다. 넷째 줄은 require 의 둘째 묶음에 붙는 // indirect 가 기능 차이 없는 표시라는 것이다.',
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




for i, sec in enumerate(('§1', '§2', '§3', '§3')):
    d.chip(34, ny(i) + NH / 2 - 4, sec, MUTED, 11, 4)

node(0, 0, '저장소', '버전 관리 장소')
node(0, 1, '모듈', '배포·버전의 단위', INFO)
node(0, 2, '패키지', '디렉터리 하나', OK)
harrow(0, 0, '담음')
harrow(0, 1, '담음')

node(1, 0, 'go mod init 경로', '전역으로 유일한 이름')
node(1, 1, 'go.mod', 'module · go · require', INFO)
node(1, 2, 'go 1.21', '최소 버전 · 언어 수준', OK)
harrow(1, 0, '만듦')
harrow(1, 1, 'go 줄')

node(2, 0, 'go 1.26 · 설치 1.25.1', '더 새 버전을 요구')
node(2, 1, 'GOTOOLCHAIN=auto', '그 버전을 내려받아 빌드', INFO)
node(2, 2, 'GOTOOLCHAIN=local', '오류로 멈춤', ACC)
harrow(2, 0, '기본값')
harrow(2, 1, '대신 local 이면', ACC, 'acc')

node(3, 0, 'require 첫 묶음', '직접 의존성')
node(3, 1, '// indirect', '의존성의 의존성', INFO)
node(3, 2, '기능 차이 없음', '사람을 위한 표시', OK)
harrow(3, 0, '둘째 묶음')
harrow(3, 1, '뜻은')


d.legend(584, [("go.mod 요소", INFO), ("결과", OK), ("멈추는 경우", ACC)])
d.save('10-01.chapter-overview.svg')
print('ok', '10-01')

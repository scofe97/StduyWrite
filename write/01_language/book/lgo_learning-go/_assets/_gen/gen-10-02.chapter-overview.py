# 10-02.chapter-overview — 대문자로 내보내고 import 경로로 가져오며, 기능을 말하는 이름을 짓고, 주석이 문서가 되며, internal 로 감추고 순환을 피하며, 모듈 종류에 따라 배치한다
# 본문 요구(10-02 「학습 목표」 개념도 문단): 첫 줄 내보내기와 import(§1), 둘째 줄 이름 짓기와 바꾸기(§2), 셋째 줄 Go Doc(§3), 넷째 줄 internal 과 순환 의존(§4), 다섯째 줄 모듈 배치(§5).
# 타입 스펙: type-architecture — 키워드 개념도. 5행 × 3열 노드 격자(11-01 개념도와 같은 공식: 열 x = 60 + j·340,
#           노드 216×64, 행 y = 112 + i·128), 행 안은 가로 화살표, 행 사이는 필요할 때만 세로 화살표.
# 사실 출처: Learning Go 2판 10장 「Building Packages」 전체, go1.25.1 로컬 실행(2026-09-27).
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


d = D(W, H, 'ARCHITECTURE · 10-02 OVERVIEW',
      '이름의 모양과 디렉터리 위치가 공개 범위를 정합니다',
      '10-02 의 키워드 개념도. 첫 줄은 대문자로 시작한 식별자가 내보내지고, 다른 패키지는 import 경로로 가져오며, 부르는 이름은 패키지 절이 정한다는 것이다. 둘째 줄은 util 같은 이름 대신 기능을 말하는 명사로 짓고, 이름이 겹치면 import 할 때 바꾼다는 것이다. 셋째 줄은 기호 이름으로 시작하는 // 주석을 go doc 과 pkgsite 가 문서로 보여 준다는 것이다. 넷째 줄은 internal 패키지가 부모 트리 안에서만 import 되고 패키지끼리 서로 import 할 수 없다는 것이다. 다섯째 줄은 애플리케이션은 로직을 internal 에, 라이브러리는 루트를 저장소 이름과 같은 패키지로 둔다는 것이다.',
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




for i, sec in enumerate(('§1', '§2', '§3', '§4', '§5')):
    d.chip(34, ny(i) + NH / 2 - 4, sec, MUTED, 11, 4)

node(0, 0, 'func Double', '대문자로 시작')
node(0, 1, 'math.Double(2)', 'import 경로로 가져와 부름', INFO)
node(0, 2, 'package 절', 'do-format 은 format', OK)
harrow(0, 0, '내보냄')
harrow(0, 1, '부르는 이름은')

node(1, 0, 'util.FormatNames', '무슨 일인지 모름')
node(1, 1, 'names.Format', '패키지 명사 · 함수 동사', OK)
node(1, 2, 'crand "crypto/rand"', '겹치면 이름 바꿈', INFO)
harrow(1, 0, '품사로 바꾸면')
harrow(1, 1, '이름이 겹치면')

node(2, 0, '// Convert converts …', '첫 단어는 기호 이름')
node(2, 1, 'go doc · pkgsite', '문서로 보여 줌', INFO)
node(2, 2, 'pkg.go.dev', 'HTML 문서', OK)
harrow(2, 0, '읽어서')
harrow(2, 1, '올리면')

node(3, 0, 'foo/internal', '부모 트리 안에서만')
node(3, 1, 'foo · foo/sibling', 'import 가능', OK)
node(3, 2, 'pet · person', '서로 import 금지', ACC)
harrow(3, 0, '허용')
harrow(3, 1, '순환이면', ACC, 'acc')

node(4, 0, '애플리케이션 모듈', 'main 은 최소')
node(4, 1, 'internal/', '로직과 공유 코드', INFO)
node(4, 2, '라이브러리 모듈', '루트 = 저장소 이름 · cmd/', OK)
harrow(4, 0, '로직은')
harrow(4, 1, '라이브러리면')


d.legend(712, [("가져오는 쪽", INFO), ("권하는 형태", OK), ("컴파일 오류", ACC)])
d.save('10-02.chapter-overview.svg')
print('ok', '10-02')

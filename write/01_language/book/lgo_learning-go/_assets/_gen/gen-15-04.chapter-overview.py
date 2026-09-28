# 15-04.chapter-overview — 의존성을 인터페이스로 받아 스텁을 끼우고, HTTP 는 httptest 서버로 바꾸고, 통합 테스트를 태그로 묶어 진짜와의 어긋남을 보며, -race 가 레이스를 찾는다
# 본문 요구(15-04 「학습 목표」 개념도 문단): 첫 줄 스텁(§1), 둘째 줄 httptest(§2), 셋째 줄 통합 테스트(§3), 넷째 줄 레이스 검출(§3).
# 타입 스펙: type-architecture — 키워드 개념도. 4행 × 3열 노드 격자(11-01 개념도와 같은 공식: 열 x = 60 + j·340,
#           노드 216×64, 행 y = 112 + i·128), 행 안은 가로 화살표, 행 사이는 필요할 때만 세로 화살표.
# 사실 출처: Learning Go 2판 15장, go1.27.1 로컬 실행(2026-09-28) — solver·stub·race, math_server 세 가지 빌드, simplewebapp 연습 문제.
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


d = D(W, H, 'ARCHITECTURE · 15-04 OVERVIEW',
      '가짜는 인터페이스 자리에 끼우고 진짜와의 어긋남은 통합 테스트가 봅니다',
      '15-04 의 키워드 개념도. 첫 줄은 Logic 이 인터페이스로 받은 Entities 자리에 임베딩이나 함수 필드로 만든 스텁을 끼워 사례마다 정해 둔 답을 돌려준다는 것이다. 둘째 줄은 RemoteSolver 에 httptest 서버의 URL 을 넘기고, 사례마다 공유 변수로 서버의 응답을 정해 서버 없이 시험한다는 것이다. 셋째 줄은 //go:build integration 파일을 -tags integration 으로 켜 진짜 계산기 서버에 붙이자, 소스로 빌드한 서버의 오류 문구가 달라 case3 이 실패했다는 것이다. 넷째 줄은 다섯 고루틴의 counter++ 를 -race 가 race.go:12 의 레이스로 짚고, 잠금이나 atomic 으로 고친다는 것이다.',
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

node(0, 0, 'Logic', 'Entities 필드')
node(0, 1, '스텁', '임베딩 · 함수 필드', INFO)
node(0, 2, '정해 둔 답', '목은 호출을 검증', OK)
harrow(0, 0, '인터페이스 자리')
harrow(0, 1, '사례마다')

node(1, 0, 'RemoteSolver', 'HTTP 로 Resolve')
node(1, 1, 'httptest 서버', '무작위 포트', INFO)
node(1, 2, '사례별 응답', '서버 없이 시험', OK)
harrow(1, 0, 'server.URL')
harrow(1, 1, '공유 변수 io')

node(2, 0, '//go:build integration', '통합 테스트 파일')
node(2, 1, '진짜 계산기 서버', 'Docker · 소스 빌드', INFO)
node(2, 2, 'case3 실패', '오류 문구가 다름', ACC)
harrow(2, 0, '-tags')
harrow(2, 1, '소스 빌드면', ACC, 'acc')

node(3, 0, 'counter++', '고루틴 다섯')
node(3, 1, 'DATA RACE', 'race.go:12', INFO)
node(3, 2, '잠금 · atomic', '증가가 안 사라짐', OK)
harrow(3, 0, '-race')
harrow(3, 1, '고치면')


d.legend(584, [("테스트 장치", INFO), ("결과", OK), ("어긋남", ACC)])
d.save('15-04.chapter-overview.svg')
print('ok', '15-04')

# 09-03.chapter-overview — panic 은 defer 를 거슬러 실행하고 끝나며, recover 는 defer 안에서 붙잡고, 공개 API 경계에서만 오류로 바꾸고, 스택 트레이스는 라이브러리로 얻는다
# 본문 요구(09-03 「학습 목표」 개념도 문단): 첫 줄 panic 과 defer 사슬(§1), 둘째 줄 recover(§2), 셋째 줄 API 경계(§2), 넷째 줄 스택 트레이스와 -trimpath(§3).
# 타입 스펙: type-architecture — 키워드 개념도. 4행 × 3열 노드 격자(11-01 개념도와 같은 공식: 열 x = 60 + j·340,
#           노드 216×64, 행 y = 112 + i·128), 행 안은 가로 화살표, 행 사이는 필요할 때만 세로 화살표.
# 사실 출처: Learning Go 2판 9장 「panic and recover」·「Getting a Stack Trace from an Error」, go1.25.1 로컬 실행(2026-09-27).
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


d = D(W, H, 'ARCHITECTURE · 09-03 OVERVIEW',
      'panic 은 비상구이고 recover 는 경계에서만 씁니다',
      '09-03 의 키워드 개념도. 첫 줄은 프로그래밍 오류로 panic 이 나면 현재 함수가 끝나고 호출 사슬을 거슬러 defer 들이 실행된 뒤 스택 트레이스를 찍고 프로그램이 끝난다는 것이다. 둘째 줄은 defer 안에서 recover 를 부르면 panic 값을 돌려받고 실행이 이어진다는 것이다. 셋째 줄은 서드파티용 라이브러리의 공개 함수가 recover 로 panic 을 오류로 바꿔 돌려준다는 것이다. 넷째 줄은 Go 오류에 스택 트레이스가 없어 서드파티 라이브러리의 %+v 로 보고, 빌드 경로는 -trimpath 로 가린다는 것이다.',
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




for i, sec in enumerate(('§1', '§2', '§2', '§3')):
    d.chip(34, ny(i) + NH / 2 - 4, sec, MUTED, 11, 4)

node(0, 0, 'panic 발생', '0 으로 나누기 · slice 범위 밖')
node(0, 1, 'defer 사슬', '호출 사슬을 거슬러', INFO)
node(0, 2, '스택 트레이스 · 종료', '복구되지 않은 panic', ACC)
harrow(0, 0, '현재 함수 끝')
harrow(0, 1, '다 돌면', ACC, 'acc')

node(1, 0, 'defer func() { … }()', 'panic 전에 등록')
node(1, 1, 'recover()', 'panic 값을 돌려받음', INFO)
node(1, 2, '실행이 이어짐', 'div60(6) → 10', OK)
harrow(1, 0, '안에서 부름')
harrow(1, 1, '붙잡으면')

node(2, 0, '라이브러리 내부 panic', '공개 함수 안')
node(2, 1, '공개 API 경계', 'recover 로 붙잡음', INFO)
node(2, 2, 'error 로 반환', '호출자가 판단', OK)
harrow(2, 0, '새어 나가기 전')
harrow(2, 1, '바꿔서')

node(3, 0, 'Go 오류', '스택 트레이스 없음')
node(3, 1, '서드파티 오류 라이브러리', 'fmt.Printf("%+v")', INFO)
node(3, 2, '-trimpath', '빌드 경로를 패키지 경로로', OK)
harrow(3, 0, '필요하면')
harrow(3, 1, '경로를 가리려면')


d.legend(584, [("장치", INFO), ("쓸 형태", OK), ("프로그램 종료", ACC)])
d.save('09-03.chapter-overview.svg')
print('ok', '09-03')

# 16-02.chapter-overview — CSV 마샬러가 태그와 Kind 로 두 방향을 바꾸고, MakeFunc 가 함수를 감싸되 메서드는 못 만들며, 리플렉션 Filter 는 제네릭보다 수십 배 느리다
# 본문 요구(16-02 「학습 목표」 개념도 문단): 첫 줄 CSV 두 방향(§1), 둘째 줄 Kind 별 변환(§1), 셋째 줄 MakeFunc·StructOf(§2), 넷째 줄 Filter 비용(§3).
# 타입 스펙: type-architecture — 키워드 개념도. 4행 × 3열 노드 격자(11-01 개념도와 같은 공식: 열 x = 60 + j·340,
#           노드 216×64, 행 y = 112 + i·128), 행 안은 가로 화살표, 행 사이는 필요할 때만 세로 화살표.
# 사실 출처: Learning Go 2판 16장, go1.27.1 로컬 실행(2026-09-29) — csv·timed_function·memoizer·reflection_filter 벤치마크.
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


d = D(W, H, 'ARCHITECTURE · 16-02 OVERVIEW',
      '리플렉션은 경계에서 쓰고 안쪽은 제네릭에 맡깁니다',
      '16-02 의 키워드 개념도. 첫 줄은 csv.ReadAll 로 읽은 텍스트를 Unmarshal 이 구조체 slice 로, Marshal 이 다시 머리글과 행으로 바꾼다는 것이다. 둘째 줄은 필드의 Kind 를 switch 로 갈라 strconv 로 바꾸고 모르는 종류는 오류를 낸다는 것이다. 셋째 줄은 MakeFunc 가 아무 함수나 감싸 시간 측정·캐시를 더하지만 메서드는 만들 수 없다는 것이다. 넷째 줄은 원소 1,000개 문자열을 거르는 리플렉션 Filter 가 108,951 ns/op·2,219 할당이고 제네릭판은 1,848 ns/op·1 할당이라는 것이다.',
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




for i, sec in enumerate(('§1', '§1', '§2', '§3')):
    d.chip(34, ny(i) + NH / 2 - 4, sec, MUTED, 11, 4)

node(0, 0, 'CSV 텍스트', 'csv.ReadAll')
node(0, 1, '[]MyData', '태그로 열 찾기', INFO)
node(0, 2, '[][]string', '머리글 + 행', OK)
harrow(0, 0, 'Unmarshal')
harrow(0, 1, 'Marshal')

node(1, 0, '필드 Kind', 'Int · String · Bool')
node(1, 1, 'strconv 변환', 'ParseInt · FormatBool', INFO)
node(1, 2, '오류', 'cannot handle field', ACC)
harrow(1, 0, 'switch')
harrow(1, 1, '모르는 종류', ACC, 'acc')

node(2, 0, 'func(int) int', '아무 함수')
node(2, 1, '감싼 함수', '시간 측정 · 캐시', INFO)
node(2, 2, '메서드 생성 불가', 'StructOf 도 승격 없음', ACC)
harrow(2, 0, 'MakeFunc')
harrow(2, 1, '그러나', ACC, 'acc')

node(3, 0, 'Filter(any, any)', '리플렉션판')
node(3, 1, '108,951 ns/op', '2,219 할당', ACC)
node(3, 2, '1,848 ns/op', '제네릭 · 약 59배 빠름', OK)
harrow(3, 0, '문자열 1,000개')
harrow(3, 1, '제네릭판은')


d.legend(584, [("리플렉션 장치", INFO), ("결과", OK), ("한계·비용", ACC)])
d.save('16-02.chapter-overview.svg')
print('ok', '16-02')

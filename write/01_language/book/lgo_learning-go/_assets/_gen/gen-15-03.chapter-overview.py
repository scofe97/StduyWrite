# 15-03.chapter-overview — 퍼저가 시드를 비틀어 실패 입력을 회귀 테스트로 남기고, 벤치마크가 한 번의 비용을 재며, Go 1.25 가 작은 버퍼의 할당을 없앴다
# 본문 요구(15-03 「학습 목표」 개념도 문단): 첫 줄 퍼즈 테스트(§1), 둘째 줄 퍼저가 찾은 입력(§1), 셋째 줄 벤치마크(§2), 넷째 줄 Go 1.25 스택 할당(§2).
# 타입 스펙: type-architecture — 키워드 개념도. 4행 × 3열 노드 격자(11-01 개념도와 같은 공식: 열 x = 60 + j·340,
#           노드 216×64, 행 y = 112 + i·128), 행 안은 가로 화살표, 행 사이는 필요할 때만 세로 화살표.
# 사실 출처: Learning Go 2판 15장, go1.27.1 로컬 실행(2026-09-28) — file_parser 퍼징, bench 를 go1.24.4·go1.27.1 로 비교.
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


d = D(W, H, 'ARCHITECTURE · 15-03 OVERVIEW',
      '퍼징은 버티는지를, 벤치마크는 얼마나 드는지를 묻습니다',
      '15-03 의 키워드 개념도. 첫 줄은 f.Add 로 넣은 시드를 퍼저가 비틀어 f.Fuzz 대상에 넣고, 실패한 입력은 testdata/fuzz 에 남아 회귀 테스트가 된다는 것이다. 둘째 줄은 이 노트의 퍼징이 -1 을 0.21초에 찾고, 고친 뒤 \\r 이 섞인 빈 줄을 찾고, 다시 고친 뒤 2분 동안 446만 회를 통과했다는 것이다. 셋째 줄은 벤치마크가 -bench·-benchmem 으로 한 번당 시간·바이트·할당 횟수를 재고, 버퍼를 루프 밖으로 옮기면 할당이 서너 번으로 고르게 준다는 것이다. 넷째 줄은 버퍼 1바이트의 할당이 go1.24.4 에서 65,208회, Go 1.25 부터 3회라는 것이다.',
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




for i, sec in enumerate(('§1', '§1', '§2', '§2')):
    d.chip(34, ny(i) + NH / 2 - 4, sec, MUTED, 11, 4)

node(0, 0, 'f.Add(시드)', '시드 코퍼스')
node(0, 1, 'f.Fuzz 대상', '패닉 · 왕복 확인', INFO)
node(0, 2, 'testdata/fuzz', '회귀 테스트로 남음', OK)
harrow(0, 0, '퍼저가 비틂')
harrow(0, 1, '실패하면')

node(1, 0, '"-1"', '0.21초에 찾음')
node(1, 1, '"3\\n\\n\\n\\r\\r"', '왕복이 어긋남', INFO)
node(1, 2, '2분 · 446만 회', 'PASS', OK)
harrow(1, 0, '고치고 다시')
harrow(1, 1, '고치고 다시')

node(2, 0, 'BenchmarkXxx(b)', 'b.N 또는 b.Loop')
node(2, 1, 'ns/op · B/op', 'allocs/op', INFO)
node(2, 2, '할당 3~4회로 고름', '메모리·속도 거래', OK)
harrow(2, 0, '-benchmem')
harrow(2, 1, '버퍼를 밖으로')

node(3, 0, 'make([]byte, 1)', '버퍼 1바이트')
node(3, 1, '65,208 allocs/op', 'go1.24.4 · 힙', INFO)
node(3, 2, '3 allocs/op', '32바이트까지 스택', ACC)
harrow(3, 0, '반복마다')
harrow(3, 1, 'Go 1.25 부터', ACC, 'acc')


d.legend(584, [("테스트 장치", INFO), ("결과", OK), ("버전 차이", ACC)])
d.save('15-03.chapter-overview.svg')
print('ok', '15-03')

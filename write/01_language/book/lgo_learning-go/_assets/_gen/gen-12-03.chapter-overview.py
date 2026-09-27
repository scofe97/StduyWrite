# 12-03.chapter-overview — 버퍼 채널로 결과를 모으고 요청을 제한하며, select 에 nil 채널과 ctx.Done() 을 넣고, WaitGroup·Once 로 기다림과 한 번 실행을 맡긴다
# 본문 요구(12-03 「학습 목표」 개념도 문단): 첫 줄 버퍼 채널과 백프레셔(§1~2), 둘째 줄 nil case 끄기와 시간 제한(§3~4), 셋째 줄 WaitGroup 과 한 번만 닫기(§5), 넷째 줄 Once·OnceValue(§6).
# 타입 스펙: type-architecture — 키워드 개념도. 4행 × 3열 노드 격자(11-01 개념도와 같은 공식: 열 x = 60 + j·340,
#           노드 216×64, 행 y = 112 + i·128), 행 안은 가로 화살표, 행 사이는 필요할 때만 세로 화살표.
# 사실 출처: Learning Go 2판 12장 「Know When to Use Buffered and Unbuffered Channels」「Implement Backpressure」「Turn Off a case in a select」「Time Out Code」「Use WaitGroups」「Run Code Exactly Once」, go1.25.1 로컬 실행(2026-09-28).
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, KR, MONO

COL_X, STRIDE, NW, NH = 60, 340, 216, 64
ROW_Y, ROW_STRIDE = 112, 128
W, H = 984, 648


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def nx(j):
    return COL_X + j * STRIDE


def ny(i):
    return ROW_Y + i * ROW_STRIDE


d = D(W, H, 'ARCHITECTURE · 12-03 OVERVIEW',
      '채널·select·context·sync 를 조합해 패턴을 만듭니다',
      '12-03 의 키워드 개념도. 첫 줄은 크기가 정해진 버퍼 채널이 고루틴 수만큼 결과를 모으는 재료이자, 토큰으로 요청 수를 제한해 넘치면 거절하는 백프레셔의 재료라는 것이다. 둘째 줄은 select 에 닫힌 채널 대신 nil 을 넣어 case 를 끄고, ctx.Done() 을 넣어 시간 제한을 거는 두 조합이다. 셋째 줄은 sync.WaitGroup 의 Add·Done·Wait 로 모든 고루틴을 기다린 뒤 감시 고루틴이 채널을 한 번만 닫는 흐름이다. 넷째 줄은 sync.Once 가 초기화를 한 번만 하고, Go 1.21 의 OnceValue 가 결과까지 캐시하는 흐름이다.',
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




for i, sec in enumerate(('§1~2', '§3~4', '§5', '§6')):
    d.chip(34, ny(i) + NH / 2 - 4, sec, MUTED, 11, 4)

node(0, 0, '버퍼 채널', '크기 고정 · len · cap', INFO)
node(0, 1, '결과 모으기', '고루틴 수만큼 버퍼')
node(0, 2, '백프레셔', '가득 차면 429', OK)
harrow(0, 0, '띄운 수를 알 때')
harrow(0, 1, '다른 쓰임 · 토큰', ACC, 'acc')

node(1, 0, 'select', 'for-select 루프', INFO)
node(1, 1, 'case 끄기', '닫힌 채널 = nil')
node(1, 2, '시간 제한', 'timeLimit · 버퍼 1', OK)
harrow(1, 0, 'nil 채널 case')
harrow(1, 1, '다른 조합 · ctx.Done()', ACC, 'acc')

node(2, 0, 'sync.WaitGroup', '제로 값 · 복사 금지', INFO)
node(2, 1, '모두 기다림', 'Add · Done · Wait')
node(2, 2, 'close 한 번', '감시 고루틴', OK)
harrow(2, 0, '클로저로 캡처')
harrow(2, 1, 'Wait 뒤에', ACC, 'acc')

node(3, 0, 'sync.Once', '제로 값 · 복사 금지', INFO)
node(3, 1, '지연 초기화', 'once.Do 한 번')
node(3, 2, 'OnceValue', '결과를 캐시', OK)
harrow(3, 0, '처음 쓸 때')
harrow(3, 1, 'Go 1.21')


d.legend(584, [("재료", INFO), ("얻는 것", OK), ("조합하는 곳", ACC)])
d.save('12-03.chapter-overview.svg')
print('ok', '12-03')

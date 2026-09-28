# 13-02.chapter-overview — Duration 은 int64 길이, Time 은 시간대를 품은 시점이고 형식은 기준 시각으로, 단조 시계가 Sub 를 지킨다
# 본문 요구(13-02 「학습 목표」 개념도 문단): 첫 줄 Duration 과 ParseDuration(§1), 둘째 줄 Time·Equal·기준 시각 형식(§2), 셋째 줄 단조 시계와 타이머(§3).
# 타입 스펙: type-architecture — 키워드 개념도. 3행 × 3열 노드 격자(11-01 개념도와 같은 공식: 열 x = 60 + j·340,
#           노드 216×64, 행 y = 112 + i·128), 행 안은 가로 화살표, 행 사이는 필요할 때만 세로 화살표.
# 사실 출처: Learning Go 2판 13장 「time」「Monotonic Time」「Timers and Timeouts」, go1.25.1 로컬 실행(2026-09-28).
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, KR, MONO

COL_X, STRIDE, NW, NH = 60, 340, 216, 64
ROW_Y, ROW_STRIDE = 112, 128
W, H = 984, 520


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def nx(j):
    return COL_X + j * STRIDE


def ny(i):
    return ROW_Y + i * ROW_STRIDE


d = D(W, H, 'ARCHITECTURE · 13-02 OVERVIEW',
      '길이는 Duration, 시점은 Time, 형식은 기준 시각',
      '13-02 의 키워드 개념도. 첫 줄은 int64 바탕의 time.Duration 을 time.Hour 같은 타입 있는 상수로 만들고, 300ms 같은 문자열은 ParseDuration 으로 읽는다는 것이다. 둘째 줄은 시간대를 품은 time.Time 을 == 대신 Equal 로 비교하고, 2006-01-02 15:04:05 기준 시각으로 형식을 적는다는 것이다. 셋째 줄은 time.Now 가 단조 시계를 함께 담아 Sub 를 벽시계 변화에서 지키고, After·Tick·NewTicker 채널이 시간 제한과 반복에 쓰인다는 것이다.',
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




for i, sec in enumerate(('§1', '§2', '§3')):
    d.chip(34, ny(i) + NH / 2 - 4, sec, MUTED, 11, 4)

node(0, 0, 'int64', '나노초 단위')
node(0, 1, 'time.Duration', '2*time.Hour + 30*time.Minute', INFO)
node(0, 2, 'ParseDuration', '"300ms" · "-1.5h"')
harrow(0, 0, '바탕 타입')
harrow(0, 1, '문자열에서')

node(1, 0, 'time.Time', '시간대를 품은 시점', INFO)
node(1, 1, 'Equal', '== 는 시간대까지 비교')
node(1, 2, '기준 시각', '2006-01-02 15:04:05', OK)
harrow(1, 0, '같은 순간 비교', ACC, 'acc')
harrow(1, 1, '형식은')

node(2, 0, 'time.Now', 'm= 단조 시계 포함', INFO)
node(2, 1, 'Sub · Since', '벽시계 변화에 안전')
node(2, 2, 'After · NewTicker', '시간 제한 · 반복', OK)
harrow(2, 0, '단조 시계로')
harrow(2, 1, '채널로')


d.legend(456, [("time 타입", INFO), ("쓰는 법", OK), ("비교 규칙", ACC)])
d.save('13-02.chapter-overview.svg')
print('ok', '13-02')

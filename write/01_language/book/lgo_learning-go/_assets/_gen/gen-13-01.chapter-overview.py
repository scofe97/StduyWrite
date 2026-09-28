# 13-01.chapter-overview — Read 는 호출자의 버퍼를 채우고, 감싸도 io.Reader 라 같은 함수가 읽으며, 한 메서드 인터페이스를 조합하고 임베딩으로 채운다
# 본문 요구(13-01 「학습 목표」 개념도 문단): 첫 줄 Read 의 규약(§1), 둘째 줄 파일 → gzip 리더 데코레이터(§2), 셋째 줄 조합 인터페이스와 NopCloser(§3).
# 타입 스펙: type-architecture — 키워드 개념도. 3행 × 3열 노드 격자(11-01 개념도와 같은 공식: 열 x = 60 + j·340,
#           노드 216×64, 행 y = 112 + i·128), 행 안은 가로 화살표, 행 사이는 필요할 때만 세로 화살표.
# 사실 출처: Learning Go 2판 13장 「io and Friends」, go1.25.1 로컬 실행(2026-09-28).
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


d = D(W, H, 'ARCHITECTURE · 13-01 OVERVIEW',
      'io.Reader 는 버퍼를 받아 채우고, 겹쳐서 기능을 더합니다',
      '13-01 의 키워드 개념도. 첫 줄은 호출자가 만든 버퍼를 Read 가 채우고 읽은 수 n 을 돌려주며, 다 읽으면 io.EOF 로 알리는 규약이다. 둘째 줄은 *os.File 을 gzip.NewReader 로 감싸도 io.Reader 라서 countLetters 같은 함수가 코드 변경 없이 읽는 데코레이터다. 셋째 줄은 Reader·Writer·Closer·Seeker 를 묶은 조합 인터페이스로 할 일을 드러내고, 모자란 Close 는 NopCloser 가 임베딩으로 채운다는 것이다.',
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

node(0, 0, 'buf := make([]byte, 2048)', '한 번 할당 · 재사용')
node(0, 1, 'r.Read(buf)', '최대 len(buf) 바이트', INFO)
node(0, 2, 'n · io.EOF', 'n 먼저 처리 · 끝 표시', OK)
harrow(0, 0, '넘겨서 채움')
harrow(0, 1, '돌려줌')

node(1, 0, '*os.File', 'io.Reader')
node(1, 1, '*gzip.Reader', 'io.Reader', INFO)
node(1, 2, 'countLetters', 'io.Reader 만 앎', OK)
harrow(1, 0, 'gzip.NewReader', ACC, 'acc')
harrow(1, 1, '같은 함수로 읽음')

node(2, 0, '한 메서드 인터페이스', 'Reader · Writer · Closer · Seeker')
node(2, 1, 'io.ReadCloser 등', '할 일을 드러냄', INFO)
node(2, 2, 'io.NopCloser', '임베딩 + Close() nil', OK)
harrow(2, 0, '조합')
harrow(2, 1, '모자라면')


d.legend(456, [("io 타입", INFO), ("얻는 것", OK), ("감싸기", ACC)])
d.save('13-01.chapter-overview.svg')
print('ok', '13-01')

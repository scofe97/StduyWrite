# 13-03.chapter-overview — 구조체 태그가 이름과 생략을 정하고, Decoder·Encoder 가 io 와 붙어 스트림을 다루며, 다른 형식은 사용자 정의 타입이나 Dup 으로 덮는다
# 본문 요구(13-03 「학습 목표」 개념도 문단): 첫 줄 태그와 Marshal·Unmarshal(§1~2), 둘째 줄 Decoder·Encoder 와 스트림(§2), 셋째 줄 사용자 정의 파싱과 struct 분리(§3).
# 타입 스펙: type-architecture — 키워드 개념도. 3행 × 3열 노드 격자(11-01 개념도와 같은 공식: 열 x = 60 + j·340,
#           노드 216×64, 행 y = 112 + i·128), 행 안은 가로 화살표, 행 사이는 필요할 때만 세로 화살표.
# 사실 출처: Learning Go 2판 13장 「encoding/json」, go1.25.1 로컬 실행(2026-09-28).
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


d = D(W, H, 'ARCHITECTURE · 13-03 OVERVIEW',
      '태그로 이름을 정하고, 스트림은 Decoder·Encoder 로',
      '13-03 의 키워드 개념도. 첫 줄은 json:"id" 같은 구조체 태그가 이름·무시·생략을 정하고, 태그는 Marshal·Unmarshal 을 부를 때만 리플렉션으로 읽힌다는 것이다. 둘째 줄은 io.Reader·io.Writer 에 붙는 json.Decoder·Encoder 로 파일이나 HTTP 본문을 바로 읽고 쓰며, 여러 값의 스트림은 io.EOF 까지 Decode 한다는 것이다. 셋째 줄은 기본과 다른 필드를 MarshalJSON 을 가진 타입이나 Dup 임베딩으로 덮어쓰고, 끝내 JSON 용 struct 와 처리용 struct 를 나눈다는 것이다.',
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




for i, sec in enumerate(('§1~2', '§2', '§3')):
    d.chip(34, ny(i) + NH / 2 - 4, sec, MUTED, 11, 4)

node(0, 0, '구조체 태그', 'json:"id,omitempty"')
node(0, 1, 'Marshal · Unmarshal', '[]byte 와 struct', INFO)
node(0, 2, '리플렉션', '16장')
harrow(0, 0, '호출할 때만 읽힘', ACC, 'acc')
harrow(0, 1, '태그를 읽는 방법')

node(1, 0, 'io.Reader · Writer', '파일 · HTTP 본문')
node(1, 1, 'Decoder · Encoder', 'NewDecoder(r)', INFO)
node(1, 2, '스트림', 'io.EOF 까지 Decode', OK)
harrow(1, 0, '바로 붙음')
harrow(1, 1, '하나씩')

node(2, 0, '다른 시간 형식', 'RFC822Z 등')
node(2, 1, 'MarshalJSON · Dup', '한 필드만 덮기', INFO)
node(2, 2, 'JSON 용 struct', '처리용과 분리', OK)
harrow(2, 0, '덮어쓰기')
harrow(2, 1, '끝내는', ACC, 'acc')


d.legend(456, [("encoding/json", INFO), ("권하는 끝", OK), ("주의할 규칙", ACC)])
d.save('13-03.chapter-overview.svg')
print('ok', '13-03')

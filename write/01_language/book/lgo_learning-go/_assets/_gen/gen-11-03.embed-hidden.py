# 11-03.embed-hidden — parent_dir · parent_dir/* · all:parent_dir 세 패턴이 숨김 파일을 어디까지 넣는가
# 본문 요구(11-03 §2): embed_hidden 예제의 세 변수가 parent_dir/.hidden 과 parent_dir/child_dir/.hidden 을 찾는지 한눈에 보인다.
#           /* 는 맨 위 디렉터리의 숨김 파일만, all: 은 모든 하위 디렉터리의 숨김 파일까지 넣는다.
# 타입 스펙: type-dp-security-matrix — 행 = 패턴(변수), 열 = 숨김 파일. 11-02.linter-matrix 와 같은 확대 공식
#           (comp_col_w 236 · role_col_w 168 · row_h 44 · row_stride 52). focal 1칸 = all: 만 넣는 하위 숨김 파일.
# 사실 출처: Learning Go 2판 11장 「Embedding Hidden Files」, 원서 예제 저장소 ch11 sample_code/embed_hidden 을 go1.25.1 로 실행(2026-09-28).
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, PAPER, PAPER2, KR, MONO

LP, RP, COMP_W, GAP0, ROLE_W, GAP = 12, 48, 220, 12, 156, 12
HEAD_Y, HEAD_H, ROW_H, ROW_S = 96, 52, 44, 52
tools = [('parent_dir/.hidden', '맨 위 숨김'), ('child_dir/.hidden', '하위 숨김')]
rows = [('parent_dir', 'noHidden'), ('parent_dir/*', 'parentHiddenOnly'), ('all:parent_dir', 'allHidden')]
cells = [[('없음', 'none'), ('없음', 'none')], [('found', 'ok'), ('없음', 'none')], [('found', 'ok'), ('found', 'focal')]]
N = len(tools)
W = LP + COMP_W + GAP0 + N * ROLE_W + (N - 1) * GAP + RP
ROW0 = HEAD_Y + HEAD_H + 16
rows_bottom = ROW0 + (len(rows) - 1) * ROW_S + ROW_H
LEG = rows_bottom + 24
H = LEG + 44


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def rx(j):
    return LP + COMP_W + GAP0 + j * (ROLE_W + GAP)


def ry(k):
    return ROW0 + k * ROW_S


d = D(W, H, 'MATRIX · 11-03 §2',
      '세 패턴이 숨김 파일을 어디까지 넣는가',
      'embed_hidden 예제의 세 embed.FS 변수가 숨김 파일 두 개를 여는지 go1.25.1 로 돌린 결과. 디렉터리 이름만 준 noHidden 은 둘 다 없다. parent_dir/* 를 준 parentHiddenOnly 는 맨 위 디렉터리의 parent_dir/.hidden 만 넣었다. all:parent_dir 를 준 allHidden 은 child_dir 안의 .hidden 까지 넣었다.',
      lead='칸 글자는 dir.Open 결과입니다. found 는 원문 출력의 표현입니다.')

d.box(LP, HEAD_Y, COMP_W, HEAD_H)
d.t(LP + COMP_W / 2, HEAD_Y + 23, '패턴', 13, INK, KR, "middle", 600)
d.t(LP + COMP_W / 2, HEAD_Y + 41, '변수 이름', 11, MUTED, kr('변수 이름'), "middle")
for j, (name, ver) in enumerate(tools):
    d.tone(rx(j), HEAD_Y, ROLE_W, HEAD_H, INFO, 6, "22", 1.0)
    d.t(rx(j) + ROLE_W / 2, HEAD_Y + 23, name, 13, INK, MONO, "middle", 600)
    d.t(rx(j) + ROLE_W / 2, HEAD_Y + 41, ver, 11, MUTED, kr(ver), "middle")

for k, (name, hint) in enumerate(rows):
    d.box(LP, ry(k), COMP_W, ROW_H, r=4)
    d.t(LP + 12, ry(k) + 20, name, 13, INK, kr(name), "start", 600)
    d.t(LP + 12, ry(k) + 36, hint, 11, MUTED, MONO, "start")
    for j, (val, lv) in enumerate(cells[k]):
        x, y = rx(j), ry(k)
        if lv == "ok":
            d.tone(x, y, ROLE_W, ROW_H, OK, 4, "18", 0.9)
            c = OK
        elif lv == "cfg":
            d.tone(x, y, ROLE_W, ROW_H, WARN, 4, "12", 0.9)
            c = WARN
        elif lv == "focal":
            d.tone(x, y, ROLE_W, ROW_H, ACC, 4, "18", 1.6)
            c = ACC
        else:
            d.box(x, y, ROLE_W, ROW_H, PAPER, RULE, 0.6, 4)
            c = SOFT
        d.t(x + ROLE_W / 2, y + 27, val, 13, c, kr(val), "middle", 600 if lv != "none" else 400)

d.legend(LEG, [("넣음", OK), ("all: 만 넣음", ACC)])
d.save('11-03.embed-hidden.svg')
print("ok", '11-03.embed-hidden.svg', W, H)

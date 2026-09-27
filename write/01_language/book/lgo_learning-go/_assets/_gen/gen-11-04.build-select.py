# 11-04.build-select — 대상 플랫폼과 -tags 에 따라 빌드에 들어가는 파일
# 본문 요구(11-04 §3 끝 표 문단): 파일 네 개로 만든 작은 모듈에서 대상과 태그에 따라 어느 파일이 빌드에 들어가는지
#           go list 와 go run 으로 확인한 결과. p.go 는 //go:build !gopher, g.go 는 //go:build gopher, x_windows_arm64.go 는 이름으로만 대상을 정했다.
# 타입 스펙: type-dp-security-matrix — 행 = 파일, 열 = 빌드 조건. 11-02.linter-matrix 와 같은 확대 공식. focal 1칸 = 이름 접미사로만 들어가는 windows/arm64.
# 사실 출처: go1.25.1 darwin/arm64 로컬 실행 — go list -f '{{.GoFiles}}' 를 기본·GOOS=windows GOARCH=arm64·GOOS=windows GOARCH=amd64 로,
#           go run . 과 go run -tags gopher . 이 plain · gopher 를 찍은 결과(2026-09-28). 원문 밖 재현이다.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, PAPER, PAPER2, KR, MONO

LP, RP, COMP_W, GAP0, ROLE_W, GAP = 12, 48, 220, 12, 156, 12
HEAD_Y, HEAD_H, ROW_H, ROW_S = 96, 52, 44, 52
tools = [('darwin/arm64', '기본'), ('darwin/arm64', '-tags gopher'), ('windows/arm64', 'GOOS·GOARCH'), ('windows/amd64', 'GOOS·GOARCH')]
rows = [('main.go', '조건 없음'), ('p.go', '//go:build !gopher'), ('g.go', '//go:build gopher'), ('x_windows_arm64.go', '이름 접미사만')]
cells = [[('포함', 'ok'), ('포함', 'ok'), ('포함', 'ok'), ('포함', 'ok')], [('포함', 'ok'), ('제외', 'none'), ('포함', 'ok'), ('포함', 'ok')], [('제외', 'none'), ('포함', 'ok'), ('제외', 'none'), ('제외', 'none')], [('제외', 'none'), ('제외', 'none'), ('포함', 'focal'), ('제외', 'none')]]
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


d = D(W, H, 'MATRIX · 11-04 §3',
      '대상과 태그에 따라 빌드에 들어가는 파일',
      '파일 네 개로 만든 모듈을 go1.25.1 로 확인한 결과. main.go 는 늘 들어간다. //go:build !gopher 를 단 p.go 는 -tags gopher 일 때만 빠지고, //go:build gopher 를 단 g.go 는 그때만 들어간다. 이름이 _windows_arm64 로 끝나는 파일은 GOOS=windows GOARCH=arm64 일 때만 들어가고 windows/amd64 에서는 빠진다.',
      lead='go list 의 GoFiles 와 go run 출력으로 확인했습니다. 원문 밖 재현입니다.')

d.box(LP, HEAD_Y, COMP_W, HEAD_H)
d.t(LP + COMP_W / 2, HEAD_Y + 23, '파일', 13, INK, KR, "middle", 600)
d.t(LP + COMP_W / 2, HEAD_Y + 41, '붙인 조건', 11, MUTED, kr('붙인 조건'), "middle")
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

d.legend(LEG, [("포함", OK), ("이름으로만 고른 파일", ACC)])
d.save('11-04.build-select.svg')
print("ok", '11-04.build-select.svg', W, H)

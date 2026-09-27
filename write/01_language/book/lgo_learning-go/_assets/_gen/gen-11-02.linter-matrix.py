# 11-02.linter-matrix — 원서 예제 다섯 개를 go vet · staticcheck · revive · golangci-lint 가 잡는가
# 본문 요구(11-02 §3 도입 문단): 이 절의 도구들이 원서 예제 다섯 개에서 각각 무엇을 잡는지 직접 돌려 채운 표.
#           golangci-lint 는 설정 없이 돌린 v2.14.0, 지역 변수 가림은 원문 설정을 줄 때만 잡힌다. 표 전체가 원문 밖 재현이다.
# 타입 스펙: type-dp-security-matrix — 행 = 예제, 열 = 도구. §2 공식(comp_col_w 208 · role_col_w 148 · gap 16 · row_stride 40)
#           을 따르되 한글 13px 하한 때문에 comp_col_w 208 → 220, role_col_w 148 → 156, role_col_gap 16 → 12(폭 상한 1000), row_h 36 → 44, row_stride 40 → 52 로 키웠다.
#           셀 level: 잡음(OK) · 설정 시(WARN) · 못 잡음(none). focal 1칸 = ineffassign 만 잡는 x 대입.
# 사실 출처: 원서 예제 저장소 ch11 의 staticcheck_test · check_err · revive_test · golangci-lint_test/{unused_vars,shadowing}
#           를 go vet(go1.25.1) · staticcheck 2026.2.1 · revive 1.17.0 · golangci-lint v2.14.0 으로 돌린 결과(2026-09-28).
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, PAPER, PAPER2, KR, MONO

LP, RP, COMP_W, GAP0, ROLE_W, GAP = 12, 48, 220, 12, 156, 12
HEAD_Y, HEAD_H, ROW_H, ROW_S = 96, 52, 44, 52
tools = [("go vet", "go1.25.1"), ("staticcheck", "2026.2.1"), ("revive", "1.17.0 기본"), ("golangci-lint", "v2.14.0 기본")]
rows = [("fmt.Sprintf 한 인자", "staticcheck_test"), ("다시 대입한 err", "check_err"),
        ("true := false", "revive_test"), ("x 대입을 읽지 않음", "unused_vars"), ("지역 변수 a·b 가림", "shadowing")]
# (값, level) — level: ok · cfg · none · focal
cells = [
    [("–", "none"), ("S1039", "ok"), ("–", "none"), ("S1039", "ok")],
    [("–", "none"), ("SA4006", "ok"), ("–", "none"), ("ineffassign", "ok")],
    [("–", "none"), ("–", "none"), ("builtin-id", "ok"), ("설정 시", "cfg")],
    [("–", "none"), ("–", "none"), ("–", "none"), ("ineffassign", "focal")],
    [("–", "none"), ("–", "none"), ("–", "none"), ("설정 시", "cfg")],
]
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


d = D(W, H, "MATRIX · 11-02 §3",
      "원서 예제 다섯 개를 네 도구가 잡는가",
      "원서 예제 다섯 개를 go vet, staticcheck, revive, golangci-lint 로 직접 돌린 결과. go vet 은 다섯 모두 통과시켰다. "
      "staticcheck 는 fmt.Sprintf 한 인자(S1039)와 다시 대입한 err(SA4006)를 잡았다. revive 는 true 가림만 잡았다. "
      "golangci-lint 는 설정 없이 첫 줄을 S1039 로, 둘째 줄을 ineffassign 으로 잡았고, x 대입을 읽지 않는 문제는 ineffassign 만 잡았다. "
      "true 가림과 지역 변수 가림은 원문의 .golangci.yml 을 줄 때만 잡혔다. 칸은 그 줄의 문제만 보인다. revive 의 패키지 주석 경고와 shadowing 예제의 var b is unused 경고는 적지 않았다.",
      lead="칸은 그 줄의 문제를 잡은 검사 이름입니다. 다른 경고는 적지 않았습니다.")

d.box(LP, HEAD_Y, COMP_W, HEAD_H)
d.t(LP + COMP_W / 2, HEAD_Y + 23, "원서 예제", 13, INK, KR, "middle", 600)
d.t(LP + COMP_W / 2, HEAD_Y + 41, "저장소 디렉터리", 11, MUTED, KR, "middle")
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

d.legend(LEG, [("잡음", OK), ("원문 설정을 줄 때만", WARN), ("이 도구만 잡음", ACC)])
d.save("11-02.linter-matrix.svg")
print("ok 11-02 matrix", W, H)

# 15-03.fuzz-loop — 퍼저는 시드를 비틀어 대상을 돌리고, 실패하면 입력을 줄여 testdata/fuzz 에 남기며, 코드를 고친 뒤 그 파일이 회귀 테스트로 돈다
# 본문 요구(15-03 §1 「퍼저가 찾은 입력은 testdata 에 남아 회귀 테스트가 됩니다」): f.Add 의 시드와 testdata/fuzz 의 파일이 코퍼스가 되고,
#           퍼저가 비튼 입력을 f.Fuzz 대상에 넣는다. 통과하면 계속 비틀고, 실패하면 입력을 줄여(minimizing) 파일로 쓴다.
#           코드를 고친 뒤 그 파일은 go test 때마다 도는 회귀 테스트다.
# 타입 스펙: type-flowchart — 윗줄 왼→오른(코퍼스 · 비틀기 · 대상 · 판단), 아랫줄 오른→왼(줄이기 · 실패 파일 · 고침), 고침에서 코퍼스로
#           올라가는 직교 귀환선과, 판단에서 비틀기로 돌아가는 "아니오" 고리. 노드 200×56, 가로 stride 248. focal 은 실패 파일 하나.
# 사실 출처: Learning Go 2판 15장 「Fuzzing」, go1.27.1 실행(2026-09-28) — 첫 실패 "-1" 0.21초, 파일 03f81b404ad91d09, 고친 뒤 2분 4,460,630회 PASS.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 984, 500
NW, NH, ST = 200, 56, 236
X = [28 + i * ST for i in range(4)]
Y1, Y2 = 128, 316


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def node(x, y, title, sub, c=None, w=NW):
    if c:
        d.tone(x, y, w, NH, c, 6, "18" if c == ACC else "12", 1.4 if c == ACC else 1.1)
    else:
        d.box(x, y, w, NH)
    d.t(x + w / 2, y + 24, title, 13, c or INK, kr(title), "middle", 600)
    d.t(x + w / 2, y + 43, sub, 11, MUTED, kr(sub), "middle")


d = D(W, H, "FLOWCHART · 15-03 §1",
      "퍼저가 찾은 실패 입력은 시드 코퍼스로 돌아가 회귀 테스트가 됩니다",
      "시드 코퍼스는 f.Add 로 넣은 값과 testdata/fuzz 아래 파일이다. 퍼저가 코퍼스를 비틀어 f.Fuzz 대상에 넣고, 패닉이나 조건 위반이 없으면 계속 비튼다. "
      "실패하면 입력을 줄여 testdata/fuzz/FuzzParseData 아래 파일로 쓴다. 코드를 고친 뒤 그 파일은 코퍼스의 한 원소가 되어 go test 때마다 도는 회귀 테스트가 된다.",
      lead="윗줄은 퍼징 한 바퀴, 아랫줄은 실패를 고치고 회귀 테스트로 남기는 길입니다.")

node(X[0], Y1, "시드 코퍼스", "f.Add · testdata/fuzz", INFO)
node(X[1], Y1, "입력 비틀기", "퍼저가 mutate")
node(X[2], Y1, "f.Fuzz 대상", "패닉 · 왕복 확인")
node(X[3], Y1, "실패했나", "t.Error · panic", WARN)
for i in range(3):
    d.arrow([(X[i] + NW + 2, Y1 + NH / 2), (X[i + 1] - 4, Y1 + NH / 2)], SOFT, "soft", 1.3)

# 아니오: 판단 → 비틀기로 돌아가는 고리
nx1 = X[3] + 40
d.arrow([(nx1, Y1 + NH + 2), (nx1, 228), (X[1] + NW / 2, 228), (X[1] + NW / 2, Y1 + NH + 4)], SOFT, "soft", 1.2)
d.t((nx1 + X[1] + NW / 2) / 2, 220, "아니오 · 계속 비틂", 11, MUTED, KR, "middle", 600)

# 예: 판단 → 줄이기
yx = X[3] + 150
d.arrow([(yx, Y1 + NH + 2), (yx, Y2 - 4)], BAD, "bad", 1.3)
d.t(yx + 10, 272, "예", 12, BAD, KR, "start", 600)

node(X[3], Y2, "입력 줄이기", "minimizing")
node(X[2], Y2, "실패 파일", "…/FuzzParseData/03f81b40…", ACC)
node(X[1], Y2, "코드 고침", "count 상한 · TrimSpace", OK)
for i in (3, 2):
    d.arrow([(X[i] - 2, Y2 + NH / 2), (X[i - 1] + NW + 4, Y2 + NH / 2)], SOFT, "soft", 1.3)

# 고침 → 코퍼스로 귀환
cx0 = X[0] + NW / 2
d.arrow([(X[1] - 2, Y2 + NH / 2), (cx0, Y2 + NH / 2), (cx0, Y1 + NH + 4)], OK, "ok", 1.3)
d.t(cx0 + 10, 264, "회귀 테스트로 남음", 11, OK, KR, "start", 600)

d.legend(432, [("코퍼스", INFO), ("판단", WARN), ("남는 실패 입력", ACC), ("고친 코드", OK)])
d.save("15-03.fuzz-loop.svg")
print("ok 15-03 fuzz-loop")

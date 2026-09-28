# 15-04.httptest-flow — 테스트 사례가 공유 변수 io 를 바꾸고 Resolve 를 부르면, httptest 서버가 io 를 읽어 그 사례의 답을 돌려준다
# 본문 요구(15-04 §2 「가짜 서버와 테스트가 변수 하나를 나눠 씁니다」): 사례마다 io = d.io, rs.Resolve 가 server.URL 로 GET,
#           가짜 서버의 핸들러가 io.expression 과 비교해 같으면 io.code · io.body 를 쓴다. Resolve 는 본문을 float64 로 바꿔 돌려주고
#           사례가 d.result · d.errMsg 와 비교한다. io 는 두 클로저가 붙잡은 한 변수다.
# 타입 스펙: type-sequence — 레인 넷(공유 변수 io · 테스트 사례 · RemoteSolver · httptest 서버), 시간은 위→아래.
#           서버가 io 를 읽는 긴 화살표가 focal(coral) 하나.
# 사실 출처: Learning Go 2판 15장 「Using httptest」, 원서 저장소 solver/remote_solver_test.go, go1.27.1 실행(2026-09-28) — 세 사례 PASS.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import Seq, PAPER, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 960, 580
d = Seq(W, H, "SEQUENCE · 15-04 §2",
        "테스트 사례가 공유 변수를 바꾸면 가짜 서버가 그 값으로 답합니다",
        "사례 하나의 흐름. 테스트는 io = d.io 로 공유 변수를 바꾸고 rs.Resolve 를 부른다. RemoteSolver 는 server.URL 로 GET 요청을 보내고, "
        "httptest 서버의 핸들러는 공유 변수 io 의 expression 과 쿼리를 비교해 같으면 io.code 와 io.body 를 쓴다. "
        "Resolve 가 본문을 float64 로 바꿔 돌려주면 사례가 기대값과 비교한다. io 는 서버 클로저와 사례 클로저가 함께 붙잡은 한 변수다.",
        lead="위에서 아래로 시간이 흐릅니다. 사례마다 이 흐름이 되풀이됩니다.")
d.lanes([("공유 변수 io", "var io info"), ("테스트 사례", "t.Run(d.name)"), ("RemoteSolver", "rs.Resolve"), ("httptest 서버", "server.URL")], y0=96, lane_w=180)
d.rails(500)


def state(key, txt, y, c):
    # Seq.state 는 반투명 칩이라 레일이 비치고 한글 폭을 작게 어림한다 — 불투명 바탕과 글자별 폭으로 다시 그린다
    x = d.LX[key]
    w = sum(11.0 if "가" <= ch <= "힣" else 6.9 for ch in txt) + 24
    d.o.append(f'<rect x="{x - w / 2}" y="{y - 12}" width="{w}" height="24" rx="4" fill="{PAPER}"/>')
    d.o.append(f'<rect x="{x - w / 2}" y="{y - 12}" width="{w}" height="24" rx="4" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
    d.t(x, y + 4, txt, 11, c, MONO, "middle", 600)


d.msg("테스트 사례", "공유 변수 io", "io = d.io", 188)
d.msg("테스트 사례", "RemoteSolver", "Resolve(ctx, expr)", 228)
d.msg("RemoteSolver", "httptest 서버", "GET ?expression=", 268)
d.msg("httptest 서버", "공유 변수 io", "io 를 읽음", 312, ACC, "acc", dash="5 4")
state("httptest 서버", "같으면 io.code · io.body", 352, INFO)
d.msg("httptest 서버", "RemoteSolver", "200 · \"22\"", 392, OK, "ok")
d.msg("RemoteSolver", "테스트 사례", "22, nil", 432, OK, "ok")
state("테스트 사례", "d.result · d.errMsg 와 비교", 472, INFO)

d.legend(524, [("서버가 공유 변수를 읽음", ACC), ("응답과 결과", OK), ("상태", INFO)])
d.save("15-04.httptest-flow.svg")
print("ok 15-04 httptest-flow")

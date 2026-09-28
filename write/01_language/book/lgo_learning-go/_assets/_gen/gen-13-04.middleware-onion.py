# 13-04.middleware-onion — terribleSecurity(RequestTimer(handler)): 바깥부터 요청을 받고, 막히면 안쪽은 불리지 않는다
# 본문 요구(13-04 §3 「감싼 순서대로 실행됩니다」): terribleSecurity 클로저가 먼저 불리고, 그다음 RequestTimer, 마지막에 실제 핸들러.
#           비밀번호가 틀리면 바깥에서 401 을 쓰고 돌아가 안쪽은 불리지 않는다. RequestTimer 는 핸들러가 돌아온 뒤 slog 로 시간을 남긴다.
# 타입 스펙: type-nested — 바깥에서 안쪽으로 terribleSecurity ⊃ RequestTimer ⊃ handler. 한 겹당 안쪽 여백 28.
#           왼쪽에서 들어오는 요청 화살표 하나와 바깥 겹 아래쪽에서 되돌아 나가는 401 화살표 하나, 둘은 교차하지 않는다. focal 은 401 경로.
# 사실 출처: Learning Go 2판 13장 「Middleware」, 원서 예제 저장소 ch13 sample_code/middleware 를 포트 18181 로 go1.25.1 에서 실행 —
#           비밀번호 없이 401, GOPHER 로 200 과 request time 로그, 401 요청에는 시간 로그 없음(2026-09-28).
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 960, 540
d = D(W, H, "NESTED · 13-04 §3",
      "바깥 미들웨어부터 요청을 받고, 핸들러가 돌아오면 안쪽부터 정리합니다",
      "terribleSecurity(RequestTimer(handler)) 로 감싼 겹. 요청은 바깥의 terribleSecurity 가 먼저 받아 X-Secret-Password 헤더를 검사하고, "
      "틀리면 401 과 메시지를 쓰고 돌아가 안쪽은 불리지 않는다. 맞으면 RequestTimer 가 시작 시각을 적고 handler 를 부르며, "
      "handler 가 Hello! 를 쓰고 돌아오면 RequestTimer 가 slog 로 경로와 걸린 시간을 남긴다.",
      lead="바깥 겹이 먼저 받고, 안쪽 겹이 먼저 끝납니다.")


def layer(x, y, w, h, title, sub, c):
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{c}0d" stroke="{c}" stroke-width="1.2"/>')
    d.t(x + 20, y + 28, title, 13, c, MONO, "start", 600)
    d.t(x + 20, y + 48, sub, 11, MUTED, KR, "start")


layer(200, 100, 736, 360, "terribleSecurity", "X-Secret-Password 검사 · 틀리면 401 쓰고 반환", INFO)
layer(228, 170, 680, 262, "RequestTimer", "start := time.Now() · 돌아오면 slog.Info(duration)", INFO)
layer(256, 240, 624, 164, "handler", "", OK)
d.t(568, 322, "w.Write(\"Hello!\\n\")", 14, OK, MONO, "middle", 600)

# 요청 들어옴
d.arrow([(24, 300), (196, 300)], SOFT, "soft", 1.4)
d.t(30, 290, "GET /hello", 12, MUTED, MONO, "start", 600)
# 401 되돌아 나감
d.arrow([(198, 420), (30, 420)], ACC, "acc", 1.6)
d.t(30, 410, "401 · 비밀번호 틀림", 12, ACC, KR, "start", 600)
d.t(568, 348, "200 · Hello!", 12, MUTED, MONO, "middle", 600)

d.legend(480, [("미들웨어 겹", INFO), ("실제 핸들러", OK), ("안쪽을 부르지 않고 반환", ACC)])
d.save("13-04.middleware-onion.svg")
print("ok 13-04 onion")

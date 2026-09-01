# 04-02 §3 — 셸이 뜨는 순서. 저자가 index.js · bootstrap.js · app.js 셋으로 나눈 이유를 시간축에 편다.
# 파일 이름과 각 파일이 하는 일은 원문 그대로다.
# 타입 스펙: type-sequence — 주체 셋 사이의 시간순 메시지. 레인 · 레일 · 메시지 문법 그대로.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, OK, PAPER, RULE, KR, MONO

W, H = 1160, 588
d = Seq(W, H, "BUILDING MICRO-FRONTENDS · 04-02 §3",
        "파일을 셋으로 쪼개야 비동기로 로드된다",
        "진입 파일이 한 줄짜리인 것이 요점이다. 동적 import 로 넘겨야 의존성이 앞에서 한꺼번에 내려오지 않는다.",
        "왼쪽에서 오른쪽으로 갈수록 나중에 평가되는 파일입니다")

d.lanes([("index.js", "entry"),
         ("bootstrap.js", "mount"),
         ("App.js", "routes")], y0=104, lane_w=280)
d.rails(496)
d.msg("index.js", "bootstrap.js", 'import("./bootstrap")', 210, ACC, "acc",
      sub="단 한 줄 · 여기서 비동기 경계가 생긴다")
d.selfmsg("bootstrap.js", "createRoot(#root)", 276, MUTED, sub="setupFetch 도 여기서 걸린다")
d.msg("bootstrap.js", "App.js", "render(<App/>)", 344, MUTED, sub="StrictMode 로 감싸 그린다")
d.selfmsg("App.js", "initializeMFEs()", 408, ACC, sub="리모트를 등록한다")
d.state("App.js", "routes ready", 464, OK)
d.legend(520, [("비동기 경계가 생기는 자리", ACC), ("그 파일이 스스로 하는 일", MUTED)])
d.save("04-02.boot-sequence.svg")
print("h 필요:", 520 + 40, " 실제:", H)

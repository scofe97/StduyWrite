# 타입 스펙: type-architecture — 클라이언트 · 처리율 제한 미들웨어 · API 서버를 존으로 세우고, 요청 3건 중 2건은 통과하고 1건은 429 로 돌아가는 번호 붙은 화살표를 건다.
# 사실 출처: 추출본 v2.txt 926~930행(초당 2건 허용 · 클라이언트가 1초에 3건 · 처음 둘은 API 서버로 · 셋째는 429), 910~912행(클라이언트는 위조 가능).
#   RFC 6585 §4 (429 Too Many Requests).
# Layout conventions: 존 셋(클라이언트 x=24 · 제한기 막대 x=432 · API 서버 x=704), 요청 화살표 y=200·244·288 stride 44, 반환 화살표 y=316. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, MUTED, INK, PAPER, PAPER2, RULE, SOFT, INFO, KR, MONO

W, H = 960, 488
d = D(W, H, "SYSTEM DESIGN INTERVIEW · 04-01 §2",
      "제한기가 막은 요청은 429 로 돌아간다",
      "클라이언트가 1초 안에 요청 3건을 보내면 처리율 제한 미들웨어가 초당 2건까지만 API 서버로 넘기고 셋째 요청은 429 로 돌려보낸다.",
      "한도는 초당 2건")

# 클라이언트
d.box(24, 112, 208, 216, PAPER2, RULE, 1.0, 8)
d.t(128, 144, "클라이언트", 14, INK, KR, "middle", 600)
d.t(128, 168, "1초 안에 요청 3건", 13, MUTED, KR)

# 제한기 막대
d.tone(432, 104, 56, 232, ACC, 6, "14", 1.4)
d.t(460, 380, "처리율 제한 미들웨어", 14, ACC, KR, "middle", 600)
d.t(460, 404, "한도 초당 2건", 13, MUTED, KR)

# API 서버
d.box(704, 112, 232, 216, PAPER2, RULE, 1.0, 8)
d.t(820, 144, "API 서버", 14, INK, KR, "middle", 600)
d.t(820, 168, "2건 도착", 13, MUTED, KR)

# 요청 1·2 통과, 요청 3 차단
for k, y in enumerate((200, 244)):
    d.t(332, y - 8, f"요청 {k + 1}", 13, MUTED, KR)
    d.arrow([(236, y), (428, y)], MUTED, "ar", 1.5)
    d.arrow([(492, y), (700, y)], OK, "ok", 1.6)
    d.t(596, y - 8, "통과", 13, OK, KR)

d.t(332, 280, "요청 3", 13, MUTED, KR)
d.arrow([(236, 288), (428, 288)], MUTED, "ar", 1.5)
d.t(460, 292, "✕", 16, BAD, MONO, "middle", 600)

# 429 반환
d.arrow([(428, 316), (236, 316)], BAD, "bad", 1.5, "5 4")
d.chip(334, 340, "429 Too Many Requests", BAD, 12)

d.legend(H - 56, [("통과", OK), ("차단", BAD), ("제한기", ACC)])
d.save("04-01.limiter-position.svg")

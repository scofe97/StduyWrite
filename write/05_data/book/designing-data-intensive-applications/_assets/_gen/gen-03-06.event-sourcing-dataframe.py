# 03-06 §1 — 커맨드가 검증을 거쳐 이벤트 로그에 쌓이고, 로그에서 구체화 뷰 셋이 파생되는 이벤트 소싱·CQRS 흐름.
# 옛 도식의 DataFrame 부분은 뺐다. 본문 §3 이 맡는다. 뷰 이름은 본문 컨퍼런스 예의 셋만 쓴다.
# 타입 스펙: type-data-flow
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, BAD, KR, MONO

W = 880
PY, PH = 100, 252
LEG = PY + PH + 32
H = LEG + 56

d = D(W, H, "03-06 · EVENT SOURCING", "이벤트 소싱과 CQRS",
      "커맨드를 검증해 유효하면 이벤트 로그에 추가하고, 구체화 뷰 셋이 그 로그에서 파생된다.",
      "쓰기 표현과 읽기 표현의 분리")

d.box(16, PY, 520, PH, PAPER, RULE, 0.9)
d.box(560, PY, 304, PH, PAPER, RULE, 0.9)
d.t(32, 124, "쓰기 최적화 표현", 14, INK, KR, "start", 600)
d.t(576, 124, "읽기 최적화 표현", 14, INK, KR, "start", 600)

d.box(32, 196, 112, 44, PAPER2, INFO, 1.2); d.t(88, 223, "커맨드", 13, INK, KR)
d.box(176, 196, 112, 44, PAPER2, INFO, 1.2); d.t(232, 223, "검증", 13, INK, KR)
d.box(352, 180, 160, 76, PAPER2, ACC, 1.6)
d.t(432, 212, "이벤트 로그", 14, INK, KR, "middle", 600)
d.t(432, 236, "이벤트 추가", 12, MUTED, KR)
d.arrow([(148, 218), (172, 218)], MUTED, "ar", 1.4)
d.arrow([(292, 218), (348, 218)], OK, "ok", 1.6)
d.chip(320, 198, "유효", OK, 11)
d.arrow([(232, 244), (232, 272)], WARN, "warn", 1.4)
d.chip(232, 290, "거부", WARN, 11)

for y, name in [(140, "예약 상태 뷰"), (196, "대시보드 차트 뷰"), (252, "배지 인쇄 파일 뷰")]:
    d.box(576, y, 272, 44, PAPER2, INFO, 1.2)
    d.t(712, y + 27, name, 13, INK, KR)
    d.arrow([(548, y + 22), (572, y + 22)] if y == 196 else [(512, 218), (548, 218), (548, y + 22), (572, y + 22)], MUTED, "ar", 1.4)
d.arrow([(512, 218), (572, 218)], MUTED, "ar", 1.4)

d.legend(LEG, [("이벤트 로그", ACC), ("커맨드 · 뷰", INFO), ("유효", OK), ("거부", WARN)])
d.save("03-06.event-sourcing-dataframe.svg")

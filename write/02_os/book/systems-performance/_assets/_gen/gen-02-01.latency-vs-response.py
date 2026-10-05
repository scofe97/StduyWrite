# 02-01 §3 — 웹 페이지 로드에서 '지연'과 '응답 시간'이 덮는 구간.
# 타입 스펙: type-gantt — 같은 시간축 위에서 막대 길이가 곧 구간이다.
#           축약: 원서(그림 2.3, p.4)에 값이 없으므로 시간축 눈금 없이 상대 길이만 쓴다.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import ACC, MUTED, SOFT, INK, INFO, OK, PAPER2, RULE, KR, MONO

W, H = 928, 556
LX, TX, TW = 24, 236, 656          # 라벨 열 · 시간축 시작 · 시간축 폭
Y0, ROW, BAR = 120, 44, 24
U = TW / 100                        # 상대 단위 100 = 시간축 전체

d = DK(W, H, "SYSTEMS PERFORMANCE · 02-01 §3",
       "같은 '지연'이 덮는 구간이 다르다",
       "웹 페이지 로드를 네 단계로 나누고, 지연과 응답 시간이라는 이름이 각각 어느 구간을 덮는지 같은 시간축에 겹쳐 보인다.",
       "막대 길이는 상대 모양 — 원서 그림에 값이 없습니다")

PHASES = [("DNS 조회", 0, 18), ("TCP 핸드셰이크", 18, 34), ("데이터 전송", 34, 76), ("브라우저 렌더", 76, 100)]
SPANS = [("TCP 연결 지연", 18, 34, INFO, "핸드셰이크만"),
         ("HTTP GET 응답 시간", 18, 76, OK, "연결 지연 + 전송"),
         ("페이지 로드 지연", 0, 100, ACC, "클릭 → 완료")]

d.t(LX, Y0 - 20, "단계", 12, SOFT, KR, "start")
for i, (name, a, b) in enumerate(PHASES):
    y = Y0 + i * ROW
    d.t(LX, y + 17, name, 13, INK, KR, "start", 600)
    d.box(TX + a * U, y, (b - a) * U, BAR, PAPER2, MUTED, 1.0, 4)

ys = Y0 + len(PHASES) * ROW + 28
d.line(TX, ys - 14, TX + TW, ys - 14, RULE, 0.8)
d.t(LX, ys + 4, "이름이 덮는 구간", 12, SOFT, KR, "start")
for i, (name, a, b, c, sub) in enumerate(SPANS):
    y = ys + 16 + i * ROW
    d.t(LX, y + 17, name, 13, c, KR, "start", 600)
    d.tone(TX + a * U, y, (b - a) * U, BAR, c, 4)
    d.t(TX + a * U + 10, y + 17, sub, 12, INK, KR, "start")

ya = ys + 16 + len(SPANS) * ROW + 4
d.arrow([(TX, ya), (TX + TW, ya)], SOFT, "soft", 1.2)
d.t(TX + TW, ya + 20, "시간", 12, SOFT, KR, "end")

d.legend(ya + 32, [("단계", MUTED), ("지연이라 부르는 구간", INFO), ("응답 시간", OK)])
d.save("02-01.latency-vs-response.svg")

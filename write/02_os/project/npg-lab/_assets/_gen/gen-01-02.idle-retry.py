# 01-02-idle-retry — I2 유휴 연결 경합을 t0 기준 ms 가로 시간축 한 줄로 보이고, 그 아래 GET·POST 두 갈래를 둔다
# 본문 요구(01-02): 백엔드 close 와 FIN 도착 사이 틈에 보낸 요청이 EOF 를 만나고, GET 만 새 연결로 다시 간다.
# 타입 스펙: type-timeline
# 사실 출처: ch08-server-idle-close-post-502.md:44-52(경합의 시간 축)·26(9건 idle 807~973ms)·112(ADR 0012 재확인, 1s 장면 불변)·116-117(UC 10/248 attempts=1, GET attempts=2 13/261),
#            0012-upstream-deadlines-and-pool.md 결정 3(프록시 빈 연결 4s, 흔한 5s 백엔드 전제)
import sys
from pathlib import Path

ASSETS_DIR = Path(__file__).resolve().parent.parent
GEN_DIR = Path(__file__).resolve().parent
if str(ASSETS_DIR) not in sys.path:
    sys.path.insert(0, str(ASSETS_DIR))
if str(GEN_DIR) not in sys.path:
    sys.path.insert(0, str(GEN_DIR))

from dd import D, INK, MUTED, SOFT, RULE, PAPER, PAPER2, ACC, WARN, INFO, OK, BAD, KR, MONO

W = 960
H = 656

# 시간축: t0(백엔드가 응답을 보낸 시각) 기준 ms. 1ms = 0.64px, 0~1200ms 를 x 96~864 에 놓는다.
X0 = 96
PX_PER_MS = 0.64
BASE_Y = 232


def X(ms):
    return round(X0 + ms * PX_PER_MS, 1)


# 기록의 값만 쓴다. 보낸 시각 = t0 + 100(응답이 프록시에 닿음) + idle x
T_RECV = 100
T_CLOSE = 1000
T_FIN = 1100
RACE = (100 + 800, 100 + 1000)      # idle x 800~1000ms
SEEN = (100 + 807, 100 + 973)       # 관찰 9건 idle 807~973ms

d = D(
    W,
    H,
    "TIMELINE · CH08 I2 RACE WINDOW · ms FROM t0",
    "유휴 연결 경합의 시간축과 재시도 분기",
    "백엔드가 응답을 보낸 시각 t0 기준으로 close 와 FIN 도착 사이 틈에 보낸 요청이 EOF 를 만나고, GET 은 새 연결로 다시 가며 POST 는 502 로 끝나는 시간축",
    lead="백엔드가 t0+1000 에 닫고 FIN 이 t0+1100 에 닿는 틈에 보낸 요청은 EOF 를 만나고, GET 만 새 연결로 다시 갑니다.",
)

# 1. 풀에서 쉬는 구간 (t0+100 부터 경합 구간 시작까지)
d.tone(X(T_RECV), 176, X(RACE[0]) - X(T_RECV), 12, INFO, r=3, op="22", sw=1.0)
d.t((X(T_RECV) + X(RACE[0])) / 2, 166, "풀에서 쉼 · idle x", 13, INFO, KR, "middle", 500)

# 2. 경합 구간 (focal) 과 관찰 9건
d.tone(X(RACE[0]), 196, X(RACE[1]) - X(RACE[0]), 44, ACC, r=4, op="20", sw=1.4)
d.tone(X(SEEN[0]), 206, X(SEEN[1]) - X(SEEN[0]), 12, BAD, r=2, op="55", sw=1.0)

# 3. 기준선과 눈금 (200ms 마다). 1000 은 close 사건 라벨이 대신한다.
d.line(72, BASE_Y, 888, BASE_Y, RULE, 1.0)
for ms in range(0, 1201, 200):
    d.line(X(ms), BASE_Y - 4, X(ms), BASE_Y + 4, SOFT, 0.8)
    if ms == 1000:
        continue
    label = "1200 ms" if ms == 1200 else str(ms)
    d.t(X(ms), BASE_Y + 22, label, 13, SOFT, MONO, "middle")

# 4. 사건 — 위: t0·close·FIN, 아래: 프록시가 응답을 받은 t0+100
def event(ms, c, r=4):
    d.o.append(f'<circle cx="{X(ms)}" cy="{BASE_Y}" r="{r}" fill="{c}"/>')

event(0, MUTED)
d.line(X(0), 138, X(0), BASE_Y - 4, RULE, 1.0)
d.t(X(0) - 8, 112, "t0", 14, INK, MONO, "start", 600)
d.t(X(0) - 8, 130, "백엔드 응답 보냄", 13, MUTED, KR, "start")

event(T_RECV, INFO)
d.line(X(T_RECV), BASE_Y + 4, X(T_RECV), 258, RULE, 1.0)
d.t(X(T_RECV) - 8, 274, "t0+100 · 프록시 응답 받음", 14, INFO, KR, "start", 600)
d.t(X(T_RECV) - 8, 292, "연결을 풀에 둠", 13, MUTED, KR, "start")

event(T_CLOSE, WARN)
d.line(X(T_CLOSE), 138, X(T_CLOSE), 196, WARN, 1.0, dash="3 3")
d.t(X(T_CLOSE) - 8, 112, "t0+1000", 14, WARN, MONO, "end", 600)
d.t(X(T_CLOSE) - 8, 130, "백엔드 close() · idle_close 1s", 13, WARN, KR, "end")

event(T_FIN, WARN)
d.line(X(T_FIN), 138, X(T_FIN), 196, WARN, 1.0, dash="3 3")
d.t(X(T_FIN) + 8, 112, "t0+1100", 14, WARN, MONO, "start", 600)
d.t(X(T_FIN) + 8, 130, "FIN 프록시 도착", 13, WARN, KR, "start")

# 5. 경합 구간 라벨 (구간 바로 아래)
mid = (X(RACE[0]) + X(RACE[1])) / 2
d.t(mid, 274, "경합 구간", 14, ACC, KR, "middle", 600)
d.t(mid, 292, "idle x 800~1000ms", 13, ACC, MONO, "middle")
d.t(mid, 310, "관찰 9건 idle 807~973ms", 13, BAD, KR, "middle", 600)

# 6. 경합에 걸린 요청 → EOF (UC)
d.arrow([(mid, 318), (mid, 344), (676, 344)], c=BAD, m="bad", sw=1.4)
d.tone(288, 328, 384, 32, BAD, r=4, op="18", sw=1.2)
d.t(480, 349, "응답 대신 EOF (UC)", 14, BAD, KR, "middle", 600)

# 7. 두 갈래 — GET 은 새 연결 재시도, POST 는 502
d.arrow([(400, 360), (400, 380), (276, 380), (276, 400)], c=INFO, m="info", sw=1.4)
d.arrow([(560, 360), (560, 380), (684, 380), (684, 400)], c=BAD, m="bad", sw=1.4)

d.tone(96, 404, 360, 76, INFO, r=6, op="14", sw=1.2)
d.t(276, 426, "GET · HEAD · OPTIONS · TRACE", 13, MUTED, MONO, "middle")
d.t(276, 448, "새 연결로 다시 보냄 → 200", 14, INFO, KR, "middle", 600)
d.t(276, 468, "attempts=2 13/261 · 502 0", 13, MUTED, MONO, "middle")

d.tone(504, 404, 360, 76, BAD, r=6, op="14", sw=1.2)
d.t(684, 426, "POST (본문 있음)", 13, MUTED, KR, "middle")
d.t(684, 448, "재시도 없음 → 손님에게 502 (UC)", 14, BAD, KR, "middle", 600)
d.t(684, 468, "attempts=1 · UC 10/248", 13, MUTED, MONO, "middle")

# 8. 유휴 기한 비교 띠 — I2 장면과 ADR 0012 결정
d.box(48, 500, 864, 88, fill=PAPER2, stroke=RULE, sw=0.9, r=6)
d.t(72, 524, "I2 장면", 14, WARN, KR, "start", 600)
d.t(72, 546, "프록시 90s > 백엔드 idle_close 1s", 13, INK, MONO, "start")
d.t(72, 568, "프록시가 더 길어 경합", 13, BAD, KR, "start")
d.line(464, 512, 464, 576, RULE, 0.8)
d.t(488, 524, "ADR 0012 결정 (흔한 5s 백엔드 전제)", 14, OK, KR, "start", 600)
d.t(488, 546, "프록시 4s < 백엔드 5s", 13, INK, KR, "start")
d.t(488, 568, "1s 백엔드 장면에서는 바뀌지 않음", 13, MUTED, KR, "start")

# 9. 범례
d.legend(604, [
    ("풀에서 쉼", INFO),
    ("경합 구간", ACC),
    ("관찰 9건", BAD),
    ("close · FIN", WARN),
])

out_path = ASSETS_DIR / "01-02-idle-retry.svg"
d.save(str(out_path))
print(f"saved: {out_path}")

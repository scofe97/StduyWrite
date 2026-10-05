# 03-02 §6 — 커널이 시스템 콜을 처리하는 도중 고우선 스레드가 깨어날 때, 세 Kconfig 설정에서 기다리는 시간.
# 타입 스펙: type-gantt — 막대 길이가 곧 구간(커널 실행 · 고우선 스레드 대기 · 고우선 스레드 실행)이다.
#           축약: 원서는 수치를 주지 않으므로 시간축은 상대 단위다(1 단위 = 48px). 정지점 위치도 설명용 가상 값이다.
#           focal 은 가장 긴 대기(NONE).
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import ACC, MUTED, SOFT, INK, INFO, OK, WARN, BAD, PAPER, PAPER2, RULE, KR, MONO

W, H = 960, 540
X0, U = 288, 48           # 0 단위 x, 1 단위 px
Y0, ST, BH = 168, 96, 28
WAKE, STOPS, END = 2, (5, 8), 10

def X(t): return X0 + t * U

d = DK(W, H, "SYSTEMS PERFORMANCE · 03-02 §6",
       "세 선점 설정에서 고우선 스레드가 기다리는 시간",
       "커널이 시스템 콜을 처리하는 도중(회색) 고우선 스레드가 깨어난다(세로선). NONE 은 커널이 유저 모드로 돌아갈 때까지, VOLUNTARY 는 다음 논리적 정지점까지 기다리고, PREEMPT 는 임계 구역 밖이면 곧바로 CPU 를 얻는다. 시간축은 상대값이다.",
       "기다림이 짧을수록 지연이 줄고, NONE 은 그 대신 처리량을 얻습니다")

ROWS = [("CONFIG_PREEMPT_NONE", "선점 비활성", END, ACC),
        ("CONFIG_PREEMPT_VOLUNTARY", "논리적 정지점에서", STOPS[0], WARN),
        ("CONFIG_PREEMPT", "임계 구역 밖 어디서든", WAKE + 0.25, OK)]
for r, (name, sub, run_at, c) in enumerate(ROWS):
    y = Y0 + r * ST
    d.t(X0 - 20, y + 12, name, 13, INK, MONO, "end", 600)
    d.t(X0 - 20, y + 30, sub, 12, MUTED, KR, "end")
    # 커널 실행: 0 → run_at
    d.box(X(0), y, X(run_at) - X(0), BH, PAPER2, RULE, 1.0, 4)
    d.t(X(0) + 12, y + 19, "커널 · syscall", 12, MUTED, KR, "start")
    # 대기: WAKE → run_at (위쪽 얇은 막대)
    if run_at - WAKE >= 0.5:
        d.tone(X(WAKE), y + BH + 6, X(run_at) - X(WAKE), 12, c, 3)
        d.t((X(WAKE) + X(run_at)) / 2, y + BH + 34, "대기", 12, c, KR, "middle", 600)
    else:
        d.tone(X(WAKE), y + BH + 6, X(run_at) - X(WAKE), 12, c, 3)
        d.t(X(run_at) + 8, y + BH + 17, "대기 거의 없음 · 곧바로", 12, c, KR, "start", 600)
    # 고우선 스레드 실행
    d.tone(X(run_at), y, 2 * U, BH, INFO, 4)
    d.t(X(run_at) + 12, y + 19, "고우선 실행", 12, INFO, KR, "start", 600)
    if r == 1:
        for s in STOPS:
            d.line(X(s), y - 6, X(s), y + BH + 2, WARN, 1.2)
        d.t(X(STOPS[0]), y - 12, "정지점", 12, WARN, KR, "middle")

# 깨어남 세로선
d.line(X(WAKE), Y0 - 28, X(WAKE), Y0 + 2 * ST + BH + 20, INK, 1.2, "4 4")
d.t(X(WAKE), Y0 - 36, "고우선 스레드 깨어남", 13, INK, KR, "middle", 600)

# 상대 시간축
AY = Y0 + 3 * ST - 8
d.line(X(0), AY, X(12), AY, MUTED, 1.0)
for t in range(0, 13, 2):
    d.line(X(t), AY - 4, X(t), AY + 4, MUTED, 1.0)
    d.t(X(t), AY + 20, str(t), 12, SOFT, MONO)
d.t(X(12) + 8, AY + 5, "상대 시간", 12, SOFT, KR, "start")

d.legend(AY + 40, [("가장 긴 대기", ACC), ("정지점까지 대기", WARN), ("곧바로 선점", OK), ("고우선 스레드 실행", INFO)])
d.save("03-02.preemption-models.svg")

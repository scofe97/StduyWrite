# 21-01 「락을 가진 스레드가 unlock 하기 전까지 다른 스레드의 lock 호출은 돌아오지 않는다」 — 두 스레드의 락 보유와 대기 구간을 시점 순서로 놓는다.
# 본문 근거: 이 노트 「3. 락과 오류 코드 확인」의 「lock 과 unlock 의 동작」.
# 값 근거: 시점 t1~t5 는 순서만 뜻하고 시간 단위가 아니다. 실측값이 아니다.
# 공식 근거: OSTEP 27장 §27.3 — 다른 스레드가 락을 쥐고 있으면 lock 을 부른 스레드는 락을 얻을 때까지 호출에서 돌아오지 않고, 락을 가진 스레드만 unlock 을 부른다.
# 타입 스펙: type-gantt — 막대 길이가 곧 구간. 행 둘(스레드 A·B), 시점 다섯. 대기 구간(WARN)이 A 의 unlock 시점에서 끝나는 것이 논지다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INK, MUTED, SOFT, RULE, PAPER, PAPER2, OK, INFO, WARN, KR, MONO

W, H = 880, 388
d = D(W, H, "OSTEP · 21-01 §3",
      "B 의 lock 호출은 A 가 unlock 할 때까지 돌아오지 않는다",
      "스레드 A 는 t1 에 락을 얻고 t3 에 unlock 한다. 스레드 B 는 t2 에 lock 을 불러 t3 까지 호출 안에서 기다리고, t3 에 락을 얻어 t5 까지 임계 구역을 지난다. "
      "두 스레드가 락을 쥔 구간은 겹치지 않는다.")

AX0, PITCH = 200, 132
d.t(24, 112, "시점 — 순서만 뜻함", 12, MUTED, KR, "start")
for i in range(5):
    d.t(AX0 + i * PITCH, 112, f"t{i+1}", 12, MUTED, MONO, "middle", 600)
d.line(24, 124, W - 24, 124, RULE, 0.8)

rows = [("스레드 A", 140), ("스레드 B", 204)]
for name, y in rows:
    d.t(24, y + 26, name, 13, INK, KR, "start", 600)
    d.line(24, y + 52, W - 24, y + 52, RULE, 0.4)


def bar(t0, t1, y, c, text, mono=False):
    x = AX0 + t0 * PITCH
    w = (t1 - t0) * PITCH
    d.tone(x, y + 8, w, 36, c)
    d.t(x + w / 2, y + 31, text, 12, INK, MONO if mono else KR, "middle")


bar(0, 2, 140, OK, "락 얻음 · x = x + 1")
bar(2, 4, 140, MUTED, "락 없이 실행")
bar(1, 2, 204, WARN, "lock 안에서 대기")
bar(2, 4, 204, OK, "락 얻음 · 임계 구역")

# A 의 unlock 시점(t3)을 세로 점선으로 잇는다
ux = AX0 + 2 * PITCH
d.line(ux, 132, ux, 268, ACC, 1.4, "4 4")
d.chip(ux, 292, "t3 A 의 unlock → B 의 lock 반환", ACC, 12, 8)

d.legend(H - 56, [("락 보유", OK), ("lock 호출 안에서 대기", WARN), ("락 없이 실행", MUTED)])
d.save("21-01.lock-contention.svg")
print("ok 21-01 lock-contention")

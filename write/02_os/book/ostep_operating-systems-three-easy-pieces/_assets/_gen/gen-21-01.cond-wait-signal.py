# 21-01 「wait 는 락을 놓고 잠들고, 깨어난 뒤 락을 다시 잡고 돌아온다」 — 대기 스레드·공유 상태·신호 스레드가 락과 ready 를 주고받는 순서.
# 본문 근거: 이 노트 「4. 조건 변수로 신호 보내기」의 「wait 가 락을 놓고 다시 잡는 순서」.
# 값 근거: 개념 도식이라 값은 없다. ready 의 0 과 1, 락 보유자 표기는 OSTEP 27장 §27.4 코드를 따라간 것이다. 실행한 출력이 아니다.
# 공식 근거: OSTEP 27장 §27.4 — wait 는 호출한 스레드를 재우면서 락을 놓고, 깨어나 돌아오기 전에 락을 다시 얻는다. 신호 쪽은 ready 를 바꿀 때와 signal 을 부를 때 락을 쥔다.
# 타입 스펙: type-sequence — 참여자 셋의 시간순 메시지. 공유 상태 레인 옆 칩이 락 보유자를 따라간다.
#
# 메시지 라벨(msg·selfmsg)은 dd.py 가 MONO 로 그리므로 ASCII 만 담고, 한글 설명은 sub 에 둔다.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, OK, INFO, WARN, RULE, KR, MONO, PAPER2

W, H = 880, 948
d = Seq(W, H, "OSTEP · 21-01 §4",
        "wait 는 락을 놓고 잠들고 깨어난 뒤 락을 다시 잡는다",
        "대기 스레드가 lock 을 얻고 ready 를 확인한 뒤 cond_wait 로 락을 놓고 잠든다. 신호 스레드가 락을 얻어 ready 를 1 로 바꾸고 cond_signal 을 부른 뒤 unlock 한다. "
        "대기 스레드는 락을 다시 얻고 wait 에서 돌아와 ready 를 다시 확인한다.",
        lead="락 보유자가 바뀌는 순서와 ready 를 확인하는 자리를 따라간다.")

d.lanes([("대기 스레드", "cond_wait 를 부름"),
         ("공유 상태", "lock · cond · ready"),
         ("신호 스레드", "cond_signal 을 부름")], lane_w=200)
d.rails(H - 140)

wx = d.LX["대기 스레드"]
sx = d.LX["공유 상태"]
gx = d.LX["신호 스레드"]


def holder(y, txt, c):
    d.state("공유 상태", txt, y, c)


Y = 212
S = 56
# 1 대기 스레드가 락을 얻는다
d.msg("대기 스레드", "공유 상태", "lock(&lock)", Y, MUTED, sub="락 얻음")
holder(Y + 28, "lock: waiter", INFO)
# 2 ready 확인
d.selfmsg("대기 스레드", "while (ready == 0)", Y + S + 4, MUTED, sub="ready 가 0 이라 기다려야 함")
# 3 cond_wait
y3 = Y + 2 * S + 24
d.msg("대기 스레드", "공유 상태", "cond_wait(&cond, &lock)", y3, WARN, mk="warn", sub="락을 놓고 잠듦")
holder(y3 + 28, "lock: free", MUTED)
d.state("대기 스레드", "sleep", y3 + 28, WARN)
# 4 신호 스레드가 락을 얻는다
y4 = y3 + S + 24
d.msg("신호 스레드", "공유 상태", "lock(&lock)", y4, MUTED, sub="락 얻음")
holder(y4 + 28, "lock: signaler", ACC)
# 5 ready = 1
y5 = y4 + S + 8
d.msg("신호 스레드", "공유 상태", "ready = 1", y5, MUTED, sub="락을 쥔 채 바꿈")
# 6 signal
y6 = y5 + S
d.msg("신호 스레드", "공유 상태", "cond_signal(&cond)", y6, ACC, mk="acc", sub="잠든 스레드를 깨움")
# 7 unlock
y7 = y6 + S
d.msg("신호 스레드", "공유 상태", "unlock(&lock)", y7, MUTED, sub="락 놓음")
holder(y7 + 28, "lock: free", MUTED)
# 8 wait 반환
y8 = y7 + S + 24
d.msg("공유 상태", "대기 스레드", "wait returns", y8, OK, mk="ok", sub="깨어나 락을 다시 얻고 돌아옴")
holder(y8 + 28, "lock: waiter", INFO)
# 9 재확인
d.selfmsg("대기 스레드", "ready != 0, exit loop", y8 + S + 4, MUTED, sub="조건을 다시 확인")
# 10 unlock
y10 = y8 + 2 * S + 24
d.msg("대기 스레드", "공유 상태", "unlock(&lock)", y10, MUTED, sub="락 놓음")
holder(y10 + 28, "lock: free", MUTED)

d.legend(H - 56, [("락 · 일반 호출", MUTED), ("cond_wait", WARN), ("cond_signal", ACC), ("wait 반환", OK)])
d.save("21-01.cond-wait-signal.svg")
print("ok 21-01 cond-wait-signal")

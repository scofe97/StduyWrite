# 02-01 「zombie 는 부모가 wait() 로 회수할 때까지 남는다」 — 자식이 끝나도 항목은 남아 반환값을 보관하고, 부모의 wait() 가 반환값을 가져가면 운영체제가 항목을 정리한다.
# 본문 근거: 이 노트 「5. 프로세스 목록과 zombie」 의 「끝났지만 정리 전인 zombie」.
# 값 근거: 개념 도식이라 값은 없다.
# 공식 근거: OSTEP 4장 §4.5 — 최종 상태(UNIX 에서는 zombie)는 부모가 반환값을 살필 수 있게 하고, 부모가 wait() 같은 호출을 마지막으로 해 자식의 완료를 기다리면서 운영체제가 관련 자료구조를 정리해도 된다고 알린다.
# 타입 스펙: type-sequence — 주체 셋(자식·운영체제·부모) 사이의 시간순 메시지. 참여자 칩은 가로, 레일은 세로.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INK, MUTED, SOFT, RULE, PAPER2, OK, WARN, INFO, KR, MONO

W, H = 920, 520
d = D(W, H, "OSTEP · 02-01 §5",
      "끝난 자식은 부모가 wait() 로 회수할 때까지 zombie 로 남는다",
      "자식이 끝나면 운영체제는 자식의 항목을 zombie 상태로 남겨 반환값을 보관한다. 부모가 wait() 를 부르면 운영체제가 자식의 반환값을 부모에게 건네고, "
      "그 뒤 자식의 항목과 관련 자료구조를 정리한다.")

LX = {"자식": 160, "운영체제": 460, "부모": 760}
for name, x in LX.items():
    d.tone(x - 80, 100, 160, 40, INFO, 6, "14", 1.1)
    d.t(x, 126, name, 13, INK, KR, "middle", 600)
    d.line(x, 140, x, 456, RULE, 1.0, "4 4")


def msg(a, b, y, label, c, m, mono=False):
    xa, xb = LX[a], LX[b]
    d.arrow([(xa + (2 if xb > xa else -2), y), (xb + (-4 if xb > xa else 4), y)], c, m, 1.6)
    d.t((xa + xb) / 2, y - 10, label, 13, c, MONO if mono else KR, "middle", 600)


msg("자식", "운영체제", 176, "종료 + 반환값", MUTED, "ar")
d.tone(380, 204, 160, 52, WARN, 6, "14", 1.2)
d.t(460, 226, "자식 항목: zombie", 13, INK, KR, "middle", 600)
d.t(460, 246, "반환값은 보관 중", 12, MUTED, KR)
msg("부모", "운영체제", 304, "wait()", ACC, "acc", True)
msg("운영체제", "부모", 344, "자식의 반환값", INFO, "info")
d.tone(380, 372, 160, 52, OK, 6, "14", 1.2)
d.t(460, 394, "자식 항목 정리", 13, INK, KR, "middle", 600)
d.t(460, 414, "자료구조를 비움", 12, MUTED, KR)

d.legend(H - 56, [("메시지", MUTED), ("wait() 호출", ACC), ("zombie 상태", WARN), ("정리 완료", OK)])
d.save("02-01.zombie-wait.svg")
print("ok 02-01 zombie-wait")

# 21-01 「스레드는 주소 공간을 함께 쓰고 스택은 따로 갖는다」 — 한 프로세스의 주소 공간 안에서 공유 영역과 스레드별 스택을 나눠 보인다.
# 본문 근거: 이 노트 「5. 컴파일과 사용 지침」의 「스레드마다 따로인 스택」.
# 값 근거: 개념 도식이라 값은 없다. 변수 이름 p·args·arg·rvals 와 {10, 20}·{1, 2} 는 OSTEP 27장 그림 27.1·27.2 의 값이다.
# 공식 근거: OSTEP 27장 §27.6 Aside 「Each thread has its own stack」 — 스레드 함수의 지역 변수는 그 스레드 전용이고, 스레드끼리 나누려면 heap 이나 전역처럼 모두가 닿는 곳에 둔다.
# 타입 스펙: type-nested — 프로세스 주소 공간 ⊃ 공유 영역·스레드별 스택의 포함 관계. 스택에서 스택으로 가는 포인터(코랄)만 focal.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INK, MUTED, SOFT, RULE, PAPER, PAPER2, OK, INFO, KR, MONO

W, H = 880, 524
d = D(W, H, "OSTEP · 21-01 §5",
      "스택은 스레드마다 하나, 나머지는 모두가 함께 쓴다",
      "프로세스의 주소 공간 안에 코드·전역 변수·heap 이 있는 공유 영역과 스레드마다 하나씩인 스택이 들어 있다. "
      "새 스레드의 arg 는 main 의 스택에 있는 args 를 가리키고, rvals 는 공유 영역의 heap 을 가리킨다.")

# 바깥: 주소 공간
d.box(24, 96, 832, 372, PAPER, RULE, 1.0, 8)
d.t(40, 118, "프로세스의 주소 공간 — 모든 스레드가 같은 주소로 읽음", 12, SOFT, KR, "start", 600)

# 왼쪽: 공유 영역
d.tone(44, 136, 380, 312, INFO, 8, "0c")
d.t(60, 158, "공유 영역 — 스레드가 함께 씀", 12, INFO, KR, "start", 600)
d.box(60, 172, 348, 52, PAPER2, RULE, 0.9)
d.t(234, 196, "코드", 12, INK, KR, "middle", 600)
d.t(234, 214, "main · mythread", 11, MUTED, MONO)
d.box(60, 240, 348, 52, PAPER2, RULE, 0.9)
d.t(234, 264, "전역 변수", 12, INK, KR, "middle", 600)
d.t(234, 282, "ready · lock", 11, MUTED, MONO)
d.tone(60, 324, 348, 108, INFO)
d.t(234, 350, "heap", 13, INK, KR, "middle", 600)
d.t(234, 374, "Malloc 으로 받은 myret_t", 12, INK, KR, "middle")
d.t(234, 396, "{ x = 1, y = 2 }", 12, MUTED, MONO)

# 오른쪽: 스레드별 스택
d.tone(444, 136, 392, 312, OK, 8, "0c")
d.t(460, 158, "스레드마다 하나씩 — 스택", 12, OK, KR, "start", 600)
d.tone(460, 172, 360, 88, OK)
d.t(640, 198, "main 스레드의 스택", 13, INK, KR, "middle", 600)
d.t(640, 222, "p · args = { 10, 20 }", 12, INK, MONO)
d.tone(460, 324, 360, 108, OK)
d.t(640, 352, "새 스레드의 스택", 13, INK, KR, "middle", 600)
d.t(640, 376, "arg = &args", 12, INK, MONO)
d.t(640, 398, "rvals", 12, INK, MONO)

# 새 스레드 → main 스택(코랄), 새 스레드 → heap(파랑)
d.arrow([(640, 324), (640, 264)], ACC, "acc", 1.6)
d.chip(640, 292, "&args", ACC, 12, 8)
d.arrow([(460, 404), (412, 404)], INFO, "info", 1.4)

d.legend(H - 56, [("모든 스레드가 공유", INFO), ("스레드마다 하나", OK), ("다른 스택을 가리킴", ACC)])
d.save("21-01.thread-memory.svg")
print("ok 21-01 thread-memory")

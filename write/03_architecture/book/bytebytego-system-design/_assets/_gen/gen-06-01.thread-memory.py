# 타입 스펙: type-nested — 같은 변수 하나에 쓴 값이 스레드(주소 공간 하나)에서는 읽히고 프로세스(주소 공간 둘)에서는 안 읽힌다. 포함 관계(주소 공간 ⊃ 힙·스택)로 공유 범위를 보인다.
# 사실 출처: clone(2) CLONE_VM — "If CLONE_VM is set, the calling process and the child process run in the same memory space ... If CLONE_VM is not set, the child process runs in a separate copy of the memory space ... at the time of the clone call"
#   https://man7.org/linux/man-pages/man2/clone.2.html · pthreads(7) — 스레드는 전역 메모리(데이터·힙)를 공유하고 스택은 스레드마다 따로 https://man7.org/linux/man-pages/man7/pthreads.7.html
#   counter = 0 → 1 은 문서용 예시 값이다(규칙은 위 두 문서).
# Layout conventions: 패널 폭 420·높이 292, 좌우 간격 16, 패널 안 주소 공간 상자 폭 388/188, 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 880, 472
d = D(W, H, "BYTEBYTEGO · 06-01 §1",
      "같은 변수에 쓴 값은 주소 공간이 하나일 때만 보인다",
      "스레드 둘은 힙의 counter 하나를 같이 쓰고 fork 한 프로세스 둘은 복사본을 따로 갖습니다 (값은 문서용 예시)",
      "counter 는 0 에서 시작하고 한쪽이 1 을 씁니다")

PY, PH, PW = 100, 292, 420
LP, RP = 12, 448
for px, head, sub in ((LP, "스레드 둘", "주소 공간 1개 · 스택 2개"), (RP, "프로세스 둘", "주소 공간 2개 · 스택 2개")):
    d.box(px, PY, PW, PH, PAPER2, RULE, 0.9, 6)
    d.t(px + 16, PY + 28, head, 13, INK, KR, "start", 600)
    d.t(px + PW - 16, PY + 28, sub, 12, MUTED, KR, "end")

# 왼쪽: 주소 공간 하나 안에 힙 하나, 스택 둘
ax, ay, aw, ah = LP + 16, PY + 48, 388, 232
d.tone(ax, ay, aw, ah, INFO, 6, "10", 1.0)
d.t(ax + 12, ay + 22, "주소 공간", 12, INFO, KR, "start", 600)
d.tone(ax + 16, ay + 36, aw - 32, 60, ACC, 6, "14", 1.4)
d.t(ax + 28, ay + 60, "힙", 12, MUTED, KR, "start")
d.t(ax + aw / 2, ay + 72, "counter = 1", 13, ACC, MONO, "middle", 600)
for k, (nm, act, c, mk) in enumerate((("스레드 A", "쓰기 counter = 1", WARN, "warn"), ("스레드 B", "읽기 → 1", OK, "ok"))):
    bx = ax + 16 + k * 176
    d.box(bx, ay + 132, 164, 84, PAPER2, RULE, 0.9, 6)
    d.t(bx + 82, ay + 154, nm, 12, INK, KR, "middle", 600)
    d.t(bx + 82, ay + 174, "스택", 12, MUTED, KR)
    d.t(bx + 82, ay + 202, act, 12, c, MONO, "middle", 600)
    # 쓰기는 스레드에서 힙으로, 읽기는 힙에서 스레드로 향한다.
    d.arrow([(bx + 82, ay + 130), (bx + 82, ay + 100)] if mk == "warn" else [(bx + 82, ay + 100), (bx + 82, ay + 130)], c, mk, 1.5)

# 오른쪽: 주소 공간 둘, 각자 힙 하나와 스택 하나
for k, (nm, val, act, c, mk, focal) in enumerate((
        ("부모 주소 공간", "counter = 1", "쓰기 counter = 1", WARN, "warn", False),
        ("자식 주소 공간", "counter = 0", "읽기 → 0", ACC, "acc", True))):
    bx = RP + 16 + k * 200
    d.tone(bx, PY + 48, 188, 232, INFO, 6, "10", 1.0)
    d.t(bx + 12, PY + 70, nm, 12, INFO, KR, "start", 600)
    if focal:
        d.tone(bx + 12, PY + 84, 164, 60, ACC, 6, "14", 1.4)
    else:
        d.box(bx + 12, PY + 84, 164, 60, PAPER2, RULE, 0.9, 6)
    d.t(bx + 24, PY + 108, "힙", 12, MUTED, KR, "start")
    d.t(bx + 94, PY + 128, val, 12, ACC if focal else INK, MONO, "middle", 600)
    d.box(bx + 12, PY + 180, 164, 84, PAPER2, RULE, 0.9, 6)
    d.t(bx + 94, PY + 202, "스택", 12, MUTED, KR)
    d.t(bx + 94, PY + 238, act, 12, c, MONO, "middle", 600)
    d.arrow([(bx + 94, PY + 178), (bx + 94, PY + 148)] if mk == "warn" else [(bx + 94, PY + 148), (bx + 94, PY + 178)], c, mk, 1.5)

d.legend(H - 44, [("쓰기", WARN), ("읽기", OK), ("주소 공간", INFO), ("값이 갈리는 칸", ACC)])
d.save("06-01.thread-memory.svg")

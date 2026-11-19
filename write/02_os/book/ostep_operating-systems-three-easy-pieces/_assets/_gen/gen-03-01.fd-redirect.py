# 03-01 「출력 리다이렉션의 구현」 — 자식의 파일 번호 0·1·2 가 fork 직후부터 exec 뒤까지 네 시점에서 어디를 가리키는지.
# 본문 근거: 이 노트 「4. fork 와 exec 을 나눈 이유」 — 출력 리다이렉션의 구현.
# 값 근거: 개념 도식이라 값은 없다. 파일 번호 0·1·2 는 POSIX unistd.h 의 STDIN_FILENO·STDOUT_FILENO·STDERR_FILENO 값이다.
# 공식 근거: OSTEP 5장 §5.4 — close(STDOUT_FILENO) 뒤 open 이 가장 낮은 빈 번호를 받는다. execve(2) — 기본적으로 파일 디스크립터는 execve 를 지나도 열린 채 남는다. POSIX.1-2024 unistd.h.
# 타입 스펙: type-process — 같은 자식 프로세스의 파일 번호 표가 네 시점에서 바뀌는 상태 전이.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, PAPER2, KR, MONO

W, H = 920, 520
d = D(W, H, "OSTEP · 03-01 §4",
      "표준 출력을 닫고 파일을 열면 1번이 파일을 가리킨다",
      "fork 직후 자식의 파일 번호 0 1 2 는 부모와 같아 0 은 키보드, 1 과 2 는 화면을 가리킨다. "
      "close 로 표준 출력을 닫으면 1번이 비고, 이어서 open 이 가장 낮은 빈 번호 1 을 받아 1번이 newfile.txt 를 가리킨다. "
      "exec 으로 wc 가 되어도 파일 번호 표는 그대로라 wc 의 출력은 파일로 간다.",
      lead="같은 자식 프로세스를 네 시점에서 본 모습입니다.")

PW, PG = 200, 16
Y_T = 110
stages = [
    ("fork 직후", "부모의 표를 물려받음",
     [("터미널 (입력)", None), ("터미널 (출력)", None), ("터미널 (출력)", None)]),
    ("close(STDOUT_FILENO)", "1번이 비었음",
     [("터미널 (입력)", None), ("(비어 있음)", WARN), ("터미널 (출력)", None)]),
    ("open(newfile.txt)", "가장 낮은 빈 번호를 받음",
     [("터미널 (입력)", None), ("newfile.txt", ACC), ("터미널 (출력)", None)]),
    ("exec(wc) 뒤", "표가 그대로 남음",
     [("터미널 (입력)", None), ("newfile.txt", ACC), ("터미널 (출력)", None)]),
]
for i, (ttl, sub, rows) in enumerate(stages):
    x = 24 + i * (PW + PG)
    d.box(x, Y_T, PW, 290, PAPER2, RULE, 1.0)
    d.t(x + PW / 2, Y_T + 28, ttl, 12, INK, MONO, "middle", 600)
    d.t(x + PW / 2, Y_T + 50, sub, 11, MUTED, KR)
    for r, (tgt, c) in enumerate(rows):
        y = Y_T + 84 + r * 72
        d.box(x + 12, y, 44, 40, PAPER2, RULE, 1.0)
        d.t(x + 34, y + 25, str(r), 14, INK, MONO, "middle", 600)
        if c is WARN:
            d.o.append(f'<rect x="{x + 82}" y="{y}" width="106" height="40" rx="6" fill="{c}14" stroke="{c}" stroke-width="1.2" stroke-dasharray="5 4"/>')
        elif c:
            d.tone(x + 82, y, 106, 40, c, 6, "14", 1.4)
        else:
            d.box(x + 82, y, 106, 40, PAPER2, RULE, 1.0)
        d.t(x + 135, y + 25, tgt, 11, c or INK, KR, "middle", 600 if c else 400)
        if c is not WARN:
            d.arrow([(x + 58, y + 20), (x + 80, y + 20)], c or MUTED, "acc" if c is ACC else "ar", 1.3)
    if i < 3:
        d.arrow([(x + PW + 2, Y_T + 20), (x + PW + PG - 2, Y_T + 20)], SOFT, "soft", 1.3)

d.t(24, Y_T + 312, "wc 는 1번에 쓸 뿐 — 그 자리가 파일인지 화면인지 모름", 12, MUTED, KR, "start")
d.legend(H - 40, [("바뀐 칸", ACC), ("비어 있음", WARN)])
d.save("03-01.fd-redirect.svg")
print("ok 03-01 fd-redirect")

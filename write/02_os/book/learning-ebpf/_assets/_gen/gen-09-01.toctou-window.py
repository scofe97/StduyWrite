# 타입 스펙: type-swimlane — 레인 넷(공격 스레드 B · 대상 스레드 A · eBPF sys_enter · 커널) × 사건 넷. 같은 filename 메모리가 읽힌 값과 복사된 값이 갈리는 창이 focal.
# 사실 출처: 추출본 src/ebpf9.txt 284~291행(입구 eBPF 가 읽은 뒤 커널이 복사하기 전의 창), 296~298행(seccomp-bpf 는 사용자 포인터를 읽지 못해 창이 없음),
#   커널 v7.2 fs/open.c 1385~1391행 SYSCALL_DEFINE4(openat, int, dfd, const char __user *, filename, …),
#   seccomp_unotify(2) 줄 957~983("cannot be used to implement a security policy"), 커널 문서 seccomp_filter.rst 줄 25~27.
#   경로 값 /tmp/x · /etc/shadow 는 설명용 예시다.
# Layout conventions: 레인 높이 84(y=112·196·280·364), 단계 상자 w=168 h=56 x=176·372·568·764(stride 196), 레인 라벨 열 x=24. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 960, 584
d = D(W, H, "LEARNING EBPF · 09-01 §3",
      "읽은 값과 복사된 값 사이의 창",
      "대상 스레드 A 가 openat 을 부르면 입구의 eBPF 가 filename 을 읽어 정책을 통과시킨다. 그 뒤 커널이 복사하기 전에 스레드 B 가 같은 메모리를 덮어쓰면 커널은 덮어쓴 경로를 연다.",
      "같은 메모리가 두 번 읽히는 사이에 값이 바뀝니다")

LANES = (("공격 스레드 B", "같은 메모리 접근", 154), ("대상 스레드 A", "openat 호출", 238),
         ("eBPF", "sys_enter", 322), ("커널", "인자 복사", 406))
for y in (112, 196, 280, 364, 448):
    d.line(24, y, W - 24, y, RULE, 0.8)
for nm, sub, cy in LANES:
    d.t(24, cy - 2, nm, 13, INK, KR, "start", 600)
    d.t(24, cy + 18, sub, 13, MUTED, KR, "start")

XS = (176, 372, 568, 764)
SW, SH = 168, 56


def step(i, cy, title, sub, c):
    x = XS[i]
    d.tone(x, cy - SH // 2, SW, SH, c, 6, "12", 1.2)
    d.t(x + SW // 2, cy - 4, title, 13, c, KR if any("가" <= ch <= "힣" for ch in title) else MONO, "middle", 600)
    d.t(x + SW // 2, cy + 16, sub, 13, MUTED, MONO)


step(0, 238, "openat", 'filename → "/tmp/x"', INFO)
step(1, 322, "filename 읽기", '"/tmp/x" · 통과', INFO)
step(2, 154, "같은 메모리 덮어쓰기", '"/etc/shadow"', BAD)
step(3, 406, "filename 복사", '"/etc/shadow" 열림', BAD)

# 흐름: A → eBPF, eBPF → 커널(창), B → 커널
d.arrow([(260, 266), (260, 322), (366, 322)], MUTED, "ar", 1.5)
d.arrow([(456, 350), (456, 406), (758, 406)], WARN, "warn", 1.5, "5 4")
d.arrow([(736, 154), (848, 154), (848, 376)], BAD, "bad", 1.6)
d.chip(608, 388, "TOCTOU 창", WARN, 13)

d.line(24, 480, W - 24, 480, RULE, 0.8)
d.t(24, 508, "seccomp-bpf", 13, OK, MONO, "start", 600)
d.t(150, 508, "포인터 안 읽음 → 창 없음", 13, MUTED, KR, "start")

d.legend(H - 56, [("읽은 값", INFO), ("덮어쓴 값", BAD), ("창", WARN), ("창 없음", OK)])
d.save("09-01.toctou-window.svg")

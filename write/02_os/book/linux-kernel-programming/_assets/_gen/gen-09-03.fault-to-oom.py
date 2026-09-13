# 09-03 §2 — 가상 페이지를 만진 순간부터 OOM killer 까지, 누가 누구에게 넘기는가.
# 본문의 mermaid 를 대체한다 — 노드 열넷으로 일회성 단순 흐름 범위를 넘고, 주체가 넷이라 시간순 메시지가 맞는다.
# 커널 로그의 스택(do_page_fault → handle_mm_fault → __alloc_pages → __alloc_pages_slowpath → out_of_memory)과 같은 순서다.
# 타입 스펙: type-sequence — 주체 넷 사이의 시간순 메시지. 아래로 갈수록 되돌아올 길이 줄어든다.
import sys; sys.path.insert(0, ".")
from ddk import SeqK
from dd import ACC, MUTED, SOFT, INK, INFO, OK, WARN, BAD, PAPER2, RULE, KR, MONO

W, H = 1000, 760

d = SeqK(W, H, "LINUX KERNEL PROGRAMMING · 09-03 §2",
         "폴트에서 OOM 까지는 한 줄기입니다",
         "가상 페이지를 만지면 MMU 가 변환을 시도하고, 매핑이 없으면 페이지 폴트 핸들러로 제어가 넘어간다. 핸들러가 정당한 접근이라 판단하면 페이지 할당자에 프레임 하나를 요청한다. 극심한 압박으로 그 프레임을 끝내 못 얻으면 out_of_memory() 가 불리고 누군가 SIGKILL 된다.",
         "커널 로그의 스택을 아래에서 위로 읽으면 이 순서가 그대로 나옵니다")

d.lanes([("프로세스", "current"), ("MMU", "silicon"), ("폴트 핸들러", "do_page_fault"), ("페이지 할당자", "buddy system")], 104, 212)

d.msg("프로세스", "MMU", "가상 페이지 touch", 196, INFO, sub="read · write · execute")
d.selfmsg("MMU", "page table walk", 252, MUTED, sub="PGD → PUD → PMD → PTE")
d.msg("MMU", "폴트 핸들러", "변환 실패 — fault", 316, WARN, "warn", sub="매핑이 없습니다")
d.selfmsg("폴트 핸들러", "정당한 접근인가", 372, WARN, sub="아니면 SIGSEGV 또는 Oops 입니다")
d.msg("폴트 핸들러", "페이지 할당자", "__alloc_pages()", 436, INFO, sub="order 0 프레임 하나를 요청합니다")
# 마지막 레인이라 selfmsg 는 오른쪽으로 넘친다 — 레인 위 상태 칩으로 대신한다.
d.state("페이지 할당자", "slowpath · 회수", 492, ACC)
d.t(d.LX["페이지 할당자"], 520, "kswapd 가 거둬 옵니다", 13, MUTED, KR)
d.msg("페이지 할당자", "폴트 핸들러", "프레임 하나", 556, OK, "ok", sub="여기서 끝나면 minor fault 입니다")
d.msg("폴트 핸들러", "프로세스", "매핑하고 재개", 612, OK, "ok")
d.msg("페이지 할당자", "프로세스", "out_of_memory() → SIGKILL", 668, BAD, "bad", dash="5 5")

d.rails(692)

d.legend(H - 40, [("정상 경로", INFO), ("분기", WARN), ("회수 시도 — 마지막 기회", ACC), ("성공", OK), ("실패", BAD)])
d.save("09-03.fault-to-oom.svg")
print("ok 09-03.fault-to-oom")

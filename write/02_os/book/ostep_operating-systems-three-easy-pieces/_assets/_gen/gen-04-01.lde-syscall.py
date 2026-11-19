# 04-01 「시스템 콜은 trap 으로 들어가 return-from-trap 으로 돌아온다」 — 부팅 때 trap table 을 등록해 두고, 실행 중에는 프로그램이 trap 을 일으켜 커널로 들어갔다가 돌아온다.
# 본문 근거: 이 노트 「2. 사용자 모드와 시스템 콜」.
# 값 근거: 개념 도식이라 값은 없다. 원서 그림 6.2 (LDE Protocol) 의 부팅 표와 실행 표를 시간순 한 장으로 합쳤다.
# 공식 근거: OSTEP 6장 §6.2 — 하드웨어는 trap 때 돌아올 곳을 저장하고 return-from-trap 때 복원한다(저장 방식은 CPU 마다 다르다. 책은 x86 의 일례로 커널 스택을 든다).
# 타입 스펙: type-sequence — 참여자 셋(프로그램 · 하드웨어 · 운영체제)의 시간순 메시지. 점선 경계로 부팅 때와 실행 중을 가른다.
#
# 메시지 라벨(msg·selfmsg)은 dd.py 가 MONO 로 그리므로 ASCII 만 담고, 한글 설명은 sub 에 둔다.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, OK, INFO, RULE, KR, MONO

W, H = 920, 768

d = Seq(W, H, "OSTEP · 04-01 LDE",
        "부팅 때 길을 깔아 두고 실행 중에는 trap 으로 커널에 들어간다",
        "위쪽은 부팅 때 운영체제가 특권 명령으로 trap table 을 하드웨어에 알려 두는 단계다. "
        "아래쪽은 프로그램이 trap 을 일으키면 하드웨어가 돌아올 곳을 저장하고 커널 모드로 바꿔 운영체제의 핸들러로 보내며, "
        "운영체제가 일을 마치고 return-from-trap 을 실행하면 하드웨어가 레지스터를 복원하고 사용자 모드로 돌려보내는 단계다.",
        lead="한 번의 시스템 콜이 지나가는 길이다.")

d.lanes([("프로그램", "user mode"),
         ("하드웨어", "CPU"),
         ("운영체제", "kernel mode")], lane_w=200)
d.rails(716)

# 부팅 때
d.t(36, 176, "부팅 때 — 커널 모드에서 한 번", 13, MUTED, KR, "start", 600)
d.msg("운영체제", "하드웨어", "set trap table", 224, INFO, mk="info", sub="특권 명령으로 핸들러 주소를 등록")

d.line(24, 268, W - 48, 268, RULE, 0.8, "4 4")

# 실행 중
d.t(36, 296, "실행 중 — 시스템 콜 한 번", 13, MUTED, KR, "start", 600)
d.msg("프로그램", "하드웨어", "trap", 340, ACC, mk="acc", sub="시스템 콜 번호를 정해진 자리에 두고 실행")
d.selfmsg("하드웨어", "save regs", 392, MUTED, sub="저장 · 커널 모드로 (방식은 CPU 마다)")
d.msg("하드웨어", "운영체제", "jump to trap handler", 450, INFO, mk="info", sub="등록해 둔 주소로 이동")
# 운영체제 레인은 오른쪽 끝이라 selfmsg 라벨이 화면 밖으로 잘린다. 루프와 라벨을 레일 왼쪽에 그린다.
ox = d.LX["운영체제"]
d.path(f"M {ox - 10} 492 L {ox - 58} 492 L {ox - 58} 512 L {ox - 13} 512", MUTED, 1.4, m="ar")
d.t(ox - 68, 498, "handle syscall", 11, MUTED, MONO, "end", 400)
d.t(ox - 68, 515, "번호를 확인하고 실행", 11, MUTED, KR, "end")
d.msg("운영체제", "하드웨어", "return-from-trap", 564, INFO, mk="info", sub="특권 명령")
d.selfmsg("하드웨어", "restore regs", 616, MUTED, sub="사용자 모드로 복귀 (방식은 CPU 마다)")
d.msg("하드웨어", "프로그램", "jump to next PC", 676, OK, mk="ok", sub="trap 다음 줄에서 이어 실행")

d.legend(H - 40, [("커널 쪽 동작", INFO), ("trap 진입", ACC), ("하드웨어 처리", MUTED), ("복귀", OK)])
d.save("04-01.lde-syscall.svg")
print("ok 04-01 lde-syscall")

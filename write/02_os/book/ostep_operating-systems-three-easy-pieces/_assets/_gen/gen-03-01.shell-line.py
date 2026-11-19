# 03-01 「셸 명령 한 줄의 일생」 — 셸이 wc p3.c > newfile.txt 를 받아 실행하는 동안 부모(셸)와 자식이 커널에 부르는 호출의 순서.
# 본문 근거: 이 노트 「셸 명령 한 줄의 일생」, 「4. fork 와 exec 을 나눈 이유」.
# 값 근거: 개념 도식이라 값은 없다. 명령은 5장의 리다이렉션 예 `wc p3.c > newfile.txt` 이다.
# 공식 근거: OSTEP 5장 §5.4 — 셸은 fork 로 자식을 만들고 exec 변형으로 명령을 돌리며 wait 로 끝나기를 기다린다. 리다이렉션이면 자식이 exec 전에 표준 출력을 닫고 파일을 연다.
# 타입 스펙: type-sequence — 참여자(셸·커널·자식) 사이의 호출과 반환을 시간순으로.
import sys; sys.path.insert(0, ".")
from dd import PAPER, Seq, ACC, MUTED, SOFT, INK, OK, INFO, RULE, KR, MONO

W, H = 920, 640
d = Seq(W, H, "OSTEP · 03-01 SHELL LINE",
        "셸 명령 한 줄은 복제, 파일 번호 조정, 덮어쓰기, 대기로 끝난다",
        "셸(부모)이 fork 를 부르면 커널이 자식을 만들어 부모에게는 자식의 PID 를, 자식에게는 0 을 돌려준다. "
        "자식은 close 와 open 으로 표준 출력을 newfile.txt 로 바꾸고 execvp 로 wc 가 된다. "
        "한편 셸은 wait 를 불러 자식이 끝나기를 기다리고, 자식이 끝나면 wait 가 돌아와 셸은 프롬프트를 다시 보인다.",
        lead="명령: wc p3.c > newfile.txt · 부모와 자식 중 누가 먼저 도는지는 스케줄러가 정합니다")
def stbk(a, txt, y, c):
    w = len(txt) * 7.0 + 18
    d.box(d.LX[a] - w / 2, y - 10, w, 20, PAPER, PAPER, 0, 4)
    d.state(a, txt, y, c)


d.lanes([("셸(부모)", "user mode"), ("커널", "kernel mode"), ("자식", "user mode")], lane_w=200)
d.rails(590)
d.msg("셸(부모)", "커널", "fork()", 190, ACC, mk="acc", sub="자식을 하나 만들어 달라")
d.msg("커널", "셸(부모)", "반환: 자식 PID", 250, MUTED, dash="5 4")
d.msg("커널", "자식", "반환: 0", 310, MUTED, dash="5 4")
stbk("자식", "close(1) · open(newfile.txt)", 372, INFO)
d.msg("자식", "커널", "execvp(\"wc\")", 440, ACC, mk="acc", sub="자식이 wc 로 바뀜")
d.msg("셸(부모)", "커널", "wait()", 500, INFO, mk="info", sub="자식이 끝날 때까지 막힘")
d.msg("커널", "셸(부모)", "wait() 반환", 560, OK, mk="ok", sub="프롬프트를 다시 보임")
d.legend(H - 40, [("복제 · 덮어쓰기", ACC), ("파일 번호 · 대기", INFO), ("대기 끝", OK)])
d.save("03-01.shell-line.svg")
print("ok 03-01 shell-line")

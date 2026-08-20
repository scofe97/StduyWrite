# 02-01.socket-syscall-order — 부르는 것과 만들어지는 것을 세로로 짝지운다
# 본문 요구: 애플리케이션이 부르는 네 호출과, 그때 커널이 만드는 네 가지를 짝으로 읽게
# 타입 스펙: type-swimlane.md — 레인 둘(부르는 쪽 / 만드는 쪽)에 같은 열을 세워
#           가로는 순서, 세로는 대응이 되게 한다.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 616
d = D(W, H, "SOCKET SYSCALLS · CALL vs WHAT IT CREATES",
      "소켓 syscall — 애플리케이션이 부르면 커널이 무엇을 만드는가",
      "가로는 부르는 순서, 세로는 그 호출이 커널에 남기는 것. 네 번의 호출이 네 가지를 만든다.",
      lead="가로는 부르는 순서 · 세로는 그 호출이 커널에 남기는 것")

BW, BH, GAP = 200, 100, 24
CX = [64 + BW // 2 + i * (BW + GAP) for i in range(4)]           # 164 388 612 836
CALL_CY, KERN_CY = 276, 452
CALLS = [("socket()", "AF_INET6 · SOCK_STREAM", "반환값 3"),
         ("bind()", "htons(8080) · [::]", "반환값 0"),
         ("listen()", "두 번째 인자 128", "반환값 0"),
         ("accept4()", "epoll 이 깨운 뒤", "연결마다 호출")]
MADE = [("파일 디스크립터 3", "연결을 파일로 다룬다", "0·1·2 다음 번호"),
        ("포트 8080 예약", "와일드카드 주소에 묶임", "v4·v6 함께 수신"),
        ("백로그 큐 128칸", "수립됐지만 아직 안 받은 연결", "넘치면 새 연결 거절"),
        ("연결마다 새 fd", "듣는 소켓과 별개", "여기부터 read·write")]
LINK = ["할당", "예약", "생성", "수락"]

ddx.band(d, 104, 568, "부르는 쪽은 이름 넷을 알면 되고, 커널이 그 뒤에서 넷을 만든다")
for y0, lab, c in [(CALL_CY - BH // 2 - 26, "애플리케이션이 부르는 것", INFO),
                   (KERN_CY - BH // 2 - 26, "커널이 만드는 것", ACC)]:
    d.o.append(f'<rect x="40" y="{y0}" width="920" height="{BH+38}" rx="8" '
               f'fill="{c}06" stroke="{c}" stroke-width="1.2" stroke-dasharray="7 6"/>')
    ddx.ring_label(d, 40, y0, lab, 11, c, off=16)

def cell(cx, cy, t, s, tag, c, mono=False):
    d.box(cx - BW // 2, cy - BH // 2, BW, BH, PAPER2, c, 1.1, 6)
    d.t(cx, cy - 20, ddx.fit(t, 13, BW - 18, t), 13, c, MONO if mono else KR, "middle", 600)
    d.t(cx, cy + 2, ddx.fit(s, 11, BW - 18, s), 11, MUTED,
        MONO if all(ord(ch) < 128 or ch in '·' for ch in s) else KR)
    d.t(cx, cy + 26, ddx.fit(tag, 10, BW - 14, tag), 10, SOFT, KR)

for cx, c in zip(CX, CALLS):  cell(cx, CALL_CY, *c, INFO, mono=True)
for cx, m in zip(CX, MADE):   cell(cx, KERN_CY, *m, ACC)
for a, b in zip(CX, CX[1:]):
    d.path(f"M {a+BW//2+6} {CALL_CY} L {b-BW//2-10} {CALL_CY}", MUTED, 1.4, m="ar")
for cx, lab in zip(CX, LINK):
    d.path(f"M {cx} {CALL_CY+BH//2+6} L {cx} {KERN_CY-BH//2-10}", ACC, 1.5, m="acc")
    d.t(cx + 12, (CALL_CY + KERN_CY) // 2 + 4, lab, 11, ACC, KR, "start")

d.t(36, 536, "listen() 의 두 번째 인자가 백로그 큐 길이다 — 그 큐가 차면 새 연결이 거절되므로 "
             "숫자 하나가 곧 수용량이 된다", 12, MUTED, KR, "start")
d.legend(584, [("부르는 쪽", INFO), ("커널이 만드는 것", ACC)])
d.save("02-01.socket-syscall-order.svg")
print("ok socket-syscall-order")

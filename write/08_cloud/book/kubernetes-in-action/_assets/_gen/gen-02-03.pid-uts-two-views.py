# 02-03 §하나의 프로세스, 두 개의 뷰
# 실측: 컨테이너 안 — ps 는 PID 1 node, hostname 은 fe6daee29272.
#       호스트 밖 — docker inspect .State.Pid 는 32687, systemd 등 수천 프로세스와 나란히.
# 타입 스펙: 대상이 하나이고 관측 지점이 둘이라, 가운데에 그 하나를 두고 좌우로 뷰를 낸다.
#           같은 것을 두 번 그리면 프로세스가 둘인 것처럼 읽히므로 반드시 하나여야 한다.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO
import ddx

W, H = 1000, 592
d = D(W, H, "KUBERNETES IN ACTION · 02-03",
      "프로세스는 하나인데 값이 둘로 보인다",
      "같은 node 프로세스를 컨테이너의 네임스페이스에서 보면 PID 1 이고 호스트의 기본 "
      "네임스페이스에서 보면 32687 이다. 어느 네임스페이스에서 보느냐가 값을 정한다.",
      lead="02-02 의 'Request processed by fe6daee29272' 와 '앱이 PID 1' 의 커널 레벨 정답이다")

MID = (500, 268)
LEFT, RIGHT = (206, 412), (794, 412)
MW, MH = 300, 84
PW, PH = 360, 148

ddx.band(d, 104, 536, "값이 둘인 것이 아니라 보는 자리가 둘이다 — 프로세스는 하나뿐이다")

d.o.append(f'<rect x="{MID[0]-MW//2}" y="{MID[1]-MH//2}" width="{MW}" height="{MH}" rx="6" '
           f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t(MID[0], MID[1] - 12, "node app.js", 15, ACC, MONO, "middle", 600)
d.t(MID[0], MID[1] + 14, "실제로는 프로세스 하나", 11, SOFT, KR)

def view(cx, cy, title, sub, lines, c):
    d.box(cx - PW // 2, cy - PH // 2, PW, PH, PAPER2, c, 1.1, 6)
    d.t(cx, cy - PH // 2 + 26, title, 13, c, KR, "middle", 600)
    d.t(cx, cy - PH // 2 + 44, sub, 10, SOFT, KR)
    for i, (cmd, out) in enumerate(lines):
        y = cy - PH // 2 + 74 + i * 34
        d.t(cx - PW // 2 + 20, y, cmd, 10, SOFT, MONO, "start")
        d.t(cx - PW // 2 + 20, y + 18, out, 12, c, MONO, "start", 600)

view(*LEFT, "컨테이너 안에서 본 뷰", "자기 uts·pid 네임스페이스 안", [
    ("$ ps -o pid,comm", "PID 1  node"),
    ("$ hostname", "fe6daee29272")], INFO)
view(*RIGHT, "호스트 밖에서 본 뷰", "호스트의 기본 네임스페이스", [
    ("$ ps (호스트 전체)", "PID 32687  node"),
    ("$ docker inspect .State.Pid", "32687")], OK)

d.path(f"M {MID[0]-MW//2-6} {MID[1]} L {LEFT[0]} {MID[1]} L {LEFT[0]} {LEFT[1]-PH//2-10}",
       INFO, 1.6, m="info")
# 코리도어는 206~344 (138px) 뿐이다 — 칩은 그 안에 들어가는 길이로 줄인다
d.chip(275, MID[1], "컨테이너 쪽에서", INFO, 11)
d.path(f"M {MID[0]+MW//2+6} {MID[1]} L {RIGHT[0]} {MID[1]} L {RIGHT[0]} {RIGHT[1]-PH//2-10}",
       OK, 1.6, m="ok")
d.chip(725, MID[1], "호스트 쪽에서", OK, 11)

# 뷰 상자가 338~486 을 쓴다 — 산문은 그 아래로
d.t(36, 512, "PID 네임스페이스가 1번부터 새로 세고 UTS 네임스페이스가 호스트명을 격리하기 "
             "때문이다 — 같은 커널이 같은 프로세스를 두 이름으로 부른다.", 12, MUTED, KR, "start")
d.legend(552, [("컨테이너 쪽 뷰", INFO), ("호스트 쪽 뷰", OK), ("보이는 대상 — 하나뿐", ACC)])
d.save("02-03-pid-uts-two-views.svg")
print("ok pid-uts-two-views")

# 05-01 §5 — 서버 블록 example.com:5300 안에서 etcd 는 services.example.com 만 답하고 나머지는 forward 로 간다.
# 본문 근거: 이 노트 §5 의 두 번째 Corefile(log · etcd services.example.com · forward example.com /etc/resolv.conf)과
#            그 아래 설명 "etcd 플러그인은 services.example.com 만 서빙합니다. 서버 블록의 나머지 질의는 forward 플러그인이 처리합니다."
# 타입 스펙: type-flowchart — 질의 이름에 따라 체인이 두 갈래로 갈리는 분기가 논지다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 450
d = D(W, H, "LEARNING COREDNS · 05-01 §5",
      "같은 서버 블록에서 존 인자가 질의를 가른다",
      "example.com:5300 블록의 질의는 모두 log 를 지난다. etcd 는 services.example.com 아래 이름에만 답하고, "
      "그 밖의 example.com 이름은 다음 플러그인인 forward 가 /etc/resolv.conf 의 서버로 넘긴다.",
      "주황 상자가 etcd 가 직접 답하는 자리입니다")

d.o.append(f'<rect x="236" y="118" width="444" height="240" rx="8" fill="none" stroke="{RULE}" '
           f'stroke-width="1.0" stroke-dasharray="4 5"/>')
d.t(250, 138, "example.com:5300 서버 블록", 12, SOFT, KR, "start", 600)

Q = (20, 200)
LOG = (250, 80)
ETCD = (346, 170)
FWD = (530, 136)
RES = (700, 160)
ROWS = [150, 262]
RH = 76


def cell(xw, y, main, sub, c=INK, focal=False, mono_main=True):
    x, w = xw
    if focal:
        d.tone(x, y, w, RH, ACC, 6, "12", 1.4)
    else:
        d.box(x, y, w, RH, PAPER2, RULE, 1.0, 6)
    d.t(x + 12, y + 32, main, 13, ACC if focal else c, MONO if mono_main else KR, "start", 600)
    if sub:
        d.t(x + 12, y + 56, sub, 12, MUTED, MONO if sub.startswith("/") else KR, "start")


def arrow(a, b, y):
    d.path(f"M {a[0] + a[1] + 2} {y} L {b[0] - 3} {y}", MUTED, 1.3, m="ar")


y1, y2 = ROWS
cell(Q, y1, "users.services.", "example.com", mono_main=True)
d.o[-1] = d.o[-1].replace(f'font-size="12" fill="{MUTED}"', f'font-size="13" fill="{INK}"')
cell(LOG, y1, "log", "기록")
cell(ETCD, y1, "etcd", "존 일치 · 직접 응답", focal=True)
cell(RES, y1, "etcd 키 조회", "/skydns/.../users", mono_main=False)
arrow(Q, LOG, y1 + 38); arrow(LOG, ETCD, y1 + 38); arrow(ETCD, RES, y1 + 38)

cell(Q, y2, "www.example.com", "")
cell(LOG, y2, "log", "기록")
cell(ETCD, y2, "etcd", "존 밖 · 다음으로", c=MUTED)
cell(FWD, y2, "forward", "example.com")
cell(RES, y2, "외부 서버", "/etc/resolv.conf", mono_main=False)
arrow(Q, LOG, y2 + 38); arrow(LOG, ETCD, y2 + 38); arrow(ETCD, FWD, y2 + 38); arrow(FWD, RES, y2 + 38)

d.t(20, 392, "etcd 는 services.example.com 아래만 · 나머지 example.com 은 forward", 13, MUTED, KR, "start")

d.legend(408, [("etcd 가 직접 답하는 질의", ACC)])
d.save("05-01.zone-split.svg")

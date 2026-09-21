# 02-02.verdict-vs-target — 반환값과 타깃은 층이 둘이다
# 본문 요구: "아래 표는 커널이 받는 반환값이고, 우리가 iptables 에 적는 ACCEPT·DROP 은 타깃입니다.
#            이름이 겹쳐 같아 보이지만 같은 층이 아닙니다. 타깃 쪽에는 반환값에 짝이 없는 것도 있어서,
#            RETURN 은 체인을 빠져나오라는 흐름 제어이고 REJECT 는 동작 여러 개를 묶은 것입니다."
#            표 둘을 나란히 두면 이름이 같은 줄끼리 1:1 로 읽혀, 짝이 없다는 말이 안 선다.
# 타입 스펙: type-layers.md — 위아래 두 층과 그 사이 사상(mapping). 세로 위치가 곧 층이고,
#           내려가는 선이 사상이다. focal 은 짝이 없는 타깃 둘 — 이 도식이 존재하는 이유다.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, INFO, BAD, OK, PAPER, PAPER2, KR, MONO

W, H = 1000, 640
d = D(W, H, "NETFILTER VERDICT VS IPTABLES TARGET",
      "반환값과 타깃 — 이름이 같아도 층이 다르다",
      "위층은 iptables 규칙에 적는 타깃이고, 아래층은 커널 훅이 돌려주는 반환값이다. "
      "이름이 같은 짝도 있지만 RETURN 은 반환값 없이 체인 흐름만 바꾸고, REJECT 는 패킷 하나를 "
      "만들어 보낸 뒤 NF_DROP 으로 떨어지는 묶음이다. 사상은 1:1 이 아니다.",
      lead="짝이 없는 쪽을 보면 두 층이 갈린다")

TOP_Y, BOT_Y = 232, 452
BW_, BH_ = 148, 60
# 두 층이 같은 격자를 쓴다 — 짝이 있는 셋은 같은 칸에 세워 곧은 선으로 잇고,
# 짝이 없는 것은 선이 없다는 사실 자체가 보이게 둔다. 148 폭 다섯에 틈 53.
COLS = [98, 299, 500, 701, 902]
TOP = COLS                           # ACCEPT DROP NFQUEUE REJECT RETURN
BOT = COLS                           # NF_ACCEPT NF_DROP NF_QUEUE NF_STOLEN NF_REPEAT

ddx.band(d, 178, 316, "iptables 규칙에 적는 것 — 타깃", x=24, w=952)
ddx.band(d, 398, 536, "커널 훅이 돌려주는 것 — 반환값", x=24, w=952)

def cell(cx, y, name, sub, c=None, focal=False):
    ddx.node(d, cx, y, name, sub, w=BW_, h=BH_, c=c, focal=focal)

def drop(x1, x2, c=MUTED, dash=None):
    d.path(f"M {x1} {TOP_Y + BH_ // 2} L {x1} {(TOP_Y + BOT_Y) // 2} "
           f"L {x2} {(TOP_Y + BOT_Y) // 2} L {x2} {BOT_Y - BH_ // 2 - 8}", c, 1.5, m="ar", dash=dash)

# 사상 먼저(z-order) — 같은 칸끼리는 곧게, REJECT 만 왼쪽 NF_DROP 으로 꺾인다
drop(TOP[0], BOT[0]); drop(TOP[1], BOT[1]); drop(TOP[2], BOT[2])
drop(TOP[3], BOT[1], ACC, "5,4")

cell(TOP[0], TOP_Y, "ACCEPT", "통과")
cell(TOP[1], TOP_Y, "DROP", "말없이 버림")
cell(TOP[2], TOP_Y, "NFQUEUE", "밖으로 넘김")
cell(TOP[3], TOP_Y, "REJECT", "알리고 버림", focal=True)
cell(TOP[4], TOP_Y, "RETURN", "체인 흐름 제어", c=INFO)

cell(BOT[0], BOT_Y, "NF_ACCEPT", "계속 진행", c=OK)
cell(BOT[1], BOT_Y, "NF_DROP", "폐기", c=BAD)
cell(BOT[2], BOT_Y, "NF_QUEUE", "유저스페이스로")
cell(BOT[3], BOT_Y, "NF_STOLEN", "소유권을 가져감")
cell(BOT[4], BOT_Y, "NF_REPEAT", "같은 훅에 재진입")

# RETURN 은 내려가는 선이 아예 없다 — 없다는 것이 이 칸의 내용이다
d.t(TOP[4], TOP_Y + BH_ // 2 + 24, "내려가는 선이 없다", 11, INFO, KR)

# REJECT 가 묶음이라는 것 — 꺾인 선 위에 한 마디
d.t(TOP[3] - 12, (TOP_Y + BOT_Y) // 2 - 10, "ICMP 오류나 RST 를 먼저 보낸 뒤", 11, ACC, KR, "end")

# 아래층에만 있는 둘 — 규칙으로는 못 적는다
d.t((BOT[3] + BOT[4]) // 2, BOT_Y + BH_ // 2 + 26, "이 둘은 위층에 적을 타깃이 없다 — 커널 모듈이 직접 돌려준다", 11, SOFT, KR)

d.legend(H - 48, [("짝이 1:1 이 아닌 타깃", ACC), ("아래층으로 안 내려가는 타깃", INFO),
                  ("통과", OK), ("폐기", BAD)])
d.save("02-02.verdict-vs-target.svg")
print("ok verdict-vs-target")

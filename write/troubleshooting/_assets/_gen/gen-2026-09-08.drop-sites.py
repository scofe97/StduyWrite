# 2026-09-08 A 문항 개념 — 패킷이 사라지는 네 자리.
# 한 장비 안에서 패킷이 버려질 수 있는 자리를 아래에서 위로 쌓고, 자리마다
# 범위(소켓 하나냐 노드 전체냐)와 확인 명령을 나란히 세운다.
# focal 은 오늘 문항의 답이 된 conntrack.
# 타입 스펙: type-layers — 전폭 밴드를 세로로 쌓고, 각 행은
#           왼쪽 인덱스 태그 · 가운데 이름 · 오른쪽 mono 서브라벨.
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dd import D, ACC, MUTED, SOFT, INK, INFO, PAPER2, RULE, KR, MONO

W, H = 800, 500
LX, LW = 160, 560
LH, Y0 = 68, 118

d = D(W, H, "TROUBLESHOOTING DRILL · 2026-09-08 A",
      "패킷이 사라지는 네 자리",
      "리눅스 한 대 안에서 패킷이 버려질 수 있는 자리를 아래에서 위로 쌓은 그림. "
      "자리마다 버린 수를 세는 카운터가 따로 있고, 범위가 소켓 하나인지 노드 전체인지가 진단의 첫 갈래다. "
      "강조된 conntrack 이 2026-09-08 A 문항의 답이었다.",
      lead="범위가 첫 갈래입니다 — 한 서비스만 아픈가, 이 노드가 통째로 아픈가")

# 아래에서 위로: 링 버퍼(물리에 가까움) → conntrack → SYN 큐 → accept 큐 → 앱
ROWS = [
    ("accept", "accept 큐", "소켓 하나", "ss -lnt", "Recv-Q vs Send-Q", False),
    ("syn",    "SYN 큐",    "소켓 하나", "netstat -s", "SYNs to LISTEN dropped", False),
    ("ct",     "conntrack", "노드 전체", "sysctl ...nf_conntrack_count/max", "count / max", True),
    ("nic",    "NIC 링 버퍼", "인터페이스", "ethtool -S eth0", "drop 증가분", False),
]

def top(k): return Y0 + k * LH
def mid(k): return top(k) + LH / 2

# 앱 (스택 위, 목적지)
d.t(LX + LW / 2, Y0 - 26, "애플리케이션 — accept() 로 꺼내 갑니다", 12, MUTED, KR)

for k, (tag, name, scope, cmd, reads, focal) in enumerate(ROWS):
    y = top(k)
    if focal:
        d.tone(LX, y, LW, LH - 4, ACC, 6)
    else:
        d.box(LX, y, LW, LH - 4, PAPER2, RULE, 0.9, 6)
    col = ACC if focal else INK
    # 왼쪽 인덱스 태그 (스택 밖)
    d.t(LX - 14, mid(k) - 4, scope, 11, ACC if focal else SOFT, KR, "end", 600 if focal else 400)
    d.t(LX - 14, mid(k) + 13, tag.upper(), 9, SOFT, MONO, "end")
    # 가운데 이름
    d.t(LX + 20, mid(k) - 3, name, 15, col, KR, "start", 600)
    # 오른쪽 mono 서브라벨 — 명령과 읽는 값
    d.t(LX + LW - 18, mid(k) - 6, cmd, 11, MUTED, MONO, "end")
    d.t(LX + LW - 18, mid(k) + 12, reads, 11, SOFT, MONO, "end")

# 바깥 실루엣
d.line(LX, Y0, LX + LW, Y0, MUTED, 1.0)
d.line(LX, top(len(ROWS)) - 4, LX + LW, top(len(ROWS)) - 4, MUTED, 1.0)

# 왼쪽 방향 표시 (스택 밖) — 세로 라벨로 두어 좌측 잘림을 피합니다
ax = 40
d.arrow([(ax, top(len(ROWS)) - 18), (ax, Y0 + 10)], SOFT, "soft", 1.2)
d.o.append(f'<text x="{ax + 13}" y="{(Y0 + top(len(ROWS))) / 2}" text-anchor="middle" '
           f'font-family="{MONO}" font-size="9" fill="{SOFT}" '
           f'transform="rotate(-90 {ax + 13} {(Y0 + top(len(ROWS))) / 2})">packets travel up</text>')

# 회선 (스택 아래)
d.t(LX + LW / 2, top(len(ROWS)) + 22, "회선", 12, MUTED, KR)

d.legend(H - 62, [("오늘 문항의 답 — 노드 전체가 공유하는 하나", ACC),
                  ("소켓 하나에만 영향 — 그 포트만 아픕니다", INFO)])
d.save(os.path.join(os.path.dirname(__file__), "..", "2026-09-08.drop-sites.svg"))
print("ok drop-sites")

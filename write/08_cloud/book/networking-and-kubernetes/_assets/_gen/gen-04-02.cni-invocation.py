# 04-02.cni-invocation — ADD 호출 한 번에 넘어가는 입력 두 갈래와 돌아오는 값
# 본문 요구: "호출마다 달라지는 값은 환경변수로 … 노드에 고정된 망 설정은 stdin JSON … 플러그인은 할당한 주소와
#           경로를 stdout JSON 으로 돌려준다"
# 타입 스펙: type-data-flow — 입력 둘이 서로 다른 통로로 바이너리에 들어가고 결과 하나가 나온다.
#           건너가는 것이 데이터라 process 가 아니라 data-flow. 손으로 쓴 SVG 를 2026-09-15 생성기로 옮겼다.
from dd import D, INK, MUTED, SOFT, RULE, OK, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 544
d = D(W, H, "CNI · WHAT ONE ADD CALL CARRIES",
      "ADD 호출 한 번에 무엇이 넘어가는가",
      "런타임은 Pod 마다 달라지는 값을 환경변수로, 노드에 고정된 망 설정을 stdin JSON 으로 넘기고, "
      "플러그인은 할당한 주소와 경로를 stdout JSON 으로 돌려준다.",
      lead="Pod 마다 달라지는 값과 노드에 고정된 값이 서로 다른 통로로 들어간다")

LX, LW = 32, 344
# 입력 1 — 환경변수
EY, EH = 104, 160
d.box(LX, EY, LW, EH, PAPER2, INFO, 1.2, 8)
d.t(LX + 20, EY + 28, "Pod 마다 달라지는 값 · 환경변수", 13, INFO, KR, "start", 600)
for i, ln in enumerate(["CNI_COMMAND=ADD", "CNI_CONTAINERID=6f3a…", "CNI_NETNS=/var/run/netns/cni-…", "CNI_IFNAME=eth0"]):
    d.t(LX + 20, EY + 60 + i * 24, ln, 12, INK, MONO, "start")

# 입력 2 — stdin JSON
SY, SH = 288, 176
d.box(LX, SY, LW, SH, PAPER2, RULE, 1.1, 8)
d.t(LX + 20, SY + 28, "노드에 고정된 값 · stdin JSON", 13, MUTED, KR, "start", 600)
for i, ln in enumerate(['{ "type": "bridge",', '  "bridge": "cni0",', '  "ipam": { "type": "host-local",',
                        '    "subnet": "10.1.3.0/24" } }']):
    d.t(LX + 20, SY + 58 + i * 22, ln, 12, INK, MONO, "start")
d.t(LX + 20, SY + 158, "위치 /etc/cni/net.d/", 12, SOFT, KR, "start")

# 플러그인 바이너리
BX, BY, BW, BH = 448, 236, 200, 96
BCY = BY + BH // 2
d.box(BX, BY, BW, BH, PAPER2, RULE, 1.1, 6)
d.t(BX + BW // 2, BY + 30, "플러그인 바이너리", 13, INK, KR, "middle", 600)
d.t(BX + BW // 2, BY + 54, "/opt/cni/bin/bridge", 12, MUTED, MONO)
d.t(BX + BW // 2, BY + 78, "실행 파일 하나", 12, SOFT, KR)

# 돌려주는 값 — stdout JSON
OX, OY, OW, OH = 704, 200, 264, 168
d.box(OX, OY, OW, OH, PAPER2, OK, 1.2, 8)
d.t(OX + 20, OY + 28, "돌려주는 값 · stdout JSON", 13, OK, KR, "start", 600)
for i, ln in enumerate(["ips:    10.1.3.7/24", "routes: 0.0.0.0/0 → 10.1.3.1", "dns:    …"]):
    d.t(OX + 20, OY + 60 + i * 24, ln, 12, INK, MONO, "start")
d.t(OX + 20, OY + 144, "Pod 의 eth0 에 붙는 주소", 12, SOFT, KR, "start")

# 통로 — 직각으로 꺾어 바이너리 왼쪽 변 두 지점으로
XJ = 412
d.arrow([(LX + LW + 6, EY + EH // 2), (XJ, EY + EH // 2), (XJ, BCY - 16), (BX - 10, BCY - 16)], INFO, "info", 1.5)
d.arrow([(LX + LW + 6, SY + SH // 2), (XJ + 12, SY + SH // 2), (XJ + 12, BCY + 16), (BX - 10, BCY + 16)], MUTED, "ar", 1.5)
d.arrow([(BX + BW + 6, BCY), (OX - 10, BCY)], OK, "ok", 1.5)

d.legend(496, [("호출마다 바뀌는 입력", INFO), ("노드에 고정된 입력", MUTED), ("플러그인이 돌려주는 값", OK)])
d.save("04-02.cni-invocation.svg")
print("ok cni-invocation")

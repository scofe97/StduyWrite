# 04-02.cni-add-flow — Pod 하나가 eth0 를 받기까지 주체 넷이 차례로 일한다
# 본문 요구: "Kubelet 이 배선을 직접 하지 않는다 … 컨테이너 런타임에게 시키면 런타임이 플러그인을 실행하고
#           플러그인은 IPAM 에게 주소를 받아옵니다 … 네임스페이스가 먼저 생겨야 CNI_NETNS 값이 존재"
# 타입 스펙: type-swimlane — 세로 레인 하나가 주체 하나, 단계 상자는 그 일을 하는 주체의 레인에만 둔다.
#           레인을 건너는 화살표(넘겨주기)는 전부 직각으로 꺾는다. 손으로 쓴 SVG 를 2026-09-15 생성기로 옮겼다.
import ddx
from dd import D, INK, MUTED, SOFT, RULE, OK, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 628
d = D(W, H, "CNI · FROM SCHEDULED POD TO A WIRED eth0",
      "Pod 하나가 주소를 받기까지",
      "Kubelet 이 Pod 를 맡으면 컨테이너 런타임이 네임스페이스를 만들고 CNI 플러그인을 실행하며, "
      "플러그인이 veth 를 놓고 IPAM 에게 주소를 받아 네임스페이스 안에 넣는다.",
      lead="Kubelet → 런타임 → 플러그인 → IPAM 순서로 일을 넘긴다")

BW, BH, STRIDE, X0 = 208, 64, 248, 24
CX = [X0 + BW // 2 + i * STRIDE for i in range(4)]          # 128 376 624 872
LANES = ["Kubelet", "컨테이너 런타임", "CNI 플러그인", "IPAM 플러그인"]
for cx, name in zip(CX, LANES):
    d.t(cx, 120, name, 12, SOFT, KR, "middle", 600)
for i in range(1, 4):
    xl = CX[i] - STRIDE // 2
    d.line(xl, 104, xl, 560, RULE, 0.8)

ROW = [136, 224, 312, 400, 400, 488]                         # 행 stride 88
STEPS = [(0, "스케줄된 Pod 수령", None, INFO),
         (1, "샌드박스 컨테이너 생성", "네트워크 네임스페이스 생성", None),
         (1, "설정 읽기 · 바이너리 실행", "CNI_COMMAND=ADD", None),
         (2, "veth 쌍 생성", "한쪽은 네임스페이스로", OK),
         (3, "대역에서 주소 하나", "10.1.3.7 배정", None),
         (2, "주소 · 기본 경로 설정", "결과 JSON 반환", OK)]

for n, ((lane, t, s, c), y) in enumerate(zip(STEPS, ROW), 1):
    cx = CX[lane]; x = cx - BW // 2
    d.box(x, y, BW, BH, PAPER2, c or RULE, 1.2 if c else 1.0, 6)
    d.t(x + 12, y + 20, str(n), 12, c or SOFT, MONO, "start", 600)
    if s:
        d.t(cx, y + 26, ddx.fit(t, 13, BW - 36, t), 13, c or INK, KR, "middle", 600)
        mono = all(ord(ch) < 128 for ch in s)
        d.t(cx, y + 48, s, 12, MUTED, MONO if mono else KR)
    else:
        d.t(cx, y + 38, ddx.fit(t, 13, BW - 36, t), 13, c or INK, KR, "middle", 600)

mid = lambda y: y + BH // 2
# 1 → 2 : Kubelet 아래로 내려와 런타임으로
d.arrow([(CX[0], ROW[0] + BH + 4), (CX[0], mid(ROW[1])), (CX[1] - BW // 2 - 10, mid(ROW[1]))], INFO, "info", 1.5)
# 2 → 3 : 같은 레인
d.arrow([(CX[1], ROW[1] + BH + 4), (CX[1], ROW[2] - 10)], MUTED, "ar", 1.5)
# 3 → 4 : 런타임 아래로 내려와 플러그인으로
d.arrow([(CX[1], ROW[2] + BH + 4), (CX[1], mid(ROW[3])), (CX[2] - BW // 2 - 10, mid(ROW[3]))], MUTED, "ar", 1.5)
# 4 → 5 : 주소 요청
d.arrow([(CX[2] + BW // 2 + 4, mid(ROW[3])), (CX[3] - BW // 2 - 10, mid(ROW[3]))], MUTED, "ar", 1.5)
# 5 → 6 : IPAM 아래로 내려와 플러그인으로
d.arrow([(CX[3], ROW[4] + BH + 4), (CX[3], mid(ROW[5])), (CX[2] + BW // 2 + 10, mid(ROW[5]))], MUTED, "ar", 1.5)
# 6 → 런타임 : stdout 으로 반환
d.arrow([(CX[2] - BW // 2 - 4, mid(ROW[5])), (CX[1] + 8, mid(ROW[5]))], OK, "ok", 1.5, "6 5")
d.t((CX[1] + CX[2] - BW // 2) // 2 + 4, mid(ROW[5]) - 12, "stdout 으로 반환", 12, OK, KR)

d.legend(580, [("시키는 쪽", INFO), ("실제로 배선하는 자리", OK)])
d.save("04-02.cni-add-flow.svg")
print("ok cni-add-flow")

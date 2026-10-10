# 타입 스펙: type-data-flow — veth 와 netkit 경로의 패킷 전달 단계와 네임스페이스 전환 비용 비교. 배정된 비교 타입이 설치 목록에 없어 두 경로 단계 흐름을 비교하는 type-data-flow 로 선언했다.
# 사실 출처: Cilium Up and Running 8장 cil8.txt 줄 1268-1293(veth ARP·네임스페이스 전환·per-CPU 백로그 큐, netkit Pod 내 조기 eBPF 훅·호스트 스택 우회), 줄 1297-1308(primary/peer 디바이스 격리·L3 모드) / docs.cilium.io v1.20 tuning(netkit datapathMode)
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 500
d = D(W, H, "CILIUM UP AND RUNNING · 08-02 §3", "veth 와 netkit 의 패킷 전달 단계 비교",
      "veth 는 네임스페이스 전환과 호스트 큐를 거치지만 netkit 은 조기 훅으로 우회한다",
      "netkit 은 Pod 내부 조기 훅과 L3 직결로 네임스페이스 전환과 per-CPU 백로그 큐 오버헤드를 줄입니다")

# 단계 상자 너비 및 배치
BOX_W = 180
BOX_H = 80
GAP = 42
X_BASE = 40

# --- 상단: veth 경로 (전통 방식) ---
Y1 = 120
d.box(24, Y1 - 14, W - 48, 128, PAPER2, RULE, 0.6, r=6)
d.t(40, Y1 + 8, "전통 veth 경로 (L2 · 호스트 스택 경유)", 12, WARN, KR, "start", 600)

steps_veth = [
    ("1. Pod 네임스페이스", "eth0 인터페이스", "소켓 버퍼 송출", None),
    ("2. 네임스페이스 전환", "veth 쌍 (@ifN)", "ARP 확인 오버헤드", WARN),
    ("3. 호스트 스택 진입", "per-CPU 백로그 큐", "per-CPU 백로그 큐 경유 지연", WARN),
    ("4. 물리 장치 송출", "물리 NIC (eth0)", "하부 망 패킷 전송", None),
]

for i, (t1, t2, sub, tone) in enumerate(steps_veth):
    x = X_BASE + i * (BOX_W + GAP)
    if tone == WARN:
        d.tone(x, Y1 + 22, BOX_W, BOX_H, WARN, r=4, op="12", sw=1.1)
    else:
        d.box(x, Y1 + 22, BOX_W, BOX_H, PAPER, RULE, 0.8, r=4)
    col = WARN if tone == WARN else INK
    d.t(x + 12, Y1 + 42, t1, 12, col, KR, "start", 600)
    d.t(x + 12, Y1 + 62, t2, 11, col, MONO, "start")
    d.t(x + 12, Y1 + 82, sub, 11, MUTED, KR, "start")
    if i < 3:
        d.arrow([(x + BOX_W + 4, Y1 + 62), (x + BOX_W + GAP - 4, Y1 + 62)], WARN, "warn", 1.2)

# --- 하단: netkit 경로 (eBPF 최적화) ---
Y2 = 280
d.box(24, Y2 - 14, W - 48, 128, PAPER2, RULE, 0.6, r=6)
d.t(40, Y2 + 8, "netkit 경로 (커널 6.8+ · L3 기본 · eBPF Host-Routing)", 12, OK, KR, "start", 600)

steps_netkit = [
    ("1. Pod 네임스페이스", "netkit peer 장치", "조기 eBPF 훅 실행", OK),
    ("2. 호스트 제어 분리", "primary 장치 제어", "Pod 변조 방지 격리", INFO),
    ("3. 스택 / 큐 우회", "물리 장치로 바로 전달", "L3 직결 · 백로그 큐 생략", OK),
    ("4. 물리 장치 직결", "물리 NIC / 다음 홉", "네임스페이스 전환 비용 감소", ACC),
]

for i, (t1, t2, sub, tone) in enumerate(steps_netkit):
    x = X_BASE + i * (BOX_W + GAP)
    if tone == ACC:
        d.tone(x, Y2 + 22, BOX_W, BOX_H, ACC, r=4, op="14", sw=1.3)
    elif tone == OK:
        d.tone(x, Y2 + 22, BOX_W, BOX_H, OK, r=4, op="10", sw=1.0)
    elif tone == INFO:
        d.tone(x, Y2 + 22, BOX_W, BOX_H, INFO, r=4, op="10", sw=0.9)
    else:
        d.box(x, Y2 + 22, BOX_W, BOX_H, PAPER, RULE, 0.8, r=4)
    col = ACC if tone == ACC else (OK if tone == OK else (INFO if tone == INFO else INK))
    d.t(x + 12, Y2 + 42, t1, 12, col, KR, "start", 600)
    d.t(x + 12, Y2 + 62, t2, 11, col, MONO, "start")
    d.t(x + 12, Y2 + 82, sub, 11, MUTED, KR, "start")
    if i < 3:
        d.arrow([(x + BOX_W + 4, Y2 + 62), (x + BOX_W + GAP - 4, Y2 + 62)], OK, "ok", 1.2)

# 범례
LEG_Y = 432
d.legend(LEG_Y, [("veth 병목 단계", WARN), ("netkit 조기 훅 및 우회", OK), ("호스트 제어 장치 분리", INFO), ("직결 최적화 완성", ACC)])
d.save("08-02.netkit-comparison.svg")

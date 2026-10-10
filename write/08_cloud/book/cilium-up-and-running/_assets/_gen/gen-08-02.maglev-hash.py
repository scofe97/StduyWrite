# 타입 스펙: type-data-flow — ECMP 로 분기된 두 진입 노드가 공유 상태 없이 독립적인 Maglev 해시로 동일한 백엔드를 선택하는 데이터 흐름.
# 사실 출처: Cilium Up and Running 8장 cil8.txt 줄 1011-1028(5-튜플·무상태 일관 해시), 줄 1124(테이블 크기 16381), 줄 1132-1144(FRR 172.18.0.8 및 worker3·worker4 ECMP 분기), 줄 1198-1208(포트 60001 에코 파드 매핑)
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 500
d = D(W, H, "CILIUM UP AND RUNNING · 08-02 §2", "ECMP 분기 환경의 Maglev 일관 해시 흐름",
      "FRR ECMP 로 진입 노드가 갈려도 동일한 5-튜플은 같은 백엔드 파드를 선택한다",
      "노드 간 동기화 없이 소수 크기 룩업 테이블로 동일 백엔드를 산출해 TCP 리셋을 줄입니다")

# 1. 외부 BGP / FRR 라우터 (좌측)
RX0, RY0, RW0, RH0 = 32, 170, 180, 150
d.box(RX0, RY0, RW0, RH0, PAPER2, RULE, 1.0, r=6)
d.t(RX0 + RW0 / 2, RY0 + 30, "FRR 라우터", 13, INK, KR, "middle", 600)
d.t(RX0 + RW0 / 2, RY0 + 50, "172.18.0.8 (BGP 피어)", 11, MUTED, MONO)
d.chip(RX0 + RW0 / 2, RY0 + 84, "ECMP 경로 분기", OK, 12)
d.t(RX0 + RW0 / 2, RY0 + 118, "목적지 192.168.100.0/32", 11, INK, MONO)
d.t(RX0 + RW0 / 2, RY0 + 138, "동일 5-튜플 (포트 60001)", 12, MUTED, KR)

# 2. 중간: 진입 노드 둘 (kind-worker3, kind-worker4)
NX, NW, NH = 264, 296, 112
NY1, NY2 = 120, 276

# 노드 1 (kind-worker3)
d.box(NX, NY1, NW, NH, PAPER2, RULE, 1.0, r=6)
d.t(NX + 16, NY1 + 24, "진입 노드 A", 13, INK, KR, "start", 600)
d.t(NX + NW - 16, NY1 + 24, "via 172.18.0.2", 11, MUTED, MONO, "end")
d.tone(NX + 14, NY1 + 42, NW - 28, 52, INFO, r=4, op="10", sw=0.9)
d.t(NX + NW / 2, NY1 + 64, "Maglev 해시 룩업 (크기 16381)", 12, INFO, KR, "middle", 600)
d.t(NX + NW / 2, NY1 + 84, "5-튜플 해시 산출 → 슬롯 매핑", 12, MUTED, KR)

# 노드 2 (kind-worker4)
d.box(NX, NY2, NW, NH, PAPER2, RULE, 1.0, r=6)
d.t(NX + 16, NY2 + 24, "진입 노드 B", 13, INK, KR, "start", 600)
d.t(NX + NW - 16, NY2 + 24, "via 172.18.0.3", 11, MUTED, MONO, "end")
d.tone(NX + 14, NY2 + 42, NW - 28, 52, INFO, r=4, op="10", sw=0.9)
d.t(NX + NW / 2, NY2 + 64, "Maglev 해시 룩업 (크기 16381)", 12, INFO, KR, "middle", 600)
d.t(NX + NW / 2, NY2 + 84, "동일 테이블 · 동일 해시 알고리즘", 12, MUTED, KR)

# 3. 우측: 백엔드 파드
BX, BW, BH = 616, 272, 92
BY1, BY2 = 130, 286

# 백엔드 Pod 1 (선택됨)
d.tone(BX, BY1, BW, BH, ACC, r=6, op="14", sw=1.3)
d.t(BX + 16, BY1 + 26, "백엔드 Pod 1 (선택됨)", 13, ACC, KR, "start", 600)
d.t(BX + 16, BY1 + 48, "echo-f69bb6cf9-42hmc", 12, INK, MONO, "start")
d.t(BX + 16, BY1 + 70, "DSR·같은 hashSeed 일 때 TCP 유지", 12, OK, KR, "start")

# 백엔드 Pod 2 (미선택)
d.box(BX, BY2, BW, BH, PAPER2, RULE, 0.8, r=6)
d.t(BX + 16, BY2 + 26, "백엔드 Pod 2", 13, SOFT, KR, "start", 600)
d.t(BX + 16, BY2 + 48, "echo-f69bb6cf9-nscx5", 12, MUTED, MONO, "start")
d.t(BX + 16, BY2 + 70, "무작위 방식 시 오선택 → RST 발생", 12, MUTED, KR, "start")

# 직교 연결선 (Orthogonal paths)
MID_X1 = 238
# FRR -> worker3
d.path(f"M {RX0 + RW0} {RY0 + 40} H {MID_X1} V {NY1 + 54} H {NX}", OK, 1.4, m="ok")
# FRR -> worker4
d.path(f"M {RX0 + RW0} {RY0 + 110} H {MID_X1} V {NY2 + 54} H {NX}", OK, 1.4, m="ok")

MID_X2 = 588
# worker3 -> Backend Pod 1
d.path(f"M {NX + NW} {NY1 + 66} H {MID_X2} V {BY1 + 40} H {BX}", ACC, 1.5, m="acc")

# worker4 -> Backend Pod 1 (동일 백엔드 선택!)
d.path(f"M {NX + NW} {NY2 + 66} H {MID_X2} V {BY1 + 60} H {BX}", ACC, 1.5, m="acc")

# 범례
LEG_Y = 432
d.legend(LEG_Y, [("ECMP 트래픽 분기", OK), ("Maglev 해시 연산", INFO), ("동일 백엔드 결정", ACC)])
d.save("08-02.maglev-hash.svg")

# 타입 스펙: type-sequence — 클러스터 A 의 K8s API·API Server·로컬 etcd 와 클러스터 B 의 KVStoreMesh·로컬 etcd·cilium-agent 간 상태 복제 시퀀스.
# 사실 출처: Cilium Up and Running 9장 cil9.txt 줄 315-328(Cluster Mesh API Server 내부 동작), 줄 538-545(KVStoreMesh 역할) / docs.cilium.io v1.20 clustermesh/intro
import sys
sys.path.insert(0, ".")
from dd import D, Seq, ACC, OK, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 540
d = Seq(W, H, "CILIUM UP AND RUNNING · 09-01 §2", "원격 클러스터 메타데이터 동기화 시퀀스",
        "상대 etcd 에서 읽어 로컬 etcd 에 캐시하고 로컬 에이전트가 eBPF 맵에 반영한다",
        "KVStoreMesh 가 중계하여 에이전트의 원격 클러스터 직접 연결 부하를 없앱니다")

LANES = [
    ("K8s API (A)", "kube-apiserver"),
    ("API 서버 (A)", "apiserver + etcd"),
    ("KVStoreMesh (B)", "원격 캐시 수집기"),
    ("로컬 etcd (B)", "단일 인스턴스 캐시"),
    ("에이전트 (B)", "cilium-agent"),
]

xs = [80, 250, 430, 610, 790]
d.LX = {}
for (nm, sub), x in zip(LANES, xs):
    d.LX[nm] = x
    d.box(x - 72, 104, 144, 48, PAPER2, RULE, 1.0)
    d.t(x, 126, nm, 12, INK, KR, "middle", 600)
    d.t(x, 143, sub, 11, MUTED, MONO)

d.lane_top = 152
d.rails(464)

L1, L2, L3, L4, L5 = [name for name, _ in LANES]

# Step 1: K8s API -> Cluster A API 서버
d.msg(L1, L2, "Watch 이벤트 수신", 184, INFO, "info")
d.t((d.LX[L1] + d.LX[L2]) / 2, 200, "엔드포인트 · 신원 변경", 11, MUTED, KR, "middle")

# Step 2: Cluster A API 서버 로컬 etcd 보관
d.selfmsg(L2, "로컬 etcd 에 보관", 228, INFO, "메모리 캐시 보관")

# Step 3: Cluster B KVStoreMesh -> Cluster A etcd mTLS 조회
d.msg(L3, L2, "32379/TCP mTLS 조회", 276, ACC, "acc")
d.t((d.LX[L3] + d.LX[L2]) / 2, 292, "원격 메타데이터 동기화 요청", 11, MUTED, KR, "middle")

# Step 4: Cluster A -> Cluster B 메타데이터 스트림 반환
d.msg(L2, L3, "엔드포인트 · 신원 스트림", 328, ACC, "acc", dash="4 4")
d.t((d.LX[L3] + d.LX[L2]) / 2, 344, "TLS 상호 인증 완료", 11, MUTED, KR, "middle")

# Step 5: KVStoreMesh -> 로컬 etcd 캐시
d.msg(L3, L4, "로컬 etcd 캐시 기록", 380, OK, "ok")
d.t((d.LX[L3] + d.LX[L4]) / 2, 396, "원격 클러스터 상태 복제", 11, MUTED, KR, "middle")

# Step 6: 에이전트 -> 로컬 etcd 감지 & BPF 맵 갱신
d.msg(L5, L4, "로컬 etcd Watch", 428, MUTED, "ar", dash="4 4")
d.state(L5, "eBPF 맵 갱신", 454, OK)

d.legend(488, [
    ("로컬 K8s 이벤트", INFO),
    ("원격 mTLS 동기화", ACC),
    ("로컬 캐시 및 eBPF 갱신", OK),
])
d.save("09-01.metadata-sync-sequence.svg")

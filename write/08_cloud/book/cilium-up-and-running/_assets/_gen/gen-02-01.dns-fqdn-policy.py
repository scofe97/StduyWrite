# 타입 스펙: type-sequence — Pod 의 DNS 질의 가로채기와 FQDN 보안 정책 eBPF 반영 시퀀스.
# 사실 출처: Cilium Up and Running 2장 The DNS Proxy.
import sys
sys.path.insert(0, ".")
from dd import Seq, ACC, OK, WARN, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 526
s = Seq(W, H, "CILIUM UP AND RUNNING · 02-01 §6", "DNS 질의 가로채기와 FQDN 정책 반영",
        "DNS 프록시가 해석한 도메인 응답 IP 를 eBPF 맵에 등록해 L4 연결을 허용하는 과정",
        "도메인 질의 응답 IP 를 동적으로 BPF 맵에 매핑해 L4 연결을 커널에서 허용합니다")

s.lanes([
    ("애플리케이션 Pod", "클라이언트 워크로드"),
    ("eBPF 데이터패스", "tc / 소켓 계층"),
    ("DNS 프록시", "에이전트 내장"),
    ("CoreDNS", "클러스터 DNS :53"),
], y0=104, lane_w=190)

s.rails(ybot=454)

# 메시지 시퀀스
s.msg("애플리케이션 Pod", "eBPF 데이터패스", "1. DNS 질의 전송 (UDP 53)", 168, INFO, "info", sub="api.example.com 주소 확인 요청")
s.msg("eBPF 데이터패스", "DNS 프록시", "2. 소켓 가로채기 (TPROXY)", 212, ACC, "acc", sub="로컬 DNS 프록시로 투명 리다이렉트")
s.msg("DNS 프록시", "CoreDNS", "3. 업스트림 질의 중계", 256, WARN, "warn", sub="CoreDNS 로 원본 패킷 전달")
s.msg("CoreDNS", "DNS 프록시", "4. DNS 응답 수신", 300, OK, "ok", dash="3 3", sub="IP: 93.184.216.34 (A 레코드)")
s.msg("DNS 프록시", "eBPF 데이터패스", "5. BPF 맵 원자적 갱신", 344, ACC, "acc", sub="ipcache_v2 신원 매핑 · 정책 맵 허용")

# 6단계: DNS 응답 반환 (화살표는 전체 연결, 라벨은 eBPF 생명선 간섭을 피해 Pod-eBPF 구간에 배치)
x_pod, x_dns = s.LX["애플리케이션 Pod"], s.LX["DNS 프록시"]
s.path(f"M {x_dns-10} 388 L {x_pod+12} 388", INFO, 1.5, m="info", dash="3 3")
mx_span1 = (x_pod + s.LX["eBPF 데이터패스"]) / 2
s.t(mx_span1, 388 - 9, "6. 최종 DNS 응답 전달", 11, INFO, KR, "middle", 600)
s.t(mx_span1, 388 + 17, "Pod 로 해석된 IP 주소 반환", 11, MUTED, KR, "middle")

s.msg("애플리케이션 Pod", "eBPF 데이터패스", "7. 목적지 HTTPS 통신", 432, OK, "ok", sub="ipcache_v2(LPM 트라이) 및 정책 검증")

# 범례
s.legend(476, [
    ("DNS 질의·응답", INFO),
    ("eBPF 가로채기·맵 반영 (핵심)", ACC),
    ("업스트림 중계", WARN),
    ("인증된 데이터패스 통과", OK),
])

s.save("02-01.dns-fqdn-policy.svg")

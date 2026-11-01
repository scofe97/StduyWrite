# 타입 스펙: type-sequence — Pod 의 DNS 질의 가로채기와 FQDN 보안 정책 eBPF 반영 시퀀스.
# 사실 출처: 《Cilium: Up and Running》 Ch.2 p.13 ("The DNS Proxy") 및 본문 §6 L228~233.
# 단계 번호는 본문 목록 1~6 과 같다(본문 3 의 중계와 응답 확인을 화살표 둘로 그리고 응답 쪽은 번호를 달지 않는다).
# api.github.com 은 본문 L224 의 예 값이다.
import sys
sys.path.insert(0, ".")
from dd import Seq, ACC, OK, WARN, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

class KoreanSeq(Seq):
    def lanes(s, names, y0=104, lane_w=210):
        s.LX = {}
        n = len(names)
        span = (s.w - 48 - 24) - lane_w
        for i, (nm, sub) in enumerate(names):
            x = 24 + lane_w / 2 + (span * i / (n - 1) if n > 1 else 0)
            s.LX[nm] = x
            s.box(x - lane_w / 2, y0, lane_w, 44, PAPER2, RULE, 1.0)
            nm_fam = KR if any('가' <= ch <= '힣' for ch in str(nm)) else MONO
            s.t(x, y0 + 20, nm, 12, INK, nm_fam, "middle", 600)
            sub_fam = KR if any('가' <= ch <= '힣' for ch in str(sub)) else MONO
            s.t(x, y0 + 37, sub, 11, MUTED, sub_fam)
        s.lane_top = y0 + 44
        return s.LX

    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]
        d = 1 if x2 > x1 else -1
        s.path(f"M {x1+10*d} {y} L {x2-12*d} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        fam = KR if any('가' <= ch <= '힣' for ch in str(label)) else MONO
        s.t(mx, y - 9, label, 11, c, fam, "middle", 600)
        if sub:
            sub_fam = KR if any('가' <= ch <= '힣' for ch in str(sub)) else MONO
            s.t(mx, y + 17, sub, 11, MUTED, sub_fam)

W, H = 920, 526
s = KoreanSeq(W, H, "CILIUM UP AND RUNNING · 02-01 §6", "DNS 질의 가로채기와 FQDN 정책 반영",
             "DNS 프록시가 해석한 도메인 응답 IP 를 eBPF 맵에 등록해 L4 연결을 허용하는 과정",
             "도메인 질의 응답 IP 의 동적 BPF 맵 매핑과 커널 L4 연결 허용 시퀀스")

s.lanes([
    ("애플리케이션 Pod", "클라이언트 워크로드"),
    ("eBPF 데이터패스", "커널"),
    ("DNS 프록시", "에이전트 내장"),
    ("CoreDNS", "클러스터 DNS :53"),
], y0=104, lane_w=190)

s.rails(ybot=454)

# 메시지 시퀀스
s.msg("애플리케이션 Pod", "eBPF 데이터패스", "1. DNS 질의 (UDP/TCP 53)", 168, INFO, "info", sub="api.github.com 해석 요청")
s.msg("eBPF 데이터패스", "DNS 프록시", "2. 패킷 가로채기", 212, ACC, "acc", sub="에이전트 로컬 DNS 프록시로 전달")
s.msg("DNS 프록시", "CoreDNS", "3. 업스트림 질의 중계", 256, WARN, "warn")
s.msg("CoreDNS", "DNS 프록시", "응답 IP 확인", 300, WARN, "warn", dash="3 3")
s.msg("DNS 프록시", "eBPF 데이터패스", "4. 응답 IP 에 보안 신원 기록", 344, ACC, "acc", sub="cilium_ipcache_v2 · 정책 맵은 보통 그대로")

# 5단계: DNS 응답 반환 (화살표는 전체 연결, 라벨은 eBPF 생명선 간섭을 피해 Pod-eBPF 구간에 배치)
x_pod, x_dns = s.LX["애플리케이션 Pod"], s.LX["DNS 프록시"]
s.path(f"M {x_dns-10} 388 L {x_pod+12} 388", INFO, 1.5, m="info", dash="3 3")
mx_span1 = (x_pod + s.LX["eBPF 데이터패스"]) / 2
s.t(mx_span1, 388 - 9, "5. 원래 DNS 응답 반환", 11, INFO, KR, "middle", 600)

s.msg("애플리케이션 Pod", "eBPF 데이터패스", "6. 해석된 IP 로 패킷 전송", 432, OK, "ok", sub="cilium_ipcache_v2 신원 조회 · 정책 맵 확인")

# 범례
s.legend(476, [
    ("DNS 질의·응답", INFO),
    ("eBPF 가로채기·맵 기록 (핵심)", ACC),
    ("업스트림 중계·응답", WARN),
    ("정책 허용 뒤 전송", OK),
])

s.save("02-01.dns-fqdn-policy.svg")

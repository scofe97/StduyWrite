# 타입 스펙: type-sequence — Pod 생성 시 컨테이너 런타임과 Cilium CNI 플러그인·에이전트 호출 흐름.
# 사실 출처: 《Cilium: Up and Running》 Ch.2 p.6-7 (Figure 2-3 "Pod creation workflow and CNI integration") 및 본문 §3 L131~137.
# 단계 번호는 본문 목록 1~7 과 같다. containerd·CRI-O 는 원서 p.6, veth(또는 netkit)·lxc...·맵 이름은 본문 L133·L135.
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

W, H = 920, 530
s = KoreanSeq(W, H, "CILIUM UP AND RUNNING · 02-01 §3", "Pod 생성 시 CNI 네트워크 연결 흐름",
             "kubelet 과 런타임에서 cilium-cni 바이너리 및 cilium-agent 로 이어지는 배선 시퀀스",
             "런타임의 CNI 바이너리 호출과 로컬 에이전트 소켓 위임 시퀀스")

s.lanes([
    ("컨테이너 런타임", "containerd / CRI-O"),
    ("cilium-cni", "/opt/cni/bin/"),
    ("cilium-agent", "cilium.sock"),
    ("리눅스 커널", "netns & eBPF 맵"),
], y0=104, lane_w=190)

s.rails(ybot=466)

# 메시지 흐름
s.msg("컨테이너 런타임", "cilium-cni", "1. CNI ADD 실행", 168, INFO, "info", sub="NetNS 생성 뒤 설정 전달")
s.msg("cilium-cni", "cilium-agent", "2. IPAM IP 할당 요청", 214, ACC, "acc", sub="UDS REST API 로 Pod IP 요청")
s.msg("cilium-cni", "리눅스 커널", "3. veth(또는 netkit) 쌍 생성", 260, OK, "ok", sub="호스트 lxc... · Pod 쪽 주소와 라우트")
s.msg("cilium-cni", "cilium-agent", "4. EndpointCreate 요청", 306, ACC, "acc", sub="UDS REST 로 엔드포인트 생성 위임")
s.msg("cilium-agent", "리눅스 커널", "5. eBPF 적재 및 맵 등록", 352, OK, "ok", sub="cilium_lxc · cilium_ipcache_v2")
s.msg("cilium-agent", "cilium-cni", "6. 엔드포인트 등록 결과 응답", 398, MUTED, "ar", dash="3 3")
s.msg("cilium-cni", "컨테이너 런타임", "7. CNI Result JSON 반환", 444, MUTED, "ar", dash="3 3")

# 범례
s.legend(484, [
    ("런타임 호출", INFO),
    ("로컬 REST 위임 (핵심)", ACC),
    ("커널 인터페이스 배선", OK),
    ("완료 응답 반환", MUTED),
])

s.save("02-01.pod-creation-cni.svg")

# a0-02 §5 다섯 파일이 각각 답하는 것.
# 값 근거(본문 §5 · 부록 E):
#   - istioctl x workload entry configure --name forum --namespace forum-services --clusterID "west-cluster" --autoregister
#   - hosts: istiod.istio-system.svc -> 동서 게이트웨이 IP (--ingressService · --ingressIP).
#   - istio-token: 수명 짧은 토큰(기본 1시간, --tokenDuration).
#   - root-cert.pem: 루트 CA 공개 인증서.
#   - cluster.env: 네임스페이스·서비스 어카운트·망·그룹 메타데이터(메시·클러스터·망 식별자 포함).
#   - mesh.yaml: discoveryAddress 와 준비 프로브 설정.
# 타입 스펙: type-tree — 한 명령이 만든 산출물이 질문별로 갈리는 계층.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, INK, PAPER2, RULE, KR, MONO

W, H = 960, 480
d = D(W, H, "ISTIO IN ACTION · A0-02 §5",
      "한 명령이 만든 다섯 파일이 각각 다른 질문에 답한다",
      "istioctl x workload entry configure 가 만들어 준 파일 다섯은 역할이 겹치지 않는다. "
      "코랄색으로 표시한 cluster.env 가 다음 절에서 열 파일이다.",
      lead="설정 양이 많아 손으로 작성하면 시행착오가 커서 istioctl 이 한 번에 생성합니다.")

RW, RH = 356, 64
d.box(302, 116, RW, RH, PAPER2, RULE, 1.0, 6)
d.t(302 + RW / 2, 142, "istioctl x workload entry configure", 13, INK, MONO, "middle", 600)
d.t(302 + RW / 2, 164, "--autoregister -o ./ch13/workload-files/", 12, MUTED, MONO)

LW, LH, LY = 172, 116, 268
FILES = [
    (24,  "hosts",         "어디로 붙나",     "동서 게이트웨이 IP", "--ingressIP"),
    (208, "istio-token",   "누구인가",        "수명 짧은 토큰 1시간", "--tokenDuration"),
    (392, "root-cert.pem", "무엇을 믿나",     "루트 CA 공개 인증서", "컨트롤 플레인 검증"),
    (576, "cluster.env",   "어떤 메타데이터", "네임스페이스·망·그룹", "메시·클러스터·망"),
    (760, "mesh.yaml",     "어떻게 준비 판정", "discoveryAddress", "준비 프로브 설정"),
]
BUS = 224
d.path(f"M 480 {116 + RH} L 480 {BUS}", MUTED, 1.3)
d.path(f"M {24 + LW / 2} {BUS} L {760 + LW / 2} {BUS}", MUTED, 1.3)

for i, (x, name, q, sub, opt) in enumerate(FILES):
    focal = (i == 3)
    d.arrow([(x + LW / 2, BUS), (x + LW / 2, LY - 2)], ACC if focal else MUTED, "acc" if focal else "ar", 1.3)
    if focal:
        d.tone(x, LY, LW, LH, ACC, 6, "14", 1.4)
    else:
        d.box(x, LY, LW, LH, PAPER2, RULE, 1.0, 6)
    d.t(x + 12, LY + 26, name, 13, ACC if focal else INK, MONO, "start", 600)
    d.t(x + 12, LY + 52, q, 13, ACC if focal else INK, KR, "start", 600)
    d.t(x + 12, LY + 76, sub, 13, MUTED, KR if any("가" <= c <= "힣" for c in sub) else MONO, "start")
    d.t(x + 12, LY + 98, opt, 12, MUTED, KR if any("가" <= c <= "힣" for c in opt) else MONO, "start")

d.legend(420, [("다음 절에서 여는 파일", ACC), ("나머지 파일 넷", MUTED)])
d.save("a0-02.vm-files.svg")
print("ok vm-files")

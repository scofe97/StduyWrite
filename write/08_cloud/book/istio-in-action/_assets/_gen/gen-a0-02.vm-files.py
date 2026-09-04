# a0-02 §5 다섯 파일이 각각 답하는 것.
# 본문(부록 E): hosts 는 istiod.istio-system.svc 를 동서 게이트웨이 IP 로 풀고(--ingressService ·
#       --ingressIP), istio-token 은 수명 짧은 토큰(기본 1시간, --tokenDuration), root-cert.pem 은
#       루트 CA 공개 인증서, cluster.env 는 메타데이터, mesh.yaml 은 디스커버리 주소와 준비 프로브.
# 타입 스펙: type-tree — 한 명령이 만든 산출물이 질문별로 갈리는 계층이 논점이다. 루트 하나에서
#           가지를 내리고 잎에 한 줄 설명을 단다.
#           축약: 목적지(13 장 config-transfer 가 이미 보인 것)는 그리지 않고 파일이 답하는 질문만 둔다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 1000, 560
d = D(W, H, "ISTIO IN ACTION · A0-02 §5",
      "한 명령이 만든 다섯이 각각 다른 질문에 답한다",
      "istioctl 이 만들어 준 파일 다섯은 목적이 겹치지 않는다. 어디로 붙나 · 누구인가 · 무엇을 믿나 · "
      "어떤 메타데이터를 지나 · 어떻게 준비를 판정하나. 색이 붙은 것이 다음 절에서 여는 파일이다.",
      "13 장이 목적지를 보였다면 이 도식은 각각이 답하는 질문을 봅니다")

RW, RH = 320, 60
d.box(340, 128, RW, RH, PAPER2, RULE, 1.0, 6)
d.t(340 + RW / 2, 154, "istioctl x workload entry configure", 12, INK, MONO, "middle", 600)
d.t(340 + RW / 2, 174, "--autoregister -o ./ch13/workload-files/", 11, MUTED, MONO)

LW, LH, LY = 176, 100, 296
FILES = [
    (28, "hosts", "어디로 붙나", "동서 게이트웨이 IP 로 푼다", False),
    (220, "istio-token", "누구인가", "수명 짧은 토큰 · 기본 1시간", False),
    (412, "root-cert.pem", "무엇을 믿나", "루트 CA 의 공개 인증서", False),
    (604, "cluster.env", "어떤 메타데이터", "네임스페이스 · 망 · 그룹", True),
    (796, "mesh.yaml", "어떻게 준비 판정", "디스커버리 주소와 프로브", False),
]
BUS = 240
d.path(f"M 500 {128 + RH} L 500 {BUS}", MUTED, 1.3)
d.path(f"M 116 {BUS} L 884 {BUS}", MUTED, 1.3)
for x, name, q, sub, focal in FILES:
    d.arrow([(x + LW / 2, BUS), (x + LW / 2, LY - 2)], MUTED, "ar", 1.3)
    if focal:
        d.o.append(f'<rect x="{x}" y="{LY}" width="{LW}" height="{LH}" rx="6" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, LY, LW, LH, PAPER2, RULE, 1.0, 6)
    d.t(x + 14, LY + 26, name, 12, ACC if focal else INK, MONO, "start", 600)
    d.t(x + 14, LY + 52, q, 12, ACC if focal else INK, KR, "start", 600)
    d.t(x + 14, LY + 76, sub, 11, MUTED, KR, "start")

d.t(28, 452, "hosts 의 기본값은 istio-eastwestgateway 의 IP — --ingressService 로 이름을, --ingressIP 로 IP 를 바꾼다", 11, SOFT, KR, "start")
d.t(28, 476, "istio-token 의 수명은 --tokenDuration 으로 바꾼다. 설정 양이 많아 손으로 짜면 시행착오가 크다", 11, MUTED, KR, "start")
d.legend(500, [("다음 절에서 여는 파일", ACC), ("나머지 넷", MUTED)])
d.save("a0-02.vm-files.svg")

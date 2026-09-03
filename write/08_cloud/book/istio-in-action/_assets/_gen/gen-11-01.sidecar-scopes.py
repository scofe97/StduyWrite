# 11-01 §6 Sidecar 설정의 세 스코프 — 원문의 "Sidecar configuration scopes" 상자.
# 본문(원문 11.3.2): 메시 전역 사이드카는 메시 안의 모든 워크로드에 적용되며 Istio 설치 네임스페이스
#       (여기서는 istio-system)에 두고 관례상 이름을 default 로 한다. 네임스페이스 사이드카는 더 구체적이라
#       메시 전역을 덮어쓰며, 원하는 네임스페이스에 workloadSelector 없이 두고 이름은 역시 default 다.
#       워크로드 사이드카는 workloadSelector 로 대상을 고르며 가장 구체적이라 앞의 둘을 모두 덮어쓴다.
# 안쪽으로 갈수록 구체적이고 바깥을 덮어쓴다 — 그래서 포함 관계로 그린다.
# 타입 스펙: type-nested — 포함으로 표현하는 계층. 링 3(3~5), 안쪽으로 갈수록 획이 진해지고 채움이 짙어진다.
#           링 라벨은 왼쪽 위 종이색 마스크 위 mono eyebrow, coral 은 가장 안쪽 초점 하나에만.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, RULE, KR, MONO

W, H = 1000, 640
d = D(W, H, "ISTIO IN ACTION · 11-01 §6",
      "안쪽이 바깥을 덮어쓴다",
      "Sidecar 설정은 세 스코프로 놓이고 안쪽이 더 구체적이라 바깥을 덮어쓴다. 색이 붙은 가장 안쪽이 "
      "workloadSelector 로 대상을 고르는 자리이고, 나머지 둘은 이름을 default 로 두는 관례를 따른다.",
      "메시 전역 하나를 깔아 두면 나머지는 팀이 자기 것만 좁히면 됩니다")

def ring(x, y, w, h, tag, sub, stroke, fill, focal=False):
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fill}" '
               f'stroke="{stroke}" stroke-width="{1.4 if focal else 1.0}"/>')
    tw = len(tag) * 6 + 16
    d.o.append(f'<rect x="{x + 20}" y="{y - 7}" width="{tw}" height="14" fill="{PAPER}"/>')
    d.t(x + 28, y + 3, tag, 8, ACC if focal else SOFT, MONO, "start", 600)
    d.t(x + 28, y + 30, sub, 11, ACC if focal else MUTED, KR, "start")

ring(64, 128, 876, 372, "MESH-WIDE · NAMESPACE ISTIO-SYSTEM", "이름은 default · 메시 전체의 기본값", f"{INK}30", f"{INK}04")
ring(100, 184, 800, 280, "NAMESPACE-WIDE · WORKLOADSELECTOR 없음", "이름은 default · 그 네임스페이스를 덮어쓴다", MUTED, f"{INK}07")
ring(136, 240, 724, 184, "WORKLOAD-SPECIFIC · WORKLOADSELECTOR 있음", "가장 구체적이라 앞의 둘을 덮어쓴다", ACC, f"{ACC}0E", focal=True)

fields = [("egress", "어디로 나갈 수 있나"),
          ("ingress", "생략하면 파드에서 유추"),
          ("outboundTrafficPolicy", "REGISTRY_ONLY · ALLOW_ANY")]
for i, (name, sub) in enumerate(fields):
    x = 196 + i * 268
    d.o.append(f'<rect x="{x}" y="{316}" width="248" height="64" rx="6" fill="{ACC}10" stroke="{ACC}66" stroke-width="1"/>')
    d.t(x + 124, 342, name, 12, INK, MONO, "middle", 600)
    d.t(x + 124, 364, sub, 11, MUTED, KR)

d.t(28, 528, "egress 를 적어 두면 컨트롤 플레인이 그 워크로드에 필요한 설정만 골라 내려보낸다", 11, SOFT, KR, "start")
d.t(28, 552, "메시 전역으로 istio-system 만 허용하면 catalog 의 설정이 2MB 에서 644K 로 줄어든다", 11, MUTED, KR, "start")
d.t(28, 576, "이미 도는 클러스터라면 팀이 자기 egress 를 먼저 적게 한 뒤에 전역 기본값을 깐다", 11, SOFT, KR, "start")
d.legend(600, [("가장 구체적인 스코프", ACC), ("그것이 덮어쓰는 스코프", MUTED)])
d.save("11-01.sidecar-scopes.svg")

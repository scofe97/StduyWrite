# 20-01 §정책은 둘로 나뉩니다
# 본문이 분리의 *이유* 를 말한다 — "Rego 의 내부 동작을 관리자에게서 감추고 구조화된 API 를
# 내놓는다". 그러니 두 리소스를 나란한 카드로 놓으면 논지가 안 산다. 한쪽이 다른 쪽을
# *만들어 낸다* 는 방향이 있어야 하고, 두 역할(쓰는 사람 / 적용하는 사람)이 갈려야 한다.
# 가운데 화살표에 "kind 를 만들어 낸다" 를 얹어, K8sAllowedRepos 라는 이름이 왼쪽에서
# 정의돼 오른쪽에서 쓰이는 것이 눈으로 이어지게 한다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, MUTED, SOFT, INK, PAPER2, PAPER, RULE, INFO, KR, MONO
import ddx

W, H = 1240, 572
d = D(W, H, "KUBERNETES UP AND RUNNING · 20-01",
      "정책을 쓰는 일과 적용하는 일을 갈라 놓는다",
      "템플릿이 Rego 와 파라미터 스키마를 담아 새 kind 를 만들어 내고, 제약이 그 kind 를 "
      "파라미터와 범위로 인스턴스화한다.",
      "이 분리 덕분에 Rego 를 모르는 관리자도 정책을 적용하고, 템플릿을 조직 사이에 공유한다")

LW, RW = 546, 546
LX, RX = 24, 670
Y0, CH = 138, 300

for x, w, (eb, kind, who, rows, c) in zip((LX, RX), (LW, RW), [
    ("정책을 쓴다", "ConstraintTemplate", "보통 커뮤니티·플랫폼 팀",
     [("apiVersion", "templates.gatekeeper.sh/v1beta1"),
      ("spec.crd.spec.names.kind", "K8sAllowedRepos"),
      ("spec.crd.spec.validation", "파라미터 openAPIV3Schema"),
      ("spec.targets[].rego", "위반 판정과 msg 문구")], INFO),
    ("정책을 적용한다", "K8sAllowedRepos", "클러스터 관리자",
     [("apiVersion", "constraints.gatekeeper.sh/v1beta1"),
      ("kind", "템플릿이 만들어 낸 이름"),
      ("spec.match", "kinds · namespaces 로 범위"),
      ("spec.parameters", "repos: [gcr.io/kuar-demo/]")], ACC)]):
    d.box(x, Y0, w, CH, PAPER2, c, 1.3, 8)
    d.t(x + 20, Y0 + 28, eb, 12, c, KR, "start", 600)
    d.t(x + w - 20, Y0 + 28, who, 10, SOFT, KR, "end")
    d.t(x + 20, Y0 + 52, kind, 14, INK, MONO, "start", 600)
    d.line(x + 20, Y0 + 66, x + w - 20, Y0 + 66, RULE, 0.8)
    for j, (k, v) in enumerate(rows):
        yy = Y0 + 84 + j * 50
        d.box(x + 20, yy, w - 40, 42, PAPER, RULE, 0.8, 5)
        d.t(x + 34, yy + 18, ddx.fit(k, 10, w - 68, k), 10, c, MONO, "start")
        d.t(x + 34, yy + 34, ddx.fit(v, 10, w - 68, v), 10, MUTED, KR, "start")

MX = (LX + LW + RX) / 2
d.arrow([(LX + LW + 6, Y0 + CH / 2), (RX - 8, Y0 + CH / 2)], ACC, "acc", 1.6)
d.chip(MX, Y0 + CH / 2 - 22, "새 kind 를 만들어 낸다", ACC, 10)
d.t(MX, Y0 + CH / 2 + 30, "Rego 는 왼쪽에만 있다", 10, SOFT, KR)

BY = Y0 + CH + 28
d.line(24, BY, W - 48, BY, RULE, 0.8)
d.t(24, BY + 24, "한 템플릿에 여러 제약을 걸 수 있다. 팀마다 허용 레지스트리가 다르면 "
                 "제약만 여럿 만들고 Rego 는 하나로 둔다.", 11, MUTED, KR, "start")
d.legend(BY + 40, [("템플릿 — 쓰는 쪽", INFO), ("제약 — 적용하는 쪽", ACC)])
d.save("../20-01.template-constraint-split.svg")
print("필요 h:", BY + 40 + 48, "· 실제:", H)

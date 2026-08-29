# 20-01 §정책은 둘로 나뉩니다
# 본문이 분리의 *이유* 를 말한다 — "Rego 의 내부 동작을 관리자에게서 감추고 구조화된 API 를
# 내놓는다". 그러니 두 리소스를 나란한 카드로 놓으면 논지가 안 산다. 한쪽이 다른 쪽을
# *만들어 낸다* 는 방향이 있어야 하고, 두 역할(쓰는 사람 / 적용하는 사람)이 갈려야 한다.
# 가운데 화살표에 "kind 를 만들어 낸다" 를 얹어, K8sAllowedRepos 라는 이름이 왼쪽에서
# 정의돼 오른쪽에서 쓰이는 것이 눈으로 이어지게 한다.
# 타입 스펙: type-er.md — 두 엔티티가 정본의 두 단 상자(머리 = 종류 이름, 몸통 = 필드 목록)이고
#           그 사이를 관계선 하나가 라벨("새 kind 를 만들어 낸다")과 함께 잇는다. 본문의 논지가
#           "한쪽이 다른 쪽을 만들어 낸다" 는 방향이므로 나란한 카드가 아니라 관계여야 한다.
#           어긋나는 지점: 관계 양 끝의 카디널리티 표기가 없다. 아래 주석이 적는 1:N
#           ("한 템플릿에 여러 제약")이 정본대로면 선 끝에 붙어야 하는 정보다 — 산문에만 있다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, MUTED, SOFT, INK, PAPER2, PAPER, RULE, INFO, KR, MONO
import ddx

W, H = 1240, 572
d = D(W, H, "KUBERNETES UP AND RUNNING · 20-01",
      "정책을 쓰는 일과 적용하는 일을 갈라 놓는다",
      "템플릿이 Rego 와 파라미터 스키마를 담아 새 kind 를 만들어 내고, 제약이 그 kind 를 "
      "파라미터와 범위로 인스턴스화한다.",
      "이 분리 덕분에 Rego 를 모르는 관리자도 정책을 적용하고, 템플릿을 조직 사이에 공유한다")

# 두 패널 사이는 가운데 칩("새 kind 를 만들어 낸다" · 10px 로 164px)과 그 아래 한 줄이
# 들어갈 만큼 벌어져 있어야 한다. 546/546 · 간격 100 이던 초판은 칩이 양쪽 패널을 32px 씩
# 물어 dd-lint 가 chip 겹침 6 건을 냈다 — 폭을 500 으로 줄여 간격을 192 로 연다.
LW, RW = 500, 500
LX, RX = 24, 716
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
AY = Y0 + CH / 2
d.arrow([(LX + LW + 6, AY), (RX - 8, AY)], ACC, "acc", 1.6)
d.chip(MX, AY - 22, "새 kind 를 만들어 낸다", ACC, 10)
# 정본(type-er)은 관계선 양 끝에 카디널리티를 엔티티 변에서 10~12px 띄워 적는다.
# 아래 주석이 "한 템플릿에 여러 제약을 걸 수 있다" 라고 적는 1:N 이 도식에는 없어
# 산문에만 있었다 — 선 끝에 올려 도식이 그 사실을 직접 나르게 한다.
# 선 *아래* 에 둔다. 위에 두면 칩 밑변과 8px 밖에 안 떨어져 붙어 보이고,
# 오른쪽 N 은 화살촉과 겹친다. 아래로 내리고 그 아래 한 줄을 40 으로 밀어 셋을 갈라 놓는다.
d.t(LX + LW + 14, AY + 16, "1", 9, ACC, MONO, "start")
d.t(RX - 20, AY + 16, "N", 9, ACC, MONO, "end")
d.t(MX, AY + 40, "Rego 는 왼쪽에만 있다", 10, SOFT, KR)

BY = Y0 + CH + 28
d.line(24, BY, W - 48, BY, RULE, 0.8)
d.t(24, BY + 24, "한 템플릿에 여러 제약을 걸 수 있다. 팀마다 허용 레지스트리가 다르면 "
                 "제약만 여럿 만들고 Rego 는 하나로 둔다.", 11, MUTED, KR, "start")
d.legend(BY + 40, [("템플릿 — 쓰는 쪽", INFO), ("제약 — 적용하는 쪽", ACC)])
d.save("20-01.template-constraint-split.svg")
print("필요 h:", BY + 40 + 48, "· 실제:", H)

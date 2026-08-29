# 17-01 §랩 — CRD 를 세우고 검증을 붙이기
# 이 랩은 "이렇게 하면 된다" 가 아니라 "넣어 봤더니 이게 돌아왔다" 의 연속이다. 그래서
# 단계 사슬이 아니라 시도와 응답을 짝지은 사다리로 그린다. 응답은 지어내지 않고 본문이
# 실측해 적어 둔 문자열을 그대로 옮긴다.
# 초점은 두 줄이다 — 네 번째와 마지막. 컨트롤러 없는 CRD 와 바인딩 없는 정책이 똑같이
# 오류도 경고도 없이 통과한다. 본문 전체에서 가장 값한 것이 이 대칭이다.
# 타입 스펙: type-process.md — 일곱 단계가 같은 의미 슬롯(넣어 본 것 · 서버가 돌려준 것)으로
#           반복되고 순서가 있다. 앞 단계의 실패가 다음 단계를 부르므로 격자가 아니라 절차다.
#           어긋나는 지점: 정본은 lane=주체 × 열=단계인데 여기서는 행이 단계이고 열이 시도/응답
#           이라 축이 뒤집혀 있다. 응답은 지어내지 않고 본문이 실측한 문자열을 그대로 옮긴다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, MUTED, SOFT, INK, PAPER2, PAPER, RULE, KR, MONO
import ddx

W, H = 1240, 770
d = D(W, H, "KUBERNETES UP AND RUNNING · 17-01",
      "선언은 절반이고 나머지 절반은 따로 있다",
      "책의 랩은 지금 그대로는 한 줄도 돌지 않는다. 현행 문법으로 다시 세우면서 서버가 무엇을 "
      "돌려주는지 그대로 옮긴다.",
      "kind 로컬 클러스터 실측 — kubectl v1.34.1 · 서버 v1.35.0")

LX, LW = 24, 470
RX, RW = 514, 702
Y0, RH, GAP = 150, 58, 10

ROWS = [
    ("책의 CRD 매니페스트를 그대로 넣는다", "kubectl apply --dry-run=server", True,
     'no matches for kind "CustomResourceDefinition" in version "…/v1beta1"', True,
     "원서가 쓰는 세 API 가 모두 v1beta1 이고, 셋 다 1.22 에서 제거됐다", BAD),
    ("apiVersion 만 v1 으로 바꿔 다시 넣는다", "", False,
     "spec.versions[0].schema.openAPIV3Schema: Required value", True,
     "문법 치환으로 넘길 수 없다 — v1 에는 스키마를 비워 둘 선택지가 없다", BAD),
    ("구조적 스키마를 채워 등록한다", "kubectl get lt 로 조회된다", False,
     "customresourcedefinition.../loadtests.beta.kuar.com created", True,
     "이름은 <복수형>.<그룹> 이어야 한다 — 그래서 타입이 겹치지 않는다", OK),
    ("LoadTest 인스턴스를 하나 만든다", "kubectl get pods -l app=loadtest", True,
     "my-loadtest created      ·      No resources found", True,
     "아무 일도 일어나지 않는다 — 반응할 컨트롤러가 클러스터에 없다", ACC),
    ("타입을 어긴 객체와 의미를 어긴 객체를 넣는다", "문자열 rps · 음수 rps · scheme: gopher", False,
     "타입 위반은 거부 · 음수와 gopher 는 created", False,
     "스키마는 타입을 지키고 의미는 지키지 않는다", WARN),
    ("ValidatingAdmissionPolicy 와 Binding 을 건다", "CEL 식 둘 — rps > 0 · scheme in [http, https]", False,
     "denied request: requestsPerSecond 는 0 보다 커야 합니다", True,
     "웹훅도 인증서도 서버도 없다. 정책이 API 서버 안에서 평가된다", OK),
    ("Binding 만 지우고 같은 객체를 다시 넣는다", "", False,
     "created (server dry run)", True,
     "오류도 경고도 없이 그냥 통과한다 — 정책은 규칙만 정의한다", ACC),
]

for i, (lt, ls, lmono, msg, mmono, note, c) in enumerate(ROWS):
    y = Y0 + i * (RH + GAP)
    cy = y + RH / 2
    focal = c is ACC
    d.box(LX, y, LW, RH, PAPER2, RULE, 1.0, 6)
    d.t(LX + 16, cy - 4 if ls else cy + 5, ddx.fit(lt, 12, LW - 32, lt), 12,
        ACC if focal else INK, KR, "start", 600)
    if ls:
        d.t(LX + 16, cy + 17, ls, 10, SOFT, MONO if lmono else KR, "start")
    if focal:
        d.o.append(f'<rect x="{RX}" y="{y}" width="{RW}" height="{RH}" rx="6" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(RX, y, RW, RH, PAPER2, c, 1.1, 6)
    d.t(RX + 18, cy - 4, msg, 10, c, MONO if mmono else KR, "start")
    d.t(RX + 18, cy + 17, ddx.fit(note, 10, RW - 36, note), 10,
        c if focal else MUTED, KR, "start")
    d.path(f"M {LX+LW} {cy} L {RX-4} {cy}", c if focal else MUTED, 1.4,
           m="acc" if focal else "ar")

d.t(LX + LW / 2, Y0 - 16, "넣어 본 것", 10, SOFT, KR)
d.t(RX + RW / 2, Y0 - 16, "서버가 돌려준 것", 10, SOFT, KR)

EY = Y0 + len(ROWS) * (RH + GAP) + 22
d.t(LX, EY, "넷째 줄과 마지막 줄이 같은 말을 한다. CRD 는 필요한 인프라의 절반이고 나머지 절반은 컨트롤러다. "
            "정책도 절반이고 나머지 절반은 바인딩이다.", 11, ACC, KR, "start")
d.t(LX, EY + 22, "둘 다 실패가 조용하다 — 만들어지긴 하는데 아무 일도 일어나지 않는다. 안 걸린다면 나머지 절반부터 확인한다.",
     11, ACC, KR, "start")
d.t(LX, EY + 48, "변환은 이야기가 다르다. 기본값 채우기는 여전히 변환 웹훅의 몫이고, 그러려면 책이 밟은 인증서 절차가 필요하다 — "
                 "실무에서는 cert-manager 에 맡긴다.", 11, MUTED, KR, "start")

d.legend(EY + 74, [("선언만으로는 아무 일도 없다", ACC), ("돌지 않는다", BAD),
                   ("잡히지 않는다", WARN), ("된다", OK)])
d.save("17-01.crd-validation-lab.svg")
print("h 필요:", EY + 74 + 48, " 실제:", H)

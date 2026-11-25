# a0-01 키워드 개념도 — `istioctl install --set profile=demo` 한 줄이 실제로 고른 것들이 갈래로 갈라졌다 모이는 모양.
# 값 근거(본문 a0-01):
#   - 루트 명령: §1 도입과 2장이 쓰는 `istioctl install --set profile=demo -y` (원문 사본 appendix-A 첫 쪽).
#   - §1 길 넷: helm · istioctl · istio-operator · kubectl. 셋은 Helm 템플릿 위(§1, 정답 1).
#   - §2: Helm 에는 사용자 입력 검증 층이 없어 IstioOperator API 가 생겼다(「검증이 서는 자리」).
#   - §3: 배포 프로파일(demo · default · empty …, 현행 문서 기준 일곱, 본문 §3). §4: control-plane(profile: demo) + ingress-gateway(profile: empty).
#   - §5: metadata.name 이 같으면 갱신, 다르면 새 설치. §6: istioctl 이냐 istio-operator 냐를 유지 비용으로 따진다.
# 타입 스펙: type-architecture — 구성요소를 노드로 두고 라벨 붙은 화살표로 잇는 그래프. 고른 이유: 이 부록의 줄기가
#           「한 줄이 고른 것들로 갈라졌다 둘로 모이고 이어진다」는 갈래라 한 열 목록이나 격자로는 갈림과 모임이 안 보인다.
#           좌표는 열 세 개(루트 · 갈래 · 모임)와 행 stride 116 으로 직접 잡았다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, KR, MONO

W, H = 920, 660

d = D(W, H, "ISTIO IN ACTION · A0-01 OVERVIEW",
      "설치 한 줄이 고른 것들",
      "istioctl install --set profile=demo 한 줄에서 갈래가 둘로 갈라진다. 위 갈래는 무엇으로 올리는지를 고르고 "
      "Helm 값에 검증이 없어서 IstioOperator API 가 생겼다. 아래 갈래는 출발점인 프로파일을 고른다. 두 갈래는 "
      "컨트롤 플레인과 게이트웨이를 별도 리소스로 나누는 자리에서 만난다. 그 뒤로 이름이 하는 일과 도구 선택이 이어진다.",
      "화살표 위 글자는 두 요소의 관계이고 칩은 그 요소를 다루는 절입니다")


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def node(x, y, w, h, title, lines, c, sec):
    d.tone(x, y, w, h, c, 6, "14", 1.2)
    d.chip(x + 24, y + 14, sec, c, 11)
    d.t(x + w / 2, y + 36, title, 14, c, kr(title), "middle", 600)
    for i, s in enumerate(lines):
        d.t(x + w / 2, y + 54 + i * 16, s, 12, MUTED, kr(s), "middle")


NH = 76
AX, AW = 24, 160
BX, BW = 340, 200
CX, CW = 670, 210
RB1, RB2, RB3 = 110, 226, 342
RC1, RC2, RC3 = 284, 400, 516

# 루트: 핵심 요약이 가리키는 한 줄
d.tone(AX, RB2, AW, NH, ACC, 6, "1e", 1.4)
d.t(AX + AW / 2, RB2 + 30, "istioctl install", 13, ACC, MONO, "middle", 600)
d.t(AX + AW / 2, RB2 + 50, "--set profile=demo", 12, MUTED, MONO, "middle")
d.t(AX + AW / 2, RB2 + 68, "책 실습의 설치 한 줄", 12, MUTED, KR, "middle")

# 갈래 B
node(BX, RB1, BW, NH, "올리는 길 넷", ["helm · istioctl", "istio-operator · kubectl"], INFO, "§1")
node(BX, RB2, BW, NH, "IstioOperator API", ["v1alpha1 스키마가", "입력을 설치 전에 검증"], INFO, "§2")
node(BX, RB3, BW, NH, "배포 프로파일", ["demo · default · empty", "minimal · remote …"], INFO, "§3")

# 모임 C
node(CX, RC1, CW, NH, "리소스 둘로 나눔", ["control-plane (demo)", "ingress-gateway (empty)"], INFO, "§4")
node(CX, RC2, CW, NH, "metadata.name", ["같으면 갱신", "다르면 새 설치"], INFO, "§5")
node(CX, RC3, CW, NH, "도구 선택", ["istioctl 이냐", "istio-operator 냐"], INFO, "§6")

# 루트 → 갈래
yR = RB2 + NH / 2
d.arrow([(AX + AW, yR), (215, yR), (215, RB1 + NH / 2), (BX - 2, RB1 + NH / 2)], MUTED, "ar", 1.4)
d.t(224, RB1 + NH / 2 - 8, "무엇으로 올리나", 12, MUTED, KR, "start")
d.arrow([(AX + AW, yR), (215, yR), (215, RB3 + NH / 2), (BX - 2, RB3 + NH / 2)], MUTED, "ar", 1.4)
d.t(224, RB3 + NH / 2 - 8, "출발점은 무엇인가", 12, MUTED, KR, "start")

# 갈래 안: 길 → API
d.arrow([(BX + BW / 2, RB1 + NH), (BX + BW / 2, RB2 - 2)], MUTED, "ar", 1.4)
d.t(BX + BW / 2 + 12, RB1 + NH + 24, "값 검증이 없어서", 12, MUTED, KR, "start")

# 갈래 → 모임
yC1 = RC1 + NH / 2
d.arrow([(BX + BW, RB2 + NH / 2), (640, RB2 + NH / 2), (640, yC1), (CX - 2, yC1)], MUTED, "ar", 1.4)
d.t(BX + BW + 10, RB2 + NH / 2 - 8, "API 로 적는다", 12, MUTED, KR, "start")
d.arrow([(BX + BW, RB3 + NH / 2), (640, RB3 + NH / 2), (640, yC1), (CX - 2, yC1)], MUTED, "ar", 1.4)
d.t(BX + BW + 10, RB3 + NH / 2 + 20, "empty 로 시작", 12, MUTED, KR, "start")

# 모임 안
d.arrow([(CX + CW / 2, RC1 + NH), (CX + CW / 2, RC2 - 2)], MUTED, "ar", 1.4)
d.t(CX + CW / 2 + 12, RC1 + NH + 24, "이름이 식별한다", 12, MUTED, KR, "start")
d.arrow([(CX + CW / 2, RC2 + NH), (CX + CW / 2, RC3 - 2)], MUTED, "ar", 1.4)
d.t(CX + CW / 2 + 12, RC2 + NH + 24, "유지 비용을 따진다", 12, MUTED, KR, "start")

d.legend(612, [("핵심 요약이 가리키는 한 줄", ACC), ("절이 푸는 선택", INFO)])
d.save("a0-01.appendix-overview.svg")

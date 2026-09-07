# 타입 스펙: type-deployment — 센서가 어디에 놓이고 어느 구역이 어느 장치로 지켜지는가.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §8.9.2 Figure 8.37 (책 622~624쪽) —
#   고보안 구역과 DMZ 의 구분, 센서를 나눠 두는 이유, 서명 기반과 이상 기반의 대비는 원문 그대로
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, OK, WARN, BAD, KR, MONO

W, H = 1000, 612
d = D(W, H, "SECTION 8.9.2 · IDS DEPLOYMENT",
      "센서를 나눠 두는 이유는 처리량입니다",
      "지나는 패킷마다 수만 개의 서명과 대조해야 한다. 하류에 나눠 두면 각 센서가 일부만 본다.",
      "구역 구분과 센서 배치는 원문 Figure 8.37 의 것입니다")

d.tone(24, 148, 300, 168, BAD, 8, "10", 1.2)
d.t(174, 180, "바깥 인터넷", 12, BAD, KR, "middle", 600)
d.t(174, 208, "초당 기가비트가", 11, MUTED, KR)
d.t(174, 230, "들어올 수 있습니다", 11, MUTED, KR)

d.tone(376, 148, 264, 168, WARN, 8, "12", 1.3)
d.t(508, 180, "DMZ", 13, WARN, KR, "middle", 600)
d.t(508, 208, "패킷 필터만 지킵니다", 11, MUTED, KR)
d.t(508, 232, "공개 웹 서버", 11, SOFT, KR)
d.t(508, 252, "권한 있는 DNS 서버", 11, SOFT, KR)
d.t(508, 288, "IDS 센서가 감시합니다", 11, ACC, KR)

d.tone(692, 148, 284, 168, OK, 8, "12", 1.3)
d.t(834, 180, "고보안 구역", 13, OK, KR, "middle", 600)
d.t(834, 208, "패킷 필터", 11, MUTED, KR)
d.t(834, 230, "+ 응용 게이트웨이", 11, MUTED, KR)
d.t(834, 288, "IDS 센서가 감시합니다", 11, ACC, KR)

d.arrow([(328, 216), (372, 216)], MUTED, "ar", 1.4)
d.arrow([(644, 216), (688, 216)], MUTED, "ar", 1.4)

CY = 348
d.box(24, CY, 470, 152, PAPER2, RULE, 1.0)
d.t(44, CY + 28, "IDS 와 IPS", 12, INK, KR, "start", 600)
d.line(44, CY + 40, 474, CY + 40, RULE, 0.8)
d.t(44, CY + 64, "IDS", 11, INFO, MONO, "start", 600)
d.t(96, CY + 64, "수상한 트래픽을 보면 경보를 냅니다", 11, MUTED, KR, "start")
d.t(44, CY + 88, "IPS", 11, INFO, MONO, "start", 600)
d.t(96, CY + 88, "수상한 트래픽을 걸러 냅니다", 11, MUTED, KR, "start")
d.t(44, CY + 120, "원문이 둘을 함께 다루는 이유는 흥미로운 지점이", 11, ACC, KR, "start")
d.t(44, CY + 140, "어떻게 탐지하느냐이지 무엇을 하느냐가 아니기 때문입니다.", 11, ACC, KR, "start")

d.box(514, CY, 462, 152, PAPER2, RULE, 1.0)
d.t(534, CY + 28, "탐지 방식 둘", 12, INK, KR, "start", 600)
d.line(534, CY + 40, 956, CY + 40, RULE, 0.8)
d.t(534, CY + 64, "서명 기반", 11, INFO, KR, "start", 600)
d.t(624, CY + 64, "알려진 공격의 서명과 대조합니다", 11, MUTED, KR, "start")
d.t(534, CY + 84, "", 11, MUTED, KR, "start")
d.t(624, CY + 84, "새 공격에는 완전히 눈이 멉니다", 11, BAD, KR, "start")
d.t(534, CY + 112, "이상 기반", 11, INFO, KR, "start", 600)
d.t(624, CY + 112, "정상 프로파일과 다른 흐름을 찾습니다", 11, MUTED, KR, "start")
d.t(624, CY + 132, "정상과 이상을 가르는 것이 극히 어렵습니다", 11, BAD, KR, "start")

d.legend(520, [("바깥", BAD), ("DMZ", WARN), ("고보안", OK), ("센서와 탐지", ACC)])
out = pathlib.Path(__file__).resolve().parent.parent / "08-05.ids-deployment.svg"
d.save(out); print("→", out.name)

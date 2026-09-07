# 타입 스펙: type-state — 연결이 어느 상태에 있느냐가 같은 모양의 패킷을 다르게 판정하게 한다.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §8.9.1 Table 8.7 · 8.8 (책 618~619쪽) —
#   3-way 핸드셰이크 관찰, FIN, 60초 무활동, 그리고 두 장면의 판정은 원문 그대로
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, OK, WARN, BAD, KR, MONO

W, H = 1000, 616
d = D(W, H, "SECTION 8.9.1 · STATEFUL FILTER",
      "같은 모양의 패킷을 표가 갈라 놓습니다",
      "전통 필터는 규칙만 본다. 상태 필터는 이 응답이 우리가 시작한 연결의 것인지를 물을 수 있다.",
      "연결 표의 판정 근거는 원문 §8.9.1 의 것입니다")

SX, SW = 24, 952
d.box(SX, 144, SW, 92, PAPER2, RULE, 1.0)
d.t(SX + 20, 172, "연결 표는 무엇을 보고 갱신됩니까", 12, INK, KR, "start", 600)
d.line(SX + 20, 184, SX + SW - 20, 184, RULE, 0.8)
# 시작·끝은 둘 다 "표의 갱신 신호" 라 같은 색으로 둔다. OK 를 쓰면 범례의 "사는 쪽" 과 뜻이 겹친다.
TR = [(44, "시작", "3-way 핸드셰이크 관찰 (SYN · SYNACK · ACK)", INFO),
      (380, "끝", "그 연결의 FIN 패킷", INFO),
      (680, "보수적 판단", "60초 무활동이면 끝난 것으로", WARN)]
for x, k, v, c in TR:
    d.t(x, 212, k, 11, c, KR, "start", 600)
    d.t(x + (72 if k != "보수적 판단" else 96), 212, v, 11, MUTED, KR, "start")

CY = 264
CASES = [(24, "공격자의 기형 패킷", "출발지 포트 80 · ACK 플래그 1",
          ["방화벽이 목록을 봅니다 — 연결 확인 표시.", "연결 표를 뒤집니다.",
           "진행 중인 어느 연결의 것도 아닙니다."], "버립니다", BAD),
         (514, "내부 사용자의 웹 서핑", "출발지 포트 80 · ACK 플래그 1",
          ["사용자가 먼저 SYN 을 보냈습니다.", "그 연결이 표에 기록됐습니다.",
           "대응하는 연결이 진행 중입니다."], "통과시킵니다", OK)]
for x, title, packet, steps, verdict, c in CASES:
    d.tone(x, CY, 462, 216, c, 8, "12", 1.3)
    d.t(x + 20, CY + 30, title, 12, c, KR, "start", 600)
    d.t(x + 20, CY + 52, packet, 11, SOFT, MONO, "start")
    d.line(x + 20, CY + 64, x + 442, CY + 64, RULE, 0.8)
    for i, ln in enumerate(steps):
        d.t(x + 20, CY + 90 + i * 22, ln, 11, MUTED, KR, "start")
    d.tone(x + 20, CY + 164, 200, 36, c, 5, "26", 1.4)
    d.t(x + 120, CY + 188, verdict, 12, c, KR, "middle", 600)

d.t(24, 520, "패킷의 모양은 같습니다. 표에 기록이 있느냐가 둘을 가릅니다.", 12, ACC, KR, "start", 600)
d.t(24, 544, "순진한 해법은 TCP ACK 를 전부 막는 것인데, 그러면 내부 사용자의 웹 서핑이 함께 죽습니다.",
    11, MUTED, KR, "start")

d.legend(560, [("막히는 쪽", BAD), ("사는 쪽", OK), ("표의 갱신 신호", INFO), ("시간 기준", WARN)])
out = pathlib.Path(__file__).resolve().parent.parent / "08-05.stateful-filter.svg"
d.save(out); print("→", out.name)

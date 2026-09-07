# 타입 스펙: type-treemap — 면적 = 비중. 슬롯 100 개의 운명을 세 조각으로 나눈 부분-전체.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §6.3.2 —
#   "the maximum efficiency of the protocol is given by 1/e = 0.37 ... 37 percent of the slots go empty
#    and 26 percent of slots have collisions"
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, BAD, KR, MONO

W, H = 940, 522
d = D(W, H, "SECTION 6.3.2 · SLOTTED ALOHA EFFICIENCY",
      "슬롯 100 개 중 37 개만 일합니다",
      "활성 노드가 많을 때 슬롯 ALOHA 의 슬롯은 셋 중 하나가 된다. 성공 37, 빈 슬롯 37, 충돌 26. 면적이 곧 비중이다.",
      "원문이 제시한 1/e = 0.37 과 26 퍼센트 그대로입니다")

TX, TY, TW, TH = 24, 116, 560, 280
SUCCESS_W = 208            # 560 x 0.37
RIGHT_X = TX + SUCCESS_W
RIGHT_W = TW - SUCCESS_W
EMPTY_H = 164              # 280 x 37/63
COLL_H = TH - EMPTY_H

d.tone(TX, TY, SUCCESS_W - 4, TH, ACC, 6, "1E", 1.6)
d.t(TX + (SUCCESS_W - 4) / 2, TY + TH / 2 - 6, "성공", 14, ACC, KR, "middle", 600)
d.t(TX + (SUCCESS_W - 4) / 2, TY + TH / 2 + 18, "37", 20, ACC, MONO, "middle", 600)

d.tone(RIGHT_X, TY, RIGHT_W, EMPTY_H - 4, MUTED, 6, "14", 1.1)
d.t(RIGHT_X + RIGHT_W / 2, TY + EMPTY_H / 2 - 6, "빈 슬롯 — 아무도 안 보냈습니다", 12, MUTED, KR, "middle", 600)
d.t(RIGHT_X + RIGHT_W / 2, TY + EMPTY_H / 2 + 18, "37", 18, MUTED, MONO)

d.tone(RIGHT_X, TY + EMPTY_H, RIGHT_W, COLL_H, BAD, 6, "14", 1.1)
d.t(RIGHT_X + RIGHT_W / 2, TY + EMPTY_H + COLL_H / 2 - 6, "충돌 — 둘 이상이 겹쳤습니다", 12, BAD, KR, "middle", 600)
d.t(RIGHT_X + RIGHT_W / 2, TY + EMPTY_H + COLL_H / 2 + 18, "26", 18, BAD, MONO)

AX, AW = 624, 292
d.box(AX, 116, AW, 132, PAPER2, RULE, 1.0)
d.t(AX + 16, 140, "무엇을 얻고 무엇을 잃었나", 11, INK, KR, "start", 600)
d.line(AX + 16, 150, AX + AW - 16, 150, RULE, 0.8)
for i, (c, s) in enumerate([
    (ACC, "혼자 보낼 때는 채널 전부 R 을 씁니다"),
    (MUTED, "충돌 감지도 재전송도 노드가 직접 합니다"),
    (BAD, "붐비면 실효 속도가 0.37 R 로 떨어집니다"),
]):
    d.t(AX + 16, 172 + i * 22, "·", 11, c, KR, "start", 600)
    d.t(AX + 30, 172 + i * 22, s, 11, MUTED, KR, "start")

d.box(AX, 264, AW, 132, PAPER2, RULE, 1.0)
d.t(AX + 16, 288, "슬롯을 없애면 절반이 됩니다", 11, INK, KR, "start", 600)
d.line(AX + 16, 298, AX + AW - 16, 298, RULE, 0.8)
d.t(AX + 16, 322, "슬롯 ALOHA", 11, MUTED, KR, "start")
d.t(AX + AW - 16, 322, "1/e = 0.37", 12, ACC, MONO, "end", 600)
d.t(AX + 16, 346, "순수 ALOHA", 11, MUTED, KR, "start")
d.t(AX + AW - 16, 346, "1/(2e) = 0.18", 12, INFO, MONO, "end", 600)
d.t(AX + 16, 374, "완전한 분산의 값입니다", 11, MUTED, KR, "start")

d.line(24, 424, W - 48, 424, RULE, 0.8)
d.t(24, 446, "100 Mbps 슬롯 ALOHA 시스템을 사서 총 80 Mbps 를 기대한 관리자는 실제로 37 Mbps 아래를 받습니다.", 11, MUTED, KR, "start")
d.t(24, 464, "채널이 프레임 하나를 100 Mbps 로 보내는 것과 장기 처리량은 다른 이야기입니다.", 11, MUTED, KR, "start")

d.legend(482, [("성공한 슬롯", ACC), ("빈 슬롯", MUTED), ("충돌한 슬롯", BAD), ("순수 ALOHA", INFO)])

out = pathlib.Path(__file__).resolve().parent.parent / "06-02.slot-fates.svg"
d.save(out)
print("→", out)

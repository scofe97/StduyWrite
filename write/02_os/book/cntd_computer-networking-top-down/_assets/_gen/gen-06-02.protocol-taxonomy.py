# 타입 스펙: type-tree — 부모 → 자식 관계. 분류 자체가 트리이고, 잎이 실제 프로토콜이다.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §6.3 — 세 분류와 이상적 프로토콜 네 조건,
#   그리고 §6.3.1~§6.3.3 이 각 분류에 대해 밝힌 충족·미충족 서술 그대로
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, BAD, WARN, KR, MONO

W, H = 1000, 572
d = D(W, H, "SECTION 6.3 · THREE FAMILIES OF MULTIPLE ACCESS",
      "다중 접속 프로토콜은 세 갈래로 갈립니다",
      "수십 가지 다중 접속 프로토콜을 채널 분할·랜덤 접속·순번 셋 중 하나로 분류할 수 있다. 갈래마다 이상적 조건 중 무엇을 만족하고 무엇을 못 만족하는지가 다르다.",
      "분류와 충족 여부는 원문 §6.3 의 서술 그대로입니다")

d.tone(400, 104, 200, 48, ACC, 6, "14", 1.5)
d.t(500, 134, "다중 접속 프로토콜", 13, ACC, KR, "middle", 600)

CARDS = [
    (24, "채널 분할", ["TDM", "FDM", "CDMA"],
     [(OK, "충돌이 없고 완벽히 공정합니다"),
      (BAD, "혼자 보내도 R/N 로 묶입니다"),
      (BAD, "늘 자기 차례를 기다립니다")]),
    (356, "랜덤 접속", ["슬롯 ALOHA", "순수 ALOHA", "CSMA", "CSMA/CD"],
     [(OK, "혼자면 채널 전부 R 을 씁니다"),
      (BAD, "붐비면 충돌로 낭비합니다"),
      (OK, "분산이고 구현이 단순합니다")]),
    (688, "순번", ["폴링", "토큰 패싱"],
     [(OK, "충돌도 빈 슬롯도 없습니다"),
      (BAD, "폴링은 컨트롤러가 단일 실패점입니다"),
      (WARN, "토큰은 분실 시 복구가 필요합니다")]),
]

CW = 288
d.line(500, 152, 500, 176, RULE, 1.1)
d.line(168, 176, 832, 176, RULE, 1.1)
for x, title, members, notes in CARDS:
    cx = x + CW / 2
    d.line(cx, 176, cx, 200, RULE, 1.1)
    d.box(x, 200, CW, 252, PAPER2, RULE, 1.0)
    d.t(cx, 228, title, 13, INK, KR, "middle", 600)
    d.line(x + 16, 242, x + CW - 16, 242, RULE, 0.8)
    for i, m in enumerate(members):
        d.chip(cx, 272 + i * 26, m, MUTED, 11)
    d.line(x + 16, 372, x + CW - 16, 372, RULE, 0.8)
    for i, (c, note) in enumerate(notes):
        d.t(x + 16, 396 + i * 20, "·", 11, c, KR, "start", 600)
        d.t(x + 30, 396 + i * 20, note, 11, MUTED, KR, "start")

d.line(24, 472, W - 48, 472, RULE, 0.8)
d.t(24, 494, "원문이 꼽는 이상적 조건 넷 — 혼자면 R bps · M 노드면 각자 평균 R/M bps · 중앙 컨트롤러 없이 분산 · 구현이 쌀 만큼 단순",
     11, MUTED, KR, "start")
d.t(24, 512, "세 갈래 중 넷을 다 만족하는 것은 없습니다. 무엇을 포기할지가 갈래를 가릅니다.", 11, MUTED, KR, "start")

d.legend(530, [("분류의 뿌리", ACC), ("만족하는 자리", OK), ("포기하는 자리", BAD), ("조건부", WARN)])

out = pathlib.Path(__file__).resolve().parent.parent / "06-02.protocol-taxonomy.svg"
d.save(out)
print("→", out)

# 타입 스펙: type-architecture — 어떤 구성요소가 어떤 상태를 들고 있고 무엇으로 서로를 찾는가.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §8.7.3 Figure 8.28 (책 600~604쪽) —
#   SA 의 여섯 상태 항목, 단방향이라는 점, 2+2n 계산, SAD 와 SPD 의 역할 분담은 원문 그대로
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, OK, WARN, KR, MONO

W, H = 1000, 604
d = D(W, H, "SECTION 8.7.3 · SECURITY ASSOCIATION",
      "SA 는 방향 하나짜리 논리 연결입니다",
      "양쪽이 서로 보내려면 둘이 필요하다. 그래서 영업 사원 n 명이면 SA 는 2+2n 개다.",
      "상태 항목과 SAD·SPD 의 역할은 원문 §8.7.3 의 것입니다")

for x, name, ip in ((24, "R1", "200.168.1.100"), (760, "R2", "193.68.2.23")):
    d.tone(x, 148, 216, 76, INFO, 8, "14", 1.3)
    d.t(x + 108, 180, name, 13, INFO, MONO, "middle", 600)
    d.t(x + 108, 204, ip, 11, MUTED, MONO)
d.arrow([(248, 172), (752, 172)], ACC, "acc", 1.6)
d.t(500, 160, "SA 하나 — 단방향", 11, ACC, KR, "middle", 600)
d.arrow([(752, 208), (248, 208)], SOFT, "soft", 1.4, "5 4")
d.t(500, 228, "돌아오려면 SA 를 하나 더 세웁니다", 11, SOFT, KR)

SX, SW = 24, 470
d.box(SX, 268, SW, 216, PAPER2, RULE, 1.0)
d.t(SX + 20, 296, "R1 이 이 SA 에 대해 들고 있는 상태", 12, INK, KR, "start", 600)
d.line(SX + 20, 308, SX + SW - 20, 308, RULE, 0.8)
ITEMS = [("SPI", "32비트 SA 식별자"), ("인터페이스", "출발과 목적"), ("암호화 방식", "예: CBC 모드 3DES"),
         ("암호화 열쇠", ""), ("무결성 방식", "예: MD5 를 쓰는 HMAC"), ("인증 열쇠", "")]
for i, (k, v) in enumerate(ITEMS):
    y = 334 + i * 24
    d.t(SX + 20, y, k, 11, OK, KR, "start", 600)
    if v:
        d.t(SX + 168, y, v, 11, MUTED, KR, "start")

DX, DW = 530, 446
d.tone(DX, 268, DW, 100, WARN, 8, "14", 1.3)
d.t(DX + 20, 296, "SAD — 어떻게 할지", 12, WARN, KR, "start", 600)
d.t(DX + 20, 322, "모든 SA 의 상태를 담습니다.", 11, MUTED, KR, "start")
d.t(DX + 20, 344, "커널 안의 자료구조입니다.", 11, MUTED, KR, "start")

d.tone(DX, 384, DW, 100, ACC, 8, "18", 1.4)
d.t(DX + 20, 412, "SPD — 무엇을 할지", 12, ACC, KR, "start", 600)
d.t(DX + 20, 438, "어떤 데이터그램을 IPsec 처리할지,", 11, MUTED, KR, "start")
d.t(DX + 20, 460, "그렇다면 어느 SA 를 쓸지 지정합니다.", 11, MUTED, KR, "start")

d.t(24, 516, "본사·지사 사이 둘 + 영업 사원마다 둘 = 2 + 2n 개. 다만 게이트웨이는 평범한 IPv4 도 함께 내보냅니다.",
    11, SOFT, KR, "start")
d.legend(536, [("IPsec 개체", INFO), ("SA 하나", ACC), ("상태 항목", OK), ("담는 자리", WARN)])
out = pathlib.Path(__file__).resolve().parent.parent / "08-04.security-association.svg"
d.save(out); print("→", out.name)

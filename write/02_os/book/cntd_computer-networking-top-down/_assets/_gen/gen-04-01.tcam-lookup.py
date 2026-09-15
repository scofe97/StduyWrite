# 04-01 §4 — 주소로 묻는 RAM 과 내용으로 묻는 TCAM. 5.12 ns 안에 백만 줄을 뒤지려면 순서대로는 닿지 않는다.
# 2026-09-14 신설: 손으로 쓴 SVG 만 있어 타입 선택 절차를 거치지 않은 장이었다.
#   바닥에 세 줄짜리 설명 문단(비싸고 전력을 많이 쓰는 이유 · 혼합 방식 · 별표의 값어치)이 얹혀 있었는데
#   그건 도식이 아니라 본문이라 걷어냈다.
# 타입 스펙: type-dp-security-matrix — 같은 물음을 두 방식에 걸고 칸마다 결과를 대조한다.
#   여기서는 격자가 곧 논지다 — RAM 은 줄을 하나씩 내려가며 클록을 쓰고, TCAM 은 한 줄에 전부가 답한다.
#   축약: 셀에 값 대신 클록 수와 일치 폭을 넣어 "몇 번 만에 답이 나오는가"를 세로로 읽게 했다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, BAD, WARN, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 424

d = D(W, H, "COMPUTER NETWORKING TOP-DOWN · 04-01 §4",
      "하나씩 훑느냐, 전부가 동시에 손을 드느냐",
      "5.12 나노초 안에 백만 줄을 뒤져야 한다. 주소로 묻는 보통 메모리는 줄마다 한 클록을 쓰므로 항목이 백만 개면 "
      "클록도 백만 번이고, 접두를 담을 방법도 없다. 내용으로 묻는 TCAM 은 모든 항목이 동시에 비교해 한 클록에 답한다.",
      "찾는 주소 …0001 1000 1010 을 두 방식에 똑같이 물었을 때")

QUERY = "…0001 1000 1010"

# ── 왼쪽 · RAM — 줄을 하나씩 내려간다. 클록이 줄 수만큼 든다.
d.t(24, 122, "보통 메모리 (RAM)", 13, SOFT, KR, "start", 600)
d.t(24, 142, "주소로 묻는다 — “3번지에 뭐 있어?”", 12, MUTED, KR, "start")

RAM = [("1번지  …00010", "✗", "1 클록", BAD),
       ("2번지  …00011000", "✓", "2 클록", WARN),
       ("3번지  …00011", "✓", "3 클록", WARN)]
for i, (row, hit, clk, c) in enumerate(RAM):
    y = 164 + i * 32
    d.box(24, y, 232, 26, PAPER2, RULE, 0.9, 4)
    d.t(36, y + 18, row, 12, INK, MONO, "start")
    d.t(272, y + 18, hit, 12, c, MONO)
    d.t(300, y + 18, clk, 12, c, MONO, "start")
d.t(36, 278, "…", 12, MUTED, MONO, "start")
d.t(300, 278, "…", 12, MUTED, MONO, "start")

d.tone(24, 292, 368, 46, BAD, 5, "0A", 1.2)
d.t(40, 312, "항목 백만 개 → 클록 백만 번", 13, BAD, KR, "start", 600)
d.t(40, 330, "저장 비트는 0·1 둘뿐 → 접두 표현 불가", 12, MUTED, KR, "start")

# ── 오른쪽 · TCAM — 한 줄에 전부가 비교한다. 여럿이 맞으면 가장 긴 것을 고른다.
d.t(456, 122, "TCAM", 13, SOFT, KR, "start", 600)
d.t(456, 142, "내용으로 묻는다 — “이 값 어디 있어?”", 12, MUTED, KR, "start")

TCAM = [("…00010", "*******", "✗ 불일치", BAD),
        ("…00011000", "****", "✓ 24비트", OK),
        ("…00011", "*******", "✓ 21비트", ACC)]
for i, (val, mask, verdict, c) in enumerate(TCAM):
    x = 456 + i * 140
    d.box(x, 164, 128, 52, PAPER2, c, 1.1 if c is ACC else 0.9, 4)
    d.t(x + 64, 184, val, 12, INK, MONO)
    d.t(x + 64, 202, mask, 12, c, MONO)
    d.t(x + 64, 232, verdict, 12, c, MONO)

d.tone(456, 250, 400, 26, INFO, 5, "14", 1.2)
d.t(476, 268, "모든 항목이 동시에 비교 — 한 클록", 13, INFO, KR, "start", 600)

d.tone(456, 292, 400, 46, ACC, 5, "12", 1.4)
d.t(472, 312, "여럿이 맞으면 가장 긴 쪽 — 최장 접두 일치", 13, ACC, KR, "start", 600)
d.t(472, 330, "저장 비트 0·1·* — * 가 “신경 안 씀” → 접두를 통째로", 12, MUTED, KR, "start")

d.t(456, 356, "→ 출력 인터페이스 1", 13, ACC, KR, "start", 600)

d.legend(H - 44, [("한 클록에 답", INFO), ("최장 접두로 채택", ACC),
                  ("클록을 더 씀", WARN), ("불일치·표현 불가", BAD)])
d.save("04-01.tcam-lookup.svg")
print("ok tcam-lookup")

# 2026-09-10 A — 드롭 카운터가 올라도 포화가 아닐 수 있다.
# 회차에서 학습자가 "drop = 고장"이라는 전제를 마지막까지 놓지 못했다. 커널 문서가
# rx_dropped 와 rx_missed_errors 를 나누는 지점이 그 전제의 해독제라 표로 고정한다.
# 타입 스펙: type-bar — 두 성격을 나란히 놓고 같은 축(왜 버렸나·앱 영향)으로 재는 대조.
#           막대 길이가 아니라 두 열의 대비가 읽을거리라 그룹 두 개로만 세운다.
#           state 를 검토했으나 드롭은 상태 전이가 아니라 분류라 기각. flowchart 도
#           분기가 아니라 대조라 기각.
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dd import D, ACC, MUTED, SOFT, INK, BAD, PAPER2, RULE, KR, MONO

W, H = 840, 568
X0, CW, GAP, Y0 = 72, 328, 32, 148

COLS = [
    ("포화", "자리가 없어 못 받았다", BAD, [
        ("rx_missed_errors", "호스트가 준 버퍼에 안 들어감"),
        ("rx_fifo_errors", "장치 FIFO 오버플로"),
    ], "앱이 아픕니다", "링 버퍼를 키우거나 CPU 를 봅니다"),
    ("무주지", "받았는데 줄 데가 없다", ACC, [
        ("rx_dropped", "모르는 프로토콜 · L2 필터링"),
        ("", ""),
    ], "앱은 멀쩡합니다", "고칠 것이 없을 수 있습니다"),
]

d = D(W, H, "TROUBLESHOOTING DRILL · 2026-09-10 A",
      "드롭은 두 종류입니다",
      "인터페이스 드롭 카운터가 오른다고 포화는 아니다. 커널 문서는 rx_dropped 를 "
      "\"지원하지 않는 프로토콜\" 쪽에 두고, 버퍼 고갈은 포함하지 않아야 한다고 못 박는다. "
      "앱이 멀쩡한지 아픈지가 두 종류를 가르는 첫 갈래다.",
      lead="같은 drop 이라도 버린 이유가 다릅니다. 이유가 다르면 처방도 다릅니다.")

for i, (name, why, c, rows, impact, fix) in enumerate(COLS):
    x = X0 + i * (CW + GAP)
    d.tone(x, Y0, CW, 300, c, 8)
    d.t(x + 20, Y0 + 34, name, 16, c, KR, "start", 600)
    d.t(x + 20, Y0 + 58, why, 13, INK, KR, "start")
    d.line(x + 20, Y0 + 76, x + CW - 20, Y0 + 76, RULE, 1.0)

    yy = Y0 + 104
    for cname, note in rows:
        if not cname:
            continue
        d.t(x + 20, yy, cname, 12, INK, MONO, "start", 600)
        d.t(x + 20, yy + 20, note, 12, MUTED, KR, "start")
        yy += 52

    d.line(x + 20, Y0 + 222, x + CW - 20, Y0 + 222, RULE, 1.0)
    d.t(x + 20, Y0 + 248, impact, 13, c, KR, "start", 600)
    d.t(x + 20, Y0 + 274, fix, 12, SOFT, KR, "start")

d.t(W // 2, Y0 + 340, "앱이 아픈지를 먼저 물으면 두 종류가 갈립니다", 13, MUTED, KR, "middle")
d.t(W // 2, Y0 + 366,
    "2026-09-10 A 문항은 오른쪽이었습니다. 초당 1건씩 규칙적으로 오르는데 아무도 안 아팠습니다.",
    12, SOFT, KR, "middle")

d.save(os.path.join(os.path.dirname(__file__), "..", "2026-09-10.drop-kinds.svg"))
print("ok")

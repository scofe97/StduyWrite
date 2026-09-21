# 02-02.rule-once-per-connection — 규칙을 갱신해도 이미 열린 연결은 옛 결정을 쓴다
# 본문 요구: "항목이 없는 첫 패킷에서만 nat 체인이 평가돼 어느 백엔드로 보낼지가 정해진다 …
#           그 뒤의 패킷들은 규칙을 다시 고르지 않고 이미 정해진 변환을 그대로 적용받는다"
#           (02-02 §3 492·502~510줄). 세 번째 칸이 경계다 — 한 레인만 그 칸에 들어간다.
# 타입 스펙: type-swimlane — 가로 레인 둘(이미 열린 연결 / 새로 여는 연결)이 같은 네 칸을
#           지나되 규칙 칸에 들어가는 레인이 하나뿐인 것을 보인다. 레인 구분은 1px hairline.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, WARN, BAD, INFO, OK, PAPER, PAPER2, KR, MONO

W, H = 920, 400
d = D(W, H, "KUBE-PROXY · WHO RE-READS THE RULES",
      "규칙을 다시 보는 것은 첫 패킷뿐이다",
      "KUBE-SVC 규칙을 갱신해도 이미 열린 연결은 conntrack 항목에 적힌 갱신 전 결정을 그대로 "
      "적용받고, 새로 여는 연결만 갱신된 규칙을 평가해 새 백엔드를 고른다.",
      lead="같은 네 칸을 지나는데 세 번째 칸에 들어가는 레인은 하나뿐이다")

LX, LW, STRIDE = 140, 168, 192          # 첫 칸 x · 칸 폭 · 칸 간격
COL = [LX + i * STRIDE for i in range(4)]
BANDS = [104, 216]                       # 레인 상단 y
BH, CELLH = 92, 64                       # 레인 높이 · 칸 높이
LABEL_X = 12


def cell(x, y, top, sub, c, dash=None, focal=False):
    if focal:
        d.tone(x, y, LW, CELLH, ACC, 6, "14", 1.4)
    elif dash:
        d.o.append(f'<rect x="{x}" y="{y}" width="{LW}" height="{CELLH}" rx="6" '
                   f'fill="none" stroke="{c}" stroke-width="1.1" stroke-dasharray="{dash}"/>')
    else:
        d.tone(x, y, LW, CELLH, c, 6, "12", 1.2)
    d.t(x + LW / 2, y + 27, top, 13, ACC if focal else c, KR, "middle", 600)
    d.t(x + LW / 2, y + 48, sub, 12, MUTED, MONO)


def lane(band, label, sublabel, rows, c):
    y = band + (BH - CELLH) // 2
    d.t(LABEL_X, band + 40, label, 12, c, MONO, "start", 600)
    d.t(LABEL_X, band + 58, sublabel, 12, SOFT, KR, "start")
    for i, (top, sub, cc, dash, focal) in enumerate(rows):
        cell(COL[i], y, top, sub, cc, dash, focal)
        if i:                                   # 인접 칸은 수평 화살표로만 잇는다
            d.arrow([(COL[i] - STRIDE + LW + 6, y + CELLH // 2), (COL[i] - 8, y + CELLH // 2)],
                    c, "info" if c is INFO else "ok", 1.4)


lane(BANDS[0], "ESTABLISHED", "이미 열린 연결", [
    ("연결 중 패킷", "seq 이어짐", INFO, None, False),
    ("conntrack 조회", "항목 있음", INFO, None, False),
    ("건너뜀", "규칙 평가 없음", MUTED, "5 4", False),
    ("Pod A", "갱신 전 결정", WARN, None, False),
], INFO)

d.line(12, 208, W - 12, 208, RULE, 1.0)          # 레인 구분 hairline

lane(BANDS[1], "NEW", "새로 여는 연결", [
    ("첫 패킷", "SYN", OK, None, False),
    ("conntrack 조회", "항목 없음", OK, None, False),
    ("KUBE-SVC 규칙", "갱신된 목록", ACC, None, True),
    ("Pod C", "갱신 후 결정", OK, None, False),
], OK)

d.t(COL[2] + LW / 2, 332, "규칙 평가는 연결마다 한 번", 12, ACC, KR, "middle", 600)

d.legend(344, [("이미 열린 연결", INFO), ("새 연결", OK), ("갱신 전 결정", WARN), ("규칙 평가 자리", ACC)])
d.save("02-02.rule-once-per-connection.svg")
print("ok rule-once-per-connection")

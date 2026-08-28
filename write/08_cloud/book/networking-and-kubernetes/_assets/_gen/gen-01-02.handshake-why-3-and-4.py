# 01-02.handshake-why-3-and-4 — 확인할 것은 양쪽 모두 넷, 합쳐지느냐가 갈랐다
# 본문 요구(01-02 §3): "2번으로 줄이면 서버의 번호가 확인되지 않은 채 연결이 열린다"는 대목의
#           짝이다. 열 때 3번 · 닫을 때 4번이라는 숫자 차이가 확인 항목의 개수 차이처럼 보이지만
#           양쪽 다 넷이고, 갈린 자리는 2·3번이 한 패킷(SYN-ACK)에 실리느냐 하나뿐이다.
#           그래서 가운데 열의 2·3행을 한 칸으로 합치고 왼쪽에 대괄호로 "합쳐짐"을 물렸다 —
#           합쳐진 칸 하나가 이 그림의 전부다.
# 타입 스펙: type-dp-security-matrix.md — 행은 확인해야 할 것 넷, 열은 여는 쪽과 닫는 쪽.
#           같은 행에서 두 열이 갈리는 자리가 판정이다.
#
# ⚠ 이 SVG 는 지금 어느 본문도 참조하지 않는다(2026-08-28 기준 md 전수 grep 0건).
#   01-02 §3 비유 절에 있던 것이 재구성 과정에서 링크만 빠진 것으로 보인다.
#   dd-lint 는 이 장에서 chip 겹침 3건을 잡는다 — "합쳐짐" 칩(폭 41px)이 라벨 열과 가운데 열
#   사이 14px 홈통보다 넓어 양옆 상자를 13.5px 씩 덮는다. 다시 실을지 지울지가 먼저 정해져야
#   고칠 자리가 정해지므로, 지금은 원본을 그대로 재현하고 결함만 여기 적어 둔다.
# 이력: 2026-08-28 신설. 생성기 없이 손으로 만들어진 SVG 였다. 값·좌표를 그대로 옮겼다.
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, PAPER2, KR, MONO

W, H = 938, 530
LX, LW = 12, 250            # 확인해야 할 것
OX, CX_, CW = 276, 590, 300  # 여는 쪽 · 닫는 쪽
HDR_Y, ROW_Y, ROW_H, STRIDE = 112, 176, 64, 74
MERGE_Y, MERGE_H = 250, 138  # 2·3행을 한 칸으로

d = D(W, H, "COMPARISON · 01-02 HANDSHAKE",
      "확인할 것은 양쪽 모두 넷 — 합쳐지느냐가 갈랐다",
      "TCP 연결을 열 때 3번, 닫을 때 4번인 이유. 확인해야 할 항목은 양쪽 모두 네 개로 같지만, "
      "열 때는 가운데 두 항목이 한 패킷(SYN-ACK)에 실려 셋이 되고 닫을 때는 각자 남아 넷이 된다.",
      lead="횟수가 갈리는 것은 확인할 것이 달라서가 아니라 합쳐지느냐 아니냐에서입니다.")

d.box(LX, HDR_Y, LW, 44, PAPER2, RULE, 0.9)
d.t(LX + LW / 2, HDR_Y + 27, "확인해야 할 것", 12, INK, KR, "middle", 600)
for x, c, head, sub in ((OX, OK, "열 때 — 3-way", "셋으로 줄어든다"),
                        (CX_, WARN, "닫을 때 — 4-way", "넷 그대로")):
    d.tone(x, HDR_Y, CW, 44, c, 6, "18", 1.2)
    d.t(x + CW / 2, HDR_Y + 20, head, 12, c, KR, "middle", 600)
    d.t(x + CW / 2, HDR_Y + 37, sub, 10, MUTED)

ROWS = [("1. 내 말이 가는지",   "SYN", "내가 SYN",   "FIN", "내가 FIN"),
        ("2. 그 답이 오는지",   None,  None,        "ACK", "상대가 ACK"),
        ("3. 상대 말이 오는지", None,  None,        "FIN", "상대가 FIN"),
        ("4. 내 답이 가는지",   "ACK", "내가 ACK",   "ACK", "내가 ACK")]

for i, (label, _o, _os, cl, cls) in enumerate(ROWS):
    y = ROW_Y + STRIDE * i
    d.box(LX, y, LW, ROW_H, PAPER2, RULE, 0.9)
    d.t(LX + 14, y + 38, label, 12, INK, KR, "start")
    d.tone(CX_, y, CW, ROW_H, WARN, 6, "0E", 0.9)
    d.t(CX_ + CW / 2, y + 30, cl, 13, WARN, MONO, "middle", 600)
    d.t(CX_ + CW / 2, y + 48, cls, 10, MUTED)

# 여는 쪽 — 1행은 그대로, 2·3행은 한 칸으로 합쳐지고, 4행이 다시 그대로
MCY = MERGE_Y + MERGE_H / 2


def open_cell(i):
    y = ROW_Y + STRIDE * i
    d.tone(OX, y, CW, ROW_H, OK, 6, "0E", 0.9)
    d.t(OX + CW / 2, y + 30, ROWS[i][1], 13, OK, MONO, "middle", 600)
    d.t(OX + CW / 2, y + 48, ROWS[i][2], 10, MUTED)


open_cell(0)
d.tone(OX, MERGE_Y, CW, MERGE_H, ACC, 6, "16", 1.6)
d.t(OX + CW / 2, MCY - 8, "SYN-ACK", 15, ACC, MONO, "middle", 600)
d.t(OX + CW / 2, MCY + 12, "2·3번이 한 패킷에 실린다", 11, ACC)
open_cell(3)

# 왼쪽 대괄호가 어느 두 행이 합쳐졌는지를 물어 준다
R2, R3 = ROW_Y + STRIDE + ROW_H / 2, ROW_Y + STRIDE * 2 + ROW_H / 2
d.path(f"M {OX-10} {R2} L {OX-4} {R2} L {OX-4} {R3} L {OX-10} {R3}", ACC, 1.4)
d.chip(OX - 7.0, MCY, "합쳐짐", ACC, 9)

d.legend(486, [("개별 패킷", OK), ("한 패킷으로 병합", ACC), ("닫을 때는 못 합침", WARN)])
d.save("01-02.handshake-why-3-and-4.svg")
print("ok handshake-why-3-and-4")

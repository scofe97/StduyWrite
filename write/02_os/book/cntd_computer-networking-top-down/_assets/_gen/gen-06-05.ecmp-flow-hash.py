# 타입 스펙: type-architecture — 세 칸이 같은 망 조각(들어오는 패킷 · ECMP 스위치 · 경로 셋 · 서버 셋)을 되풀이하고
#       칸마다 무엇으로 경로를 고르는지 하나만 바꾼다. gen-05-02.ospf-ecmp.py 와 같은 칸 반복 문법이다.
# 출처: 원문 §6.6.1 "Equal Cost Multi Path (ECMP) [RFC 2992], which performs a randomized next-hop selection"
#       + 같은 문단 "While these schemes perform multi-path routing at the flow level, there are also designs
#       that route individual packets within a flow among multiple paths". 원문 밖 사실은 RFC 에서 가져왔다.
#       - 흐름을 가리키는 헤더 필드를 해시해 다음 홉을 고르고, 구역이 그대로면 같은 흐름은 같은 다음 홉: RFC 2992 §1 · §2.2
#       - 패킷마다 차례·무작위로 고르면 한 흐름이 여러 경로로 흩어진다: RFC 2991 §2
#       - 주소 둘만으로 순서는 지키고, 포트까지 넣으면 더 고르게 나뉜다: RFC 6438 §1.1
#       - ICMP 오류는 원래 세션과 같은 곳으로 해시된다는 보장이 없다 · 적재량 헤더는 해시에 안 들어간다: RFC 7690 §1 · §2
#       - 중간 라우터가 만든 ICMPv6 의 출발지는 그 라우터 자신의 주소: RFC 4443 §2.2 (b)
# 노트의 예시: 다음 홉 셋이 서로 다른 서버로 이어지는 배치(RFC 7690 Figure 1 의 형태), 연결 이름 가·나·다,
#       흐름이 몇 번 경로에 배정되는지는 전부 예시다. 해시 값을 계산해 정한 배정이 아니다.
# focal: 둘째 칸 — 본문이 짚는 "흐름마다 고정 · 흐름끼리 흩어짐".
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 1000, 784
d = D(W, H, "SECTION 6.6.1 · ECMP AT THE FLOW LEVEL",
      "같은 흐름은 같은 경로로, 포트 없는 ICMP 는 따로 떨어집니다",
      "ECMP 스위치 하나가 다음 홉 셋 가운데 하나를 고르고 경로마다 서버가 하나씩 있다. "
      "첫 칸은 패킷마다 고를 때로 한 연결 가 의 패킷 셋이 서버 셋에 흩어진다. "
      "둘째 칸은 주소 · 프로토콜 · 포트를 해시할 때로 연결 가 의 패킷은 전부 서버 1 에 가고 나 와 다 는 다른 서버에 간다. "
      "셋째 칸은 가 의 응답 때문에 생긴 Packet Too Big 이 출발지와 포트가 달라 서버 2 로 가고, 가 의 상태를 가진 서버 1 은 알림을 받지 못한다.",
      "세 칸 모두 같은 스위치와 경로 셋입니다. 서버 배치와 흐름 배정은 예시입니다")

PANEL_Y0, PANEL_H, PANEL_STRIDE = 96, 192, 208
PW, PH = 36, 20                            # 패킷 한 개
SW_X, SW_W, SW_H = 244, 112, 40            # ECMP 스위치
JX = 400                                   # 갈라지는 자리
SV_X, SV_W, SV_H = 668, 120, 32            # 서버
BRANCH_DY = (-48, 0, 48)                   # 경로 1 · 2 · 3 의 중심 y 오프셋
PKT_X = (484, 532, 580)                    # 경로 위 패킷 자리
CHIP_CX = 880


def packet(x, cy, label, c=INFO):
    w = PW + (8 if len(label) > 2 else 0)
    d.box(x, cy - PH / 2, w, PH, PAPER, "none", 0, 3)    # 경로 선이 패킷 안으로 비치지 않게
    d.tone(x, cy - PH / 2, w, PH, c, 3, "22", 1.1)
    fam = KR if any("가" <= ch <= "힣" for ch in label) else MONO
    d.t(x + w / 2, cy + 5, label, 13, c, fam, "middle", 600)


def chip(cy, txt, c):
    w = len(txt) * 13 + 16
    d.tone(CHIP_CX - w / 2, cy - 12, w, 24, c, 4, "14", 1.1)
    d.t(CHIP_CX, cy + 5, txt, 13, c, KR, "middle", 600)


def panel(i, title, note, note_c, queue, branches, chips, rule, rule_c=MUTED, idle=(), focal=False):
    y0 = PANEL_Y0 + i * PANEL_STRIDE
    if focal:
        d.tone(24, y0, 952, PANEL_H, ACC, 10, "0A", 1.4)
    else:
        d.box(24, y0, 952, PANEL_H, f"{INK}05", RULE, 1.0, 10)
    d.t(40, y0 + 24, title, 13, INK, KR, "start", 600)
    d.t(960, y0 + 24, note, 13, note_c, KR, "end", 600)
    cy = y0 + 112
    # 들어오는 패킷
    qx = 40
    for lab, c in queue:
        packet(qx, cy, lab, c)
        qx += PW + (8 if len(lab) > 2 else 0) + 8
    d.arrow([(qx, cy), (SW_X - 4, cy)], MUTED, "ar", 1.4)
    d.t(40, y0 + 176, rule, 13, rule_c, KR, "start")
    # 경로 셋 — 빈 경로는 점선
    for k, dy in enumerate(BRANCH_DY):
        by = cy + dy
        dash = "4 4" if k in idle else None
        c = RULE if k in idle else MUTED
        if dy == 0:
            d.path(f"M {SW_X + SW_W} {cy} L {SV_X - 4} {cy}", c, 1.2, dash=dash)
        else:
            d.path(f"M {SW_X + SW_W} {cy} L {JX} {cy} L {JX} {by} L {SV_X - 4} {by}", c, 1.2, dash=dash)
        d.t(JX + 12, by - 8, f"경로 {k + 1}", 12, SOFT, KR, "start")
        for j, (lab, pc) in enumerate(branches[k]):
            packet(PKT_X[j], by, lab, pc)
        d.box(SV_X, by - SV_H / 2, SV_W, SV_H, PAPER2, RULE, 1.0, 6)
        d.t(SV_X + SV_W / 2, by + 5, f"서버 {k + 1}", 13, INK, KR, "middle", 600)
        if chips[k]:
            chip(by, *chips[k])
    d.box(SW_X, cy - SW_H / 2, SW_W, SW_H, PAPER2, MUTED, 1.2, 6)
    d.t(SW_X + SW_W / 2, cy + 5, "ECMP 스위치", 13, INK, KR, "middle", 600)


# ── 1. 패킷마다 고를 때 ──
panel(0, "1. 패킷마다 고를 때", "한 연결이 세 서버로 갈림", BAD,
      [("가1", INFO), ("가2", INFO), ("가3", INFO)],
      [[("가1", INFO)], [("가2", INFO)], [("가3", INFO)]],
      [("가 상태 있음", OK), ("가 상태 없음", BAD), ("가 상태 없음", BAD)],
      "고르는 기준 · 패킷마다 차례 또는 무작위")

# ── 2. 흐름마다 해시할 때 ──
panel(1, "2. 흐름마다 해시할 때", "같은 흐름 → 같은 서버", OK,
      [("가1", INFO), ("나1", INFO), ("가2", INFO), ("다1", INFO)],
      [[("가1", INFO), ("가2", INFO)], [("다1", INFO)], [("나1", INFO)]],
      [("가 상태 있음", OK), ("다 상태 있음", OK), ("나 상태 있음", OK)],
      "해시 입력 · 주소 둘 · TCP · 포트 둘", focal=True)

# ── 3. 포트 없는 ICMP ──
panel(2, "3. 포트 없는 ICMP", "서버 1 은 알림을 못 받음", WARN,
      [("가1", INFO), ("가2", INFO), ("PTB", WARN)],
      [[("가1", INFO), ("가2", INFO)], [("PTB", WARN)], []],
      [("가 상태 있음", OK), ("가 상태 없음 · 버림", BAD), None],
      "PTB 해시 입력 · 라우터 주소 · 서버 주소 · ICMP", WARN, idle=(2,))

d.legend(728, [("TCP 패킷", INFO), ("연결 상태 있음", OK), ("상태 없음", BAD), ("ICMP 오류", WARN), ("본문이 짚는 칸", ACC)])
d.t(960, 776, "KUROSE-ROSS 9E 6.6.1 · RFC 2992 · RFC 2991 §2 · RFC 6438 §1.1 · RFC 7690 §2", 8, SOFT, MONO, "end")

out = pathlib.Path(__file__).resolve().parent.parent / "06-05.ecmp-flow-hash.svg"
d.save(out)
print("→", out)

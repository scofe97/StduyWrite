# 05-01 결정 치트시트 — 캡처에서 어느 메시지까지 갔는지로 원인을 가르는 판단 흐름. 치트시트 표의 행과 대응한다.
# 타입 스펙: type-flowchart — 조건에 따라 갈라지는 판단 논리. 마름모가 판단, 오른쪽 칸이 결론이다.
#           focal 은 학습자가 "바로 써도 된다"고 예측했던 판단 하나(REQUEST 뒤 답이 왔나).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, WARN, BAD, INFO, PAPER2, RULE, KR, MONO

def kr(s): return KR if any("가" <= c <= "힣" for c in s) else MONO

W, H = 880, 884
d = D(W, H, "PACKET ANALYSIS WITH WIRESHARK · 05-01 CHEATSHEET",
      "어느 메시지까지 갔나",
      "주소 할당을 담은 캡처를 위에서부터 판단한다. DHCP 가 보이는지, 서버가 답했는지, 첫 답이 REPLY 인지, REQUEST 를 보냈는지, 그 뒤 답이 왔는지, 거절인지, DECLINE 이 있는지 순서로 갈린다.",
      "마름모 하나가 치트시트 표의 한 행입니다 — 오른쪽으로 빠지는 곳이 원인입니다")

CX, HW, HH = 244, 176, 26      # 판단 열 중심 · 마름모 반폭 · 반높이
RX, RW, RH = 668, 336, 52      # 결론 칸 중심 · 너비 · 높이
R_LEFT = RX - RW / 2
Y0, ST = 164, 84               # 첫 마름모 위 · stride

def oval(cx, y, w, h, txt, c=INK):
    d.o.append(f'<rect x="{cx - w / 2}" y="{y}" width="{w}" height="{h}" rx="20" '
               f'fill="{PAPER2}" stroke="{c}" stroke-width="1.1"/>')
    d.t(cx, y + h / 2 + 5, txt, 13, c, KR, "middle", 600)

def diamond(cy, txt, focal=False):
    c = ACC if focal else INK
    d.o.append(f'<polygon points="{CX},{cy - HH} {CX + HW},{cy} {CX},{cy + HH} {CX - HW},{cy}" '
               f'fill="{ACC + "12" if focal else PAPER2}" stroke="{c}" stroke-width="{1.4 if focal else 1.1}"/>')
    d.t(CX, cy + 5, txt, 13, c, kr(txt), "middle", 600)

def result(cy, title, sub, c, focal=False):
    y = cy - RH / 2
    if focal:
        d.o.append(f'<rect x="{R_LEFT}" y="{y}" width="{RW}" height="{RH}" rx="6" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
        c = ACC
    else:
        d.tone(R_LEFT, y, RW, RH, c, 6)
    d.t(RX, y + 22, title, 13, c, kr(title), "middle", 600)
    d.t(RX, y + 40, sub, 12, MUTED, kr(sub))

STEPS = [  # (판단, 오른쪽으로 빠지는 답, 결론 제목, 결론 부제, 색, focal)
    ("DHCP 교환이 보이나?",      "아니오", "정적 설정 · SLAAC",   "icmpv6.type == 134",           INFO, False),
    ("서버가 답했나?",           "아니오", "서버 무응답",          "기동 · 릴레이 · 세그먼트 · v4 는 주소 풀", WARN, False),
    ("첫 답이 REPLY 인가?",      "예",    "rapid commit",        "NoAddrsAvail 없으면 정상",               OK,   False),
    ("REQUEST 를 보냈나?",       "아니오", "제안이 안 닿음 · 못 고름",   "캡처 위치 · 플래그 · v6 NoAddrsAvail",       WARN, False),
    ("REQUEST 뒤 답이 왔나?",    "아니오", "확정 못 함",           "옵션 54 의 서버 · §5 예약 아님",   ACC,  True),
    ("NAK · NoAddrsAvail 인가?", "예",    "서버가 거절",          "v4 NAK 무효·먼저 확정 · v6 주소 풀",        BAD,  False),
    ("DECLINE 이 보이나?",       "예",    "주소 충돌",            "ARP 로 그 주소의 장비 찾기",        BAD,  False),
]

oval(CX, 92, 240, 36, "주소 할당 캡처를 연다")
d.arrow([(CX, 128 + 4), (CX, Y0 + 26 - HH - 4)], MUTED, "ar", 1.4)
for i, (q, side, title, sub, c, focal) in enumerate(STEPS):
    cy = Y0 + 26 + i * ST
    diamond(cy, q, focal)
    d.arrow([(CX + HW + 4, cy), (R_LEFT - 4, cy)], ACC if focal else c, "acc" if focal else {INFO: "info", WARN: "warn", OK: "ok", BAD: "bad"}[c], 1.4)
    d.t(CX + HW + 24, cy - 8, side, 12, ACC if focal else c, KR, "start", 600)
    result(cy, title, sub, c, focal)
    other = "예" if side == "아니오" else "아니오"
    d.arrow([(CX, cy + HH + 4), (CX, cy + ST - HH - 4)], MUTED, "ar", 1.4)
    d.t(CX + 12, cy + HH + 22, other, 12, MUTED, KR, "start", 600)

END_Y = Y0 + 26 + len(STEPS) * ST - HH
oval(CX, END_Y, 240, 36, "ACK · REPLY 로 확정", OK)

d.legend(H - 56, [("ACK 가 필요한 이유로 가는 갈래", ACC), ("원인 후보", WARN), ("거절 · 충돌", BAD), ("정상", OK), ("주소 경로가 다름", INFO)])
d.save("05-01.triage.svg")

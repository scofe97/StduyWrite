# 05-02 §1 — 접속이 안 될 때 이름 해석에서 막혔는지 연결에서 막혔는지를 캡처에 무엇이 있고 없는지로 가른다.
# 본문 요구: "서버에 못 붙는다는 신고에서 이름 해석이 실패한 것인지 연결이 실패한 것인지는 완전히 다른
#            문제입니다." 이름이 안 풀리면 목적지로 가는 SYN 이 아예 없다(학습자 예측). 캐시는 RFC 1034
#            §5.3.3 1단계, RCODE 3 은 RFC 1035 §4.1.1, RST·무응답 재전송은 3장 03-02 §1 이 근거다.
# 타입 스펙: type-flowchart — 조건에 따라 갈라지는 판단 논리. 마름모가 판단, 오른쪽 칸이 결론이다.
#           05-01.triage 의 판단 열·결론 칸 좌표를 그대로 쓴다. focal 은 이름 해석이 끝나는 판단 하나.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, WARN, BAD, INFO, PAPER2, RULE, KR, MONO

def kr(s): return KR if any("가" <= c <= "힣" for c in s) else MONO

W, H = 880, 640
d = D(W, H, "PACKET ANALYSIS WITH WIRESHARK · 05-02 §1",
      "이름 해석 실패인가, 연결 실패인가",
      "접속이 안 되는 캡처를 위에서부터 판단한다. dns 질의가 보이는지, 응답이 왔는지, 답에 주소가 있는지까지가 이름 해석이고, 그 주소로 보낸 SYN 에 SYN/ACK 가 오는지부터가 연결이다.",
      "위 셋이 이름 해석, 마지막 하나가 연결입니다 — 이름이 안 풀리면 SYN 이 없습니다")

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
    ("dns 질의가 보이나?",      "아니오", "선에 안 나간 질의",    "TTL 안의 캐시 · DoT · DoH",      INFO, False),
    ("질의에 응답이 왔나?",     "아니오", "리졸버에 못 닿음",     "UDP 53 경로 · 리졸버 주소",      WARN, False),
    ("답에 주소가 있나?",       "아니오", "이름 해석 실패",       "RCODE 3 이면 그 이름이 없음",    ACC,  True),
    ("SYN 에 SYN/ACK 가 왔나?", "아니오", "연결 실패",           "RST 면 거절 · 무응답이면 재전송",  BAD,  False),
]

oval(CX, 92, 240, 36, "접속 실패 캡처를 연다")
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

# 이름 해석과 연결의 경계 — 셋째 판단과 넷째 판단 사이. 화살표와 "예" 라벨 자리는 비운다
DIV_Y = Y0 + 26 + 2 * ST + ST / 2
d.line(24, DIV_Y, CX - 32, DIV_Y, SOFT, 1.0, "4 4")
d.line(CX + 48, DIV_Y, W - 24, DIV_Y, SOFT, 1.0, "4 4")
d.t(24, DIV_Y - 8, "이름 해석", 12, SOFT, KR, "start", 600)
d.t(24, DIV_Y + 20, "연결", 12, SOFT, KR, "start", 600)

END_Y = Y0 + 26 + len(STEPS) * ST - HH
oval(CX, END_Y, 280, 36, "연결 성립 · 다음은 HTTP", OK)

d.legend(H - 56, [("이름 해석이 끝나는 판단", ACC), ("선에 안 보임", INFO), ("원인 후보", WARN), ("연결 실패", BAD), ("정상", OK)])
d.save("05-02.resolve-vs-connect.svg")

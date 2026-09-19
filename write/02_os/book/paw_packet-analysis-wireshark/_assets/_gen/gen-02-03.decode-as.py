# 02-03 §1 — Wireshark 가 프로토콜을 정하는 두 단계(포트 표 → 휴리스틱)와 둘 다 빗나갔을 때 Decode-As 로
# 사람이 덮어쓰는 경로. 본문: "먼저 포트 표를 보고, 표에 없으면 패킷 내용으로 짐작하는 휴리스틱 디섹터에게
# 넘깁니다" · "휴리스틱이 없는 프로토콜이 표에 없는 포트에서 돌 때 … Decode As 로 풀립니다".
# 타입 스펙: type-flowchart — 조건에 따라 갈라지는 판단 논리. 도형이 종류를 나른다
#           (사각형=단계, 마름모=판단). 스펙 관례대로 예는 오른쪽, 아니오는 아래로 나간다.
#           focal 은 TCP 로만 보이는 갈림을 만드는 판단 하나(휴리스틱). 예시 포트는 tshark 4.6.8 실측값.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, WARN, PAPER2, RULE, KR, MONO

W, H = 880, 624
d = D(W, H, "PACKET ANALYSIS WITH WIRESHARK · 02-03 §1",
      "포트 표와 짐작으로 프로토콜을 정합니다",
      "Wireshark 는 TCP 포트를 포트 표에서 먼저 찾고, 표에 없으면 휴리스틱 디섹터가 패킷 내용으로 짐작한다. 둘 다 빗나가면 TCP 로만 보이고 Decode-As 가 그 매핑을 사람이 덮어쓴다.",
      "4433 의 TLS 는 휴리스틱이 잡고, 16379 의 Redis 는 Decode As 가 있어야 풀립니다")

AX, BX = 220, 610            # 판단 열 · 결과 열 중심
AW, BW = 280, 300            # 상자 폭
HW, HH = 140, 36             # 마름모 반폭 · 반높이

def step(cx, y, w, h, title, sub, c=None, sub_mono=False):
    if c: d.tone(cx - w / 2, y, w, h, c, 6)
    else: d.box(cx - w / 2, y, w, h, PAPER2, RULE, 1.0, 6)
    d.t(cx, y + 24, title, 13, c if c else INK, KR, "middle", 600)
    d.t(cx, y + 44, sub, 12, MUTED, MONO if sub_mono else KR)

def diamond(cx, y, txt, focal=False):
    cy, c = y + HH, (ACC if focal else INK)
    d.o.append(f'<polygon points="{cx},{y} {cx + HW},{cy} {cx},{y + 2 * HH} {cx - HW},{cy}" '
               f'fill="{ACC + "12" if focal else PAPER2}" stroke="{c}" stroke-width="{1.4 if focal else 1.1}"/>')
    d.t(cx, cy + 5, txt, 13, c, KR, "middle", 600)

Y_S, Y_D1, Y_D2, Y_TCP, Y_DA = 100, 184, 292, 400, 492
C_D1, C_D2 = Y_D1 + HH, Y_D2 + HH
RAIL = 800

# 연결선 — 상자보다 먼저 깐다
d.arrow([(AX, Y_S + 60), (AX, Y_D1 - 4)], MUTED, "ar", 1.4)
d.arrow([(AX, Y_D1 + 2 * HH), (AX, Y_D2 - 4)], MUTED, "ar", 1.4)
d.arrow([(AX, Y_D2 + 2 * HH), (AX, Y_TCP - 4)], WARN, "warn", 1.4)
d.arrow([(AX, Y_TCP + 64), (AX, Y_DA - 4)], WARN, "warn", 1.4)
d.arrow([(AX + HW, C_D1), (BX - BW / 2 - 4, C_D1)], OK, "ok", 1.4)
d.arrow([(AX + HW, C_D2), (BX - BW / 2 - 4, C_D2)], OK, "ok", 1.4)
d.arrow([(BX + BW / 2, C_D1), (RAIL, C_D1), (RAIL, Y_DA + 32), (BX + BW / 2 + 4, Y_DA + 32)], OK, "ok", 1.4)
d.arrow([(BX, C_D2 + 32), (BX, Y_DA - 4)], OK, "ok", 1.4)
d.arrow([(AX + AW / 2, Y_DA + 32), (BX - BW / 2 - 4, Y_DA + 32)], WARN, "warn", 1.4)

step(AX, Y_S, AW, 60, "프레임 수신", "TCP 포트 읽기")
diamond(AX, Y_D1, "포트 표에 있나?")
diamond(AX, Y_D2, "내용으로 짐작되나?", focal=True)
step(BX, C_D1 - 32, BW, 64, "포트 표의 디섹터로 해석", "443 → TLS · 6379 → RESP", c=OK, sub_mono=True)
step(BX, C_D2 - 32, BW, 64, "휴리스틱 디섹터로 해석", "4433 의 TLS 레코드", c=OK)
step(AX, Y_TCP, AW, 64, "TCP 로만 표시", "16379 의 Redis · 휴리스틱 없음", c=WARN)
step(AX, Y_DA, AW, 64, "Decode As · tshark -d", "포트에 디섹터를 손으로 지정", c=WARN)
step(BX, Y_DA, BW, 64, "Packet Details 에 펼침", "복호화가 아닌 해석")

# 갈림 라벨 — 모든 출구에 붙인다
d.t(AX + HW + 12, C_D1 - 10, "예", 12, OK, KR, "start", 600)
d.t(AX + HW + 12, C_D2 - 10, "예", 12, OK, KR, "start", 600)
d.t(AX + 12, Y_D1 + 2 * HH + 16, "아니오", 12, MUTED, KR, "start", 600)
d.t(AX + 12, Y_D2 + 2 * HH + 16, "아니오", 12, WARN, KR, "start", 600)

d.legend(572, [("TCP 로만 보이게 갈리는 판단", ACC), ("자동 판별이 맞은 경로", OK), ("사람이 덮어쓰는 경로", WARN)])
d.save("02-03.decode-as.svg")

# 01-01-i2-fix — 계측으로 본 분기: 같은 쉰 연결 경합을 GET 은 다시 보내 숨기고 POST 는 502 로 드러낸다
# 본문 요구(01-01 I2 고친 뒤): ADR 0013 재확인에서 GET 재전송 13건(attempts=2)과 POST 502 10건(attempts=1)이 갈린 분기를 보인다.
# 타입 스펙: type-flowchart — 쉰 연결 경합 한 곳에서 GET 행과 POST 행으로 갈리는 4열 흐름. focal 은 POST 의 재전송 없음.
# 사실 출처: ch08-server-idle-close-post-502.md ADR 0013 재확인(509건, GET 261·POST 248), ADR 0013 결정 1·4
import sys
from pathlib import Path

ASSETS_DIR = Path(__file__).resolve().parent.parent
GEN_DIR = Path(__file__).resolve().parent
if str(ASSETS_DIR) not in sys.path:
    sys.path.insert(0, str(ASSETS_DIR))
if str(GEN_DIR) not in sys.path:
    sys.path.insert(0, str(GEN_DIR))

from dd import D, INK, MUTED, SOFT, ACC, WARN, OK, KR, MONO
from ddk import node

W = 960
H = 468

# 4열: 폭 합 168+176+200+224 = 768, 간격 3칸 × 48 = 144, 좌우 여백 24 → 960
XA, WA = 24, 168
XB, WB = 240, 176
XC, WC = 464, 200
XD, WD = 712, 224

Y_GET, H_ROW = 128, 76
Y_POST = 280
Y_MID = (Y_GET + Y_POST + H_ROW) / 2 - H_ROW / 2

d = D(
    W,
    H,
    "FLOW · CH08 I2 FIX",
    "계측으로 본 GET 과 POST 의 분기",
    "백엔드가 먼저 닫은 쉰 연결로 요청이 나갔을 때 GET 은 새 연결로 다시 보내져 숨겨지고 POST 는 502 UC 로 드러나는 분기",
    lead="같은 경합에 걸린 비율은 GET 약 5.0%, POST 약 4.0%로 비슷하지만 손님에게 보이는 결과는 갈립니다.",
)

# 공통 시작: 쉰 연결
node(d, XA, Y_MID, WA, H_ROW, "쉰 연결 경합", "백엔드가 먼저 닫음")

# GET 행
node(d, XB, Y_GET, WB, H_ROW, "GET 판정", "다시 보내도 안전")
node(d, XC, Y_GET, WC, H_ROW, "새 연결로 재전송", "attempts=2 · 13건")
node(d, XD, Y_GET, WD, H_ROW, "200 으로 숨김", "502 0/261건", c=OK)

# POST 행
node(d, XB, Y_POST, WB, H_ROW, "POST 판정", "재전송 대상 아님")
node(d, XC, Y_POST, WC, H_ROW, "재전송 없음", "attempts=1 · 프록시 재시도 층 없음", c=ACC, focal=True)
node(d, XD, Y_POST, WD, H_ROW, "502 (UC) 로 노출", "10/248건 (약 4.0%)", c=WARN)

# 시작 → 두 행: 꺾는 화살표
sx = XA + WA
mid_y = Y_MID + H_ROW / 2
bx = (sx + XB) / 2
d.arrow([(sx + 3, mid_y), (bx, mid_y), (bx, Y_GET + H_ROW / 2), (XB - 3, Y_GET + H_ROW / 2)], MUTED, "ar", 1.3)
d.arrow([(bx, mid_y), (bx, Y_POST + H_ROW / 2), (XB - 3, Y_POST + H_ROW / 2)], MUTED, "ar", 1.3)

# 행 안 화살표
for y in (Y_GET, Y_POST):
    cy = y + H_ROW / 2
    c, m = (SOFT, "soft")
    d.arrow([(XB + WB + 3, cy), (XC - 3, cy)], c, m, 1.3)
    d.arrow([(XC + WC + 3, cy), (XD - 3, cy)], c, m, 1.3)

d.t(24, 440, "측정: 2026-10-29 약 4분, 프록시 509건 (GET 261 · POST 248), 백엔드 idle_close 1초", 12, MUTED, KR, "start")

d.legend(392, [("재전송이 없는 자리 (focal)", ACC), ("손님에게 보이는 실패", WARN), ("숨겨진 경합", OK)])

d.save("01-01-i2-fix.svg")

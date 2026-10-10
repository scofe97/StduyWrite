# 타입 스펙: type-flowchart — 송신자 측 SWS 회피 알고리즘의 네 가지 전송 조건 판정 순서도.
# 사실 출처: RFC 9293 §3.8.6.2.1 · RFC 1122 §4.2.3.4 · 원서 §15.5.3 — 풀 세그먼트(MSS), PUSH 및 미확인 없음 잔여 전체, 미확인 없음 최대 창 절반, 오버라이드 타임아웃.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 590
d = D(W, H, "TCP/IP ILLUSTRATED VOL.1 · 15-02 §3",
      "송신자 SWS 회피 알고리즘 판정 순서도",
      "송신자는 작은 세그먼트를 쏟아내지 않기 위해 MSS 크기를 채우거나, PUSH 플래그로 잔여분을 다 보내거나, 수신자 최대 창의 절반 이상일 때만 전송한다. 모든 조건에 미달하면 전송을 보류하고 창이 열리길 기다린다.",
      "네 조건 중 하나라도 충족해야 데이터를 전송합니다")

COL_CHK = 70
COL_ACT = 680
BOX_W, BOX_H = 480, 68
ACT_W, ACT_H = 170, 160

Y_START = 104
Y_GAP = 86

checks = [
    ("조건 1: 풀 세그먼트 충족", "min(D, U) ≥ Eff.snd.MSS", "최대 세그먼트 크기를 채워 전송 효율 극대화"),
    ("조건 2: PUSH 및 잔여 전체 전송", "[SND.NXT = SND.UNA and] PUSHed and D ≤ U", "PUSH 지정·큐 잔여 전체 전송 (대괄호는 Nagle 이 켜졌을 때 더해지는 조건)"),
    ("조건 3: 최대 광고 창 절반 충족", "[SND.NXT = SND.UNA and] min(D, U) ≥ ½ · Max(SND.WND)", "최대 창의 절반 이상 채움 (대괄호는 Nagle 조건)"),
    ("조건 4: 재정의 타이머 만료", "오버라이드 타임아웃(0.1~1.0초)", "영구 교착 방지 강제 전송 (persist 타이머와 합쳐 구현 가능)"),
]

# 오른쪽 전송 결정 상자
d.box(COL_ACT, Y_START + 80, ACT_W, ACT_H, PAPER2, OK, 1.2, 8)
d.tone(COL_ACT, Y_START + 80, ACT_W, 36, OK, 8, "20", 1.0)
d.t(COL_ACT + ACT_W/2, Y_START + 104, "데이터 즉시 전송", 14, OK, KR, "middle", 600)
d.t(COL_ACT + ACT_W/2, Y_START + 144, "세그먼트 구성 후 송신", 12, INK, KR, "middle")
d.t(COL_ACT + ACT_W/2, Y_START + 172, "SWS 회피 조건 충족", 11, MUTED, KR, "middle")

# 아래 보류 상자
Y_WAIT = Y_START + 4 * Y_GAP
d.box(COL_CHK, Y_WAIT, BOX_W, 56, PAPER2, WARN, 1.2, 8)
d.tone(COL_CHK, Y_WAIT, BOX_W, 56, WARN, 8, "15", 1.0)
d.t(COL_CHK + BOX_W/2, Y_WAIT + 24, "송신 보류 (대기)", 14, WARN, KR, "middle", 600)
d.t(COL_CHK + BOX_W/2, Y_WAIT + 44, "창 확장 또는 버퍼 소비 대기", 12, MUTED, KR, "middle")

for i, (title, formula, note) in enumerate(checks):
    y = Y_START + i * Y_GAP
    d.box(COL_CHK, y, BOX_W, BOX_H, PAPER2, RULE, 1.0, 6)
    d.t(COL_CHK + 16, y + 21, title, 13, INK, KR, "start", 600)
    d.t(COL_CHK + 16, y + 41, formula, 11, ACC, MONO, "start", 600)
    d.t(COL_CHK + 16, y + 58, note, 11, MUTED, KR, "start")

    # 예 화살표 -> 직교 배선으로 오른쪽 전송 상자에 연결
    arrow_y = y + BOX_H / 2
    target_y = Y_START + 80 + 36 + i * 28
    corner_x = COL_ACT - 24 + i * 4
    d.arrow([(COL_CHK + BOX_W, arrow_y), (corner_x, arrow_y), (corner_x, target_y), (COL_ACT, target_y)], OK, "ok", 1.4)
    d.t(COL_CHK + BOX_W + 18, arrow_y - 6, "예", 11, OK, KR, "middle", 600)

    # 아니오 화살표 -> 다음 검사 또는 보류
    if i < len(checks) - 1:
        ny = y + Y_GAP
        d.arrow([(COL_CHK + 40, y + BOX_H), (COL_CHK + 40, ny)], MUTED, "ar", 1.2)
        d.t(COL_CHK + 52, y + BOX_H + 11, "아니오", 11, MUTED, KR, "start")
    else:
        d.arrow([(COL_CHK + 40, y + BOX_H), (COL_CHK + 40, Y_WAIT)], MUTED, "ar", 1.2)
        d.t(COL_CHK + 52, y + BOX_H + 11, "아니오", 11, MUTED, KR, "start")

d.legend(H - 46, [("조건 충족 (즉시 전송)", OK), ("조건 미달 (대기)", WARN), ("판정 수식", ACC)])
d.save("15-02.sws-sender-avoidance.svg")

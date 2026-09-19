# 2026-09-10 E · 원인 분석 — 같은 lock() 대기가 synchronized 안이냐 밖이냐로 갈린다.
# 이 장의 논지는 "갈림길" 하나다. 원이 어떻게 닫히는지는 deadlock-cycle 이 맡는다.
# 기전은 Netflix 원문(2024-07-30)을 따른다 — 기다린 것은 I/O 가 아니라 ReentrantLock 이고,
# 인스턴스가 4 vCPU 라 캐리어도 4개였다. 2026-09-13 이전 판은 I/O 대기로 그려 틀렸다.
# 타입 스펙: type-flowchart — 시작 타원 → 결정 마름모 하나 → 두 갈래. 스펙대로 모양이 종류를 나른다.
#           accent 는 가장 중요한 결정(마름모) 한 곳에만 쓴다. 끝 상자 두 개는 상태색(ok/bad).
#           loop·state 는 이전 판에서 기각했고 이유가 그대로다(끝이 있는 경로, 자원 점유 관계).
# 좌표: 스펙은 수치 공식이 없다(Layout conventions). stride — 열 중심 196/684, 행 96, 모든 값 4의 배수.
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dd import D, ACC, MUTED, SOFT, INK, BAD, OK, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 668
d = D(W, H, "TROUBLESHOOTING DRILL · 2026-09-10 E",
      "같은 락 대기, 갈리는 두 경로",
      "가상 스레드가 lock() 에서 기다릴 때 synchronized 블록 밖이면 캐리어에서 내려와 자리를 비우고, "
      "안이면 내려오지 못해 캐리어를 붙든 채 멈춘다. 캐리어 4개가 모두 이렇게 묶이면 락이 풀려도 "
      "다음 차례가 올라탈 자리가 없다.",
      lead="synchronized 블록 안이냐 밖이냐가 캐리어를 놓느냐를 가릅니다.")

def kr(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO

CX = W // 2
LX, RX = 196, 684          # 두 열의 중심
BW, BH = 288, 64
ROW = [324, 420, 516]      # stride 96

# 시작 — 타원
d.box(CX - 180, 100, 360, 48, PAPER2, RULE, 1.0, 24)
d.t(CX, 130, "가상 스레드가 lock() 에서 기다림", 14, INK, KR, "middle", 600)
d.arrow([(CX, 148), (CX, 176)], MUTED, "ar", 1.3)

# 결정 — 마름모. 이 도식의 focal
DY, DW, DH = 236, 170, 56
d.o.append(f'<polygon points="{CX},{DY-DH} {CX+DW},{DY} {CX},{DY+DH} {CX-DW},{DY}" '
           f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t(CX, DY + 5, "synchronized 블록 안인가?", 14, INK, KR, "middle", 600)

# 두 갈래 — 꼭짓점에서 열 중심으로 꺾어 내려간다
d.arrow([(CX - DW, DY), (LX, DY), (LX, ROW[0])], MUTED, "ar", 1.3)
d.arrow([(CX + DW, DY), (RX, DY), (RX, ROW[0])], MUTED, "ar", 1.3)
d.t(LX - 12, 292, "아니오 · 블록 밖", 13, OK, KR, "end", 600)
d.t(RX + 12, 292, "예 · 블록 안", 13, BAD, KR, "start", 600)

def column(cx, rows, c):
    x = cx - BW // 2
    for i, (name, sub) in enumerate(rows):
        y = ROW[i]
        last = i == len(rows) - 1
        if last:
            d.tone(x, y, BW, BH, c, 6)
        else:
            d.box(x, y, BW, BH, PAPER2, RULE, 1.0, 6)
        d.t(x + 16, y + 27, name, 14, c if last else INK, KR, "start", 600)
        d.t(x + 16, y + 49, sub, 12, MUTED, kr(sub), "start")
        if not last:
            d.arrow([(cx, y + BH), (cx, ROW[i + 1])], SOFT, "soft", 1.2)

column(LX, [
    ("캐리어에서 내려옴", "park · unmount"),
    ("다른 가상 스레드가 올라탐", "캐리어 재사용"),
    ("캐리어가 남으면 다시 올라타 진행", "자리가 돌아 처리량 유지"),
], OK)

column(RX, [
    ("내려오지 못함", "pinned · 캐리어 붙든 채 park"),
    ("캐리어 4개가 전부 묶임", "4 vCPU → 캐리어 4개"),
    ("다음 차례가 올라탈 자리 없음", "락은 비었는데 아무도 못 가져감"),
], BAD)

d.line(12, 600, W - 48, 600, RULE, 0.8)
d.t(CX, 628, "새 요청의 가상 스레드는 한 줄도 못 돌고 소켓을 쥔 채 쌓입니다 — CLOSE_WAIT 4127",
    13, MUTED, KR, "middle")
d.t(CX, 652, "원이 어떻게 닫히는지는 '왜 스스로 풀리지 않는가' 그림이 봅니다.",
    12, SOFT, KR, "middle")

d.save(os.path.join(os.path.dirname(__file__), "..", "2026-09-10.pinning-deadlock.svg"))
print("ok")

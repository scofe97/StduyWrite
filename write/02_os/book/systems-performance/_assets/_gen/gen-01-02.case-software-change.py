# 01-02 §8 소프트웨어 변경 — 고정 부하의 CPU 사용률과 서버를 100% 로 몬 천장이 같은 비율로 움직인다(원서 1.11.2).
# 타입 스펙: type-bar — 두 버전의 수치 비교. 단위가 다른 두 판(CPU % · 요청/초)을 나란히 두고 판마다 y 축은 0 에서 시작한다.
#           축약: 막대 넷(판마다 둘)이라 4~8 상한 안이다. 판 사이 화살표 대신 계산식 한 줄로 두 판을 잇는다.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import ACC, MUTED, SOFT, INK, INFO, WARN, PAPER2, RULE, KR, MONO

W, H = 920, 512
YB, PH = 400, 240                       # 0 의 y · 판 높이
BW = 88

d = DK(W, H, "SYSTEMS PERFORMANCE · 01-02 §8 · SEC 1.11.2",
       "같은 부하에 CPU 를 더 쓰면 천장이 그만큼 낮다",
       "원서 1.11.2 의 사례. 초당 700 요청 고정 부하에서 현 버전은 CPU 32개를 평균 20%, 새 버전은 30% 썼다. 클라이언트를 병렬로 띄워 서버를 CPU 100% 까지 몰자 현 버전 3,500, 새 버전 2,300 요청/초에 닿았다.",
       "700 × 100 ÷ 20 = 3,500 · 700 × 100 ÷ 30 ≈ 2,333")

def panel(x0, title, unit, vmax, ticks, bars):
    d.t(x0, YB - PH - 28, title, 14, INK, KR, "start", 600)
    for t in ticks:
        y = YB - t / vmax * PH
        d.line(x0 + 48, y, x0 + 360, y, RULE, 1.0 if t == 0 else 0.6)
        d.t(x0 + 40, y + 4, f"{t:,}", 12, SOFT, MONO, "end")
    d.t(x0 + 40, YB - PH - 8, unit, 12, SOFT, KR, "end")
    for k, (lab, v, c, vtxt) in enumerate(bars):
        bx = x0 + 96 + k * 136
        h = v / vmax * PH
        d.tone(bx, YB - h, BW, h, c, 4)
        d.t(bx + BW / 2, YB - h - 10, vtxt, 13, c, MONO, "middle", 600)
        d.t(bx + BW / 2, YB + 22, lab, 13, INK, KR, "middle", 600)

panel(24, "고정 부하 700 요청/초의 CPU 사용률", "%", 40, [0, 10, 20, 30, 40],
      [("현 버전", 20, INFO, "20%"), ("새 버전", 30, WARN, "30%")])
panel(480, "서버를 CPU 100% 로 몬 처리량", "요청/초", 4000, [0, 1000, 2000, 3000, 4000],
      [("현 버전", 3500, INFO, "3,500"), ("새 버전", 2300, ACC, "2,300")])
y700 = YB - 700 / 4000 * PH
d.line(480 + 48, y700, 480 + 360, y700, SOFT, 1.0, "4 4")
d.t(480 + 360, YB - PH - 8, "점선 · 단일 스레드 클라이언트의 천장 700", 12, SOFT, KR, "end")

d.legend(YB + 48, [("현 버전", INFO), ("새 버전 — 고정 부하", WARN), ("새 버전 — 회귀가 낮춘 천장", ACC)])
d.save("01-02.case-software-change.svg")

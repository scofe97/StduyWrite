# 04-02 §2 — 원문 Figure 4.9 의 출력 포트 큐잉. 패브릭이 회선의 N 배로 빨라도 출력 링크는 단위 시간에 하나만 내보내므로
# 같은 출력으로 몰리면 줄이 선다. 넘치면 새로 온 것을 버리거나(꼬리 버리기) 이미 선 것을 빼내고, 차기 전에 미리 표시하는 것이 AQM 이다.
# 큐 슬롯 다섯·입력 셋은 장면을 위한 값이다. 원문에 수치 예는 없다.
# 타입 스펙: type-data-flow — semantic-patterns 의 "Fan-in queue / bottleneck". 출발지 여럿 · 보이는 슬롯 · 용량 라벨 · 병목 하나 · 결과 둘.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, BAD, WARN, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 560
SX, SW, SH = 40, 120, 44
SY = [190, 254, 318]
CX = 200                     # 수집선
QX, QY, QW, QH = 256, 236, 360, 80
SLOT_W, SLOT_H, SLOT_STRIDE = 56, 40, 64
SVX, SVY, SVW, SVH = 664, 248, 160, 56

d = D(W, H, "COMPUTER NETWORKING TOP-DOWN · 04-02 §2",
      "빨라도 출력에는 줄이 섭니다",
      "원문 Figure 4.9. 입력 여럿이 같은 출력 포트로 몰리면 단위 시간에 하나만 내보내는 출력 링크 앞에 줄이 서고, 메모리가 차면 버려야 한다.",
      "패브릭 속도와 무관하게 링크 하나가 병목입니다")

for i, y in enumerate(SY):
    d.box(SX, y - SH / 2, SW, SH, PAPER2, RULE, 1.0, 6)
    d.t(SX + SW / 2, y - 4, f"입력 포트 {i+1}", 13, INK, KR, "middle", 600)
    d.t(SX + SW / 2, y + 14, "단위 시간에 1개", 12, SOFT, KR)
    d.line(SX + SW + 2, y, CX, y, MUTED, 1.2)
d.line(CX, SY[0], CX, SY[-1], MUTED, 1.2)
d.path(f"M {CX} {SY[1]} L {QX - 6} {SY[1]}", MUTED, 1.4, m="ar")

d.box(QX, QY, QW, QH, PAPER2, RULE, 1.0, 6)
d.t(QX + 12, QY - 10, "출력 포트 큐", 12, SOFT, KR, "start")
for i in range(5):
    x = QX + 20 + i * SLOT_STRIDE
    y = QY + (QH - SLOT_H) / 2
    if i < 4:
        d.tone(x, y, SLOT_W, SLOT_H, INFO, 5, "14", 1.0)
        d.t(x + SLOT_W / 2, y + 25, f"p{4-i}", 12, INFO, MONO, "middle", 600)
    else:
        d.o.append(f'<rect x="{x}" y="{y}" width="{SLOT_W}" height="{SLOT_H}" rx="5" fill="none" stroke="{RULE}" stroke-width="1" stroke-dasharray="4 3"/>')
        d.t(x + SLOT_W / 2, y + 25, "빈 칸", 12, SOFT, KR)
d.t(QX, QY + QH + 22, "도착은 단위 시간에 3개, 나가는 것은 1개 — 줄이 자랍니다", 12, WARN, KR, "start")

d.path(f"M {QX + QW + 4} {SY[1]} L {SVX - 6} {SY[1]}", ACC, 1.4, m="acc")
d.tone(SVX, SVY, SVW, SVH, ACC, 6, "14", 1.4)
d.t(SVX + SVW / 2, SVY + 24, "출력 링크", 14, ACC, KR, "middle", 600)
d.t(SVX + SVW / 2, SVY + 44, "단위 시간에 1개 · R_line", 12, SOFT, KR)

d.path(f"M {SVX + SVW + 4} {SY[1]} L 876 {SY[1]}", OK, 1.4, m="ok")
d.tone(880, SY[1] - 20, 80, 40, OK, 6, "14", 1.0)
d.t(920, SY[1] + 5, "전송됨", 13, OK, KR)

DX, DY, DW, DH = 660, 152, 200, 40
d.path(f"M {QX + QW - 16} {QY - 2} L {QX + QW - 16} {DY + DH / 2} L {DX - 6} {DY + DH / 2}", BAD, 1.4, m="bad", dash="5 4")
d.tone(DX, DY, DW, DH, BAD, 6, "14", 1.0)
d.t(DX + DW / 2, DY + 25, "메모리가 차면 버림", 13, BAD, KR)
d.t(DX, DY + DH + 22, "꼬리 버리기 · 이미 선 것 빼내기", 12, SOFT, KR, "start")

d.t(24, 428, "패브릭이 회선의 N 배로 빨라도 출력 링크는 단위 시간에 하나만 내보냅니다. 그 하나가 나가는 동안 N 개가 새로 도착할 수 있습니다.", 13, MUTED, KR, "start")
d.t(24, 450, "버리는 대신 차기 전에 미리 버리거나 헤더에 표시하는 것이 AQM 입니다 — RED · PIE · CoDel. 그 표시가 03-05 의 ECN 비트입니다.", 13, MUTED, KR, "start")
d.t(24, 472, "이 줄을 얼마나 길게 둘지가 다음 절의 물음입니다.", 13, SOFT, KR, "start")

d.legend(H - 44, [("병목 — 출력 링크 하나", ACC), ("줄 선 패킷", INFO), ("내보냄", OK), ("버림", BAD)])
d.save("04-02.output-queue.svg")

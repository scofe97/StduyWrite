# 타입 스펙: type-process — 노출 줄 두 개가 분해되어 이름+라벨(시계열 키)·값·시각으로 갈리고 라벨 값 하나만 달라도 시계열이 둘이 되며 시계열마다 점 하나가 현재 블록(메모리 + WAL)에 붙는 세 단계. 같은 두 줄을 단계마다 다시 그려 어느 조각이 시계열을 가르는지를 값으로 보인다.
# 사실 출처: Prometheus 노출 형식 문서의 텍스트 형식 예(http_requests_total{method="post",code="200"} 1027 1395066363000 · …code="400"} 3 1395066363000, prometheus/docs 605cf81 docs/instrumenting/exposition_formats.md L130-L131),
#   데이터 모델 문서(시계열은 이름과 라벨 쌍으로 식별, 라벨 값이 바뀌거나 라벨이 더해지면 새 시계열, 샘플은 float64 값과 밀리초 정밀도 타임스탬프, docs/concepts/data_model.md L26·L42-L43),
#   Prometheus v3.15.0 docs/storage.md L14(샘플은 2시간 블록으로 묶임)·L22-L24(현재 블록은 메모리에 있고 WAL 로 장애에 대비).
#   문서의 예 줄은 열 맞춤용 공백이 있으나 SVG 에서는 한 칸으로 줄였다. 1395066363000 ms 는 2014-03-17T14:26:03Z 이다(계산).
# Layout conventions: 라벨 열 x=24, 내용 열 x=188 폭 788, 행 y=104(노출 줄)·212(머리)·232·292(분해 두 줄)·372(저장 상자, 높이 140, 안쪽 두 줄 y=412·460). 분해 행은 키 칸 폭 412, 값 칸 x=616 폭 160, 시각 칸 x=792 폭 184, 칸 높이 48. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 1000, 576
d = D(W, H, "BYTEBYTEGO · 08-03 §1",
      "라벨 값 하나만 달라도 시계열은 둘이 된다",
      "노출된 두 줄이 이름+라벨·값·시각으로 갈리고 시계열은 이름과 라벨 조합으로 구분됩니다.",
      "예 줄은 Prometheus 노출 형식 문서의 값이고 시각은 밀리초입니다")

LX, CX, CW = 24, 188, 788
NAME = "http_requests_total"
LAB_A, LAB_B = '{method="post",code="200"}', '{method="post",code="400"}'
TS = "1395066363000"

# 1 노출 줄
d.t(LX, 148, "1 노출 줄", 13, INK, KR, "start", 600)
d.box(CX, 104, CW, 76, PAPER2, RULE, 1.0, 6)
d.t(CX + 16, 134, f"{NAME}{LAB_A} 1027 {TS}", 12, INK, MONO, "start")
d.t(CX + 16, 162, f"{NAME}{LAB_B} 3 {TS}", 12, INK, MONO, "start")
d.arrow([(588, 182), (588, 210)], MUTED, "ar", 1.4)

# 2 분해
d.t(LX, 280, "2 분해", 13, INK, KR, "start", 600)
d.t(CX, 224, "시계열 키 = 이름 + 라벨", 13, SOFT, KR, "start")
d.t(616, 224, "값", 13, SOFT, KR, "start")
d.t(792, 224, "시각 (ms)", 13, SOFT, KR, "start")
for y, lab, val in ((236, LAB_A, "1027"), (292, LAB_B, "3")):
    d.tone(CX, y, 412, 48, INFO, 4, "14", 1.0)
    d.t(CX + 12, y + 29, f"{NAME}{lab}", 12, INK, MONO, "start")
    d.tone(616, y, 160, 48, OK, 4, "14", 1.0)
    d.t(696, y + 29, val, 12, INK, MONO, "middle")
    d.tone(792, y, 184, 48, WARN, 4, "14", 1.0)
    d.t(884, y + 29, TS, 12, INK, MONO, "middle")
d.arrow([(588, 344), (588, 368)], MUTED, "ar", 1.4)

# 3 저장
d.t(LX, 448, "3 저장", 13, INK, KR, "start", 600)
d.tone(CX, 372, CW, 140, ACC, 6, "14", 1.4)
d.t(CX + 16, 396, "현재 블록 · 메모리 + WAL · 시계열 2개 · code 라벨 값만 다름", 13, ACC, KR, "start", 600)
for y, lab, val in ((412, LAB_A, "1027"), (460, LAB_B, "3")):
    d.tone(CX + 16, y, 396, 40, INFO, 4, "14", 1.0)
    d.t(CX + 28, y + 25, f"{NAME}{lab}", 12, INK, MONO, "start")
    d.tone(616, y, 112, 40, OK, 4, "14", 1.0)
    d.t(672, y + 25, val, 12, INK, MONO, "middle")
    d.t(744, y + 25, "@", 12, SOFT, MONO, "middle")
    d.tone(760, y, 200, 40, WARN, 4, "14", 1.0)
    d.t(860, y + 25, TS, 12, INK, MONO, "middle")

d.legend(H - 44, [("시계열 키", INFO), ("값", OK), ("시각", WARN), ("이 절의 초점", ACC)])
d.save("08-03.series-process.svg")

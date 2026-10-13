# 타입 스펙: type-process — 레인 셋(할당 용량 · 하루 업로드 · 업로드 QPS)이 값 셋씩으로 환산되고 칸마다 실제 값이 바뀐다. focal 은 피크 QPS.
# 사실 출처: 추출본 v2.txt 4394~4401행(가입 5,000 만·DAU 1,000 만·무료 10 GB·하루 2 건·평균 500 KB·QPS ~240·피크 ×2 = 480).
#   계산: 50,000,000 × 10 GB = 500,000,000 GB = 500 PB · 10,000,000 × 2 = 20,000,000 건 × 500 KB = 10,000,000,000 KB = 10 TB · 20,000,000 ÷ 86,400 = 231.5 ≈ 231, 추출본은 240 으로 올림 · 240 × 2 = 480.
# Layout conventions: 라벨 열 폭 128, 노드 폭 176·높이 64, 칸 stride 224, 레인 stride 96, 연산 칩은 칸 사이 중앙. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, MUTED, INK, SOFT, KR, MONO

W, H = 880, 440
d = D(W, H, "SYSTEM DESIGN INTERVIEW · 15-01 §1",
      "하루 신규 데이터는 10 TB, 업로드 피크는 초당 480 건",
      "가입 5,000 만 명과 DAU 1,000 만 명, 하루 2 건, 평균 500 KB 라는 설계 가정에서 세 값이 나온다.",
      "할당 500 PB 는 쓰는 양이 아니라 약속한 양")

NX = (168, 392, 616)
NW, NH = 176, 64
ROWS = (
    (116, "할당 용량", (("5,000 만 명", "가입 사용자"), ("10 GB", "사용자당 무료"), ("500 PB", "할당 총량")), ("×", "="), INFO),
    (212, "하루 업로드", (("2,000 만 건", "1,000 만 × 2"), ("500 KB", "평균 크기"), ("10 TB", "하루 신규 데이터")), ("×", "="), INFO),
    (308, "업로드 QPS", (("2,000 만 건", "하루"), ("86,400 초", "24 × 3,600"), ("231 → 240", "피크 × 2 = 480")), ("÷", "="), ACC),
)

for y, lab, nodes, ops, c in ROWS:
    d.t(24, y + 38, lab, 14, SOFT, KR, "start", 600)
    for i, (v, sub) in enumerate(nodes):
        last = i == 2
        col = c if last else INFO
        d.tone(NX[i], y, NW, NH, col, 6, "12", 1.4 if (last and c == ACC) else 1.0)
        d.t(NX[i] + NW // 2, y + 30, v, 16, INK, MONO, "middle", 600)
        d.t(NX[i] + NW // 2, y + 52, sub, 13, MUTED, KR)
    for i, op in enumerate(ops):
        d.chip(NX[i] + NW + 24, y + 32, op, MUTED, 13)

d.legend(H - 56, [("계산 값", INFO), ("가장 중심인 값", ACC)])
d.save("15-01.estimate-calc.svg")

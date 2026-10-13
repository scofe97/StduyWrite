# 타입 스펙: type-process — 주체 없는 단계 지도(Stage framework with semantic slots). §2 공식이 전제하는 주체 레인은 두지 않고 한 줄 다섯 칸으로 줄였다.
# 사실 출처: 추출본 v2.txt 548~653행(2 의 거듭제곱 · 지연 시간 · 가용성 · 예제 · 팁), PDF 34~38쪽 표 2-1·2-2·2-3,
#   Jeff Dean 슬라이드 PDF(research.google.com/people/jeff/stanford-295-talk.pdf, 2007 년 봄 CS295 강의) 지연 시간 표,
#   예제 계산은 본문 §4 의 식(150 M × 2 ÷ 86,400 ≈ 3,472, 30 TB × 365 × 5 = 54,750 TB).
# Layout conventions: 칸 폭 160·높이 232, stride 184(간격 24), x0=32, y=120. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, MUTED, INK, PAPER, PAPER2, RULE, SOFT, INFO, KR, MONO

W, H = 960, 480
d = D(W, H, "SYSTEM DESIGN INTERVIEW · 02-01",
      "기준 값 셋에서 예제 한 개로, 마지막은 습관이다",
      "2 의 거듭제곱 단위, 지연 시간 표, 가용성 9 의 개수가 기준 값이고, 이 값으로 QPS 와 저장 용량을 어림하며, 반올림·가정·단위 습관으로 마무리한다.",
      "다섯 절의 지도")

CW, CH, STRIDE, X0, Y0 = 160, 232, 184, 32, 120


def cell(i, tag, title, lines, foot, c, focal=False):
    x = X0 + i * STRIDE
    d.tone(x, Y0, CW, CH, c, 6, "12", 1.4 if focal else 1.2)
    d.t(x + 14, Y0 + 28, tag, 11, c, MONO, "start", 600)
    d.t(x + CW / 2, Y0 + 64, title, 15, INK, KR, "middle", 600)
    d.line(x + 16, Y0 + 84, x + CW - 16, Y0 + 84, RULE, 0.8)
    for k, ln in enumerate(lines):
        fam = KR if any("가" <= ch <= "힣" for ch in ln) else MONO
        d.t(x + CW / 2, Y0 + 116 + k * 28, ln, 13, INK, fam)
    if foot:
        d.t(x + CW / 2, Y0 + CH - 20, foot, 13, MUTED, KR)


cell(0, "§1", "단위", ["2^10 ≈ 10^3", "2^30 ≈ 10^9", "2^50 ≈ 10^15"], "1,024 의 거듭제곱", INFO)
cell(1, "§2", "지연 시간", ["L1 캐시 0.5 ns", "메모리 100 ns", "디스크 탐색 10 ms"], "2007 년 기준 값", INFO)
cell(2, "§3", "가용성", ["99.9% · 8.77 시간", "99.99% · 52.60 분", "99.999% · 5.26 분"], "1 년 허용 중단", INFO)
cell(3, "§4", "QPS · 저장", ["150 M DAU", "≈ 3,500 QPS", "≈ 7,000 피크", "≈ 55 PB"], None, ACC, True)
cell(4, "§5", "습관", ["100,000 ÷ 10", "가정 적기", "30 TB ≠ 30 MB"], "반올림 · 가정 · 단위", OK)

for i in range(4):
    x = X0 + i * STRIDE + CW
    d.arrow([(x + 2, Y0 + CH // 2), (x + 20, Y0 + CH // 2)], MUTED, "ar", 1.5)

d.legend(H - 56, [("기준 값", INFO), ("계산 예제", ACC), ("습관", OK)])
d.save("02-01.chapter-overview.svg")

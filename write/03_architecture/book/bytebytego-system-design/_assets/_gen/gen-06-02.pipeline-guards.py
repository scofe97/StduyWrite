# 타입 스펙: type-process — 변경 하나가 병합부터 운영 전체까지 거치는 단계 다섯 칸. 칸마다 안전장치의 실제 값이 같은 자리에 반복되고 화살표는 진행 순서를, 점선은 03·04 단계로의 되돌림을 나른다(Stage framework with semantic slots).
# 사실 출처: AWS Builders' Library "Automating safe, hands-off deployments"(builder.aws.com/content/3ErTKQOTKc5NIw031UePBPxTQ6I)
#   · 코드 리뷰는 사람이 거치는 마지막 검토, gamma 원박스 30분 또는 1시간, 운영 원박스는 요청 최대 10%, 원박스 뒤 최소 1시간,
#     첫 리전 웨이브 뒤 최소 12시간, 이후 웨이브 뒤 2~4시간, 롤링은 한 번에 최대 33% 교체·용량 66% 이상, 알람이 울리면 이전 패키지로 자동 롤백, 전 리전 도달 약 4~5 영업일.
# Layout conventions: 카드 폭 176·높이 212, 가로 stride 192(x=24+192k), 카드 y=112, 화살표는 카드 중앙 y=218, 되돌림 화살표는 카드 아래 32px·48px. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 992, 468
d = D(W, H, "BYTEBYTEGO · 06-02 §2",
      "병합에서 운영 전체까지 사람 손 없이 가는 길",
      "단계마다 노출 폭과 기다리는 시간이 정해져 있고 알람이 울리면 이전 패키지로 돌아갑니다",
      "아마존 서비스 팀 파이프라인의 전형적인 값입니다")

CW, CH, STRIDE, X0, Y0 = 176, 212, 192, 24, 112
cards = [
    ("01", "코드 리뷰", "팀원 승인 필수", "병합하면 시작", "사람의 마지막 검토", INFO),
    ("02", "사전 운영", "alpha · beta · gamma", "원박스 30분 또는 1시간", "운영과 같은 설정", INFO),
    ("03", "운영 원박스", "요청 ≤10%", "대기 ≥1시간", "원박스 전용 알람", INFO),
    ("04", "롤링 웨이브", "교체 ≤33%", "용량 ≥66%", "첫 웨이브 뒤 ≥12시간", INFO),
    ("05", "알람 · 롤백", "집계 알람 하나", "전 리전 4~5 영업일", "지켜보는 사람 없음", ACC),
]
for k, (tag, title, v1, v2, sub, c) in enumerate(cards):
    x = X0 + k * STRIDE
    cx = x + CW / 2
    if c == ACC:
        d.tone(x, Y0, CW, CH, ACC, 6, "14", 1.4)
    else:
        d.box(x, Y0, CW, CH, PAPER2, RULE, 0.9, 6)
    d.t(x + 12, Y0 + 24, tag, 12, SOFT, MONO, "start")
    d.t(cx, Y0 + 52, title, 13, c if c == ACC else INK, KR, "middle", 600)
    d.line(x + 12, Y0 + 68, x + CW - 12, Y0 + 68, RULE, 0.6)
    d.t(cx, Y0 + 104, v1, 12, c, KR if any("가" <= ch <= "힣" for ch in v1) else MONO, "middle", 600)
    d.t(cx, Y0 + 132, v2, 12, INK, KR, "middle")
    d.t(cx, Y0 + 176, sub, 12, MUTED, KR, "middle")
    if k < len(cards) - 1:
        d.arrow([(x + CW + 2, Y0 + CH / 2), (x + STRIDE - 4, Y0 + CH / 2)], MUTED, "ar", 1.4)

# 되돌림: 05 알람 칸 아래에서 04 롤링 칸 아래로 점선
x5 = X0 + 4 * STRIDE + CW / 2
x4 = X0 + 3 * STRIDE + CW / 2
yb = Y0 + CH
x3 = X0 + 2 * STRIDE + CW / 2
d.arrow([(x5, yb + 2), (x5, yb + 32), (x4, yb + 32), (x4, yb + 4)], BAD, "bad", 1.5, "5 4")
d.arrow([(x5, yb + 32), (x5, yb + 48), (x3, yb + 48), (x3, yb + 4)], BAD, "bad", 1.5, "5 4")
d.t((x3 + x5) / 2, yb + 76, "이전 패키지로", 12, BAD, KR, "middle")

d.legend(H - 44, [("자동 롤백 초점", ACC), ("단계별 안전 값", INFO), ("되돌림", BAD)])
d.save("06-02.pipeline-guards.svg")

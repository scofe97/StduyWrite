# 타입 스펙: type-process — 편 전체 지도. 절 번호·이름·실제 값이 칸마다 같은 자리에 반복되고 화살표는 읽는 순서를 나른다(semantic-patterns 의 Stage framework with semantic slots, 주체 없는 단계 지도라서 selection 표의 알려진 공백 대체).
# 사실 출처: AWS CodeDeploy 사용자 가이드 "Deployment configurations on an AWS Lambda compute platform"(LambdaCanary10Percent5Minutes 는 처음 10%, 5분 뒤 나머지 90%)
#   · AWS Builders' Library "Automating safe, hands-off deployments"(원박스는 요청 최대 10%, 롤링은 한 번에 최대 33% 교체·용량 66% 이상)
#   · 추출본 v1.txt 1265~1318행(대시보드 전부 0 · 50명 · 10시간) · 1729~1741행(vmstat · iostat · netstat · lsof · pidstat).
# Layout conventions: 카드 폭 204·높이 212, 가로 stride 224(x=40+224k), 카드 y=112, 화살표는 카드 중앙 y=218. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 960, 392
d = D(W, H, "BYTEBYTEGO · 06-02",
      "새 버전을 내보내고 장애에서 되돌아오는 네 장치",
      "배포 전략, 자동 파이프라인, 장애 대응 순서, 진단 도구가 값 하나씩을 들고 이어집니다.",
      "네 절이 값 하나씩을 들고 이어집니다")

CW, CH, STRIDE, X0, Y0 = 204, 212, 224, 40, 112
cards = [
    ("§1", "배포 전략", "카나리 10% → 100%", "블루그린 0% → 100%", "새 버전을 조금씩 노출", ACC),
    ("§2", "자동 파이프라인", "원박스 ≤10%", "롤링 ≤33% 교체", "지켜보지 않는 배포", INFO),
    ("§3", "장애 대응", "지표 전부 0", "50명 · 10시간", "역할 분담 뒤 사후 검토", INFO),
    ("§4", "진단 도구", "CPU · 메모리 · IO", "네트워크 · 열린 파일", "자원마다 다른 창", INFO),
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
    d.t(cx, Y0 + 104, v1, 12, c, KR, "middle", 600)
    d.t(cx, Y0 + 132, v2, 12, INK, KR, "middle")
    d.t(cx, Y0 + 176, sub, 12, MUTED, KR, "middle")
    if k < len(cards) - 1:
        d.arrow([(x + CW + 2, Y0 + CH / 2), (x + STRIDE - 4, Y0 + CH / 2)], MUTED, "ar", 1.4)

d.legend(H - 44, [("이 편의 초점", ACC), ("절별 대표 값", INFO)])
d.save("06-02.chapter-overview.svg")

# 타입 스펙: type-process — 편 전체 지도. 절 번호·이름·실제 값이 칸마다 같은 자리에 반복되고 화살표는 읽는 순서를 나른다(semantic-patterns 의 Stage framework with semantic slots, 주체 없는 단계 지도라서 selection 표의 알려진 공백 대체).
# 사실 출처: pthreads(7)·clone(2)(CLONE_VM) https://man7.org/linux/man-pages/man7/pthreads.7.html
#   · Firecracker NSDI'20 논문 §2.1·§4(커널 공유·slot=microVM, Listing 1 의 0→1) https://www.usenix.org/system/files/nsdi20-paper-agache.pdf
#   · NIST SP 800-145 (IaaS·PaaS·SaaS 정의) · AWS Lambda 보안 개요 백서(공동 책임 모델)
#   · 값은 본문과 같은 계산: 커널 수 1+2=3 · 같은 커널 앱 쌍 C(3,2)=3 대 VM 안 쌍 1 · 5개 층 중 내가 맡는 층 4/1/0 · 바뀐 이름 13(본문 §5 목록).
# Layout conventions: 카드 폭 164·높이 212, 가로 stride 180(x=24+180k), 카드 y=112, 화살표는 카드 중앙 y=218. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 960, 392
d = D(W, H, "BYTEBYTEGO · 06-01",
      "운영 책임과 격리 층을 갈라 보는 다섯 절",
      "스레드의 공유부터 서버리스 호출 경로와 세 클라우드의 서비스 대응까지 값 하나씩을 들고 이어집니다.",
      "절마다 세어 볼 수 있는 값이 하나씩 있습니다")

CW, CH, STRIDE, X0, Y0 = 164, 212, 180, 24, 112
cards = [
    ("§1", "프로세스와 스레드", "스택만 따로", "힙 · fd 는 공유", "CLONE_VM = 메모리 공유", INFO),
    ("§2", "VM 과 컨테이너", "커널 3 ↔ 1", "앱 쌍 1 ↔ 3", "같은 커널을 쓰는 쌍", INFO),
    ("§3", "서비스 모델", "내 층 4 → 1 → 0", "서버리스 1 + 조건부", "다섯 층 중", ACC),
    ("§4", "Lambda 호출", "슬롯 1 = VM 1", "반환 0 → 1", "같은 슬롯 재사용", INFO),
    ("§5", "빅데이터 대응표", "5단계 × 3사", "바뀐 이름 13", "단계로 대응", INFO),
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
d.save("06-01.chapter-overview.svg")

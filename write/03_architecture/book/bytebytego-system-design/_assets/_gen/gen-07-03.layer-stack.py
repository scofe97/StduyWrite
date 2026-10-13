# 타입 스펙: type-layers — 사용자 요청이 내려가는 다섯 층에 층마다 붙는 대책을 둔다. 층 순서는 요청이 지나는 순서이고 초점은 재고를 두는 저장소 층이다.
# 사실 출처: 추출본 v1.txt 3816~3850행(디자인 원칙 여섯)과 PDF 156쪽 그림의 대책 상자 여섯(제품·프런트엔드·처리율 제한·과판매 방지·데이터 저장·백엔드 서비스).
# Layout conventions: 층 5개·높이 72·간격 8(stride 80), 폭 860(x=104), 왼쪽 여백에 방향 표지. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, BAD, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 1000, 576
d = D(W, H, "BYTEBYTEGO · 07-03 §5~7",
      "요청이 내려가는 다섯 층마다 몰림을 줄이는 대책이 붙는다",
      "화면에서 저장소까지 층마다 붙는 대책이며 재고는 맨 아래 캐시에서 차감합니다.",
      "층 구성은 플래시 세일 설계를 따랐습니다")

layers = [
    ("L1", "화면", "브라우저", "요소 줄이기 · JS 로딩 줄이기 · reCAPTCHA", ""),
    ("L2", "엣지", "방화벽 · CDN", "정적 콘텐츠는 CDN 에서", ""),
    ("L3", "진입", "NGINX · 위험 통제", "DDoS 방어 · 의심 IP 차단 · IP 당 요청 제한", ""),
    ("L4", "서비스", "전용 인스턴스", "큐로 비동기 처리 · RPC 와 의존 줄이기", "단일 장애점 없음"),
    ("L5", "저장소", "전용 캐시 · DB", "재고는 캐시에서 차감 · DB 는 따로 일괄 갱신", "주문 때 잠금 · 결제 뒤 차감"),
]
X, Y0, LW, LH, ST = 104, 104, 860, 72, 80
fam = lambda s: KR if any("가" <= ch <= "힣" for ch in s) else MONO
for k, (tag, name, comp, a, b) in enumerate(layers):
    y = Y0 + k * ST
    focal = (k == len(layers) - 1)
    if focal:
        d.tone(X, y, LW, LH, ACC, 6, "14", 1.4)
    else:
        d.box(X, y, LW, LH, PAPER2, RULE, 0.9, 6)
    d.t(X + 16, y + 28, tag, 11, SOFT, MONO, "start")
    d.t(X + 56, y + 32, name, 16, ACC if focal else INK, KR, "start", 600)
    d.t(X + 56, y + 56, comp, 13, MUTED, fam(comp), "start")
    d.t(X + 244, y + (32 if b else 44), a, 13, INK, fam(a), "start")
    if b:
        d.t(X + 244, y + 56, b, 13, ACC if focal else MUTED, fam(b), "start", 600 if focal else 400)

# 왼쪽 여백의 방향 표지: 요청이 위에서 아래로 내려간다.
d.arrow([(56, Y0 + 12), (56, Y0 + 5 * ST - 24)], MUTED, "ar", 1.4)
d.t(56, Y0 + 5 * ST - 4, "요청", 13, MUTED, KR, "middle")

d.legend(H - 56, [("층 대책", INK), ("이 절의 초점", ACC)])
d.save("07-03.layer-stack.svg")

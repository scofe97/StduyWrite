# a0-03 전체 인과 지도 — 비밀 금지 제약에서 시작해 Istio 부트스트랩과 요청 인가까지 이어지는 사슬.
# 값 근거(본문 a0-03):
#   - §2·§3: SPIFFE 네 규격과 SPIFFE ID (spiffe://trust-domain/path).
#   - §4: 비밀 금지 제약 -> Workload Endpoint(증명·CSR) -> Workload API(서명·발급).
#   - §5: Istio 부품 배치(파일럿 에이전트·Istio CA·Envoy)와 X.509 SVID(auto mTLS).
#   - §6: 부트스트랩 다섯 걸음(SA 토큰 -> SPIFFE ID·CSR -> CA TokenReview 검증 -> SDS -> Envoy).
#   - §7: 요청 신원(jwt_authn·PeerAuthentication -> filter metadata -> 인가 필터 4단계).
#   - §1: 사슬 밖 경계(PKI·TLS 위임).
# 타입 스펙: type-architecture — 세 구역(규격·제약 → Istio 구현·부트스트랩 → 요청 신원 소비)을
#           좌에서 우로 잇는 인과 사슬. 모든 화살표는 직교 경로이며 4의 배수 좌표를 사용한다.
import sys; sys.path.insert(0, ".")
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, INFO, KR, MONO

W, H = 984, 696


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


d = D(W, H, "ISTIO IN ACTION · A0-03 OVERVIEW",
      "비밀 금지 제약에서 요청 인가까지의 인과 사슬",
      "a0-03 전체 인과 지도. 왼쪽은 비밀 금지 제약에서 Workload Endpoint 와 Workload API, SPIFFE ID 가 나오는 규격 구조다. "
      "가운데는 Istio 가 부품 셋을 배치하고 X.509 SVID 로 auto mTLS 를 세우며 토큰으로 인증서를 부트스트랩하는 과정이다. "
      "오른쪽은 요청마다 두 인증 필터가 filter metadata 를 채우고 인가 필터가 네 단계로 판정하는 흐름이다.",
      lead="화살표 위 글자는 관계, 칩은 해당 절 번호, 왼쪽에서 오른쪽으로 읽습니다.")


def node(x, y, w, h, title, sub, c, sec, focal=False, sub2=None):
    d.tone(x, y, w, h, c, 6, "1e" if focal else "14", 1.4 if focal else 1.2)
    d.chip(x + 28, y + 16, sec, c, 11)
    d.t(x + w / 2 + 12, y + 24, title, 14, c, kr(title), "middle", 600)
    d.t(x + w / 2, y + 50, sub, 13, MUTED, kr(sub), "middle")
    if sub2:
        d.t(x + w / 2, y + 68, sub2, 13, MUTED, kr(sub2), "middle")


def lab(x, y, txt, c=MUTED):
    lw = sum(13 if "가" <= ch <= "힣" else 8 for ch in txt) + 16
    d.o.append(f'<rect x="{x - lw / 2}" y="{y - 14}" width="{lw}" height="20" rx="3" fill="{PAPER}"/>')
    d.t(x, y, txt, 13, c, kr(txt), "middle", 600)


# 구역 헤더
headers = [
    (24, 296, "1. SPIFFE 규격 · 제약", INFO),
    (364, 640, "2. Istio 구현 · 부트스트랩", OK),
    (708, 960, "3. 요청 신원 소비", INFO),
]
for x1, x2, cap, col in headers:
    d.t(x1, 114, cap, 13, col, KR, "start", 600)
    d.line(x1, 122, x2, 122, RULE, 0.8)

# 1. 규격·제약 (§2·§3·§4)
node(24, 144, 272, 72, "비밀 금지 제약", "신원 비밀 직접 소유 불가", ACC, "§4", focal=True)
node(24, 268, 272, 72, "Workload Endpoint", "곁에서 증명 · CSR 생성", INFO, "§4")
node(24, 392, 272, 72, "Workload API", "CA 키로 CSR 서명 · 발급", INFO, "§2·§4")
node(24, 516, 272, 72, "SPIFFE ID", "spiffe://trust-domain/path", INFO, "§3")

d.arrow([(160, 216), (160, 266)], ACC, "acc", 1.5)
d.t(172, 246, "인증 공백", 13, ACC, KR, "start", 600)
d.arrow([(160, 340), (160, 390)], INFO, "info", 1.4)
d.t(172, 370, "CSR 제출", 13, MUTED, KR, "start", 600)

# 2. Istio 구현·부트스트랩 (§5·§6)
node(364, 144, 276, 72, "Istio 부품 배치", "에이전트 · Istio CA · Envoy", OK, "§5")
node(364, 268, 276, 72, "SVID (X.509) 선택", "SAN URI + 공개 키 → auto mTLS", OK, "§5")

# §6 부트스트랩 묶음 박스
BX, BY, BW, BH = 364, 392, 276, 196
d.tone(BX, BY, BW, BH, OK, 6, "14", 1.2)
d.chip(BX + 28, BY + 16, "§6", OK, 11)
d.t(BX + BW / 2 + 12, BY + 24, "부트스트랩 다섯 걸음", 14, OK, KR, "middle", 600)
boot_rows = [
    "SA 토큰 → SPIFFE ID · CSR",
    "CA 가 TokenReview 검증 · 서명",
    "SDS 로 Envoy 에 인증서 전달",
]
for i, row in enumerate(boot_rows):
    ry = BY + 48 + i * 46
    d.box(BX + 16, ry, BW - 32, 36, PAPER2, RULE, 0.9, 4)
    d.t(BX + BW / 2, ry + 23, row, 13, INK, kr(row), "middle")

d.arrow([(502, 216), (502, 266)], OK, "ok", 1.4)
d.t(514, 246, "X.509 채택", 13, OK, KR, "start", 600)
d.arrow([(502, 340), (502, 390)], OK, "ok", 1.4)
d.t(514, 370, "발급 실행", 13, OK, KR, "start", 600)

# 구역 1 -> 구역 2 직교 화살표
d.arrow([(296, 304), (332, 304), (332, 180), (362, 180)], INFO, "info", 1.4)
lab(332, 244, "부품 대응", INFO)
d.arrow([(296, 428), (362, 428)], INFO, "info", 1.4)
lab(330, 412, "서명", MUTED)
d.arrow([(296, 552), (362, 552)], INFO, "info", 1.4)
lab(330, 536, "SAN URI", MUTED)

# 3. 요청 신원 소비 (§7)
node(708, 144, 252, 84, "인증 필터 둘", "jwt_authn", INFO, "§7", sub2="PeerAuthentication")
node(708, 288, 252, 112, "filter metadata", "Principal · Namespace", INFO, "§7", sub2="Request principal · Claims")
node(708, 460, 252, 128, "인가 필터 순서", "1. 커스텀 → 2. 거부", OK, "§7", sub2="3. 허용 → 4. catch-all")

d.arrow([(834, 228), (834, 286)], INFO, "info", 1.4)
d.t(846, 262, "추출 · 저장", 13, MUTED, KR, "start", 600)
d.arrow([(834, 400), (834, 458)], OK, "ok", 1.4)
d.t(846, 434, "읽어 판정", 13, OK, KR, "start", 600)

# 구역 2 -> 구역 3 직교 화살표
d.arrow([(640, 492), (674, 492), (674, 186), (706, 186)], OK, "ok", 1.5)
lab(674, 252, "mTLS 신원", OK)

d.t(24, 622, "§1 은 이 사슬 밖에서 PKI·TLS 를 넘기고 워크로드 신원이 필요한 경계를 긋는다", 13, SOFT, KR, "start")
d.legend(644, [("핵심 제약", ACC), ("규격 · 요청 단계", INFO), ("Istio 구현 · 인가", OK)])
d.save("a0-03.appendix-overview.svg")
print("ok a0-03 overview")

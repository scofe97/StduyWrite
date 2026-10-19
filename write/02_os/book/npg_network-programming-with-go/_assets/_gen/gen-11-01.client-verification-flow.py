# 타입 스펙: type-flowchart
# 사실 출처: NPG Ch.11 Listing 11-2, crypto/x509, crypto/tls
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 960, 480
d = D(W, H, "FLOWCHART · CLIENT CERTIFICATE VERIFICATION",
      "클라이언트의 서버 인증서 검증 흐름과 InsecureSkipVerify 우회",
      "Go 검증기가 서버 인증서를 확인하는 두 단계(호스트명 SAN 일치, CA 서명 사슬)와 InsecureSkipVerify 우회 경로입니다.",
      lead="기본 클라이언트는 엄격히 검증하며, InsecureSkipVerify 는 중간자 공격을 부릅니다.")

def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO

# 1. 진입 노드
d.tone(40, 200, 160, 80, INFO, 6, "16", 1.1)
d.t(120, 232, "서버 인증서 수신", 13, INFO, KR, "middle", 600)
d.t(120, 255, "핸드셰이크 전달값", 11, MUTED, KR, "middle")

# 화살표 1 -> 2
d.arrow([(200, 240), (256, 240)], c=MUTED, m="ar")

# 2. 결정 노드 1: SAN 호스트명 검사 (Go 검증기는 사슬보다 호스트명을 먼저 본다)
d.tone(260, 200, 190, 80, INFO, 6, "16", 1.1)
d.t(355, 230, "호스트명(SAN) 검사", 13, INK, KR, "middle", 600)
d.t(355, 253, "접속 주소와 SAN 비교", 11, MUTED, KR, "middle")

# 실패 1: HostnameError (아래로)
d.arrow([(355, 280), (355, 336)], c=BAD, m="bad")
d.t(365, 308, "불일치 (호스트명 다름)",  11, BAD, KR, "start")

d.tone(250, 340, 210, 64, BAD, 6, "16", 1.1)
d.t(355, 366, "HostnameError", 11, BAD, MONO, "middle", 600)
d.t(355, 388, "사칭 또는 잘못된 주소 거부",  11, MUTED, KR, "middle")

# 화살표 2 -> 3 (통과)
d.arrow([(450, 240), (506, 240)], c=OK, m="ok")
d.t(478, 230, "일치",  11, OK, KR, "middle")

# 3. 결정 노드 2: CA 서명 사슬 검사
d.tone(510, 200, 190, 80, INFO, 6, "16", 1.1)
d.t(605, 230, "신뢰 CA 서명 검사", 13, INK, KR, "middle", 600)
d.t(605, 253, "RootCAs 또는 OS 루트 대조", 11, MUTED, KR, "middle")

# 실패 2: UnknownAuthorityError (아래로)
d.arrow([(605, 280), (605, 336)], c=BAD, m="bad")
d.t(615, 308, "서명자를 모름",  11, BAD, KR, "start")

d.tone(500, 340, 210, 64, BAD, 6, "16", 1.1)
d.t(605, 366, "UnknownAuthorityError", 11, BAD, MONO, "middle", 600)
d.t(605, 388, "자체 서명 등 신뢰 불가 거부",  11, MUTED, KR, "middle")

# 화살표 3 -> 4 (통과)
d.arrow([(700, 240), (756, 240)], c=OK, m="ok")
d.t(728, 230, "서명 확인",  11, OK, KR, "middle")

# 4. 성공 노드
d.tone(760, 200, 160, 80, OK, 6, "18", 1.2)
d.t(840, 232, "검증 통과 및 수립", 13, OK, KR, "middle", 600)
d.t(840, 255, "안전한 TLS 세션 시작", 11, INK, KR, "middle")

# 우회 바이패스 경로: InsecureSkipVerify: true
# 칩 폭은 dd.chip 공식(35자 × 11 + 14 = 399)이라 좌우 끝이 280·680 이다
d.path("M 120 200 L 120 105 L 279 105", c=WARN, dash="4 4")
d.chip(480, 105, "InsecureSkipVerify: true (검증 전체 생략)", WARN, 11)
d.arrow([(681, 105), (840, 105), (840, 194)], c=WARN, m="warn", dash="4 4")
d.t(480, 134, "중간자 공격(MITM)을 막지 못함 · 시험 전용",  11, BAD, KR, "middle")

d.legend(430, [("정상 검증 단계", INFO), ("검증 성공", OK), ("검증 실패 거부", BAD), ("위험 우회 설정", WARN)])

svg_path = pathlib.Path(__file__).resolve().parent.parent / "11-01.client-verification-flow.svg"
d.save(str(svg_path))
print("ok 11-01 client-verification-flow")

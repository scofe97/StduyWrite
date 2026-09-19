# 타입 스펙: type-flowchart — 세 절의 읽는 순서를 동일한 간격으로 배치한다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, INK, INFO, PAPER2, RULE, KR, MONO
W, H = 880, 468
d = D(W, H, "PACKET ANALYSIS WITH WIRESHARK · 04-02",
      "열쇠와 실패 — 분석의 세 단계",
      "TLS 버전과 키 교환을 확인하고 복호화 재료를 구분한 뒤, 실패한 연결은 마지막 메시지와 Alert 방향으로 좁힌다. ServerHello 이전에도 협상이 실패할 수 있으며 인증서 신뢰는 별도로 점검한다.",
      "버전·키 교환 → 복호화 재료 → 실패 단계·방향을 확인합니다")
CW, CH, GAP, Y0 = 256, 136, 32, 156
cards = [
    ("§1", "버전·키 교환", "TLS 1.2: suite의 키 교환", "TLS 1.3: 별도 협상", False),
    ("§2", "복호화 재료", "RSA 개인키: 조건 확인", "세션 비밀값: 양쪽 종단", True),
    ("§3", "실패 단계·방향", "마지막 메시지 · Alert 송신자", "협상 조건 · 인증서 신뢰", False),
]
for i, (num, title, sub, hint, focal) in enumerate(cards):
    x = 24 + i * (CW + GAP)
    col = ACC if focal else INK
    d.box(x, Y0, CW, CH, PAPER2, ACC if focal else RULE, 1.4 if focal else 1, 8)
    d.t(x + CW / 2, Y0 + 28, num, 13, MUTED, MONO)
    d.t(x + CW / 2, Y0 + 56, title, 16, col, KR, "middle", 600)
    d.t(x + CW / 2, Y0 + 88, sub, 13, MUTED, KR)
    d.t(x + CW / 2, Y0 + 112, hint, 13, MUTED, KR)
    if i < len(cards) - 1:
        d.arrow([(x + CW + 4, Y0 + CH / 2), (x + CW + GAP - 4, Y0 + CH / 2)], MUTED, "ar", 1.4)
d.t(24, 344, "ServerHello 이전 실패도 분석 대상", 14, INFO, KR, "start", 600)
d.t(24, 372, "인증서 신뢰: cipher suite와 별도의 점검 축", 13, MUTED, KR, "start")
d.legend(H - 48, [("복호화 재료 구분", ACC), ("실패 위치 확인", INFO)])
d.save("04-02.chapter-overview.svg")

# 07-01 §6 — 원서가 인용한 키 롤오버 권고와 그 출처 문서의 표, 그리고 개정판의 권고를 나란히 놓는다.
# 근거: NIST SP 800-81-2 체크리스트 30(KSK 1~2년, ZSK 1~3개월), 같은 문서 Table 9-1(RSA ZSK 1024bit 1-3 months,
#       ECDSA P-256/P-384 ZSK 12-24 months), SP 800-81r3 "recommended maximum lifetime of 1-3 years", RRSIG "short (e.g., 5-7 days)".
# 타입 스펙: type-dp-security-matrix — 출처(행) × 키 종류(열)에서 같은 칸의 값이 문서마다 달라지는 것이 논지다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 880, 446
d = D(W, H, "LEARNING COREDNS · 07-01 §6",
      "롤오버 주기 권고는 두 번 바뀌었다",
      "원서가 옮긴 ZSK 1~3개월은 SP 800-81-2 표에서 RSA 1024비트 줄의 값이다. 원서 예제의 ECDSA 는 같은 표에서 ZSK 도 12~24개월이다. "
      "그 문서는 2026년 SP 800-81r3 로 대체돼 키 구분 없이 1~3년, 대신 RRSIG 유효 기간을 짧게 두라고 한다.",
      "주황 칸이 원서 예제의 알고리즘에 맞는 값입니다")

COLS = [(20, 260, "출처"), (290, 170, "KSK"), (470, 170, "ZSK"), (650, 210, "강조점")]
rows = [
    (("원서 인용", "SP 800-81-2 체크리스트 30"), ("1~2년", ""), ("1~3개월", ""), ("키 수명", "")),
    (("SP 800-81-2 표 9-1", "ECDSA P-256 · P-384 줄"), ("12~24개월", ""), ("12~24개월", "RSA 1024 줄은 1~3개월"), ("알고리즘별 수명", "")),
    (("SP 800-81r3", "2026-03-19 이전 판을 대체"), ("1~3년", "구분 없음"), ("1~3년", "구분 없음"), ("RRSIG 유효 기간", "5~7일처럼 짧게")),
]
FOCAL = (1, 2)

for x, w, head in COLS:
    d.t(x + 10, 118, head, 12, SOFT, KR, "start", 600)

for i, cells in enumerate(rows):
    y = 132 + i * 80
    for k, (a, b) in enumerate(cells):
        x, w, _ = COLS[k]
        foc = (i, k) == FOCAL
        if foc:
            d.tone(x, y, w, 66, ACC, 6, "12", 1.4)
        else:
            d.box(x, y, w, 66, PAPER2, RULE, 1.0, 6)
        if b:
            d.t(x + 12, y + 27, a, 14 if k else 13, ACC if foc else INK, KR, "start", 600)
            d.t(x + 12, y + 49, b, 12, MUTED, KR, "start")
        else:
            d.t(x + 12, y + 38, a, 14, ACC if foc else INK, KR, "start", 600)

d.t(20, 386, "원서 예제의 ZSK 는 ECDSAP256SHA256 · 인용된 문서 기준으로도 1~3개월 대상이 아니다", 13, MUTED, KR, "start")

d.legend(400, [("원서 예제 알고리즘에 맞는 값", ACC)])
d.save("07-01.rollover-guidance.svg")

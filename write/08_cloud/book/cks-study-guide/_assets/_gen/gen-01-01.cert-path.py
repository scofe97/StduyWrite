# 01-01 §1 — CNCF 쿠버네티스 자격증 경로에서 CKS 만 CKA 합격을 선행 조건으로 요구한다.
# 본문 근거: 이 노트 §1 「자격증 경로에서 CKS 의 자리」.
# 공식 근거: Linux Foundation CKS 페이지 Prerequisites ("CKS candidates must have taken and passed the CKA exam prior to attempting the CKS exam.") 및
#            KCNA·KCSA·CKAD·CKA 페이지 ("There are no prerequisites for this exam.").
# 타입 스펙: type-dependency — 좌→우 의존 그래프로 선행 조건(CKA → CKS) 방향만 화살표로 잇는다.
# 축약: 스펙의 상하 계층 대신 좌→우(입문 객관식 → 실기 → CKS) 배치와 한글 12px 이상 규칙을 적용했다.
import sys
sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, OK, INFO, KR, MONO

W, H = 880, 356
d = D(W, H, "CKS STUDY GUIDE · 01-01 §1",
      "CNCF 쿠버네티스 자격증 선행 관계",
      "KCNA와 KCSA는 입문 객관식이고 CKAD·CKA·CKS는 실기 시험이며, 다섯 자격증 가운데 CKS만 CKA 합격을 선행 조건으로 요구함을 보인 의존 그래프다.",
      "화살표는 필수 선행 조건만 가리키며, 입문·실기 4종은 선행 없이 바로 응시할 수 있습니다")

# 3열 좌→우 배치 (모든 좌표 4의 배수)
COL_W = 208
COLS = [
    (24, "입문 · 객관식", "선행 조건 없음"),
    (284, "실기 · 2시간", "선행 조건 없음"),
    (604, "보안 실기 · 2시간", "CKA 합격 필수"),
]
for x, head, sub in COLS:
    w = 252 if x == 604 else COL_W
    d.t(x + w / 2, 108, head, 13, INK, KR, "middle", 600)
    d.t(x + w / 2, 126, sub, 12, MUTED, KR)

# 노드 좌표
BH = 64
Y1, Y2 = 148, 232

nodes = [
    # (x, y, w, name, desc, color, focal)
    (24, Y1, COL_W, "KCNA", "클라우드 네이티브 기초", INFO, False),
    (24, Y2, COL_W, "KCSA", "보안 기술 기초", INFO, False),
    (284, Y1, COL_W, "CKAD", "앱 설계·빌드·배포 실기", OK, False),
    (284, Y2, COL_W, "CKA", "클러스터 관리 실기", OK, False),
    (604, Y2, 252, "CKS", "클러스터·워크로드 보안 실기", ACC, True),
]

for x, y, w, name, desc, c, focal in nodes:
    d.tone(x, y, w, BH, c, 6, "1E" if focal else "12", 1.4 if focal else 1.0)
    d.t(x + w / 2, y + 26, name, 15, c if focal else INK, MONO, "middle", 600)
    d.t(x + w / 2, y + 48, desc, 12, MUTED, KR)

# 유일한 선행 조건 화살표: CKA → CKS
ay = Y2 + BH / 2
d.path(f"M {284 + COL_W + 4} {ay} L {604 - 4} {ay}", ACC, 1.6, m="acc")
d.t(548, ay - 12, "선행 필수", 12, ACC, KR, "middle", 600)

d.legend(312, [("객관식 (선행 없음)", INFO), ("실기 (선행 없음)", OK), ("선행 조건 필수 (CKS)", ACC)])
d.save("01-01.cert-path.svg")

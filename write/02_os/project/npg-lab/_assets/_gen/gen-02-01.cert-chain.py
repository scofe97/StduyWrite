# 02-01-cert-chain — 인증서 사슬 구조(루트·중간·잎)와 certmagic 자동 갱신 규칙 및 점검 타이머 불일치 관측
# 본문 요구: 위에서 아래로 루트 CA(3600일) → 중간 CA(7일) → 잎 api.corp.internal(12시간). 서명 화살표. 오른쪽에 갱신 규칙 두 줄: 남은 수명 1/3, 점검 간격 5배 아래면 비상 갱신. 아래 각주 칸 하나: 3분 잎을 load 로 올리자 점검 타이머가 첫 기동 값(10분) 그대로라 만료된 잎을 6분 5초 내밈. focal 은 중간 CA(일상 발급을 맡는 자리).
# 타입 스펙: type-tree
# 사실 출처: 02-01.프록시 운영 — 무중단 설정 교체·인증서 사슬·모듈 등록부.md:82-90, ch10-e5-internal-tls.md:28-33,82-88,92-94, ca.go:3600d,7d, internalissuer.go:12h, maintain.go:1/3,5x
import sys
from pathlib import Path

ASSETS_DIR = Path(__file__).resolve().parent.parent
GEN_DIR = Path(__file__).resolve().parent
if str(ASSETS_DIR) not in sys.path:
    sys.path.insert(0, str(ASSETS_DIR))
if str(GEN_DIR) not in sys.path:
    sys.path.insert(0, str(GEN_DIR))

from dd import D, INK, MUTED, RULE, PAPER2, ACC, OK, WARN, BAD, INFO, KR

W = 960
H = 492

d = D(
    W,
    H,
    "TREE · CERTIFICATE CHAIN & RENEWAL",
    "인증서 사슬 구조와 자동 갱신 규칙",
    "신뢰의 뿌리부터 도메인까지 이어지는 인증서 사슬과 certmagic 자동 갱신 메커니즘",
    lead="루트가 서명을 중간 CA 에 위임하고, 일상 발급은 7일 중간 CA 가 맡습니다.",
)

# 상단 구분선 (4의 배수)
d.line(24, 92, 936, 92, RULE, 0.8)

# 1. 왼쪽: 인증서 사슬 (트리: 루트 -> 중간 -> 잎)
# 루트 CA
d.box(56, 116, 360, 60, fill=PAPER2, stroke=INFO, sw=1.0, r=6)
d.t(236, 140, "루트 CA (3600일)", 14, INFO, KR, "middle", 600)
d.t(236, 160, "운영은 오프라인 권장", 13, MUTED, KR, "middle")

# 서명 화살표 1 (루트 -> 중간)
d.arrow([(236, 176), (236, 212)], c=MUTED, m="ar", sw=1.4)
d.t(244, 198, "서명 (위임)", 13, MUTED, KR, "start")

# 중간 CA (focal)
d.tone(56, 212, 360, 60, ACC, r=6, op="14", sw=1.6)
d.t(236, 236, "중간 CA (7일)", 14, ACC, KR, "middle", 600)
d.t(236, 256, "일상 발급 대리 (온라인)", 13, INK, KR, "middle")

# 서명 화살표 2 (중간 -> 잎)
d.arrow([(236, 272), (236, 308)], c=ACC, m="acc", sw=1.4)
d.t(244, 294, "서명 (발급)", 13, ACC, KR, "start")

# 잎 인증서
d.box(56, 308, 360, 60, fill=PAPER2, stroke=OK, sw=1.2, r=6)
d.t(236, 332, "잎 api.corp.internal", 14, OK, KR, "middle", 600)
d.t(236, 352, "수명 12시간 · 서비스 신원", 13, INK, KR, "middle")

# 2. 오른쪽: 자동 갱신 규칙 영역
d.box(480, 116, 440, 252, fill="rgba(245,245,243,0.02)", stroke=RULE, sw=0.8, r=8)
d.t(500, 148, "certmagic 자동 갱신 규칙", 14, INK, KR, "start", 600)
d.line(500, 168, 900, 168, RULE, 0.8)

# 규칙 1: 남은 수명 1/3
d.box(500, 184, 400, 72, fill=PAPER2, stroke=INFO, sw=0.9, r=6)
d.t(516, 212, "규칙 1 · 남은 수명 1/3", 13, INFO, KR, "start", 600)
d.t(516, 236, "수명 1/3 남은 시점에 자동 갱신", 13, INK, KR, "start")

# 규칙 2: 점검 간격 5배
d.box(500, 272, 400, 72, fill=PAPER2, stroke=WARN, sw=0.9, r=6)
d.t(516, 300, "규칙 2 · 점검 간격 5배", 13, WARN, KR, "start", 600)
d.t(516, 324, "남은 수명 < 점검 간격×5 → 비상 갱신", 13, INK, KR, "start")

# 잎 -> 갱신 규칙 연결 감시 화살표
d.arrow([(416, 338), (480, 338)], c=WARN, m="warn", sw=1.4)
d.t(448, 328, "만료 감시", 13, WARN, KR, "middle")

# 3. 아래 각주 칸: 타이머 불일치 장애 관측
d.box(56, 384, 864, 48, fill=PAPER2, stroke=BAD, sw=1.0, r=6)
d.t(72, 412, "장애 관측 · 타이머 불일치", 13, BAD, KR, "start", 600)
d.line(260, 396, 260, 420, RULE, 0.8)
d.t(276, 412, "3분 잎 load 시 10분 타이머 유지로 만료 잎 6분 5초 내밈", 13, INK, KR, "start")

# 4. 범례 (y=448, 높이 492 안에서 448+22=470, 여유 22px >= 16px)
d.legend(
    448,
    [
        ("중간 CA (focal)", ACC),
        ("신뢰 뿌리 · 일반 갱신", INFO),
        ("서비스 잎 인증서", OK),
        ("비상 갱신 창", WARN),
        ("장애 관측", BAD),
    ],
)

d.save("02-01-cert-chain.svg")

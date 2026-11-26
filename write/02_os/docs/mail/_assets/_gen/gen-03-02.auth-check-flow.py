# 사실 출처: RFC 7208(SPF), RFC 6376(DKIM), RFC 7489 / RFC 9989(DMARC)
# 타입 스펙: type-flowchart
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W = 960
H = 600

d = D(
    W, H,
    "FLOWCHART · RECEIVER MTA AUTHENTICATION",
    "수신 MTA의 3단계 발신자 인증과 DMARC 정책 분기",
    "접속 IP와 봉투 주소로 SPF를 확인하고, 서명과 본문으로 DKIM을 검증한 뒤, 헤더 From과의 도메인 정렬로 최종 처리 정책을 결정합니다",
    "RFC 7208(SPF), RFC 6376(DKIM), RFC 7489 및 RFC 9989(DMARC) 수신 MTA 판단 기준"
)

# ── 1. 수신 메일 정보 (상단 입력 영역) ──
d.box(24, 100, 912, 58, PAPER2, RULE, 1.0)
d.t(44, 134, "수신 메일", 12, INK, KR, "start", 600)

d.chip(210, 134, "IP 198.51.100.1", INFO, 11)
d.chip(470, 134, "MAIL FROM: bounce@example.com", INFO, 11)
d.chip(780, 134, "From: alice@example.com", ACC, 11)

# 상단 입력에서 SPF/DKIM 검사 단계로 내려가는 수직 화살표
d.arrow([(250, 158), (250, 186)], INFO, "info", 1.4)
d.arrow([(710, 158), (710, 186)], INFO, "info", 1.4)

# ── 2. SPF 및 DKIM 검증 단계 (좌우 병렬 평가) ──
# [좌측] SPF 검사
d.box(44, 186, 412, 78, PAPER2, OK, 1.2)
d.t(60, 208, "1. SPF 검사 (발송 IP 대조)", 12, INK, KR, "start", 600)
d.t(60, 226, "DNS 질의: TXT example.com", 11, MUTED, MONO, "start")
d.t(60, 244, "레코드: v=spf1 ip4:198.51.100.0/24 -all", 11, MUTED, MONO, "start")
d.chip(380, 226, "SPF pass", OK, 11)

# [우측] DKIM 검사
d.box(504, 186, 412, 78, PAPER2, OK, 1.2)
d.t(520, 208, "2. DKIM 검사 (전자서명 검증)", 12, INK, KR, "start", 600)
d.t(520, 226, "DNS 질의: TXT s1._domainkey.example.com", 11, MUTED, MONO, "start")
d.t(520, 244, "서명 헤더: d=example.com · bh=해시 검증", 11, MUTED, MONO, "start")
d.chip(840, 226, "DKIM pass", OK, 11)

# SPF / DKIM 에서 DMARC 정렬 상자로 모이는 직각 꺾임 화살표
d.arrow([(250, 264), (250, 286), (480, 286), (480, 306)], OK, "ok", 1.4)
d.arrow([(710, 264), (710, 286), (480, 286)], OK, "ok", 1.4)

# ── 3. DMARC 식별자 정렬 (중앙 마름모/박스) ──
d.box(80, 306, 800, 72, PAPER2, ACC, 1.4)
d.t(480, 328, "3. DMARC 식별자 정렬 (Identifier Alignment)", 13, INK, KR, "middle", 600)
d.t(480, 346, "헤더 From(example.com)과 인증 도메인 대조", 11, MUTED, KR, "middle")

d.chip(260, 362, "SPF 정렬 pass", OK, 11)
d.chip(700, 362, "DKIM 정렬 pass", OK, 11)

# DMARC 판단 후 좌우 분기 화살표 (수직-수평 직각)
# 좌측 분기: 정렬 통과 (DMARC pass)
d.arrow([(250, 378), (250, 428)], OK, "ok", 1.5)
d.t(190, 404, "정렬 성공 (Pass)", 12, OK, KR, "middle")

# 우측 분기: 정렬 실패 (DMARC fail)
d.arrow([(710, 378), (710, 428)], BAD, "bad", 1.5)
d.t(770, 404, "정렬 실패 (Fail)", 12, BAD, KR, "middle")

# ── 4. 최종 결과 및 정책 분기 ──
# [좌측] DMARC 통과 결과
d.tone(44, 428, 412, 82, OK, r=6, op="18", sw=1.4)
d.t(250, 450, "DMARC pass (인증 및 정렬 통과)", 13, OK, KR, "middle", 600)
d.t(250, 472, "거부 정책 미적용 · SMTP 수락", 12, INK, KR, "middle")
d.t(250, 492, "이후 평판 및 콘텐츠 필터 평가 단계로", 12, MUTED, KR, "middle")

# [우측] DMARC 실패 정책 분기 영역
d.box(504, 428, 412, 82, PAPER2, RULE, 1.0)
d.t(710, 446, "DMARC FAIL (도메인 정책 p= 집행)", 12, WARN, KR, "middle", 600)

# 세부 정책 카드 3개 (p=none / p=quarantine / p=reject)
d.box(514, 460, 118, 42, PAPER2, INFO, 0.9)
d.t(573, 477, "p=none", 11, INFO, MONO, "middle", 600)
d.t(573, 493, "모니터링 배달", 11, MUTED, KR, "middle")

d.box(646, 460, 128, 42, PAPER2, WARN, 0.9)
d.t(710, 477, "p=quarantine", 11, WARN, MONO, "middle", 600)
d.t(710, 493, "스팸함 격리", 11, MUTED, KR, "middle")

d.box(788, 460, 118, 42, PAPER2, BAD, 0.9)
d.t(847, 477, "p=reject", 11, BAD, MONO, "middle", 600)
d.t(847, 493, "수신 거부 (550)", 11, MUTED, KR, "middle")

# ── 5. 범례 ──
d.legend(536, [
    ("인증 통과 / 수신", OK),
    ("식별자 정렬 / 핵심", ACC),
    ("격리 정책", WARN),
    ("인증 실패 / 거부", BAD),
    ("DNS 조회 / 검증", INFO)
])

d.save(Path(__file__).parent.parent / "03-02.auth-check-flow.svg")

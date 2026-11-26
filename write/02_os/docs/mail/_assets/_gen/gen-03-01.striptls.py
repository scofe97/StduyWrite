# 사실 출처: RFC 3207 Section 6, RFC 8461 Section 1·5.1, RFC 8460 Section 1
# 타입 스펙: type-sequence
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from dd import D, Seq, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W = 960
H = 880

class DiagramB(Seq):
    def lanes(s, names, y0=104, lane_w=180):
        s.LX = {}
        # 3개 레인 균등 배치 (180, 480, 780)
        positions = [180, 480, 780]
        for i, (nm, sub) in enumerate(names):
            x = positions[i]
            s.LX[nm] = x
            s.box(x - lane_w // 2, y0, lane_w, 44, PAPER2, RULE, 1.0)
            s.t(x, y0 + 20, nm, 12, INK, KR, "middle", 600)
            s.t(x, y0 + 37, sub, 11, MUTED, MONO)
        s.lane_top = y0 + 44
        return s.LX

    def alt_frame(s, x, y, w, h, op_text="ALT"):
        s.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="rgba(245,245,245,0.02)" stroke="{RULE}" stroke-width="1"/>')
        s.o.append(f'<rect x="{x}" y="{y}" width="40" height="18" rx="2" fill="{PAPER2}" stroke="{RULE}" stroke-width="1"/>')
        s.o.append(f'<text x="{x+20}" y="{y+13}" fill="{MUTED}" font-size="8" font-family="{MONO}" font-weight="600" text-anchor="middle" letter-spacing="0.12em">{op_text}</text>')

    def guard(s, x, y, text):
        s.t(x, y, text, 11, SOFT, fam=KR, anchor="start", weight=600)

    def alt_divider(s, x1, y, x2):
        s.line(x1, y, x2, y, RULE, 1.0, dash="4 3")

    def selfmsg_matched(s, a, label, y, c=MUTED, mk=None, sub=None):
        x = s.LX[a]
        m = mk or ("bad" if c == BAD else "ok" if c == OK else "info" if c == INFO else "warn" if c == WARN else "acc" if c == ACC else "ar")
        s.path(f"M {x+10} {y-10} L {x+52} {y-10} L {x+52} {y+10} L {x+13} {y+10}", c, 1.4, m=m)
        fam = KR if any('가' <= ch <= '힣' for ch in label) else MONO
        s.t(x + 60, y - 4, label, 11, c, fam=fam, anchor="start", weight=600)
        if sub:
            s.t(x + 60, y + 14, sub, 11, MUTED, fam=KR, anchor="start")

d = DiagramB(
    W, H,
    "SECURITY INCIDENT & MITIGATION · STRIPTLS & MTA-STS",
    "STRIPTLS 공격과 MTA-STS 정책 방어 흐름",
    "중간자가 평문 세션에서 STARTTLS 광고를 삭제해 평문 전송을 유도할 때, MTA-STS 정책이 암호화 누락을 감지하고 세션을 중단한다.",
    "기회적 TLS는 중간자의 광고 삭제에 취약하지만, 사전 배포된 MTA-STS 정책이 있으면 평문 전송을 거부합니다."
)

names = [
    ("발송 MTA", "Sending MTA"),
    ("네트워크 중간자", "MITM Attacker"),
    ("수신 MTA", "Receiving Server")
]
d.lanes(names, y0=104, lane_w=180)

# Lifelines
d.rails(788)

# Step 1: 클라이언트 -> 중간자 EHLO
d.msg("발송 MTA", "네트워크 중간자", "EHLO mail.example.com", 180, c=MUTED, mk="ar", sub="확장 기능 지원 확인 질의")

# Step 2: 중간자 -> 서버 전달
d.msg("네트워크 중간자", "수신 MTA", "EHLO mail.example.com", 216, c=MUTED, mk="ar", sub="수신 서버로 질의 전달")

# Step 3: 수신 서버 -> 중간자 STARTTLS 응답
d.msg("수신 MTA", "네트워크 중간자", "250-STARTTLS", 258, c=INFO, mk="info", dash="4 3", sub="정상 TLS 지원 광고 응답")

# Step 4: 중간자 STARTTLS 삭제 변조 (Focal)
d.selfmsg_matched("네트워크 중간자", "STARTTLS 삭제 변조", 298, c=BAD, sub="중간자 다운그레이드 공격 (STRIPTLS)")

# Step 5: 중간자 -> 클라이언트 변조된 목록 전달
d.msg("네트워크 중간자", "발송 MTA", "250-8BITMIME", 340, c=MUTED, mk="ar", dash="4 3", sub="STARTTLS 누락 목록 전달 (변조)")

# Combined Fragment: ALT (x=100..860 으로 180, 480, 780 세 생명선 완전 포괄)
frame_x = 100
frame_w = 760
d.alt_frame(frame_x, 376, frame_w, 396, "ALT")

# Region 1: 기회적 TLS 평문 폴백
d.guard(frame_x + 16, 404, "[기회적 TLS 기본 동작 (암호화 실패 시 평문 폴백)]")
d.msg("발송 MTA", "네트워크 중간자", "MAIL FROM:<alice@example.com>", 436, c=WARN, mk="warn", sub="평문 전송 (도청 취약)")
d.msg("네트워크 중간자", "수신 MTA", "MAIL FROM:<alice@example.com>", 472, c=MUTED, mk="ar", sub="수신 서버로 평문 중계")
d.msg("발송 MTA", "네트워크 중간자", "DATA (본문 평문 노출)", 508, c=WARN, mk="warn", sub="패킷 스니핑 및 도청 피해")
d.msg("네트워크 중간자", "수신 MTA", "DATA (본문 전달)", 544, c=MUTED, mk="ar", sub="평문 메일 수신 완료")

# Divider
d.alt_divider(frame_x + 8, 576, frame_x + frame_w - 8)

# Region 2: MTA-STS 정책 방어
d.guard(frame_x + 16, 604, "[MTA-STS enforce 모드 적용 시 (RFC 8461)]")
d.selfmsg_matched("발송 MTA", "MTA-STS 정책 캐시 대조", 636, c=OK, sub="STARTTLS 미제공 탐지")
d.msg("발송 MTA", "네트워크 중간자", "QUIT", 680, c=INFO, mk="info", sub="평문 전송 거부 및 세션 즉시 중단")
d.msg("네트워크 중간자", "수신 MTA", "QUIT", 716, c=MUTED, mk="ar", sub="세션 종료 전달")
d.selfmsg_matched("발송 MTA", "TLS-RPT 실패 기록", 752, c=INFO, sub="하루 단위 집계 보고서에 기록")

# Legend
d.legend(820, [
    ("공격 (STRIPTLS)", BAD),
    ("방어 (MTA-STS)", OK),
    ("위험 (도청)", WARN),
    ("보호 (QUIT·기록)", INFO)
])

out = Path(__file__).parent.parent / "03-01.striptls.svg"
d.save(str(out))
print(f"생성 완료: {out} ({W}x{H})")

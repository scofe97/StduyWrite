# 사실 출처: RFC 5321 Section 2.2.1, RFC 4954 Section 3·4·6, RFC 3207 Section 3
# 타입 스펙: type-sequence
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from dd import D, Seq, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W = 960
H = 724

class DiagramA(Seq):
    def lanes(s, names, y0=104, lane_w=200):
        s.LX = {}
        # 2개 레인을 화면 중앙 대칭(x=240, x=720)으로 균형 배치
        positions = [240, 720]
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

d = DiagramA(
    W, H,
    "PROTOCOL SEQUENCE · SMTP EXTENSION & POLICY",
    "EHLO 기능 광고와 서버 정책 요구의 분리",
    "클라이언트가 EHLO 명령으로 확인한 기능 목록은 지원 기능 광고이며, 실제 인증 집행은 서버 정책에 따라 250 허용 또는 530 거절로 갈린다.",
    "EHLO 응답의 AUTH·STARTTLS는 지원 가능성 안내일 뿐, 실제 강제 여부는 서버 정책으로 결정됩니다."
)

names = [
    ("발송 클라이언트", "MUA · 제출 애플리케이션"),
    ("SMTP 수신 서버", "MTA · MSA")
]
d.lanes(names, y0=104, lane_w=200)

# Lifelines
d.rails(624)

# Step 1: EHLO
d.msg("발송 클라이언트", "SMTP 수신 서버", "EHLO client.example.com", 180, c=MUTED, mk="ar", sub="확장 기능 지원 확인 요청")

# Step 2: 250- 호스트 식별
d.msg("SMTP 수신 서버", "발송 클라이언트", "250-mail.example.net", 220, c=MUTED, mk="ar", dash="4 3", sub="서버 식별 환영 응답")

# Step 3: STARTTLS 광고
d.msg("SMTP 수신 서버", "발송 클라이언트", "250-STARTTLS", 260, c=INFO, mk="info", dash="4 3", sub="TLS 보안 채널 협상 지원 광고")

# Step 4: AUTH 광고 (Focal 포인트)
d.msg("SMTP 수신 서버", "발송 클라이언트", "250-AUTH LOGIN PLAIN", 300, c=ACC, mk="acc", dash="4 3", sub="SASL 인증 메커니즘 지원 광고")

# Step 5: 250 종료
d.msg("SMTP 수신 서버", "발송 클라이언트", "250 8BITMIME", 340, c=MUTED, mk="ar", dash="4 3", sub="확장 기능 목록 종결")

# Step 6: 클라이언트 발송 시도
d.msg("발송 클라이언트", "SMTP 수신 서버", "MAIL FROM:<sender@example.com>", 388, c=MUTED, mk="ar", sub="AUTH 로그인 없이 발송 시도")

# Combined Fragment: ALT (x=160..800으로 두 생명선 x=240, 720을 완전 포괄)
frame_x = 160
frame_w = 640
d.alt_frame(frame_x, 428, frame_w, 184, "ALT")

# Region 1: 허용 정책
d.guard(frame_x + 16, 460, "[서버 정책: 미인증 발송 허용 (사내 릴레이 등)]")
d.msg("SMTP 수신 서버", "발송 클라이언트", "250 (수락 · 문구는 서버마다)", 488, c=OK, mk="ok", dash="4 3", sub="작업 수락 (광고된 인증 미사용 허용)")

# Divider
d.alt_divider(frame_x + 8, 524, frame_x + frame_w - 8)

# Region 2: 인증 필수 정책
d.guard(frame_x + 16, 548, "[서버 정책: 인증 필수 요구 (공용 제출 서버 등)]")
d.msg("SMTP 수신 서버", "발송 클라이언트", "530 5.7.0 Authentication required", 576, c=WARN, mk="warn", dash="4 3", sub="정책 집행 (작업 거절 및 인증 요구)")

# Legend (간결한 라벨로 우측 이탈 방지)
d.legend(664, [
    ("인증 광고 (AUTH)", ACC),
    ("보안 광고 (STARTTLS)", INFO),
    ("허용 응답 (250)", OK),
    ("거절 응답 (530)", WARN)
])

out = Path(__file__).parent.parent / "03-01.advertise-vs-require.svg"
d.save(str(out))
print(f"생성 완료: {out} ({W}x{H})")

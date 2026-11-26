# 사실 출처: RFC 5321(MX), RFC 6409(Submission), Google Workspace 도움말(174125, 176600), MS Learn(Exchange Online), 네이버 고객센터(21344), 공개 DNS 조회(2026-10-15)
# 타입 스펙: type-architecture
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, KR, MONO

W = 960
H = 560

d = D(
    W, H,
    "SYSTEM ARCHITECTURE · INBOUND MX VS CLIENT SUBMISSION",
    "대형 메일 서비스의 인바운드 MX와 제출 창구 분리",
    "Gmail·네이버·Microsoft 365 세 서비스의 인터넷 수신 창구(MX, 포트 25)와 사용자/앱 제출 창구(MSA, 포트 587/465) 분리 구조 (조회일 2026-10-15)",
    "인터넷에서 들어오는 수신 창구와 사용자가 인증하고 맡기는 제출 창구가 서로 다른 호스트와 포트로 격리된 구조"
)

# 1. 2개 Zone 영역 (상단 수신 MX, 하단 제출 MSA)
def draw_zone(x, y, w, h, label, c=RULE):
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="rgba(245,245,245,0.02)" stroke="{c}" stroke-width="0.9"/>')
    d.t(x + 16, y + 22, label, 12, SOFT, fam=KR, weight=600, anchor="start")

# 상단: 인터넷 수신 MX 영역
draw_zone(24, 96, 912, 168, "인터넷 수신 창구 · 인바운드 MX (포트 25 · 익명 수신 · 도메인 수신자 전용)", INFO)

# 하단: 클라이언트 제출 MSA 영역
draw_zone(24, 288, 912, 192, "사용자 및 앱 제출 창구 · 아웃바운드 MSA (포트 587/465 · 인증 필수 · 외부 인터넷 전송)", OK)

# 격리 경계선 (칩 좌우로 분할해 선이 글자에 닿지 않도록 함)
d.line(32, 276, 340, 276, WARN, sw=0.9, dash="4 4")
d.line(620, 276, 928, 276, WARN, sw=0.9, dash="4 4")
d.chip(480, 276, "호스트 · 포트 · 인증 정책 격리 경계", WARN, size=11)

# 열 정의 (Google, Naver, Microsoft 365)
cols = [
    {
        "name": "Google (Gmail · Workspace)",
        "mx_title": "Google 수신 MX",
        "mx_items": [
            ("5 gmail-smtp-in.l.google.com. (개인)", MONO),
            ("1 aspmx.l.google.com. (조직)", MONO),
            ("우선순위 5~40 alt1~alt4 폴백", KR),
            ("인증 없음 · 해당 도메인 메일함 배달", KR),
        ],
        "sub_title": "Google 제출 창구",
        "sub_items": [
            ("smtp.gmail.com:587(TLS) / 465(SSL)", MONO),
            ("smtp-relay.gmail.com:587/465/25", MONO),
            ("인증: 앱 비밀번호 · OAuth 2.0 · IP 등록", KR),
            ("외부 인터넷 전송 허용 (MTA 릴레이)", KR),
        ],
        "is_focal": True
    },
    {
        "name": "네이버 메일 (Naver Mail)",
        "mx_title": "네이버 수신 MX",
        "mx_items": [
            ("10 mx1.mail.naver.com. (기본)", MONO),
            ("20 mx4 · mx5 · mx6.mail.naver.com.", MONO),
            ("단일 도메인 naver.com 수신", KR),
            ("인증 없음 · 네이버 메일함 배달", KR),
        ],
        "sub_title": "네이버 메일 제출 창구",
        "sub_items": [
            ("smtp.naver.com:587 (TLS)", MONO),
            ("인증: 2단계 인증 전용 앱 비밀번호", KR),
            ("환경설정 'IMAP/SMTP 사용함' 필수", KR),
            ("외부 인터넷 전송 허용 (개인 발송)", KR),
        ],
        "is_focal": False
    },
    {
        "name": "Microsoft 365 (Exchange Online)",
        "mx_title": "Microsoft 365 수신 MX",
        "mx_items": [
            ("<도메인>-com (조직 MX / 포트 25)", MONO),
            ("  .mail.protection.outlook.com", MONO),
            ("Direct Send: 인증 없음 · 내부 전용", KR),
            ("커넥터(IP/인증서): 포트 25 외부 중계", KR),
        ],
        "sub_title": "Exchange Online 제출 창구",
        "sub_items": [
            ("smtp.office365.com:587 (STARTTLS)", MONO),
            ("클라이언트 제출: 사서함 계정 인증", KR),
            ("인증: Entra ID OAuth 2.0 권장", KR),
            ("외부 인터넷 전송 허용 (테넌트 사용자)", KR),
        ],
        "is_focal": False
    }
]

# 상자 배치
for i, col in enumerate(cols):
    bx = 36 + i * 304
    bw = 284

    # 1. 상단 수신 MX 카드
    d.box(bx, 128, bw, 124, fill=PAPER2, stroke=INFO, sw=1.0)
    d.t(bx + 16, 150, col["mx_title"], 13, INK, fam=KR, weight=600, anchor="start")
    d.line(bx + 16, 158, bx + bw - 16, 158, c=RULE, sw=0.6)
    for j, (it, fam) in enumerate(col["mx_items"]):
        d.t(bx + 16, 178 + j * 18, it, 11.5, MUTED, fam=fam, anchor="start")

    # 2. 하단 제출 MSA 카드
    if col["is_focal"]:
        d.tone(bx, 324, bw, 140, c=ACC, r=6, op="14", sw=1.4)
        d.t(bx + 16, 348, col["sub_title"], 13, ACC, fam=KR, weight=600, anchor="start")
        d.line(bx + 16, 356, bx + bw - 16, 356, c=ACC, sw=0.6)
        for j, (it, fam) in enumerate(col["sub_items"]):
            d.t(bx + 16, 376 + j * 18, it, 11.5, INK if j == 0 else MUTED, fam=fam, anchor="start")
    else:
        d.box(bx, 324, bw, 140, fill=PAPER2, stroke=OK, sw=1.0)
        d.t(bx + 16, 348, col["sub_title"], 13, INK, fam=KR, weight=600, anchor="start")
        d.line(bx + 16, 356, bx + bw - 16, 356, c=RULE, sw=0.6)
        for j, (it, fam) in enumerate(col["sub_items"]):
            d.t(bx + 16, 376 + j * 18, it, 11.5, MUTED, fam=fam, anchor="start")

# 범례 (Legend)
d.legend(H - 44, [
    ("수신 창구 (포트 25)", INFO),
    ("제출 창구 (포트 587/465)", OK),
    ("핵심 창구 (인증 필수)", ACC),
    ("호스트 격리 경계", WARN)
])

out = Path(__file__).parent.parent / "04-01.inbound-vs-submission.svg"
d.save(str(out))
print(f"생성 완료: {out} ({W}x{H})")

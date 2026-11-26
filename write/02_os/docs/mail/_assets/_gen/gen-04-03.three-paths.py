# 사실 출처: Google Cloud Sending Mail, AWS EC2 Port 25, Twilio SendGrid SMTP, RFC 1912 §2.1, Postfix OVERVIEW
# 타입 스펙: type-flowchart
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W = 960
H = 580

d = D(
    W, H,
    "FLOWCHART · THREE OUTBOUND PATHS",
    "앱이 메일을 보내는 세 갈래",
    "사내 중계(스마트 호스트), 클라우드 ESP, 수신 MX 직접 발송의 포트, 전달 경로, 평판 주체와 반송 수신처 비교",
    "앱 환경과 발송 목적에 따라 선택하는 세 가지 발송 통로와 제약"
)

# ── 상단 앱 노드 ──────────────────────────────────────────────────────────
APP_CX = 480
APP_CY = 110
APP_W = 280
APP_H = 46

d.box(APP_CX - APP_W / 2, APP_CY - APP_H / 2, APP_W, APP_H, fill=PAPER2, stroke=ACC, sw=1.4, r=8)
d.t(APP_CX, APP_CY - 3, "애플리케이션 (JavaMailSender)", 13, INK, KR, "middle", 600)
d.t(APP_CX, APP_CY + 15, "메일 발송 요청 생성 (MUA)", 11, MUTED, KR, "middle")

# ── 분기 버스 라인 ────────────────────────────────────────────────────────
BUS_Y = 160
d.line(APP_CX, APP_CY + APP_H / 2, APP_CX, BUS_Y, c=RULE, sw=1.2)

C1 = 175   # 사내 중계
C2 = 480   # 클라우드 ESP
C3 = 785   # MX 직접 발송

d.line(C1, BUS_Y, C3, BUS_Y, c=RULE, sw=1.2)

# ── 공통 카드 그리기 함수 ──────────────────────────────────────────────────
BW = 260
BH_HEAD = 52
BH_MID = 56
BH_DEST = 52
BH_META = 68

Y_HEAD = 190
Y_MID = 276
Y_DEST = 366
Y_META = 438

# 화살표 버스 -> 헤드
for cx in (C1, C2, C3):
    d.arrow([(cx, BUS_Y), (cx, Y_HEAD)], c=RULE, m="ar", sw=1.2)

# ── 1열: 사내 중계 (스마트 호스트) ──────────────────────────────────────────
# 헤더 카드
d.box(C1 - BW / 2, Y_HEAD, BW, BH_HEAD, fill=PAPER2, stroke=OK, sw=1.2)
d.t(C1, Y_HEAD + 20, "1. 사내 중계 (스마트 호스트)", 13.5, OK, KR, "middle", 600)
d.t(C1, Y_HEAD + 38, "사내망 포트 587 / 25", 11.5, MUTED, MONO, "middle")

# 연결선
d.arrow([(C1, Y_HEAD + BH_HEAD), (C1, Y_MID)], c=OK, m="ok", sw=1.3)
d.t(C1 + 8, (Y_HEAD + BH_HEAD + Y_MID) / 2 + 4, "내부 제출", 12.5, OK, KR, "start")

# 중간 릴레이 카드
d.box(C1 - BW / 2, Y_MID, BW, BH_MID, fill=PAPER2, stroke=RULE, sw=1.0)
d.t(C1, Y_MID + 22, "사내 스마트 호스트", 13.5, INK, KR, "middle", 600)
d.t(C1, Y_MID + 40, "Postfix · Exchange 큐잉 및 재시도", 12.5, MUTED, KR, "middle")

# 연결선
d.arrow([(C1, Y_MID + BH_MID), (C1, Y_DEST)], c=MUTED, m="ar", sw=1.3)
d.t(C1 + 8, (Y_MID + BH_MID + Y_DEST) / 2 + 4, "포트 25 릴레이", 11.5, MUTED, MONO, "start")

# 수신 카드
d.box(C1 - BW / 2, Y_DEST, BW, BH_DEST, fill=PAPER2, stroke=INFO, sw=1.0)
d.t(C1, Y_DEST + 21, "외부 수신 메일 서버 (MX)", 13.5, INK, KR, "middle", 600)
d.t(C1, Y_DEST + 39, "정상 수신 및 사용자 사서함 배달", 12.5, MUTED, KR, "middle")

# 메타 카드
d.tone(C1 - BW / 2, Y_META, BW, BH_META, c=OK, r=6, op="14", sw=1.0)
d.t(C1, Y_META + 24, "평판: 사내 공인 IP · 사내 도메인", 12.5, OK, KR, "middle", 600)
d.t(C1, Y_META + 48, "반송: 사내 MTA 큐 · 발신 사서함", 12.5, MUTED, KR, "middle")

# ── 2열: 클라우드 ESP ─────────────────────────────────────────────────────
# 헤더 카드
d.box(C2 - BW / 2, Y_HEAD, BW, BH_HEAD, fill=PAPER2, stroke=ACC, sw=1.2)
d.t(C2, Y_HEAD + 20, "2. 클라우드 ESP", 13.5, ACC, KR, "middle", 600)
d.t(C2, Y_HEAD + 38, "HTTPS API (443) / 포트 587", 11.5, MUTED, MONO, "middle")

# 연결선
d.arrow([(C2, Y_HEAD + BH_HEAD), (C2, Y_MID)], c=ACC, m="acc", sw=1.3)
d.t(C2 + 8, (Y_HEAD + BH_HEAD + Y_MID) / 2 + 4, "API / 릴레이 위임", 12.5, ACC, KR, "start")

# 중간 ESP 인프라 카드
d.box(C2 - BW / 2, Y_MID, BW, BH_MID, fill=PAPER2, stroke=RULE, sw=1.0)
d.t(C2, Y_MID + 22, "ESP 인프라 (SES · SendGrid)", 13.5, INK, KR, "middle", 600)
d.t(C2, Y_MID + 40, "글로벌 평판 관리 풀 · 서프레션", 12.5, MUTED, KR, "middle")

# 연결선
d.arrow([(C2, Y_MID + BH_MID), (C2, Y_DEST)], c=MUTED, m="ar", sw=1.3)
d.t(C2 + 8, (Y_MID + BH_MID + Y_DEST) / 2 + 4, "포트 25 아웃바운드", 11.5, MUTED, MONO, "start")

# 수신 카드
d.box(C2 - BW / 2, Y_DEST, BW, BH_DEST, fill=PAPER2, stroke=INFO, sw=1.0)
d.t(C2, Y_DEST + 21, "외부 수신 메일 서버 (MX)", 13.5, INK, KR, "middle", 600)
d.t(C2, Y_DEST + 39, "정상 수신 및 사용자 사서함 배달", 12.5, MUTED, KR, "middle")

# 메타 카드
d.tone(C2 - BW / 2, Y_META, BW, BH_META, c=ACC, r=6, op="14", sw=1.0)
d.t(C2, Y_META + 24, "평판: ESP 공유 IP 풀 (또는 전용 IP)", 12.5, ACC, KR, "middle", 600)
d.t(C2, Y_META + 48, "반송: ESP 웹훅 · SNS 이벤트 전달", 12.5, MUTED, KR, "middle")

# ── 3열: 수신 MX 직접 발송 ────────────────────────────────────────────────
# 헤더 카드
d.box(C3 - BW / 2, Y_HEAD, BW, BH_HEAD, fill=PAPER2, stroke=BAD, sw=1.2)
d.t(C3, Y_HEAD + 20, "3. MX 직접 발송", 13.5, BAD, KR, "middle", 600)
d.t(C3, Y_HEAD + 38, "인터넷 아웃바운드 포트 25", 11.5, MUTED, MONO, "middle")

# 연결선
d.arrow([(C3, Y_HEAD + BH_HEAD), (C3, Y_MID)], c=BAD, m="bad", sw=1.3)
d.t(C3 + 8, (Y_HEAD + BH_HEAD + Y_MID) / 2 + 4, "포트 25 직접 연결", 12.5, BAD, KR, "start")

# 중간 직접 발송 제약 카드
d.box(C3 - BW / 2, Y_MID, BW, BH_MID, fill=PAPER2, stroke=BAD, sw=1.0)
d.t(C3, Y_MID + 22, "클라우드 25번 차단 · PTR 부재", 13.5, BAD, KR, "middle", 600)
d.t(C3, Y_MID + 40, "AWS · GCP · Azure 차단 / 유동 IP", 12.5, MUTED, KR, "middle")

# 연결선
d.arrow([(C3, Y_MID + BH_MID), (C3, Y_DEST)], c=BAD, m="bad", sw=1.3)
d.t(C3 + 8, (Y_MID + BH_MID + Y_DEST) / 2 + 4, "PBL 등재 · 거부", 12.5, BAD, KR, "start")

# 수신 카드 (실패/차단)
d.box(C3 - BW / 2, Y_DEST, BW, BH_DEST, fill=PAPER2, stroke=BAD, sw=1.0)
d.t(C3, Y_DEST + 21, "수신 거부(550) 또는 스팸 분류", 13.5, BAD, KR, "middle", 600)
d.t(C3, Y_DEST + 39, "Spamhaus PBL · FCrDNS 불일치", 12.5, MUTED, KR, "middle")

# 메타 카드
d.tone(C3 - BW / 2, Y_META, BW, BH_META, c=BAD, r=6, op="14", sw=1.0)
d.t(C3, Y_META + 24, "평판: 앱 서버 IP (초기 평판 없음)", 12.5, BAD, KR, "middle", 600)
d.t(C3, Y_META + 48, "반송: 앱 자체 처리 (재시도 큐 구현)", 12.5, MUTED, KR, "middle")

# ── 범례 ───────────────────────────────────────────────────────────────────
d.legend(H - 46, [
    ("사내 중계", OK),
    ("클라우드 ESP", ACC),
    ("직접 발송 제약", BAD),
    ("수신 MX", INFO),
])

out = Path(__file__).parent.parent / "04-03.three-paths.svg"
d.save(str(out))
print(f"생성 완료: {out}")

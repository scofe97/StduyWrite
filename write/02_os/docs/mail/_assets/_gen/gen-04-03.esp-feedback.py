# 사실 출처: Twilio SendGrid Tracking Events, AWS SES Notification Guide, RFC 5321 §6.1
# 타입 스펙: type-sequence
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W = 960
H = 810

d = D(
    W, H,
    "SEQUENCE · ESP EVENT FEEDBACK LOOP",
    "ESP의 비동기 반송·컴플레인 피드백 루프",
    "메일 발송 위임 후 수신 MX의 5xx 거부 또는 사용자 스팸 신고가 발생했을 때 웹훅 이벤트를 통해 앱 DB에 반영되는 흐름",
    "동기 발송 접수(202/250)와 실제 배달 실패를 분리해 발신 평판을 지키는 피드백 구조"
)

# 비동기 열린 화살표 마커 추가
d.o.append(
    f'<defs><marker id="ar-open" viewBox="0 0 8 8" refX="7" refY="4" '
    f'markerWidth="6.5" markerHeight="6.5" orient="auto">'
    f'<polyline points="1 1, 7 4, 1 7" fill="none" stroke="{MUTED}" stroke-width="1.3"/>'
    f'</marker></defs>'
)

# ── 참여자 레인 ────────────────────────────────────────────────────────────
LANES_Y = 100
LANE_W = 230
L1 = 180   # 애플리케이션
L2 = 490   # 클라우드 ESP
L3 = 800   # 수신 메일 인프라
BOTTOM_Y = 730

# 레인 머리 박스
d.box(L1 - LANE_W / 2, LANES_Y, LANE_W, 44, fill=PAPER2, stroke=INFO, sw=1.2)
d.t(L1, LANES_Y + 19, "애플리케이션 (앱 서버)", 13.5, INK, KR, "middle", 600)
d.t(L1, LANES_Y + 36, "MailService · Webhook", 12, MUTED, MONO, "middle")

d.box(L2 - LANE_W / 2, LANES_Y, LANE_W, 44, fill=PAPER2, stroke=ACC, sw=1.2)
d.t(L2, LANES_Y + 19, "클라우드 ESP 인프라", 13.5, INK, KR, "middle", 600)
d.t(L2, LANES_Y + 36, "Amazon SES · SendGrid", 12, MUTED, MONO, "middle")

d.box(L3 - LANE_W / 2, LANES_Y, LANE_W, 44, fill=PAPER2, stroke=RULE, sw=1.0)
d.t(L3, LANES_Y + 19, "수신 메일 인프라", 13.5, INK, KR, "middle", 600)
d.t(L3, LANES_Y + 36, "수신 도메인 MX · 사서함", 12.5, MUTED, KR, "middle")

# 수직 생명선 (점선)
for lx in (L1, L2, L3):
    d.line(lx, LANES_Y + 44, lx, BOTTOM_Y, c=RULE, sw=1.0, dash="3 6")

# ── 메시지 도우미 함수 ──────────────────────────────────────────────────────
def call_msg(x1, x2, y, label, sub=None, c=MUTED, mk="ar", dash=None):
    d.path(f"M {x1 + 8} {y} L {x2 - 8} {y}", c=c, sw=1.4, m=mk, dash=dash)
    mx = (x1 + x2) / 2
    d.t(mx, y - 9, label, 12, c if c != MUTED else INK, MONO, "middle", 600)
    if sub:
        d.t(mx, y + 17, sub, 12.5, MUTED, KR, "middle")

def ret_msg(x1, x2, y, label, sub=None, c=MUTED, mk="ar"):
    # 반송선: dashed + filled marker
    d.path(f"M {x1 - 8} {y} L {x2 + 8} {y}", c=c, sw=1.4, m=mk, dash="5 4")
    mx = (x1 + x2) / 2
    d.t(mx, y - 9, label, 12, c, MONO, "middle", 600)
    if sub:
        d.t(mx, y + 17, sub, 12.5, MUTED, KR, "middle")

def self_msg(lx, y, label, sub=None, c=MUTED):
    d.path(f"M {lx + 6} {y - 10} L {lx + 46} {y - 10} L {lx + 46} {y + 10} L {lx + 8} {y + 10}", c=c, sw=1.4, m="ar")
    d.t(lx + 54, y - 4, label, 12.5, c, KR, "start", 600)
    if sub:
        d.t(lx + 54, y + 15, sub, 12, MUTED, KR if any('가' <= ch <= '힣' for ch in str(sub)) else MONO, "start")

# ── 1단계: 동기 위임 및 접수 성공 ──────────────────────────────────────────
# 1. 앱 -> ESP 발송 요청
call_msg(L1, L2, 168, "POST /v3/mail/send (SendGrid)", "발송 요청 위임 (또는 SMTP 587)", c=INFO, mk="info")

# 2. ESP -> 앱 접수 응답 (Headline Success: 단 1개만 ACC 강조)
ret_msg(L2, L1, 216, "202 Accepted (SendGrid) / 250 Ok", "접수 완료 (ESP 내부 큐 적재)", c=ACC, mk="acc")

# 3. ESP -> 수신 MX 아웃바운드 시도
call_msg(L2, L3, 264, "SMTP DATA (TCP 25)", "외부 인터넷 발송 시도", c=MUTED, mk="ar")

# ── 2단계: ALT 결합 프래그먼트 (반송 vs 스팸 신고) ─────────────────────────
FRAME_X = 60
FRAME_W = 840
FRAME_Y = 300
FRAME_H = 420
DIV_Y = 514

# ALT 프레임 외곽
d.o.append(
    f'<rect x="{FRAME_X}" y="{FRAME_Y}" width="{FRAME_W}" height="{FRAME_H}" rx="4" '
    f'fill="rgba(245,245,245,0.03)" stroke="{RULE}" stroke-width="1"/>'
)
# ALT 연산자 탭
d.o.append(
    f'<rect x="{FRAME_X}" y="{FRAME_Y}" width="40" height="18" rx="2" '
    f'fill="{PAPER}" stroke="{RULE}" stroke-width="1"/>'
)
d.t(FRAME_X + 20, FRAME_Y + 13, "ALT", 9, SOFT, MONO, "middle", 600)

# ── 분기 A: [수신 거부 (하드 바운스)] ──────────────────────────────────────
d.t(FRAME_X + 54, FRAME_Y + 14, "[수신 거부 — 없는 계정 또는 영구 실패]", 12, SOFT, KR, "start")

# 4. 수신 MX -> ESP (550 반송 거부)
ret_msg(L3, L2, 348, "550 5.1.1 User unknown", "영구 배달 실패 (DSN)", c=BAD, mk="bad")

# 5. ESP 자체 처리: 서프레션 등록
self_msg(L2, 392, "서프레션 목록 자동 등록", "SendGrid: suppression list", c=BAD)

# 6. ESP -> 앱 비동기 이벤트 알림
d.path(f"M {L2 - 8} {436} L {L1 + 8} {436}", c=MUTED, sw=1.4, m="ar-open", dash="5 4")
d.t((L1 + L2) / 2, 427, "POST /webhook (event: bounce)", 12, INK, MONO, "middle", 600)
d.t((L1 + L2) / 2, 453, "AWS SES: Bounce 알림", 12.5, MUTED, KR, "middle")

# 7. 앱 자체 처리: DB 주소 비활성화
self_msg(L1, 480, "수신 주소 비활성화", "발송 대상 제외 플래그 갱신", c=WARN)

# ── 영역 구분선 ────────────────────────────────────────────────────────────
d.line(FRAME_X + 8, DIV_Y, FRAME_X + FRAME_W - 8, DIV_Y, c=RULE, sw=1.0, dash="4 3")

# ── 분기 B: [사용자 스팸 신고 (컴플레인)] ──────────────────────────────────
d.t(FRAME_X + 16, DIV_Y + 16, "[사용자 스팸 신고 — 피드백 루프(FBL) 제공처 (Gmail 제외)]", 12, SOFT, KR, "start")

# 8. 수신 메일 서버 -> ESP 피드백 루프 알림
ret_msg(L3, L2, 558, "피드백 루프 (FBL) 통보", "수신자 스팸 차단 (FBL 제공 포털)", c=WARN, mk="warn")

# 9. ESP 자체 처리: 서프레션 등록
self_msg(L2, 602, "서프레션 목록 자동 등록", "동일 주소 추가 발송 차단", c=BAD)

# 10. ESP -> 앱 비동기 이벤트 알림
d.path(f"M {L2 - 8} {646} L {L1 + 8} {646}", c=MUTED, sw=1.4, m="ar-open", dash="5 4")
d.t((L1 + L2) / 2, 637, "POST /webhook (event: spamreport)", 12, INK, MONO, "middle", 600)
d.t((L1 + L2) / 2, 663, "AWS SES: Complaint 알림", 12.5, MUTED, KR, "middle")

# 11. 앱 자체 처리: 마케팅 수신 거부 목록 추가
self_msg(L1, 690, "수신 거부 목록에 추가", "마케팅 발송 대상 제외", c=WARN)

# ── 범례 ───────────────────────────────────────────────────────────────────
d.legend(H - 46, [
    ("위임 접수 성공 (2xx)", ACC),
    ("배달 실패 (5xx 바운스)", BAD),
    ("스팸 신고 (컴플레인)", WARN),
    ("동기 요청 / 정보 전달", INFO),
])

out = Path(__file__).parent.parent / "04-03.esp-feedback.svg"
d.save(str(out))
print(f"생성 완료: {out}")

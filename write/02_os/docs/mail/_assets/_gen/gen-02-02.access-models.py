# 사실 출처: RFC 1939(POP3), RFC 3501(IMAP4rev1), RFC 9051(IMAP4rev2), RFC 8620·8621(JMAP)
# 타입 스펙: type-swimlane
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W = 960
H = 560

d = D(
    W, H,
    "MAILBOX ACCESS PROTOCOLS · MULTI-DEVICE COMPARISON",
    "메일함 접근 모델 비교 — POP3 · IMAP · JMAP",
    "동일 시나리오(메일 3통 수신 후 노트북 열람 → 스마트폰 재확인)에서 서버와 기기별 상태 전이",
    "서버 보관 여부와 동기화 메커니즘에 따른 다중 기기 환경의 사서함 정합성 비교"
)

# 컬럼 가이드 헤더
cols = [
    (168, 148, "초기 사서함 상태"),
    (330, 190, "노트북 접속 & Msg 1 열람"),
    (534, 190, "스마트폰 접속 & 재확인"),
    (738, 198, "다중 기기 동기화 결과")
]
for cx, cw, ctitle in cols:
    d.t(cx + cw / 2, 114, ctitle, 12, SOFT, fam=KR, weight=600)

def draw_lane(y, proto, role_kr, port_str, c_badge):
    # 레인 헤더 카드
    d.box(24, y, 130, 112, PAPER2, RULE, 1.0)
    d.t(89, y + 36, proto, 16, c_badge, fam=MONO, weight=600)
    d.t(89, y + 62, role_kr, 12, INK, fam=KR, weight=600)
    d.t(89, y + 84, port_str, 12, MUTED, fam=KR)

# 구분선 함수
def lane_div(y):
    d.line(24, y, W - 24, y, RULE, 0.8, dash="4 4")

# ==========================================
# Lane 1: POP3 (RFC 1939)
# ==========================================
y1 = 128
draw_lane(y1, "POP3", "내려받기 모델", "포트 110 접속", BAD)

# POP3 Col 0: 초기 상태
d.box(168, y1 + 10, 148, 92, PAPER2, RULE, 0.9)
d.t(242, y1 + 34, "서버 사서함", 12, SOFT, fam=KR, weight=600)
d.t(242, y1 + 56, "Msg 1, 2, 3", 12, INK, fam=MONO, weight=600)
d.chip(242, y1 + 80, "미열람 3통", INFO, size=12)

d.arrow([(316, y1 + 56), (330, y1 + 56)], MUTED, "ar", 1.2)

# POP3 Col 1: 노트북 접속
d.box(330, y1 + 10, 190, 92, PAPER2, RULE, 0.9)
d.t(425, y1 + 30, "RETR 1~3 · DELE 1~3", 11, INFO, fam=MONO)
d.t(425, y1 + 54, "노트북: 3통 로컬 저장", 12, INK, fam=KR)
d.t(425, y1 + 74, "Msg 1 열람 (로컬 플래그)", 12, MUTED, fam=KR)
d.t(425, y1 + 92, "서버: 0통 (QUIT 시 삭제)", 12, BAD, fam=KR)

d.arrow([(520, y1 + 56), (534, y1 + 56)], MUTED, "ar", 1.2)

# POP3 Col 2: 스마트폰 접속
d.box(534, y1 + 10, 190, 92, PAPER2, RULE, 0.9)
d.t(629, y1 + 32, "STAT → +OK 0 0", 11, MUTED, fam=MONO)
d.t(629, y1 + 58, "스마트폰: 0통 표시", 12, BAD, fam=KR, weight=600)
d.t(629, y1 + 82, "서버 사서함 비어 있음", 12, MUTED, fam=KR)

d.arrow([(724, y1 + 56), (738, y1 + 56)], MUTED, "ar", 1.2)

# POP3 Col 3: 동기화 결과
d.box(738, y1 + 10, 198, 92, PAPER2, BAD, 1.2)
d.t(837, y1 + 36, "기기간 데이터 고립", 12, BAD, fam=KR, weight=600)
d.t(837, y1 + 60, "기본 삭제 시 타 기기 불가", 12, INK, fam=KR)
d.t(837, y1 + 82, "남겨도 읽음 상태 미공유", 12, MUTED, fam=KR)

lane_div(250)

# ==========================================
# Lane 2: IMAP4 (RFC 3501, RFC 9051)
# ==========================================
y2 = 258
draw_lane(y2, "IMAP4", "서버 보관 모델", "포트 143 접속", OK)

# IMAP Col 0: 초기 상태
d.box(168, y2 + 10, 148, 92, PAPER2, RULE, 0.9)
d.t(242, y2 + 34, "서버 사서함", 12, SOFT, fam=KR, weight=600)
d.t(242, y2 + 56, "Msg 1, 2, 3", 12, INK, fam=MONO, weight=600)
d.chip(242, y2 + 80, "미열람 3통", INFO, size=12)

d.arrow([(316, y2 + 56), (330, y2 + 56)], MUTED, "ar", 1.2)

# IMAP Col 1: 노트북 접속
d.box(330, y2 + 10, 190, 92, PAPER2, RULE, 0.9)
d.t(425, y2 + 30, "STORE 1 +FLAGS (\\Seen)", 11, INFO, fam=MONO)
d.t(425, y2 + 54, "노트북: Msg 1 읽음 표시", 12, INK, fam=KR)
d.t(425, y2 + 74, "서버: Msg 1 \\Seen 저장", 12, OK, fam=KR)
d.t(425, y2 + 92, "서버 원격 사서함 유지", 12, MUTED, fam=KR)

d.arrow([(520, y2 + 56), (534, y2 + 56)], MUTED, "ar", 1.2)

# IMAP Col 2: 스마트폰 접속
d.box(534, y2 + 10, 190, 92, PAPER2, RULE, 0.9)
d.t(629, y2 + 32, "FETCH 1:* FLAGS", 11, MUTED, fam=MONO)
d.t(629, y2 + 58, "스마트폰: 3통 모두 수신", 12, OK, fam=KR, weight=600)
d.t(629, y2 + 82, "Msg 1 읽음 상태 일치", 12, MUTED, fam=KR)

d.arrow([(724, y2 + 56), (738, y2 + 56)], MUTED, "ar", 1.2)

# IMAP Col 3: 동기화 결과
d.box(738, y2 + 10, 198, 92, PAPER2, OK, 1.2)
d.t(837, y2 + 36, "서버 중심 상태 일치", 12, OK, fam=KR, weight=600)
d.t(837, y2 + 60, "다중 기기 동기화 성공", 12, INK, fam=KR)
d.t(837, y2 + 82, "플래그·폴더 원격 공유", 12, MUTED, fam=KR)

lane_div(380)

# ==========================================
# Lane 3: JMAP (RFC 8620, RFC 8621)
# ==========================================
y3 = 388
draw_lane(y3, "JMAP", "JSON·배치 모델", "HTTP POST 접속", ACC)

# JMAP Col 0: 초기 상태
d.box(168, y3 + 10, 148, 92, PAPER2, RULE, 0.9)
d.t(242, y3 + 34, "서버 사서함", 12, SOFT, fam=KR, weight=600)
d.t(242, y3 + 56, "Msg 1, 2, 3", 12, INK, fam=MONO, weight=600)
d.chip(242, y3 + 80, "미열람 3통", INFO, size=12)

d.arrow([(316, y3 + 56), (330, y3 + 56)], MUTED, "ar", 1.2)

# JMAP Col 1: 노트북 접속
d.box(330, y3 + 10, 190, 92, PAPER2, RULE, 0.9)
d.t(425, y3 + 30, "Email/set (keywords/$seen)", 11, INFO, fam=MONO)
d.t(425, y3 + 54, "단일 HTTP 요청 일괄 처리", 12, INK, fam=KR)
d.t(425, y3 + 74, "서버: Msg 1 $seen 반영", 12, OK, fam=KR)
d.t(425, y3 + 92, "상태 식별자 갱신", 12, MUTED, fam=KR)

d.arrow([(520, y3 + 56), (534, y3 + 56)], MUTED, "ar", 1.2)

# JMAP Col 2: 스마트폰 접속
d.box(534, y3 + 10, 190, 92, PAPER2, RULE, 0.9)
d.t(629, y3 + 32, "Email/changes (1 RTT)", 11, MUTED, fam=MONO)
d.t(629, y3 + 58, "스마트폰: 델타 동기화", 12, OK, fam=KR, weight=600)
d.t(629, y3 + 82, "SSE 푸시 알림 수신", 12, MUTED, fam=KR)

d.arrow([(724, y3 + 56), (738, y3 + 56)], MUTED, "ar", 1.2)

# JMAP Col 3: 동기화 결과
d.tone(738, y3 + 10, 198, 92, ACC, r=6, op="14", sw=1.4)
d.t(837, y3 + 36, "모바일 고효율 동기화", 12, ACC, fam=KR, weight=600)
d.t(837, y3 + 60, "왕복 시간·배터리 최소화", 12, INK, fam=KR)
d.t(837, y3 + 82, "서버 푸시 기반 즉시 갱신", 12, MUTED, fam=KR)

# 범례
d.legend(518, [
    ("정상 동기화 · 일치", OK),
    ("데이터 고립 · 불일치", BAD),
    ("프로토콜 명령 · 요청", INFO),
    ("모바일 최적화", ACC)
])

out = Path(__file__).parent.parent / "02-02.access-models.svg"
d.save(str(out))
print(f"생성 완료: {out} ({W}x{H})")

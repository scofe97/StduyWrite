# 사실 출처: Google Workspace 도움말(176600, 2956491)
# 타입 스펙: type-flowchart
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, KR, MONO

W = 960
H = 580

d = D(
    W, H,
    "DECISION FLOW · GOOGLE WORKSPACE OUTBOUND",
    "Google Workspace 외부 앱 발송 경로 선택",
    "외부 애플리케이션이 Google Workspace 환경에서 메일을 보낼 때 수신자 범위와 인증 지원 여부에 따라 선택하는 세 가지 경로",
    "수신자 범위(Gmail/Workspace 한정 여부)와 인증 수단(계정 자격 증명 또는 고정 IP)에 따른 발송 경로 결정 흐름"
)

CX = 250
RX = 570
RW = 354
RH = 54
DW = 280
DH = 52

def diamond(cx, cy, text):
    pts = f"{cx},{cy - DH // 2} {cx + DW // 2},{cy} {cx},{cy + DH // 2} {cx - DW // 2},{cy}"
    d.o.append(f'<polygon points="{pts}" fill="{PAPER2}" stroke="{RULE}" stroke-width="0.9"/>')
    d.t(cx, cy + 5, text, 12, INK, fam=KR, anchor="middle", weight=600)

def result_box(rx, y, main, sub, c):
    d.tone(rx, y - RH // 2, RW, RH, c, r=6, op="14", sw=1.2)
    d.t(rx + 16, y - 4, main, 13, c, fam=MONO if ":" in main else KR, anchor="start", weight=600)
    d.t(rx + 16, y + 16, sub, 11, MUTED, fam=KR, anchor="start")

# 1. 시작 타원 (y = 96, 높이 36)
d.o.append(f'<rect x="{CX - 120}" y="96" width="240" height="36" rx="18" fill="{PAPER2}" stroke="{RULE}" stroke-width="0.9"/>')
d.t(CX, 119, "외부 앱 메일 발송 설정", 13, INK, fam=KR, weight=600)
# 시작 화살표: 132 -> 178 (길이 46px >= 180/4)
d.arrow([(CX, 132), (CX, 178)], SOFT, "soft", 1.2)

# 2. 질문 1 (y = 204)
diamond(CX, 204, "외부 일반 도메인 수신자 포함 여부")
# 분기 1-1: Gmail/Workspace 수신자만 (오른쪽 -> aspmx)
d.arrow([(CX + DW // 2, 204), (RX, 204)], INFO, "info", 1.4)
d.t((CX + DW // 2 + RX) // 2, 194, "Gmail/Workspace 수신자만", 11, INFO, fam=KR, anchor="middle", weight=600)
result_box(RX, 204, "aspmx.l.google.com:25", "Restricted SMTP · 인증 불필요 · Gmail/Workspace만", INFO)

# 분기 1-2: 예 (아래로 -> 질문 2)
d.arrow([(CX, 204 + DH // 2), (CX, 312 - DH // 2)], SOFT, "soft", 1.2)
d.t(CX + 14, 258, "예", 11, MUTED, fam=KR, anchor="start", weight=600)

# 3. 질문 2 (y = 312)
diamond(CX, 312, "계정 인증(앱 비밀번호) 가능 여부")
# 분기 2-1: 예 (오른쪽 -> smtp.gmail.com) [FOCAL]
d.arrow([(CX + DW // 2, 312), (RX, 312)], ACC, "acc", 1.6)
d.t((CX + DW // 2 + RX) // 2, 302, "예 (인증 가능)", 11, ACC, fam=KR, anchor="middle", weight=600)
result_box(RX, 312, "smtp.gmail.com:587 / 465", "Gmail SMTP · 앱 비밀번호 인증 · 사용자당 일 2,000통", ACC)

# 분기 2-2: 아니오 (아래로 -> 질문 3)
d.arrow([(CX, 312 + DH // 2), (CX, 420 - DH // 2)], SOFT, "soft", 1.2)
d.t(CX + 14, 366, "아니오", 11, MUTED, fam=KR, anchor="start", weight=600)

# 4. 질문 3 (y = 420)
diamond(CX, 420, "고정 공인 IP 등록 가능 여부")
# 분기 3-1: 예 (오른쪽 -> smtp-relay.gmail.com)
d.arrow([(CX + DW // 2, 420), (RX, 420)], OK, "ok", 1.4)
d.t((CX + DW // 2 + RX) // 2, 410, "예 (IP 등록)", 11, OK, fam=KR, anchor="middle", weight=600)
result_box(RX, 420, "smtp-relay.gmail.com:587 / 465 / 25", "SMTP relay · 고정 IP 허용 · 사용자당 일 10,000명", OK)

# 분기 3-2: 아니오 (아래로 -> 발송 불가 / 끝 노드, 446 -> 492 길이 46px)
d.arrow([(CX, 420 + DH // 2), (CX, 492)], WARN, "warn", 1.2)
d.t(CX + 14, 466, "아니오", 11, WARN, fam=KR, anchor="start", weight=600)

# 5. 끝 타원 (y = 492, 높이 36)
d.o.append(f'<rect x="{CX - 130}" y="492" width="260" height="36" rx="18" fill="{PAPER2}" stroke="{WARN}" stroke-width="1.0"/>')
d.t(CX, 515, "발송 불가 (인증 또는 IP 등록 필수)", 12, WARN, fam=KR, weight=600)

# 범례 (Legend)
d.legend(H - 44, [
    ("Gmail/Workspace 수신자만", INFO),
    ("계정 인증 (소규모 발송)", ACC),
    ("IP 중계 (대량 릴레이)", OK),
    ("발송 불가 조건", WARN)
])

out = Path(__file__).parent.parent / "04-01.workspace-paths.svg"
d.save(str(out))
print(f"생성 완료: {out} ({W}x{H})")

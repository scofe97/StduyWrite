# 사실 출처: RFC 5321 §2.3.10 (Relay/Delivery) · §3.6.2 (Relay 550) · RFC 2505 §2.1 (Anti-Relay) · RFC 6409 §4.3 (Submission AUTH)
# 타입 스펙: type-flowchart
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W = 880
H = 580

d = D(
    W, H,
    "SMTP INBOUND DECISION LOGIC · FLOWCHART",
    "메일 수신 서버의 중계와 배달 판정 흐름",
    "서버가 메일(RCPT TO)을 받았을 때 수신자 도메인과 발신자 인증에 따라 배달·중계·거절을 가르는 판단 기준",
    "RFC 5321 §2.3.10 및 RFC 2505 안티 스팸 릴레이 통제 권고 기준"
)

# 1. 시작 단계 (인바운드 수신)
# Oval 형태 상자 (rx=20)
d.box(332, 96, 216, 44, PAPER2, RULE, 1.0, r=20)
d.t(440, 116, "SMTP 연결 및 수신", 13, INK, fam=KR, weight=600)
d.t(440, 130, "MAIL FROM + RCPT TO", 11, MUTED, fam=MONO)

# 시작 -> 판정 1 화살표
d.arrow([(440, 140), (440, 172)], MUTED, "ar", 1.4)


# 2. 첫 번째 판정: 수신자 도메인이 로컬인가? (FOCAL POINT)
d.tone(316, 172, 248, 64, ACC, r=6, op="14", sw=1.4)
d.t(440, 198, "받는 사람 도메인이 내 것인가?", 13, INK, fam=KR, weight=600)
d.t(440, 218, "RCPT TO 로컬 도메인 판정", 12, MUTED, fam=KR)

# 판정 1 -> 왼쪽 분기 ("예" -> 로컬 배달)
d.arrow([(316, 204), (280, 204)], OK, "ok", 1.4)
d.t(298, 192, "예", 12, OK, fam=KR, anchor="middle", weight=600)

# 왼쪽 결과 상자: 로컬 사서함 배달 (OK)
d.box(64, 172, 216, 64, PAPER2, OK, 1.2)
d.t(172, 198, "로컬 사서함 배달 (MDA)", 13, OK, fam=KR, weight=600)
d.t(172, 218, "사서함에 저장 (보관 목적)", 12, MUTED, fam=KR)
d.chip(172, 256, "250 OK · 최종 배달", OK, size=11)

# 판정 1 -> 아래 분기 ("아니오" -> 판정 2)
d.arrow([(440, 236), (440, 308)], MUTED, "ar", 1.4)
d.t(448, 272, "아니오", 12, MUTED, fam=KR, anchor="start", weight=600)


# 3. 두 번째 판정: 보낸 이가 인증했거나 허용 IP인가?
d.box(316, 308, 248, 64, PAPER2, INFO, 1.2)
d.t(440, 334, "보낸 이가 인증·허용 IP인가?", 13, INK, fam=KR, weight=600)
d.t(440, 354, "SMTP AUTH 또는 발송 허용 대역", 12, MUTED, fam=KR)

# 판정 2 -> 오른쪽 분기 ("예" -> 다음 MX 중계)
d.arrow([(564, 340), (600, 340)], INFO, "info", 1.4)
d.t(582, 328, "예", 12, INFO, fam=KR, anchor="middle", weight=600)

# 오른쪽 결과 상자: 다음 MX로 중계 (INFO)
d.box(600, 308, 216, 64, PAPER2, INFO, 1.2)
d.t(708, 334, "다음 MX로 중계 (MTA)", 13, INFO, fam=KR, weight=600)
d.t(708, 354, "외부 전송 (전달 목적)", 12, MUTED, fam=KR)
d.chip(708, 392, "250 OK · 홉 전달", INFO, size=11)

# 판정 2 -> 아래 분기 ("아니오" -> 중계 거절)
d.arrow([(440, 372), (440, 436)], BAD, "bad", 1.4)
d.t(448, 404, "아니오", 12, BAD, fam=KR, anchor="start", weight=600)

# 아래쪽 결과 상자: 중계 거절 및 차단 (BAD)
d.tone(316, 436, 248, 64, BAD, r=6, op="14", sw=1.2)
d.t(440, 462, "중계 거절 (차단)", 13, BAD, fam=KR, weight=600)
d.t(440, 482, "5xx 중계 거부", 12, BAD, fam=KR, weight=600)
d.chip(440, 520, "오픈 릴레이 차단", BAD, size=11)


# ── 범례 (Legend) ──
d.legend(H - 44, [
    ("판정 기준 (focal)", ACC),
    ("로컬 배달 (보관)", OK),
    ("외부 중계 (전달)", INFO),
    ("중계 거절 (차단)", BAD)
])

out = Path(__file__).parent.parent / "01-02.relay-vs-store.svg"
d.save(str(out))
print(f"생성 완료: {out} ({W}x{H})")

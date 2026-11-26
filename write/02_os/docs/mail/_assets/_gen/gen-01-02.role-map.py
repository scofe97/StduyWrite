# 사실 출처: RFC 5598 §4.2-4.3 (Email Architecture), RFC 5321 §2.3.10 (Originator/Delivery/Relay), RFC 6409 §3.1 (Submission)
# 타입 스펙: type-architecture
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W = 960
H = 540

d = D(
    W, H,
    "RFC 5598 EMAIL ARCHITECTURE · ROLE MAP",
    "인터넷 메일의 다섯 역할과 전송·배달 경계",
    "작성자 MUA부터 수신자 MUA까지 메일이 거치는 다섯 역할과 조직 간 중계·최종 배달 구분",
    "RFC 5598 전자메일 아키텍처 및 RFC 5321·6409 표준 프로토콜 규격 기준"
)

# 1. 2개 관리 도메인(ADMD) Zone 영역
def draw_zone(x, y, w, h, label, sub):
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="rgba(245,245,245,0.02)" stroke="{RULE}" stroke-width="0.9"/>')
    d.t(x + 16, y + 24, label, 13, SOFT, fam=KR, weight=600, anchor="start")
    d.t(x + 16, y + 42, sub, 12, MUTED, fam=MONO, anchor="start")

# Zone 1: 발신 관리 도메인 (보내는 조직)
draw_zone(24, 100, 400, 368, "발신 관리 도메인 (ADMD)", "example.com · 제출 및 발신 중계")

# Zone 2: 수신 관리 도메인 (받는 조직)
draw_zone(536, 100, 400, 368, "수신 관리 도메인 (ADMD)", "example.net · 인바운드 수신 및 최종 배달")

# 중앙 공용 인터넷 경계선
d.line(480, 108, 480, 460, RULE, 0.8, dash="4 4")
d.t(480, 136, "공용 인터넷", 13, SOFT, fam=KR, anchor="middle")

# ── [Zone 1] 발신 조직 내부 컴포넌트 ──
# 1. 작성자 MUA
d.box(48, 160, 152, 64, PAPER2, RULE, 1.0)
d.t(124, 186, "작성자 MUA", 14, INK, fam=KR, weight=600)
d.t(124, 206, "메일 작성 및 제출", 13, MUTED, fam=KR)

# 2. MSA (Mail Submission Agent)
d.box(48, 304, 152, 64, PAPER2, OK, 1.2)
d.t(124, 330, "MSA (제출)", 14, OK, fam=KR, weight=600)
d.t(124, 350, "정책 강제 및 검증", 13, MUTED, fam=KR)

# 3. 발신 MTA (Outbound MTA)
d.box(256, 304, 152, 64, PAPER2, INFO, 1.2)
d.t(332, 330, "발신 MTA (중계)", 14, INFO, fam=KR, weight=600)
d.t(332, 350, "DNS MX 질의·전송", 13, MUTED, fam=KR)

# Zone 1 내부 연결
# MUA -> MSA (587 제출)
d.arrow([(124, 224), (124, 304)], OK, "ok", 1.4)
d.t(132, 264, "587 제출 (AUTH)", 12, OK, fam=MONO, anchor="start", weight=600)

# MSA -> 발신 MTA (로컬 큐 전달)
d.arrow([(200, 336), (256, 336)], INFO, "info", 1.4)
d.t(228, 324, "큐 전달", 13, MUTED, fam=KR, anchor="middle")


# ── 조직 간 연결 (공용 인터넷 횡단) ──
# 발신 MTA -> 수신 MTA (25 중계)
d.arrow([(408, 336), (552, 336)], ACC, "acc", 1.8)
d.t(480, 324, "25 중계 (SMTP)", 12, ACC, fam=MONO, anchor="middle", weight=600)


# ── [Zone 2] 수신 조직 내부 컴포넌트 ──
# 4. 수신 MTA / MX
d.box(552, 304, 152, 64, PAPER2, INFO, 1.2)
d.t(628, 330, "수신 MTA / MX", 14, INFO, fam=KR, weight=600)
d.t(628, 350, "외부 25 수신·판정", 13, MUTED, fam=KR)

# 5. MDA (Mail Delivery Agent) - FOCAL POINT
d.tone(760, 304, 152, 64, ACC, op="14", sw=1.4)
d.t(836, 330, "MDA (배달)", 14, ACC, fam=KR, weight=600)
d.t(836, 350, "사서함 배달", 13, MUTED, fam=KR)

# 6. MS (Message Store)
d.box(760, 160, 152, 64, PAPER2, INFO, 1.2)
d.t(836, 186, "MS (메시지 저장소)", 14, INFO, fam=KR, weight=600)
d.t(836, 206, "사서함 보관", 13, MUTED, fam=KR)

# 7. 수신자 MUA
d.box(552, 160, 152, 64, PAPER2, RULE, 1.0)
d.t(628, 186, "수신자 MUA", 14, INK, fam=KR, weight=600)
d.t(628, 206, "메일 열람 및 조회", 13, MUTED, fam=KR)

# Zone 2 내부 연결
# 수신 MTA -> MDA (배달 인계)
d.arrow([(704, 336), (760, 336)], ACC, "acc", 1.4)
d.t(732, 324, "배달 인계", 13, ACC, fam=KR, anchor="middle")

# MDA -> MS (사서함 저장)
d.arrow([(836, 304), (836, 224)], INFO, "info", 1.4)
d.t(844, 264, "사서함 저장", 13, MUTED, fam=KR, anchor="start")

# 수신자 MUA -> MS (IMAP 조회)
d.arrow([(704, 192), (760, 192)], MUTED, "ar", 1.4)
d.t(732, 180, "IMAP", 12, MUTED, fam=MONO, anchor="middle")


# ── 범례 (Legend) ──
d.legend(H - 44, [
    ("최종 배달 책임 (MDA)", ACC),
    ("메일 제출 및 검증 (MSA)", OK),
    ("중계 및 저장소 (MTA / MS)", INFO)
])

out = Path(__file__).parent.parent / "01-02.role-map.svg"
d.save(str(out))
print(f"생성 완료: {out} ({W}x{H})")

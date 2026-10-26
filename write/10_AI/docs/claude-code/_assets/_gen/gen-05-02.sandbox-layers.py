"""커널 격리 계층과 프록시 자격 증명 마스킹 아키텍처.

# 타입 스펙: type-architecture
"""
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent))

from dd import D, ACC, OK, BAD, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 960, 500
d = D(
    W, H,
    "SANDBOX ARCHITECTURE · CREDENTIAL MASKING",
    "커널 격리 계층과 보안 프록시 자격 증명 마스킹 아키텍처",
    "호스트 커널 경계부터 샌드박스 센티널 파일, TLS 보안 프록시의 비밀키 치환 및 외부 통신 통제",
    lead="샌드박스 내부에는 가짜 키를 제공하고, 외부 네트워크 요청 시 보안 프록시가 실제 키로 치환합니다"
)

# 1. 3개 영역 (Zones) — 라벨 배경 rect 없이 text 로만 표시해 겹침 방지
# Zone 1: 호스트 환경
d.box(24, 104, 216, 320, fill="rgba(245,245,243,0.02)", stroke=RULE, sw=0.8, r=8)
d.t(36, 122, "HOST SCOPE", 8, SOFT, MONO, "start")

# Zone 2: 샌드박스 내부
d.box(296, 104, 244, 320, fill="rgba(245,245,243,0.02)", stroke=RULE, sw=0.8, r=8)
d.t(308, 122, "SANDBOX ZONE", 8, SOFT, MONO, "start")

# Zone 3: 보안 프록시 및 네트워크
d.box(600, 104, 336, 320, fill="rgba(245,245,243,0.02)", stroke=RULE, sw=0.8, r=8)
d.t(612, 122, "SECURITY PROXY", 8, SOFT, MONO, "start")

# 2. 노드 정의 함수
def draw_node(x, y, w, h, title, sub, focal=False, is_ok=False, is_bad=False):
    if focal:
        d.tone(x, y, w, h, ACC, r=6, op="14", sw=1.4)
        tc, sc = ACC, INK
    elif is_ok:
        d.tone(x, y, w, h, OK, r=6, op="14", sw=1.2)
        tc, sc = OK, MUTED
    elif is_bad:
        d.tone(x, y, w, h, BAD, r=6, op="14", sw=1.2)
        tc, sc = BAD, MUTED
    else:
        d.box(x, y, w, h, fill=PAPER2, stroke=RULE, sw=1.0, r=6)
        tc, sc = INK, MUTED

    d.t(x + w / 2, y + 25, title, 12.5, tc, KR, "middle", 600)
    if sub:
        fam = MONO if any(c in sub for c in ("~", ":", "*", ".")) else KR
        d.t(x + w / 2, y + 45, sub, 11, sc, fam, "middle")

# 3. 연결 화살표 (Z-order: 노드보다 먼저 그린다)
# Arrow 1: 호스트 자격 증명 (N2) -> 센티널 가짜 사본 (N3)
d.arrow([(236, 168), (300, 168)], MUTED, "ar", 1.4)
d.t(268, 158, "사본 생성", 11, MUTED, KR, "middle")

# Arrow 2: 센티널 가짜 사본 (N3) -> Sandboxed Bash (N4)
d.arrow([(412, 200), (412, 252)], MUTED, "ar", 1.4)
d.t(462, 228, "가짜 키 주입", 11, MUTED, KR, "middle")

# Arrow 3: Sandboxed Bash (N4) -> TLS 보안 프록시 (N5, focal!)
d.path("M 524 284 H 560 Q 568 284 568 276 V 212 Q 568 204 576 204 H 616", ACC, 1.6, m="acc")
d.t(568, 304, "요청 전송", 11, ACC, KR, "middle", 600)

# Arrow 4: 호스트 자격 증명 (N2) -> TLS 보안 프록시 (N5) 실제 비밀키 참조 채널
d.path("M 136 136 V 104 Q 136 98 144 98 H 760 Q 768 98 768 104 V 136", SOFT, 1.2, m="soft", dash="4 3")
d.t(450, 92, "실제 비밀키 바인딩", 11, SOFT, KR, "middle")

# Arrow 5: TLS 보안 프록시 (N5) -> 인가 도메인 전송 (N6)
d.arrow([(768, 204), (768, 252)], OK, "ok", 1.4)
d.t(820, 230, "치환 전송", 11, OK, KR, "middle")

# Arrow 6: TLS 보안 프록시 (N5) -> 비인가 호스트 차단 (N7)
d.path("M 920 170 H 924 Q 932 170 932 178 V 356 Q 932 364 924 364 H 920", BAD, 1.4, m="bad")

# 4. 노드 배치
# Zone 1 노드
draw_node(36, 136, 200, 64, "호스트 자격 증명", "~/.aws/credentials")
draw_node(36, 252, 200, 64, "호스트 커널 격리", "bwrap (Linux·WSL2)")
d.t(136, 340, "macOS (Seatbelt): deny 로 대체", 11, MUTED, KR, "middle")

# Zone 2 노드
draw_node(300, 136, 224, 64, "센티널 가짜 사본", "mode: mask")
draw_node(300, 252, 224, 64, "Sandboxed Bash", "명령 실행 · 가짜 키 사용")

# Zone 3 노드
draw_node(616, 136, 304, 68, "TLS 보안 프록시 · 실제 키 치환", "tlsTerminate 필요 · env 쌍은 SigV4 재서명", focal=True)
draw_node(616, 252, 304, 60, "인가 도메인 전송", "allowedDomains", is_ok=True)
draw_node(616, 336, 304, 56, "비인가 호스트 차단", "deniedDomains", is_bad=True)

# 범례
d.legend(440, [
    ("마스킹 치환 (focal)", ACC),
    ("인가 전송", OK),
    ("비인가 차단", BAD),
    ("비밀키 바인딩", SOFT),
])

d.save("05-02.sandbox-layers.svg")

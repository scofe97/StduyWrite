# 사실 출처: Tomcat 11.0.24 ManagerBase L147·StandardSession L112 · Spring Security 7.1.1 SessionRegistryImpl L56-L59·HttpSessionSecurityContextRepository L92·SecurityContextHolder · 별도 JVM 관찰
# 타입 스펙: type-architecture
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 880, 568
d = D(
    W, H,
    "ARCHITECTURE · WHO HOLDS WHAT",
    "세션 정보를 나눠 들고 있는 네 곳",
    "브라우저는 ID 하나, Tomcat 은 데이터 묶음, SessionRegistry 는 ID 장부, SecurityContextHolder 는 요청 하나 동안의 참조",
    "ID 문자열이 곳곳을 잇고 SecurityContext 객체는 Tomcat 과 스레드가 같은 것을 가리킴"
)

ZY, ZH = 100, 372


def zone(x, w, label):
    d.o.append(f'<rect x="{x}" y="{ZY}" width="{w}" height="{ZH}" rx="8" fill="rgba(245,245,245,0.02)" stroke="{RULE}" stroke-width="0.9"/>')
    d.t(x + 14, ZY + 24, label, 12, SOFT, KR, "start", 600)


def node(x, cy, w, title, sub, c=RULE, focal=False):
    if focal:
        d.tone(x, cy - 28, w, 56, ACC, op="12", sw=1.4)
    else:
        d.box(x, cy - 28, w, 56, PAPER2, c, 1.1)
    d.t(x + w / 2, cy - 4, title, 12, INK, MONO, "middle", 600)
    d.t(x + w / 2, cy + 15, sub, 12, MUTED, KR if any("가" <= ch <= "힣" for ch in sub) else MONO)


zone(24, 160, "브라우저")
zone(240, 280, "JVM 메모리 · Tomcat")
zone(600, 256, "JVM 메모리 · Spring Security")

C1, C2, C3, C4 = 156, 246, 336, 426
BX, BW = 40, 128      # 브라우저 노드
TX, TW = 256, 248     # Tomcat 노드
SX, SW = 614, 228     # Spring 노드

# 연결선 먼저
d.arrow([(BX + BW, C1), (TX - 2, C1)], MUTED, "ar", 1.5)                  # 쿠키 → sessions
for a, b in ((C1, C2), (C2, C3), (C3, C4)):
    d.arrow([(TX + TW / 2, a + 28), (TX + TW / 2, b - 30)], MUTED, "ar", 1.4)
d.arrow([(SX + SW / 2, C1 + 28), (SX + SW / 2, C2 - 30)], WARN, "warn", 1.3)   # principals → sessionIds
d.arrow([(SX + SW / 2, C2 + 28), (SX + SW / 2, C3 - 30)], WARN, "warn", 1.3)   # sessionIds → SessionInformation
d.path(f"M {SX-2} {C2} L {TX+TW+2} {C2}", WARN, 1.3, dash="4 4")                # sessionIds ··· StandardSession (같은 ID)
d.arrow([(TX + TW, C4), (SX - 2, C4)], ACC, "acc", 1.6)                         # context → holder

# 브라우저
node(BX, C1, BW, "JSESSIONID", "ID 문자열 하나", INFO)
node(BX, C2, BW, "XSRF-TOKEN", "세션 아님", RULE)

# Tomcat
node(TX, C1, TW, "StandardManager.sessions", "ID → StandardSession", INFO)
node(TX, C2, TW, "StandardSession", "ID · 마지막 접근 · 유효 시간", INFO)
node(TX, C3, TW, "attributes", "이름 → 객체", INFO)
node(TX, C4, TW, "SPRING_SECURITY_CONTEXT", "SecurityContext → LoginUser", ACC, focal=True)

# Spring
node(SX, C1, SW, "principals", "userId → {ID, ID}", WARN)
node(SX, C2, SW, "sessionIds", "ID → SessionInformation", WARN)
node(SX, C3, SW, "SessionInformation", "principal · expired · 시각", INFO)
node(SX, C4, SW, "SecurityContextHolder", "ThreadLocal · 요청 스레드", INFO)

# 화살표 라벨
d.t((BX + BW + TX) / 2, C1 - 10, "Cookie", 12, MUTED, MONO)
d.t((TX + TW + SX) / 2, C2 - 10, "같은 ID", 12, WARN, KR)
d.t((TX + TW + SX) / 2, C4 - 10, "같은 객체", 12, ACC, KR)
d.t(SX + SW / 2 + 10, (C1 + C2) / 2 + 4, "ID 목록", 12, WARN, KR, "start")
d.t(SX + SW / 2 + 10, (C2 + C3) / 2 + 4, "값", 12, WARN, KR, "start")

d.legend(H - 60, [
    ("SecurityContext 가 사는 칸 (핵심)", ACC),
    ("ID 를 키로 쓰는 장부", WARN),
    ("데이터 구조", INFO),
])

out_path = Path(__file__).parent.parent / "01-02.four-places.svg"
d.save(str(out_path))
print(f"생성 완료: {out_path}")

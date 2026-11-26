# 사실 출처: Tomcat 11.0.24 ManagerBase L147·StandardSession L112 · Spring Security 7.1.1 HttpSessionSecurityContextRepository L92·L213 · 별도 JVM 관찰
# 타입 스펙: type-process
# 고른 이유: 쿠키 ID 하나가 맵 둘과 객체 둘을 차례로 거쳐 사용자까지 가는 순서가 논지라 주체별 단계 파이프라인을 쓴다.
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 880, 500
d = D(
    W, H,
    "PROCESS · ONE ID TO ONE USER",
    "쿠키의 ID 하나가 로그인 사용자까지 가는 길",
    "JSESSIONID 문자열이 sessions 맵, 속성 맵, SecurityContext 를 차례로 거쳐 LoginUser 에 닿는다",
    "한 요청 안에서 Tomcat 과 Spring 이 이어 하는 조회 네 번"
)

BW, GAP, X0 = 184, 32, 24
BY, BH = 150, 132
steps = [
    ("브라우저", "Cookie 헤더", "JSESSIONID=", "92ECBC8A…", INFO),
    ("Tomcat 관리자", "sessions.get(ID)", "ID → ", "StandardSession", INFO),
    ("Tomcat 세션", "attributes.get(이름)", "속성 이름 →", "SPRING_SECURITY_CONTEXT", INFO),
    ("Spring 컨텍스트", "getPrincipal()", "Authentication → ", "LoginUser", ACC),
]


def sx(i):
    return X0 + i * (BW + GAP)


# 연결선 먼저
for i in range(3):
    d.arrow([(sx(i) + BW, BY + 66), (sx(i + 1) - 2, BY + 66)], MUTED, "ar", 1.6)

for i, (who, call, v1, v2, c) in enumerate(steps):
    x = sx(i)
    d.t(x + BW / 2, BY - 18, who, 12, SOFT, KR, "middle", 600)
    if c == ACC:
        d.tone(x, BY, BW, BH, ACC, op="12", sw=1.4)
    else:
        d.box(x, BY, BW, BH, PAPER2, c, 1.1)
    d.t(x + BW / 2, BY + 30, call, 12, INK, MONO, "middle", 600)
    d.line(x + 14, BY + 46, x + BW - 14, BY + 46, RULE, 0.8)
    d.t(x + BW / 2, BY + 78, v1, 12, MUTED, MONO)
    d.t(x + BW / 2, BY + 100, v2, 11 if len(v2) > 18 else 12, INK, MONO, "middle", 600)

# 아래 줄: 단계마다 무엇이 바뀌는지
cap = [
    "문자열 하나",
    "맵의 키로 사용",
    "속성 이름으로 조회",
    "객체 안의 주체",
]
for i, t in enumerate(cap):
    d.t(sx(i) + BW / 2, BY + BH + 28, t, 12, MUTED, KR)

# 실패 갈래
d.path(f"M {sx(1) + BW/2} {BY + BH + 44} L {sx(1) + BW/2} {BY + BH + 72}", BAD, 1.3, m="bad", dash="4 4")
d.tone(sx(1) - 20, BY + BH + 74, BW + 40, 44, BAD)
d.t(sx(1) + BW / 2, BY + BH + 93, "ID 가 맵에 없음", 12, BAD, KR, "middle", 600)
d.t(sx(1) + BW / 2, BY + BH + 110, "세션 없음 · 익명 요청", 12, MUTED, KR)

d.legend(H - 40, [
    ("마지막 단계 (핵심)", ACC),
    ("조회 · 데이터 구조", INFO),
    ("실패", BAD),
])

out_path = Path(__file__).parent.parent / "01-02.lookup-path.svg"
d.save(str(out_path))
print(f"생성 완료: {out_path}")

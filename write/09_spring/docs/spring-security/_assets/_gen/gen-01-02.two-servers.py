# 사실 출처: Tomcat 11.0.24 ManagerBase L147 · Spring Security 7.1.1 SessionRegistryImpl L56-L59
# 타입 스펙: type-deployment
# 고른 이유: 같은 맵 구조가 서버 두 대에 각각 따로 있다는 배치가 논지라 존과 복제본을 보이는 배치 타입을 쓴다.
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 880, 560
d = D(
    W, H,
    "DEPLOYMENT · TWO SERVERS, TWO MEMORIES",
    "서버가 두 대가 되면 세션이 갈라지는 모습",
    "A 서버에서 만든 세션 ID 는 B 서버의 맵에 없어서 다음 요청이 B 로 가면 로그인이 풀린다",
    "각 서버는 자기 JVM 메모리의 sessions 맵과 장부만 안다"
)


def zone(x, y, w, h, label, c=RULE):
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="rgba(245,245,245,0.02)" stroke="{c}" stroke-width="0.9"/>')
    d.t(x + 14, y + 24, label, 12, SOFT, KR, "start", 600)


def node(x, y, w, h, title, sub, c):
    d.box(x, y, w, h, PAPER2, c, 1.1)
    d.t(x + w / 2, y + 20, title, 12, INK, MONO, "middle", 600)
    d.t(x + w / 2, y + 38, sub, 12, MUTED, KR if any("가" <= ch <= "힣" for ch in sub) else MONO)


zone(320, 100, 360, 176, "서버 A · JVM 메모리")
zone(320, 316, 360, 176, "서버 B · JVM 메모리", BAD)

# 연결선
d.arrow([(184, 222), (256, 222), (256, 168), (318, 168)], OK, "ok", 1.6)          # 1. 로그인 → A
d.arrow([(184, 258), (256, 258), (256, 384), (318, 384)], BAD, "bad", 1.6)        # 2. 다음 요청 → B
d.arrow([(682, 404), (710, 404)], BAD, "bad", 1.6)                                 # B → 401

# 브라우저
d.box(24, 200, 160, 80, PAPER2, INFO, 1.2)
d.t(104, 226, "브라우저", 12, INK, KR, "middle", 600)
d.t(104, 248, "쿠키 JSESSIONID", 11, MUTED, MONO)
d.t(104, 266, "= ID1", 11, INK, MONO, "middle", 600)

# 서버 A
node(336, 134, 156, 56, "sessions", "{ID1}", INFO)
node(508, 134, 156, 56, "장부", "{ID1}", WARN)
node(336, 204, 328, 56, "응답", "Set-Cookie: JSESSIONID=ID1", OK)
# 서버 B
node(336, 350, 156, 56, "sessions", "{ }", BAD)
node(508, 350, 156, 56, "장부", "{ }", BAD)
d.tone(336, 420, 328, 56, BAD)
d.t(500, 442, "ID1 을 모름 · 세션 없음", 12, BAD, KR, "middle", 600)
d.t(500, 462, "expireAll 표시도 A 의 장부에만 있음", 12, MUTED, KR)

# 결과
d.tone(712, 376, 144, 56, BAD)
d.t(784, 400, "401", 12, BAD, MONO, "middle", 600)
d.t(784, 418, "다시 로그인", 12, MUTED, KR)

# 화살표 라벨
d.t(200, 206, "1. 로그인", 12, OK, KR, "start", 600)
d.t(246, 304, "2. 다음 요청", 12, BAD, KR, "end", 600)

d.legend(H - 48, [
    ("세션이 갈라지는 지점 (핵심)", BAD),
    ("정상", OK),
    ("맵 · 구조", INFO),
    ("장부", WARN),
])

out_path = Path(__file__).parent.parent / "01-02.two-servers.svg"
d.save(str(out_path))
print(f"생성 완료: {out_path}")

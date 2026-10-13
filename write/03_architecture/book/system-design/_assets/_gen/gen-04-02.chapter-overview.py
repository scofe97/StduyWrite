# 타입 스펙: type-process — 절 일곱을 카드 슬롯(절 번호·이름·핵심 값)으로 두 줄에 늘어놓고 화살표가 읽는 순서를 나른다. focal 은 §4.
# 사실 출처: 추출본 v2.txt 1127~1296행(개략 구조 1127 · 규칙 1156 · 한도 초과 1177 · 분산 환경 1207 · 성능 1250 · 모니터링 1261 · 마무리 1270),
#   Redis INCR 문서(https://redis.io/docs/latest/commands/incr/), RFC 6585 §4, RFC 9110 §10.2.3.
# Layout conventions: 카드 폭 208·높이 124, x stride 232(24·256·488·720), 줄 stride 172(y=104·276). 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, MUTED, INK, SOFT, PAPER2, RULE, KR, MONO

W, H = 960, 484
d = D(W, H, "SYSTEM DESIGN INTERVIEW · 04-02",
      "처리율 제한 미들웨어를 일곱 절로 읽는다",
      "카운터를 세는 구조에서 출발해 규칙·거절 응답을 거쳐 경쟁 조건과 동기화를 풀고 성능·감시·남은 선택으로 닫는다.",
      "카운터 하나가 요청 하나에 어떻게 닿는지에서 여러 서버가 그 카운터를 같이 고치는 문제까지")

CW, CH = 208, 124
XS = (24, 256, 488, 720)
YS = (104, 276)
CARDS = (
    ("§1", "Redis 카운터", "INCR · EXPIRE", INFO),
    ("§2", "규칙 파일", "domain · key · value", INFO),
    ("§3", "거절 응답", "429 · Retry-After", INFO),
    ("§4", "경쟁 조건", "3 → 4 · 정답 5", ACC),
    ("§5", "카운터 공유", "3 + 3 = 6 > 5", INFO),
    ("§6", "지연과 감시", "엣지 · shadow_mode", INFO),
    ("§7", "남은 선택", "경성 · 연성 · L3 · L7", INFO),
)


def fam(t):
    return KR if any("가" <= ch <= "힣" for ch in t) else MONO


pos = []
for i, (tag, title, val, c) in enumerate(CARDS):
    row, col = (0, i) if i < 4 else (1, i - 4)
    x, y = XS[col], YS[row]
    pos.append((x, y))
    d.tone(x, y, CW, CH, c, 6, "12", 1.4 if c == ACC else 1.0)
    d.t(x + 14, y + 28, tag, 12, c, MONO, "start", 600)
    d.t(x + 14, y + 64, title, 16, INK, KR, "start", 600)
    d.t(x + 14, y + 100, val, 12, MUTED, fam(val), "start")

for i in range(6):
    if i == 3:
        continue
    x, y = pos[i]
    d.arrow([(x + CW + 2, y + 62), (pos[i + 1][0] - 6, y + 62)], MUTED, "ar", 1.5)
# 첫 줄 끝 카드에서 둘째 줄 첫 카드로 내려가는 읽기 순서
d.arrow([(pos[3][0] + CW // 2, YS[0] + CH + 4), (pos[3][0] + CW // 2, 252), (pos[4][0] + CW // 2, 252), (pos[4][0] + CW // 2, YS[1] - 4)], MUTED, "ar", 1.5)

d.legend(H - 56, [("절", INFO), ("가장 중심인 절", ACC)])
d.save("04-02.chapter-overview.svg")

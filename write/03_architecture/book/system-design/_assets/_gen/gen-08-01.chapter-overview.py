# 타입 스펙: type-process — 절 일곱을 카드 슬롯(절 번호·이름·핵심 값)으로 두 줄에 늘어놓고 화살표가 읽는 순서를 나른다. focal 은 §5.
# 사실 출처: 추출본 v2.txt 2100~2108행(추정 수치)·2125~2146행(API·301·302)·2176~2183행(62^7)·2187~2209행(해시+충돌 해소·블룸 필터)·2210~2231행(base62, 11157 → 2TX)·2238~2278행(두 흐름)·2279~2295행(확장),
#   계산: 100 M ÷ 86,400 = 1,157 ≈ 1,160 · 365 B × 100 B = 36.5 TB · 62^7 = 3,521,614,606,208.
# Layout conventions: 카드 폭 208·높이 124, x stride 232(24·256·488·720), 줄 stride 172(y=104·276). 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, MUTED, INK, KR, MONO

W, H = 960, 484
d = D(W, H, "SYSTEM DESIGN INTERVIEW · 08-01",
      "URL 단축기를 일곱 절로 읽는다",
      "규모 추정에서 키 길이를 정하고, 키를 만드는 두 방식을 견준 뒤, 단축과 리디렉션 두 흐름으로 이어 확장 주제로 닫는다.",
      "숫자 → 키 길이 → 두 방식 → 두 흐름")

CW, CH = 208, 124
XS = (24, 256, 488, 720)
YS = (104, 276)
CARDS = (
    ("§1", "규모 추정", "1,160 QPS · 36.5 TB", INFO),
    ("§2", "API 와 리디렉션", "POST · GET · 301 · 302", INFO),
    ("§3", "키 길이", "62^7 ≈ 3.5 조", INFO),
    ("§4", "해시 + 충돌 해소", "CRC32 · 블룸 필터", INFO),
    ("§5", "base62 변환", "11157 → 2TX", ACC),
    ("§6", "두 흐름", "zn9edcu · 302", INFO),
    ("§7", "확장", "제한기 · 복제 · 샤딩", INFO),
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
d.arrow([(pos[3][0] + CW // 2, YS[0] + CH + 4), (pos[3][0] + CW // 2, 252), (pos[4][0] + CW // 2, 252), (pos[4][0] + CW // 2, YS[1] - 4)], MUTED, "ar", 1.5)

d.legend(H - 56, [("절", INFO), ("가장 중심인 절", ACC)])
d.save("08-01.chapter-overview.svg")

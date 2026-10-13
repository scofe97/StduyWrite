# 타입 스펙: type-process — 절 일곱을 카드 슬롯(절 번호·이름·핵심 값)으로 두 줄에 늘어놓고 화살표가 읽는 순서를 나른다. focal 은 §5.
# 사실 출처: 추출본 v2.txt 2707~2709행(푸시 1,000 만·SMS 100 만·이메일 500 만)·2716~2754행(알림 유형)·2756~2771행(연락처 표)·2795~2803행(단일 서버 문제 셋)·2804~2840행(큐·작업자 여섯 단계)·2849~2870행(유실·중복)·2871~2933행(부가 기능),
#   계산: 16,000,000 ÷ 86,400 = 185.2.
# Layout conventions: 카드 폭 208·높이 124, x stride 232(24·256·488·720), 줄 stride 172(y=104·276). 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, MUTED, INK, KR, MONO

W, H = 960, 484
d = D(W, H, "SYSTEM DESIGN INTERVIEW · 10-01",
      "알림 시스템을 일곱 절로 읽는다",
      "규모와 전달 경로를 정하고, 주소를 모아 두고, 서버 한 대의 한계를 큐와 작업자로 나눈 뒤 유실과 중복을 다루고 부가 기능으로 닫는다.",
      "숫자 → 전달 경로 → 주소 → 한계 → 큐 → 유실·중복 → 부가")

CW, CH = 208, 124
XS = (24, 256, 488, 720)
YS = (104, 276)
CARDS = (
    ("§1", "요구사항", "1,600 만 건 · 185 QPS", INFO),
    ("§2", "전달 경로", "APNs · FCM · SMS · 이메일", INFO),
    ("§3", "주소 저장", "user 표 · device 표", INFO),
    ("§4", "서버 한 대의 한계", "SPOF · 확장 · 병목", INFO),
    ("§5", "큐와 작업자", "큐 4 개 · 6 단계", ACC),
    ("§6", "유실과 중복", "알림 로그 · 이벤트 ID", INFO),
    ("§7", "부가 기능", "설정 · 제한 · 재시도", INFO),
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
    d.t(x + 14, y + 100, val, 13 if fam(val) == KR else 12, MUTED, fam(val), "start")

for i in range(6):
    if i == 3:
        continue
    x, y = pos[i]
    d.arrow([(x + CW + 2, y + 62), (pos[i + 1][0] - 6, y + 62)], MUTED, "ar", 1.5)
d.arrow([(pos[3][0] + CW // 2, YS[0] + CH + 4), (pos[3][0] + CW // 2, 252), (pos[4][0] + CW // 2, 252), (pos[4][0] + CW // 2, YS[1] - 4)], MUTED, "ar", 1.5)

d.legend(H - 56, [("절", INFO), ("가장 중심인 절", ACC)])
d.save("10-01.chapter-overview.svg")

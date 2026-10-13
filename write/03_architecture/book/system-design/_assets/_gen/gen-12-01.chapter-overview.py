# 타입 스펙: type-process — 절 아홉을 카드 슬롯(절 번호·이름·핵심 값)으로 두 줄에 늘어놓고 화살표가 읽는 순서를 나른다. focal 은 §7.
# 사실 출처: 추출본 v2.txt 3166~3200행(범위: 5,000 만 명·그룹 100 명)·3234~3269행(폴링·롱 폴링·웹소켓)·3270~3323행(서비스 세 부류)·3324~3366행(저장소·표)·3367~3381행(메시지 ID)·3386~3400행(서비스 탐색)·3401~3449행(메시지 흐름)·3450~3500행(접속 상태)·3501~3526행(마무리).
# Layout conventions: 카드 폭 168·높이 124, x stride 192(24·216·408·600·792), 줄 stride 172(y=104·276). 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, MUTED, INK, KR, MONO

W, H = 1000, 484
d = D(W, H, "SYSTEM DESIGN INTERVIEW · 12-01",
      "채팅 시스템을 아홉 절로 읽는다",
      "범위를 정하고 전달 방식과 서버 부류와 저장소를 고른 뒤, ID 와 탐색과 흐름과 상태로 이어 간다.",
      "범위 → 전달 → 서버 → 저장 → ID → 탐색 → 흐름 → 상태 → 확장")

CW, CH = 168, 124
XS = (24, 216, 408, 600, 792)
YS = (104, 276)
CARDS = (
    ("§1", "요구사항", "5,000 만 · 100 명", INFO),
    ("§2", "전달 방식", "웹소켓 선택", INFO),
    ("§3", "서버 세 부류", "무상태 · 상태 유지", INFO),
    ("§4", "저장소와 키", "키-값 · 표 둘", INFO),
    ("§5", "메시지 ID", "전역 · 지역", INFO),
    ("§6", "서비스 탐색", "ZooKeeper", INFO),
    ("§7", "메시지 흐름", "큐 · 수신함", ACC),
    ("§8", "접속 상태", "5 초 · 30 초", INFO),
    ("§9", "확장 주제", "암호화 · 캐시", INFO),
)


def fam(t):
    return KR if any("가" <= ch <= "힣" for ch in t) else MONO


pos = []
for i, (tag, title, val, c) in enumerate(CARDS):
    row, col = (0, i) if i < 5 else (1, i - 5)
    x, y = XS[col], YS[row]
    pos.append((x, y))
    d.tone(x, y, CW, CH, c, 6, "12", 1.4 if c == ACC else 1.0)
    d.t(x + 14, y + 28, tag, 12, c, MONO, "start", 600)
    d.t(x + 14, y + 64, title, 16, INK, KR, "start", 600)
    d.t(x + 14, y + 100, val, 13 if fam(val) == KR else 12, MUTED, fam(val), "start")

for i in range(8):
    if i == 4:
        continue
    x, y = pos[i]
    d.arrow([(x + CW + 2, y + 62), (pos[i + 1][0] - 6, y + 62)], MUTED, "ar", 1.5)
d.arrow([(pos[4][0] + CW // 2, YS[0] + CH + 4), (pos[4][0] + CW // 2, 252), (pos[5][0] + CW // 2, 252), (pos[5][0] + CW // 2, YS[1] - 4)], MUTED, "ar", 1.5)

d.legend(H - 56, [("절", INFO), ("가장 중심인 절", ACC)])
d.save("12-01.chapter-overview.svg")

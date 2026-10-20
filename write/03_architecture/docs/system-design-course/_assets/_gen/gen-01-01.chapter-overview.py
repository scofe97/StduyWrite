# 타입 스펙: type-process — 절 여섯을 카드 슬롯(절 번호·이름·핵심 값)으로 두 줄에 늘어놓고 화살표가 읽는 순서를 나른다. focal 은 §2.
# 사실 출처: 본문 01-01.md §1~§6(목차 및 핵심 수치), 요약 §3.1~§3.13, 도식 값 표(1,000 QPS/17 TPS, 날짜 행·상한 110, reservation_id, 109→111, 대기·재시도·영향 행, 캐시 DEL·CDC).
# Layout conventions: 캔버스 960×480, 카드 폭 272·높이 116, x = 48·344·640, y = 108·268. 모든 좌표 4의 배수.
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from dd import D, ACC, INFO, MUTED, INK, KR, MONO

W, H = 960, 480
d = D(
    W, H,
    "SYSTEM DESIGN COURSE · 01-01",
    "호텔 예약 시스템을 여섯 절로 읽는다",
    "읽기와 쓰기를 분리하고 날짜별 재고 행과 멱등 키를 설계한 뒤, 격리 수준 한계를 짚고 세 동시성 해법과 캐시·색인 전파로 완성합니다.",
    "용량 분리 → 날짜 재고 모델 → 멱등 키 → 경쟁 조건 → 세 해법 → 캐시·색인 전파"
)

CW, CH = 272, 116
XS = (48, 344, 640)
YS = (108, 268)

CARDS = (
    ("§1", "읽기·쓰기 분리", "1,000 QPS · 17 TPS", INFO),
    ("§2", "날짜별 재고 행", "날짜 행 · 상한 110", ACC),
    ("§3", "멱등 키 재전송", "reservation_id", INFO),
    ("§4", "격리 수준 한계", "109 → 111 초과", INFO),
    ("§5", "동시성 세 해법", "대기 · 재시도 · 영향 행", INFO),
    ("§6", "캐시와 색인 전파", "캐시 DEL · CDC", INFO),
)


def fam(t):
    return KR if any("가" <= ch <= "힣" for ch in t) else MONO


pos = []
for i, (tag, title, val, c) in enumerate(CARDS):
    row, col = (0, i) if i < 3 else (1, i - 3)
    x, y = XS[col], YS[row]
    pos.append((x, y))
    d.tone(x, y, CW, CH, c, 6, "14", 1.4 if c == ACC else 1.0)
    d.t(x + 16, y + 28, tag, 12, c, MONO, "start", 600)
    d.t(x + 16, y + 64, title, 16, INK, KR, "start", 600)
    d.t(x + 16, y + 96, val, 13, MUTED, fam(val), "start")

# 1줄 수평 화살표 (§1 -> §2, §2 -> §3)
d.arrow([(XS[0] + CW + 2, YS[0] + 58), (XS[1] - 6, YS[0] + 58)], MUTED, "ar", 1.5)
d.arrow([(XS[1] + CW + 2, YS[0] + 58), (XS[2] - 6, YS[0] + 58)], MUTED, "ar", 1.5)

# 줄바꿈 ㄷ자 화살표 (§3 -> §4)
cx_end = XS[2] + CW // 2
cx_start = XS[0] + CW // 2
y_mid = 246
d.arrow([
    (cx_end, YS[0] + CH + 4),
    (cx_end, y_mid),
    (cx_start, y_mid),
    (cx_start, YS[1] - 6)
], MUTED, "ar", 1.5)

# 2줄 수평 화살표 (§4 -> §5, §5 -> §6)
d.arrow([(XS[0] + CW + 2, YS[1] + 58), (XS[1] - 6, YS[1] + 58)], MUTED, "ar", 1.5)
d.arrow([(XS[1] + CW + 2, YS[1] + 58), (XS[2] - 6, YS[1] + 58)], MUTED, "ar", 1.5)

d.legend(432, [("절 카드", INFO), ("핵심 도메인 모델 (focal)", ACC)])

out_path = Path(__file__).parent.parent / "01-01.chapter-overview.svg"
d.save(str(out_path))
print(f"saved: {out_path}")

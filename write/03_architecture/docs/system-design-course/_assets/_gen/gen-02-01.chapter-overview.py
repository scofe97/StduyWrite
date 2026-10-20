# 타입 스펙: type-process — 절 여섯을 2행 3열 카드 슬롯(절 번호·이름·핵심 값)으로 배열하고 직각 화살표로 읽는 순서를 연결한다. focal 은 §4 로컬 Outbox.
# 사실 출처: 요약 §4.4·§4.7·§4.10·§4.13·§4.18·§4.20, 조사 보고서 행 1~22, 본문 02-01 전체 구조(§1 유실 지점 3곳, §2 DB 선영속과 Redis 폴백, §3 Kafka ISR 리더 선출, §4 메모리 버퍼 10만과 로컬 WAL, §5 메시지 1001 과 Cassandra upsert, §6 비용과 잔여 유실 한계).
# Layout conventions: 카드 폭 280, 높이 132, 2행 3열(XS: 24·340·656, YS: 112·280). 모든 좌표 4의 배수. 화살표는 수평·수직 직각만.
import pathlib
import sys

ASSETS_DIR = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ASSETS_DIR))
from dd import D, ACC, INFO, INK, KR, MONO, MUTED, RULE

W, H = 960, 480
d = D(
    W,
    H,
    "SYSTEM DESIGN COURSE · 02-01",
    "메시징 장애 복원력을 여섯 절로 읽는다",
    "확인 응답과 영속화 사이의 틈을 방어하고 Redis 와 Kafka 장애를 대체 저장소로 흡수하는 여섯 단계 구조.",
    "유실 지점 3곳 → DB 선영속 → ISR 리더 선출 → 로컬 Outbox → Cassandra 업서트 → 잔여 한계",
)

CW, CH = 280, 132
XS = (24, 340, 656)
YS = (112, 280)

CARDS = [
    ("§1", "정상 경로와 유실 지점", "전송 확인 · 비동기 틈", "유실 지점 세 곳", INFO, False),
    ("§2", "수신함 DB 선영속", "delivered IS NULL", "Redis 장애 시 DB 폴백", INFO, False),
    ("§3", "Kafka ISR 리더 선출", "RF=3 · min.isr=2", "acks=all 무유실 보장", INFO, False),
    ("§4", "로컬 Outbox WAL", "상한 100,000건", "SSD fsync 로 브로커 격리", ACC, True),
    ("§5", "Cassandra 멱등 업서트", "메시지 1001 · 50ms", "단일 파티션 묶음 쓰기", INFO, False),
    ("§6", "비용과 잔여 유실 한계", "2회 쓰기 · 지연 증가", "디스크 고갈 · 물리 파손", INFO, False),
]


def fam(t):
    return KR if any("가" <= ch <= "힣" for ch in t) else MONO


pos = []
for i, (tag, title, val1, val2, c, focal) in enumerate(CARDS):
    row, col = (0, i) if i < 3 else (1, i - 3)
    x, y = XS[col], YS[row]
    pos.append((x, y))

    d.tone(x, y, CW, CH, c, 6, "14" if focal else "08", 1.4 if focal else 1.0)
    d.chip(x + 36, y + 26, tag, c, 12, 6)
    d.t(x + 68, y + 30, title, 15, INK, KR, "start", 600)
    d.line(x + 16, y + 54, x + CW - 16, y + 54, c if focal else RULE, 0.8)
    d.t(x + 20, y + 80, val1, 13, INK if focal else c, fam(val1), "start", 600)
    d.t(x + 20, y + 108, val2, 12, MUTED, fam(val2), "start")

# Row 0 수평 연결
d.arrow([(pos[0][0] + CW + 4, pos[0][1] + CH // 2), (pos[1][0] - 4, pos[1][1] + CH // 2)], MUTED, "ar", 1.4)
d.arrow([(pos[1][0] + CW + 4, pos[1][1] + CH // 2), (pos[2][0] - 4, pos[2][1] + CH // 2)], MUTED, "ar", 1.4)

# Row 0 Card 2 -> Row 1 Card 3 (직각 우회 연결)
c2_cx = pos[2][0] + CW // 2
c3_cx = pos[3][0] + CW // 2
mid_y = (YS[0] + CH + YS[1]) // 2  # 262
d.arrow(
    [(c2_cx, YS[0] + CH + 4), (c2_cx, mid_y), (c3_cx, mid_y), (c3_cx, YS[1] - 4)],
    MUTED,
    "ar",
    1.4,
)

# Row 1 수평 연결
d.arrow([(pos[3][0] + CW + 4, pos[3][1] + CH // 2), (pos[4][0] - 4, pos[4][1] + CH // 2)], MUTED, "ar", 1.4)
d.arrow([(pos[4][0] + CW + 4, pos[4][1] + CH // 2), (pos[5][0] - 4, pos[5][1] + CH // 2)], MUTED, "ar", 1.4)

d.legend(H - 44, [("절", INFO), ("가장 중심인 절 (Outbox)", ACC)])

out_path = str(ASSETS_DIR / "02-01.chapter-overview.svg")
d.save(out_path)
print(f"saved: {out_path}")

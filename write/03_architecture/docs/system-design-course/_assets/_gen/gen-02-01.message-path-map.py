# 타입 스펙: type-architecture — 존으로 묶은 컴포넌트 맵에 번호 붙은 직각 화살표로 메시지 정상 경로와 3대 유실 지점(✕)을 배치한다. focal 은 Cassandra 영속 저장소.
# 사실 출처: 요약 §4.4·§4.10, 조사 보고서 행 1·2·3·10, 본문 1절(발신자 앱 → 채팅 서버 → sent 확인 후 비동기 발행, 온라인 수신자 Redis 조회 후 채팅 서버 B 전달, 오프라인 수신함 및 푸시 알림, Kafka 파티션 → 저장 서비스 → Cassandra, 유실 지점 1·2·3).
# Layout conventions: 3개 계층 존(실시간 라우팅·오프라인 수신함·영속화 파이프라인), W=960, H=560. 모든 노드와 화살표 좌표 4의 배수. 연결선은 수평·수직 직각만 허용.
import pathlib
import sys

ASSETS_DIR = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ASSETS_DIR))
from dd import D, ACC, BAD, INFO, INK, KR, MONO, MUTED, OK, RULE, SOFT, WARN

W, H = 960, 560
d = D(
    W,
    H,
    "SYSTEM DESIGN COURSE · 02-01 §1",
    "메시지 정상 전달 경로와 유실 지점 세 곳",
    "발신자 전송 확인 후 브로커와 캐시와 영속 계층의 이음매에서 생기는 유실 창과 두 갈래 전달 경로.",
    "정상 전달 번호 ①~⑦ · 유실 지점 ✕ 3곳(채팅 서버 크래시 · Redis 비동기 복제 · 컨슈머 커밋 틈)",
)


def fam(t):
    return KR if any("가" <= ch <= "힣" for ch in t) else MONO


# -------------------------------------------------------------
# 1. 3개 존 (Zone Rects)
# -------------------------------------------------------------
# Zone 1: 실시간 라우팅 계층
z1_x, z1_y, z1_w, z1_h = 176, 96, 608, 116
d.box(z1_x, z1_y, z1_w, z1_h, "#12171F", RULE, 0.8, 8)
d.t(z1_x + 16, z1_y + 18, "ROUTING & REALTIME TIER", 8, SOFT, MONO, "start")

# Zone 2: 오프라인 수신함 및 푸시 계층
z2_x, z2_y, z2_w, z2_h = 348, 232, 436, 120
d.box(z2_x, z2_y, z2_w, z2_h, "#12171F", RULE, 0.8, 8)
d.t(z2_x + 16, z2_y + 18, "OFFLINE INBOX & NOTIFICATION", 8, SOFT, MONO, "start")

# Zone 3: 메시지 영속화 계층
z3_x, z3_y, z3_w, z3_h = 176, 368, 764, 120
d.box(z3_x, z3_y, z3_w, z3_h, "#12171F", RULE, 0.8, 8)
d.t(364, z3_y + 18, "PERSISTENCE & BROKER PIPELINE", 8, SOFT, MONO, "start")


# -------------------------------------------------------------
# 2. 노드 박스 함수
# -------------------------------------------------------------
def node_box(x, y, w, h, title, sub, c, focal=False):
    d.tone(x, y, w, h, c, 6, "16" if focal else "08", 1.4 if focal else 1.0)
    d.t(x + w // 2, y + 24, title, 14, INK, KR, "middle", 600)
    d.t(x + w // 2, y + 44, sub, 12, c if focal else MUTED, fam(sub), "middle")


# -------------------------------------------------------------
# 3. 노드 배치
# -------------------------------------------------------------
# 클라이언트
node_box(20, 128, 96, 56, "앱 A", "발신 기기", INFO)
node_box(844, 128, 96, 56, "앱 B", "수신 기기", OK)

# Zone 1 노드
node_box(184, 128, 132, 56, "채팅 서버 A", "웹소켓 접속", INFO)
node_box(388, 128, 140, 56, "Redis 레지스트리", "사용자 라우팅", INFO)
node_box(636, 128, 136, 56, "채팅 서버 B", "B 접속 서버", OK)

# Zone 2 노드
node_box(384, 256, 144, 52, "Redis 수신함", "미전달 큐", WARN)
node_box(636, 256, 136, 52, "알림 서비스", "APNs · FCM", WARN)

# Zone 3 노드
node_box(188, 404, 136, 56, "Kafka 파티션", "토픽 로그 P0", INFO)
node_box(456, 404, 136, 56, "메시지 저장 서비스", "컨슈머 워커", INFO)
node_box(764, 404, 160, 56, "Cassandra DB", "PK: (room, msg_id)", ACC, focal=True)


# -------------------------------------------------------------
# 4. 정상 경로 화살표 (번호 부여)
# -------------------------------------------------------------
# ① 앱 A -> 채팅 서버 A (메시지 전송)
d.arrow([(116, 144), (180, 144)], INK, "ar", 1.4)
d.t(148, 136, "① 전송", 11, INK, KR, "middle", 600)

# ② 채팅 서버 A -> 앱 A (sent 확인 응답)
d.arrow([(180, 168), (116, 168)], OK, "ok", 1.4, dash="4 3")
d.t(148, 184, "② sent", 11, OK, MONO, "middle", 600)

# ③ 채팅 서버 A -> Redis 레지스트리 (B 접속 조회)
d.arrow([(316, 156), (384, 156)], INFO, "info", 1.4)
d.t(350, 146, "③ 위치 조회", 11, INFO, KR, "middle")

# ④a 온라인: Redis 레지스트리 -> 채팅 서버 B -> 앱 B
d.arrow([(528, 156), (632, 156)], OK, "ok", 1.4)
d.t(580, 146, "④a 온라인 전달", 11, OK, KR, "middle")
d.arrow([(772, 156), (840, 156)], OK, "ok", 1.4)
d.t(806, 146, "웹소켓", 11, OK, KR, "middle")

# ④b 오프라인: 채팅 서버 A -> Redis 수신함 -> 알림 서비스
d.arrow([(280, 184), (280, 282), (380, 282)], WARN, "warn", 1.4)
d.t(312, 274, "④b 오프라인", 11, WARN, KR, "middle")
d.arrow([(528, 282), (632, 282)], WARN, "warn", 1.4)
d.t(580, 274, "푸시 발송", 11, WARN, KR, "middle")

# ⑤ 채팅 서버 A -> Kafka 파티션 (비동기 발행)
d.arrow([(244, 184), (244, 400)], INFO, "info", 1.4)
d.t(176, 292, "⑤ 비동기 발행", 11, INFO, KR, "middle")

# ⑥ Kafka 파티션 -> 저장 서비스 (컨슈머 폴링)
d.arrow([(324, 432), (456, 432)], INFO, "info", 1.4)
d.t(390, 422, "⑥ 컨슈머 폴링", 11, INFO, KR, "middle")

# ⑦ 저장 서비스 -> Cassandra (최종 영속화)
d.arrow([(592, 432), (760, 432)], ACC, "acc", 1.4)
d.t(676, 422, "⑦ 최종 영속화", 11, ACC, KR, "middle", 600)


# -------------------------------------------------------------
# 5. 유실 지점 3곳 (✕ 마크 및 라벨)
# -------------------------------------------------------------
# 지점 1: sent 확인 후 브로커 비동기 발행 사이 (채팅 서버와 Kafka 사이)
d.chip(120, 336, "✕ 지점 1: 브로커 발행 전 크래시", BAD, 11, 4)

# 지점 2: Redis 비동기 복제 유실 창 (수신함 하단)
d.chip(456, 332, "✕ 지점 2: 비동기 복제 유실", BAD, 11, 4)

# 지점 3: 컨슈머 커밋과 DB 쓰기 사이 (저장 서비스와 Cassandra 사이)
d.chip(678, 456, "✕ 지점 3: 커밋 불일치", BAD, 11, 4)


# -------------------------------------------------------------
# 6. 범례 (Legend)
# -------------------------------------------------------------
d.legend(
    H - 44,
    [
        ("정상 흐름", INFO),
        ("온라인 전달", OK),
        ("오프라인 분기", WARN),
        ("유실 위험 지점", BAD),
        ("최종 영속화 (초점)", ACC),
    ],
)

out_path = str(ASSETS_DIR / "02-01.message-path-map.svg")
d.save(out_path)
print(f"saved: {out_path}")

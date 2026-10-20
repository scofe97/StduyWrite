# 타입 스펙: type-process — 파티션 P0 복제본(브로커 1·2·3)과 프로듀서 쓰기를 세 시점(t1·t2·t3)에 반복하여 리더 승격과 쓰기 거절 메커니즘을 보인다. focal 은 브로커 2 의 새 리더 승격.
# 사실 출처: 요약 §4.4·§4.10, 조사 보고서 행 6·7·8·10, Kafka Operations 문서, 본문 3절(RF=3, min.insync.replicas=2, acks=all 설정 하에서 t1 정상 복제 ISR=3, t2 브로커 1 다운 시 컨트롤러가 ISR 내 브로커 2 를 새 Leader 로 선출하여 쓰기 계속 ISR=2, t3 브로커 3 도 다운 시 ISR=1 로 min.insync.replicas 미달되어 NotEnoughReplicasException 쓰기 거절, 리밸런스 용어 배제).
# Layout conventions: 3개 시점 컬럼(x=24·340·656, 폭 280), 각 컬럼 동일 객체 반복(브로커 1·2·3 및 프로듀서 결과), W=960, H=540. 모든 좌표 4의 배수.
import pathlib
import sys

ASSETS_DIR = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ASSETS_DIR))
from dd import D, ACC, BAD, INFO, INK, KR, MONO, MUTED, OK, RULE, SOFT, WARN

W, H = 960, 540
d = D(
    W,
    H,
    "SYSTEM DESIGN COURSE · 02-01 §3",
    "브로커 장애 시 리더 승격과 쓰기 거절의 세 시점",
    "브로커 1대 장애는 ISR 내 리더 승격으로 흡수하고, 2대 장애 시 min.insync.replicas 미달로 쓰기를 거절합니다.",
    "[t1] ISR=3 정상 복제 → [t2] 브로커 1 다운 · 브로커 2 리더 승격 (ISR=2) → [t3] 브로커 3 다운 · 쓰기 거절",
)


def fam(t):
    return KR if any("가" <= ch <= "힣" for ch in t) else MONO


XS = (28, 346, 664)
CW = 268

COLS = [
    {
        "t": "t1 : 정상 복제",
        "sub": ["RF=3 · acks=all", "min.insync.replicas=2"],
        "isr": "ISR = 3  (정상 정족수 충족)",
        "isr_col": OK,
        "brokers": [
            ("브로커 1", "Leader (P0)", OK, False),
            ("브로커 2", "Follower (ISR)", INFO, False),
            ("브로커 3", "Follower (ISR)", INFO, False),
        ],
        "result_tag": "acks=all 커밋 완료",
        "result_col": OK,
        "result_lines": ["프로듀서 정상 쓰기", "최소 2대 복제본 커밋 확인"],
    },
    {
        "t": "t2 : 브로커 1 다운",
        "sub": "컨트롤러 장애 감지 및 리더 승격",
        "isr": "ISR = 2  (최소 정족수 유지)",
        "isr_col": OK,
        "brokers": [
            ("브로커 1", "하드웨어 크래시 (다운)", BAD, False),
            ("브로커 2", "새 Leader 승격 (P0)", ACC, True),
            ("브로커 3", "Follower (ISR)", INFO, False),
        ],
        "result_tag": "acks=all 쓰기 지속",
        "result_col": OK,
        "result_lines": ["브로커 2 로 리더십 이전", "120초 타임아웃 내 발행 유지"],
    },
    {
        "t": "t3 : 브로커 3 도 다운",
        "sub": "ISR 미달 발생 · 일관성 보호",
        "isr": "ISR = 1  < min.insync.replicas=2",
        "isr_col": BAD,
        "brokers": [
            ("브로커 1", "다운 상태 유지", BAD, False),
            ("브로커 2", "단독 Leader (ISR 1대)", WARN, False),
            ("브로커 3", "추가 다운 (ISR 제외)", BAD, False),
        ],
        "result_tag": "NotEnoughReplicas",
        "result_col": BAD,
        "result_lines": ["NotEnoughReplicasException", "유실 방지를 위한 쓰기 거절"],
    },
]

for i, col in enumerate(COLS):
    x = XS[i]

    # 시점 외곽 프레임
    d.box(x, 96, CW, 356, "#12171F", RULE, 0.8, 8)

    # 시점 헤더
    subs = col["sub"] if isinstance(col["sub"], list) else [col["sub"]]
    if len(subs) == 1:
        d.t(x + CW // 2, 122, col["t"], 15, INK, KR, "middle", 600)
        d.t(x + CW // 2, 140, subs[0], 11, MUTED, fam(subs[0]), "middle")
    else:
        d.t(x + CW // 2, 118, col["t"], 15, INK, KR, "middle", 600)
        d.t(x + CW // 2, 133, subs[0], 11, MUTED, fam(subs[0]), "middle")
        d.t(x + CW // 2, 146, subs[1], 11, MUTED, fam(subs[1]), "middle")
    d.line(x + 12, 154, x + CW - 12, 154, RULE, 0.8)

    # 브로커 3대 박스
    by0 = 164
    for b_idx, (b_name, b_role, b_col, is_focal) in enumerate(col["brokers"]):
        by = by0 + b_idx * 52
        bx, bw, bh = x + 16, CW - 32, 44
        d.tone(bx, by, bw, bh, b_col, 6, "16" if is_focal else "08", 1.4 if is_focal else 1.0)
        d.t(bx + 16, by + 26, b_name, 13, INK, KR, "start", 600)
        d.t(bx + bw - 16, by + 26, b_role, 12, b_col if is_focal else MUTED, fam(b_role), "end")

    # ISR 상태 표시
    d.line(x + 16, 324, x + CW - 16, 324, RULE, 0.6)
    d.t(x + CW // 2, 342, col["isr"], 12, col["isr_col"], MONO, "middle", 600)

    # 하단 프로듀서 결과 상자
    rx, ry, rw, rh = x + 16, 356, CW - 32, 84
    r_col = col["result_col"]
    d.box(rx, ry, rw, rh, "#161B22", r_col, 0.9, 6)
    d.chip(rx + rw // 2, ry + 22, col["result_tag"], r_col, 11, 8)
    for l_idx, line in enumerate(col["result_lines"]):
        d.t(rx + rw // 2, ry + 48 + l_idx * 20, line, 11, INK if l_idx == 0 else MUTED, fam(line), "middle")

# 시점 간 전이 화살표
d.arrow([(296, 240), (342, 240)], WARN, "warn", 1.4)
d.t(321, 226, "고장", 11, WARN, KR, "middle")

d.arrow([(614, 240), (660, 240)], BAD, "bad", 1.4)
d.t(639, 226, "다운", 11, BAD, KR, "middle")

# 범례 (Legend)
d.legend(
    H - 44,
    [
        ("정상 / 복제", OK),
        ("동기화 복제본", INFO),
        ("장애 / 거절", BAD),
        ("정족수 미달 경고", WARN),
        ("새 리더 승격 (초점)", ACC),
    ],
)

out_path = str(ASSETS_DIR / "02-01.broker-failover.svg")
d.save(out_path)
print(f"saved: {out_path}")

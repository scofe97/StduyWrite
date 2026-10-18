# 사실 출처: gosuda/portal-tunnel 0a3b9c06 · sdk/listener.go:37,636 · sdk/reverse_transport.go:53 · portal/api_server.go:564 · portal/transport/reverse_pool.go:16,52,112,186 · portal/lease.go:33-34 · portal/server.go:37,1037
# 타입 스펙: type-data-flow
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 1000, 560
d = D(
    W, H,
    "DATA FLOW · REVERSE CONNECTION POOLING",
    "리버스 풀 데이터 흐름 — 연결 사전 개설·대기 풀 보관·클레임 인출",
    "터널 슬롯 루프가 아웃바운드 연결을 공급하고 릴레이 ReversePool 은 최대 8개까지 보관하며 인그레스 요청 시 즉시 인출합니다",
    "터널 슬롯(2개) → 101 하이잭 → ReversePool(최대 8개) → Acquire 인출 → 클라이언트 브리지"
)

# 배경 구획 (Zone)
def zone(x, y, w, h, label):
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="rgba(245,245,245,0.02)" stroke="{RULE}" stroke-width="0.9" stroke-dasharray="4 4"/>')
    d.t(x + 16, y + 20, label, 11, SOFT, KR, "start", 600)

zone(20, 104, 206, 396, "터널 에이전트 (NAT 내부)")
zone(296, 104, 368, 396, "릴레이 ReversePool (중계 서버)")
zone(710, 104, 270, 396, "공개 인그레스 및 브리지")

# 1. 터널 슬롯 (좌측)
SLOT1_X, SLOT1_Y, SLOT_W, SLOT_H = 34, 160, 178, 88
SLOT2_X, SLOT2_Y = 34, 280

d.tone(SLOT1_X, SLOT1_Y, SLOT_W, SLOT_H, INFO, 6, "14", 1.2)
d.t(SLOT1_X + 14, SLOT1_Y + 28, "작업 슬롯 1 (Slot 1)", 12, INFO, KR, "start", 600)
d.t(SLOT1_X + 14, SLOT1_Y + 52, "runReverseSessionLoop", 10, INK, MONO, "start")
d.t(SLOT1_X + 14, SLOT1_Y + 72, "openRaw() 호출 대기", 10, MUTED, KR, "start")

d.tone(SLOT2_X, SLOT2_Y, SLOT_W, SLOT_H, INFO, 6, "14", 1.2)
d.t(SLOT2_X + 14, SLOT2_Y + 28, "작업 슬롯 2 (Slot 2)", 12, INFO, KR, "start", 600)
d.t(SLOT2_X + 14, SLOT2_Y + 52, "defaultReadyTarget = 2", 10, INK, MONO, "start")
d.t(SLOT2_X + 14, SLOT2_Y + 72, "핸드셰이크·인계 후 보충", 10, MUTED, KR, "start")

# 터널 -> 릴레이 연결 화살표 (HTTP/1.1 101 Upgrade)
d.arrow([(SLOT1_X + SLOT_W, SLOT1_Y + 44), (312, SLOT1_Y + 44)], INFO, "info", 1.4)
d.arrow([(SLOT2_X + SLOT_W, SLOT2_Y + 44), (312, SLOT2_Y + 44)], INFO, "info", 1.4)

d.t(256, SLOT1_Y + 36, "GET /connect", 10, INFO, MONO, "middle")
d.t(256, SLOT2_Y + 36, "101 Upgrade", 10, INFO, MONO, "middle")

# 2. 릴레이 풀 내부 (중앙)
# 2-1. Offer (ReserveOffer + Commit)
OFFER_X, OFFER_Y, OFFER_W, OFFER_H = 312, 150, 336, 74
d.tone(OFFER_X, OFFER_Y, OFFER_W, OFFER_H, OK, 6, "12", 1.1)
d.t(OFFER_X + 16, OFFER_Y + 24, "Offer 단계 (동시성 제어)", 12, OK, KR, "start", 600)
d.t(OFFER_X + 16, OFFER_Y + 46, "ReserveOffer: 슬롯 한도 선점 예약", 11, INK, KR, "start")
d.t(OFFER_X + 16, OFFER_Y + 64, "Commit: pooledConn 생성 및 대기열 등록", 10, MUTED, KR, "start")

# 2-2. FIFO 대기열
QUEUE_X, QUEUE_Y, QUEUE_W, QUEUE_H = 312, 248, 336, 106
d.box(QUEUE_X, QUEUE_Y, QUEUE_W, QUEUE_H, PAPER2, RULE, 1.0)
d.t(QUEUE_X + 16, QUEUE_Y + 24, "대기 큐 (readyLimit = 8)", 12, INK, KR, "start", 600)

# 큐 내부 연결 슬롯 시각화
for idx in range(4):
    bx = QUEUE_X + 16 + idx * 76
    by = QUEUE_Y + 36
    if idx < 2:
        d.tone(bx, by, 68, 36, OK, 4, "20", 1.0)
        d.t(bx + 34, by + 16, f"conn-{idx+1}", 10, OK, MONO, "middle")
        d.t(bx + 34, by + 30, "ready", 9, INK, MONO, "middle")
    else:
        d.box(bx, by, 68, 36, PAPER, RULE, 0.8)
        d.t(bx + 34, by + 22, "empty", 9, SOFT, MONO, "middle")

d.t(QUEUE_X + 16, QUEUE_Y + 92, "keepIdle 루프: 15s 주기 0x00 하트비트", 10, OK, KR, "start")

# Offer -> Queue 화살표
d.arrow([(OFFER_X + OFFER_W // 2, OFFER_Y + OFFER_H), (OFFER_X + OFFER_W // 2, QUEUE_Y)], OK, "ok", 1.4)

# 2-3. Acquire 인출
ACQ_X, ACQ_Y, ACQ_W, ACQ_H = 312, 376, 336, 68
d.tone(ACQ_X, ACQ_Y, ACQ_W, ACQ_H, ACC, 6, "14", 1.2)
d.t(ACQ_X + 16, ACQ_Y + 24, "Acquire(ctx) 인출", 12, ACC, KR, "start", 600)
d.t(ACQ_X + 16, ACQ_Y + 44, "close(c.stop) 호출로 유휴 하트비트 중단", 11, INK, KR, "start")
d.t(ACQ_X + 16, ACQ_Y + 60, "죽은 소켓 감지 시 폐기 후 다음 연결 인출", 10, MUTED, KR, "start")

# Queue -> Acquire 화살표
d.arrow([(QUEUE_X + QUEUE_W // 2, QUEUE_Y + QUEUE_H), (ACQ_X + ACQ_W // 2, ACQ_Y)], ACC, "acc", 1.4)

# 3. 공개 인그레스 및 브리지 (우측)
ING_X, ING_Y, ING_W, ING_H = 724, 160, 242, 94
d.tone(ING_X, ING_Y, ING_W, ING_H, INFO, 6, "14", 1.1)
d.t(ING_X + 16, ING_Y + 26, "외부 공개 요청 도착", 13, INFO, KR, "start", 600)
d.t(ING_X + 16, ING_Y + 50, "SNI ClientHello 또는 TCP 연결", 11, INK, KR, "start")
d.t(ING_X + 16, ING_Y + 72, "defaultClaimTimeout = 10s", 11, MUTED, MONO, "start")

BRG_X, BRG_Y, BRG_W, BRG_H = 724, 290, 242, 114
d.tone(BRG_X, BRG_Y, BRG_W, BRG_H, ACC, 6, "14", 1.2)
d.t(BRG_X + 16, BRG_Y + 26, "활성 브리지 결합", 13, ACC, KR, "start", 600)
d.t(BRG_X + 16, BRG_Y + 50, "WriteTLSStart / WriteRawStart", 11, INK, MONO, "start")
d.t(BRG_X + 16, BRG_Y + 72, "양방향 바이트 스트림 중계", 11, MUTED, KR, "start")
d.t(BRG_X + 16, BRG_Y + 96, "활성화 마커로 ReadStart 해제", 10, OK, KR, "start")

# 인그레스 -> Acquire 요청 신호 화살표
d.arrow([(ING_X + ING_W // 2, ING_Y + ING_H), (ING_X + ING_W // 2, 272), (ACQ_X + ACQ_W, 272), (ACQ_X + ACQ_W, ACQ_Y + 26)], INFO, "info", 1.3, dash="4 3")
d.t(688, 264, "Acquire", 10, INFO, MONO, "middle")

# Acquire -> 브리지 전달 화살표
d.arrow([(ACQ_X + ACQ_W, ACQ_Y + 48), (BRG_X, BRG_Y + 56)], ACC, "acc", 1.6)
d.t(688, ACQ_Y + 54, "Conn", 10, ACC, MONO, "middle")

# 브리지 결합 -> 터널 새 연결 보충 피드백 화살표 (하단 우측 -> 좌측)
d.path(f"M {BRG_X + 60} {BRG_Y + BRG_H} L {BRG_X + 60} 474 L 123 474 L 123 {SLOT2_Y + SLOT_H}", OK, 1.3, m="ok", dash="4 3")
d.t(450, 466, "핸드셰이크 후 슬롯 보충 (readyCount = 2 유지)", 10, OK, KR, "middle")

# 범례 (Legend)
d.legend(H - 44, [
    ("사전 연결·개설", INFO),
    ("대기 풀·하트비트", OK),
    ("인출·브리지 결합", ACC),
    ("한도·타임아웃", WARN)
])

out_path = Path(__file__).parent.parent / "01-04-pool.svg"
d.save(str(out_path))
print(f"saved: {out_path}")

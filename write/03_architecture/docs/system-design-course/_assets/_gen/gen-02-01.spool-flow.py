# 타입 스펙: type-data-flow — Kafka 전면 장애 시 메시지가 거치는 5단계 완충·영속·재발행 파이프라인.
# 사실 출처: 요약 §4.4·§4.20, 조사 보고서 행 11·12·13, 본문 4절(메모리 버퍼 상한 100,000건, append-only WAL + fsync, 백그라운드 릴레이 재발행, acks=all 커밋 후 로그 삭제).
# Layout conventions: 5단계 가로 카드 x = 20, 212, 404, 596, 788 (폭 156, 높이 240, 간격 36), y = 112..352. 모든 좌표 4의 배수. 화살표는 수평 직선만.
import sys, pathlib
ASSETS_DIR = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ASSETS_DIR))
from dd import D, ACC, OK, WARN, BAD, INFO, MUTED, INK, SOFT, KR, MONO, RULE

W, H = 960, 464
d = D(W, H, "SYSTEM DESIGN COURSE · 02-01 §4",
      "발행 실패에서 재발행까지 메시지가 머무는 곳",
      "Kafka 다운 시 메모리 버퍼와 디스크 WAL 에 보관하고, 복구 후 릴레이가 재발행합니다.",
      "메시지 ID 1001 의 완충 · 영속 · 재발행 경로")

CW, CH = 156, 252
Y0 = 108
XS = (20, 212, 404, 596, 788)

cards = [
    {
        "num": "01",
        "title": "1. 발행 실패",
        "sub": "채팅 서버 프로듀서",
        "color": BAD,
        "focal": False,
        "box_title": "장애 감지",
        "paths": [
            ("delivery.timeout.ms", MONO, INK, 10.5),
            ("120초 초과", KR, BAD, 11),
            ("버퍼 가득 →", KR, INK, 11),
            ("max.block.ms", MONO, INK, 10.5),
            ("60초 뒤 예외", KR, BAD, 11),
        ],
    },
    {
        "num": "02",
        "title": "2. 메모리 버퍼",
        "sub": "애플리케이션 RAM",
        "color": WARN,
        "focal": False,
        "box_title": "1차 완충 (FIFO)",
        "lines": [
            ("FIFO 큐 적재", KR, INK),
            ("상한 100,000건", KR, WARN),
            ("초과 시 백프레셔", KR, MUTED),
        ],
    },
    {
        "num": "03",
        "title": "3. 로컬 WAL",
        "sub": "로컬 SSD 로그",
        "color": INFO,
        "focal": False,
        "box_title": "2차 영속화",
        "lines": [
            ("append-only", MONO, INK),
            ("OS fsync 즉시 호출", KR, INFO),
            ("크래시 유실 방어", KR, MUTED),
        ],
    },
    {
        "num": "04",
        "title": "4. 릴레이",
        "sub": "백그라운드 스레드",
        "color": ACC,
        "focal": True,
        "box_title": "복구 후 재발행",
        "lines": [
            ("로그 순차 읽기", KR, INK),
            ("Replay(1001)", MONO, ACC),
            ("Kafka 로 재전송", KR, MUTED),
        ],
    },
    {
        "num": "05",
        "title": "5. 커밋·삭제",
        "sub": "Kafka 브로커 복구",
        "color": OK,
        "focal": False,
        "box_title": "영속 완료",
        "lines": [
            ("acks=all 커밋", MONO, OK),
            ("읽기 오프셋 전진", KR, INK),
            ("로컬 로그 삭제", KR, MUTED),
        ],
    },
]

for i, c in enumerate(cards):
    x = XS[i]
    is_focal = c["focal"]
    col = c["color"]

    # 카드 외곽 테두리 및 톤
    d.tone(x, Y0, CW, CH, col, 6, "14" if is_focal else "08", 1.4 if is_focal else 1.0)

    # 상단 단계 칩
    d.chip(x + 28, Y0 + 22, c["num"], col, 11, 6)

    # 카드 헤더 텍스트
    d.t(x + 54, Y0 + 26, c["title"], 13, INK, KR, "start", 600)
    d.t(x + 14, Y0 + 50, c["sub"], 13, col if is_focal else MUTED, KR, "start")

    # 내부 데이터 상자
    bx, by, bw, bh = x + 10, Y0 + 68, CW - 20, 168
    d.box(bx, by, bw, bh, "#161B22", col, 0.9, 4)
    d.t(bx + bw // 2, by + 22, c["box_title"], 13, INK, KR, "middle", 600)
    d.line(bx + 8, by + 34, bx + bw - 8, by + 34, col, 0.6)

    if "paths" in c:
        d.t(bx + bw // 2, by + 52, c["paths"][0][0], c["paths"][0][3], c["paths"][0][2], c["paths"][0][1], "middle")
        d.t(bx + bw // 2, by + 68, c["paths"][1][0], c["paths"][1][3], c["paths"][1][2], c["paths"][1][1], "middle")
        d.line(bx + 16, by + 82, bx + bw - 16, by + 82, RULE, 0.6, dash="3 3")
        d.t(bx + bw // 2, by + 100, c["paths"][2][0], c["paths"][2][3], c["paths"][2][2], c["paths"][2][1], "middle")
        d.t(bx + bw // 2, by + 116, c["paths"][3][0], c["paths"][3][3], c["paths"][3][2], c["paths"][3][1], "middle")
        d.t(bx + bw // 2, by + 132, c["paths"][4][0], c["paths"][4][3], c["paths"][4][2], c["paths"][4][1], "middle")
    else:
        for j, (txt, fam, tcol) in enumerate(c["lines"]):
            d.t(bx + bw // 2, by + 60 + j * 36, txt, 13, tcol, fam, "middle")

    # 단계 사이 수평 화살표 (여백 36px 안에서 깔끔하게 연결)
    if i < 4:
        ax1 = x + CW + 4
        ax2 = XS[i + 1] - 4
        ay = Y0 + CH // 2
        d.arrow([(ax1, ay), (ax2, ay)], MUTED, "ar", 1.4)

d.legend(H - 44, [
    ("장애 감지", BAD),
    ("메모리 버퍼", WARN),
    ("디스크 WAL", INFO),
    ("재발행 (초점)", ACC),
    ("커밋 및 삭제", OK),
])

out_path = str(ASSETS_DIR / "02-01.spool-flow.svg")
d.save(out_path)
print(f"saved: {out_path}")

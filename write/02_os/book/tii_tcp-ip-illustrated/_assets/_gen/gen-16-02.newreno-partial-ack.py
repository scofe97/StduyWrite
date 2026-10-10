# 타입 스펙: type-process — NewReno 부분 ACK 수신 시 단계별 cwnd 와 세그먼트 전송 격자 (계산 예시).
# 사실 출처: RFC 6582 §3.2 · ch16.txt 722~760행
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 480
d = D(W, H, "TCP/IP ILLUSTRATED VOL.1 · 16-02 §1", "NewReno 부분 ACK 와 혼잡 창 전이 (계산 예시)",
      "초기 창 10(세그먼트 1–10) 중 1과 3이 손실된 상황이다. 빠른 재전송 진입 시 복구 지점을 11로 정한다. 추가 중복 ACK 누적으로 cwnd가 11·12·13으로 팽창해 새 세그먼트 11·12·13을 보내고, ACK 3(부분 ACK) 도착 시 cwnd=12(13−2+1)로 줄이며 세그먼트 3을 재전송한다.",
      "부분 ACK 는 복구 종료가 아니라 다음 구멍 재전송 신호입니다")

# 4개 단계 열 (카드)
COLS = [
    {
        "step": "1단계 · 빠른 재전송 진입",
        "ack": "ACK 1 (3rd dup)",
        "rec": "복구 지점 11 설정",
        "cwnd": "cwnd = 8 (5 + 3)",
        "ssthresh": "ssthresh = 5",
        "send": "세그먼트 1 재전송",
        "note": "첫 구멍 재전송 및 팽창",
        "color": WARN
    },
    {
        "step": "2단계 · 추가 중복 ACK 누적",
        "ack": "ACK 1 (총 8개 누적)",
        "rec": "복구 지점 11 유지",
        "cwnd": "cwnd = 13 (5 + 8)",
        "ssthresh": "ssthresh = 5",
        "send": "새 세그먼트 11·12·13 송신",
        "note": "창 팽창으로 새 데이터 허용",
        "color": INFO
    },
    {
        "step": "3단계 · 부분 ACK 수신",
        "ack": "ACK 3 (부분 ACK)",
        "rec": "3 < 11 (복구 미완료)",
        "cwnd": "cwnd = 12 (13−2+1)",
        "ssthresh": "ssthresh = 5",
        "send": "세그먼트 3 재전송",
        "note": "부분 창 축소 · 둘째 구멍 해결",
        "color": ACC
    },
    {
        "step": "4단계 · 전체 ACK 수신",
        "ack": "ACK 14 (전체 ACK)",
        "rec": "14 ≥ 11 (복구 완료)",
        "cwnd": "cwnd = 5 (ssthresh)",
        "ssthresh": "ssthresh = 5",
        "send": "정상 새 세그먼트 송신",
        "note": "팽창 해제 · 혼잡 회피 전이",
        "color": OK
    }
]

CW = 206
CH = 310
GAP = 16
X0 = 24
Y0 = 118

for i, col in enumerate(COLS):
    x = X0 + i * (CW + GAP)
    c = col["color"]
    d.box(x, Y0, CW, CH, PAPER2, RULE, 1.0, 8)
    # 상단 헤더 바
    d.tone(x, Y0, CW, 38, c, 6, "22", 1.0)
    d.t(x + CW/2, Y0 + 24, col["step"], 12, c, KR, "middle", 600)
    
    # 1. ACK 번호
    d.t(x + 14, Y0 + 64, "수신 피드백", 11, MUTED, KR, "start")
    d.chip(x + CW/2, Y0 + 88, col["ack"], c, 12)
    
    # 2. 복구 지점 판정
    d.t(x + 14, Y0 + 124, "복구 지점 판정", 11, MUTED, KR, "start")
    d.t(x + CW/2, Y0 + 144, col["rec"], 12, INK, MONO, "middle", 600)
    
    # 3. cwnd & ssthresh
    d.t(x + 14, Y0 + 176, "혼잡 창 상태", 11, MUTED, KR, "start")
    d.t(x + CW/2, Y0 + 196, col["cwnd"], 12, ACC if "12" in col["cwnd"] else INK, MONO, "middle", 600)
    d.t(x + CW/2, Y0 + 214, col["ssthresh"], 11, SOFT, MONO, "middle")
    
    # 4. 보낸 동작
    d.t(x + 14, Y0 + 246, "즉시 동작", 11, MUTED, KR, "start")
    d.t(x + CW/2, Y0 + 268, col["send"], 12, c, KR, "middle", 600)
    d.t(x + CW/2, Y0 + 292, col["note"], 11, MUTED, KR, "middle")
    
    # 열 간 연결 화살표
    if i < len(COLS) - 1:
        d.arrow([(x + CW + 2, Y0 + 88), (x + CW + GAP - 4, Y0 + 88)], MUTED, "ar", 1.2)

d.save("16-02.newreno-partial-ack.svg")

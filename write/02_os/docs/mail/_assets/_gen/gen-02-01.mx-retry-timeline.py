# 사실 출처: RFC 5321 §4.5.4.1(큐 및 재시도 간격), §5.1(우선순위 순서 접속 및 폴백)
# 타입 스펙: type-sequence
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W = 960
H = 660

d = D(
    W, H,
    "SEQUENCE · MX PRIORITY & QUEUE RETRY",
    "MX 우선순위 접속과 실패 시 큐 재시도 흐름",
    "1순위 접속 실패와 2순위 4xx 응답 시 발송 큐에 보관하고 RFC 권고 간격(최소 30분) 후 재시도하는 과정",
    "우선순위 10 실패 후 우선순위 20으로 폴백하며 임시 오류 수신 시 로컬 큐에 보관하고 지연 후 다시 1순위부터 시도하는 흐름"
)

# 1. 참여자 레인 (4개)
LANE_W = 180
LANES_Y = 96
X1 = 120  # 보내는 MTA
X2 = 360  # 1순위 MX
X3 = 600  # 2순위 MX
X4 = 840  # 발송 큐

d.box(X1 - LANE_W // 2, LANES_Y, LANE_W, 44, PAPER2, RULE, 1.0)
d.t(X1, LANES_Y + 19, "보내는 MTA", 13, INK, KR, "middle", 600)
d.t(X1, LANES_Y + 35, "Outbound MTA", 11, MUTED, MONO)

d.box(X2 - LANE_W // 2, LANES_Y, LANE_W, 44, PAPER2, RULE, 1.0)
d.t(X2, LANES_Y + 19, "1순위 MX", 13, INK, KR, "middle", 600)
d.t(X2, LANES_Y + 35, "mx1 (우선순위 10)", 11, MUTED, MONO)

d.box(X3 - LANE_W // 2, LANES_Y, LANE_W, 44, PAPER2, RULE, 1.0)
d.t(X3, LANES_Y + 19, "2순위 MX (백업)", 13, INK, KR, "middle", 600)
d.t(X3, LANES_Y + 35, "backup (우선순위 20)", 11, MUTED, MONO)

d.box(X4 - LANE_W // 2, LANES_Y, LANE_W, 44, PAPER2, INFO, 1.2)
d.t(X4, LANES_Y + 19, "발송 큐", 13, INK, KR, "middle", 600)
d.t(X4, LANES_Y + 35, "Local Queue", 11, MUTED, MONO)

# 2. 생명선
BOT_Y = 564
for x in (X1, X2, X3, X4):
    d.line(x, LANES_Y + 44, x, BOT_Y, RULE, 1.0, "3 6")

# 3. 활성 막대 (Activation bars)
d.o.append(f'<rect x="{X1 - 4}" y="152" width="8" height="{BOT_Y - 152}" fill="{PAPER2}" stroke="{MUTED}" stroke-width="0.8"/>')
d.o.append(f'<rect x="{X2 - 4}" y="168" width="8" height="60" fill="{PAPER2}" stroke="{BAD}" stroke-width="0.8"/>')
d.o.append(f'<rect x="{X3 - 4}" y="260" width="8" height="64" fill="{PAPER2}" stroke="{WARN}" stroke-width="0.8"/>')
d.o.append(f'<rect x="{X4 - 4}" y="356" width="8" height="72" fill="{PAPER2}" stroke="{INFO}" stroke-width="0.8"/>')
d.o.append(f'<rect x="{X2 - 4}" y="456" width="8" height="64" fill="{PAPER2}" stroke="{ACC}" stroke-width="1.0"/>')

def call(x_from, x_to, label, y, c=MUTED, mk="ar", dash=None, sub=None):
    direction = 1 if x_to > x_from else -1
    d_path = f"M {x_from + 6*direction} {y} L {x_to - 8*direction} {y}"
    d.path(d_path, c, 1.4, m=mk, dash=dash)
    mx = (x_from + x_to) // 2
    d.t(mx, y - 8, label, 13, c if c != MUTED else INK, MONO if not any("가"<=ch<="힣" for ch in label) else KR, "middle", 600)
    if sub:
        d.t(mx, y + 16, sub, 12, MUTED, KR, "middle")

def reply(x_from, x_to, label, y, c=OK, mk="ok", dash="6 4", sub=None):
    direction = 1 if x_to > x_from else -1
    d_path = f"M {x_from + 6*direction} {y} L {x_to - 8*direction} {y}"
    d.path(d_path, c, 1.4, m=mk, dash=dash)
    mx = (x_from + x_to) // 2
    d.t(mx, y - 8, label, 13, c, MONO if not any("가"<=ch<="힣" for ch in label) else KR, "middle", 600)
    if sub:
        d.t(mx, y + 16, sub, 12, MUTED, KR, "middle")

# 흐름 1: 1순위 MX 접속 시도 및 실패
call(X1, X2, "TCP SYN (포트 25)", 180, MUTED, "ar", sub="1순위 호스트 우선 접속")
reply(X2, X1, "연결 실패 (타임아웃)", 224, BAD, "bad", "4 3", sub="호스트 응답 없음")

# 흐름 2: 2순위 백업 MX 폴백 및 4xx 임시 오류
call(X1, X3, "TCP 연결 및 메일 발송 시도", 272, MUTED, "ar", sub="2순위 백업 호스트로 전환")
reply(X3, X1, "451 (임시 처리 실패)", 316, WARN, "warn", "4 3", sub="사서함 서버 점검 중")

# 흐름 3: 로컬 큐에 보관 및 대기
call(X1, X4, "메시지 큐 보관", 364, INFO, "info", sub="재시도 대기열 적재")
reply(X4, X1, "재시도 트리거 (최소 30분 지연)", 412, INFO, "info", "4 3", sub="RFC 5321 권고 간격 대기")

# 흐름 4: 1순위 MX부터 다시 시도 및 250 수신 완료 (Focal)
call(X1, X2, "1순위 재접속 시도 (포트 25)", 460, MUTED, "ar", sub="우선순위 순서 준수 재시도")
reply(X2, X1, "250 OK (수신 완료)", 504, ACC, "acc", None, sub="정상 배달 완료")

# 흐름 5: 전송 완료 후 큐 정리
call(X1, X4, "큐에서 메시지 삭제", 544, OK, "ok", sub="배달 성공 확인")

# 범례
d.legend(H - 44, [
    ("정상 완료 (250 OK / Focal)", ACC),
    ("임시 오류 (4xx)", WARN),
    ("연결 실패 (타임아웃)", BAD),
    ("큐 보관 및 재시도", INFO)
])

out = Path(__file__).parent.parent / "02-01.mx-retry-timeline.svg"
d.save(str(out))
print(f"생성 완료: {out} ({W}x{H})")

# 타입 스펙: type-flowchart
# 14-03.err-vs-cause — WithTimeout 과 WithCancelCause 로 감싼 context 의 두 가지 종료 갈래
# 본문 요구(14-03 §1 「Err 가 끝난 까닭을, Cause 가 그 이유를 알려 줍니다」):
#           WithTimeout 을 WithCancelCause 로 감싼 context 에서 갈래 둘.
#           (가) 시간이 다 됨 → Err·Cause 모두 context.DeadlineExceeded.
#           (나) 기한 전에 나쁜 상태로 취소 → Err 는 context.Canceled, Cause 는 그 오류.
# 사실 출처: Learning Go 2판 14장 「Contexts with Deadlines」 timeout_error_http, go1.25.1 실행(2026-09-28)
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER2, KR, MONO

W, H = 984, 508
CX = 492
START_Y = 104
START_H = 44
Q_Y = 212
DW, DH = 224, 64
LX, RX = 256, 728
BW, BH = 380, 44
OH = 76

d = D(W, H, "FLOWCHART · 14-03 §1",
      "종료 원인에 따른 Err 와 Cause 의 반환값",
      "WithTimeout(3s) 을 WithCancelCause 로 감싼 context 의 두 종료 경로. "
      "3초 시간 제한 만료 시 Err 와 Cause 는 모두 context.DeadlineExceeded 를 돌려준다. "
      "기한 전 status 고루틴이 bad status 로 취소하면 Err 는 context.Canceled, Cause 는 bad status 오류를 돌려준다.",
      lead="기한 만료는 표준 오류를, 명시적 취소는 취소 함수에 넘긴 고유 원인을 남깁니다.")

# 시작 노드: context 구성
d.box(CX - 190, START_Y, 380, START_H, fill=PAPER2, stroke=RULE, sw=1.0, r=20)
d.t(CX, START_Y + 27, "ctx: WithTimeout(3s) · WithCancelCause", 13, INK, MONO, "middle", 600)

# 분기 판단으로 이동
d.arrow([(CX, START_Y + START_H), (CX, Q_Y - DH // 2)], SOFT, "soft", 1.2)

# 판단 마름모: 종료 사건 분기
pts = f"{CX},{Q_Y - DH // 2} {CX + DW // 2},{Q_Y} {CX},{Q_Y + DH // 2} {CX - DW // 2},{Q_Y}"
d.o.append(f'<polygon points="{pts}" fill="{PAPER2}" stroke="rgba(191,192,192,0.22)" stroke-width="0.9"/>')
d.t(CX, Q_Y + 5, "종료 조건 판정", 13, INK, KR, "middle", 600)

# 갈래 (가): 3초 시간 제한 만료 (좌측)
d.arrow([(CX - DW // 2, Q_Y), (LX, Q_Y), (LX, 268)], SOFT, "soft", 1.3)
d.t((CX - DW // 2 + LX) // 2, 192, "3초 시간 제한 만료", 13, MUTED, KR, "middle", 600)

d.box(LX - BW // 2, 268, BW, BH, fill=PAPER2, stroke=RULE, sw=1.0, r=6)
d.t(LX, 268 + 27, "3초 시간 초과 발생", 13, INK, KR, "middle", 400)

d.arrow([(LX, 268 + BH), (LX, 344)], SOFT, "soft", 1.3)

d.tone(LX - BW // 2, 344, BW, OH, INFO, r=6, op="14", sw=1.2)
d.t(LX, 344 + 30, "Err:   context.DeadlineExceeded", 13, INFO, MONO, "middle", 600)
d.t(LX, 344 + 56, "Cause: context.DeadlineExceeded", 13, INFO, MONO, "middle", 600)

# 갈래 (나): 기한 전 취소 함수 호출 (우측 — focal)
d.arrow([(CX + DW // 2, Q_Y), (RX, Q_Y), (RX, 268)], ACC, "acc", 1.3)
d.t((CX + DW // 2 + RX) // 2, 192, "기한 전 취소 호출", 13, ACC, KR, "middle", 600)

d.box(RX - BW // 2, 268, BW, BH, fill=PAPER2, stroke=RULE, sw=1.0, r=6)
d.t(RX, 268 + 27, 'cancelFunc(errors.New("bad status"))', 13, ACC, MONO, "middle", 600)

d.arrow([(RX, 268 + BH), (RX, 344)], ACC, "acc", 1.3)

d.tone(RX - BW // 2, 344, BW, OH, ACC, r=6, op="18", sw=1.4)
d.t(RX, 344 + 30, "Err:   context.Canceled", 13, MUTED, MONO, "middle", 400)
d.t(RX, 344 + 56, "Cause: bad status", 13, ACC, MONO, "middle", 600)

# 범례
d.legend(460, [("시간 초과 (표준 오류)", INFO), ("명시적 취소 (원인 보존)", ACC)])

d.save("14-03.err-vs-cause.svg")
print("ok 14-03 err-vs-cause")
